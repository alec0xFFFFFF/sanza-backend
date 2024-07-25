# api/recipes.py
from flask import Blueprint, request, jsonify
from app.models import Recipe
from pydantic import BaseModel, ValidationError
from ..utils import get_gcs_client, generate_embedding
from celery import shared_task
from app import posthog, db

bp = Blueprint('recipes', __name__, url_prefix='/api/recipes')

# Pydantic model for request validation
class RecipeCreate(BaseModel):
    title: str
    ingredients: list[str]
    instructions: str
    image: str  # Base64 encoded image

@shared_task
def process_recipe_image(recipe_id, image_data):
    gcs_client = get_gcs_client()
    bucket = gcs_client.bucket('sanza-recipe-images')
    blob = bucket.blob(f'recipe_{recipe_id}.jpg')
    blob.upload_from_string(image_data, content_type='image/jpeg')
    image_url = blob.public_url
    
    recipe = Recipe.query.get(recipe_id)
    recipe.image_url = image_url
    db.session.commit()

@shared_task
def generate_recipe_embedding(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    embedding = generate_embedding(recipe.title + ' ' + ' '.join(recipe.ingredients) + ' ' + recipe.instructions)
    recipe.embedding = embedding
    db.session.commit()

@bp.route('/', methods=['POST'])
def create_recipe():
    """Create a new recipe"""
    # Use PostHog
    posthog.posthog.capture('user-id', 'create-recipe')
    try:
        recipe_data = RecipeCreate(**request.json)
    except ValidationError as e:
        return jsonify({'message': 'Invalid input', 'errors': e.errors()}), 400

    new_recipe = Recipe(
        title=recipe_data.title,
        ingredients=recipe_data.ingredients,
        instructions=recipe_data.instructions,
        user_id=1  # TODO: Replace with actual user ID from authentication
    )

    db.session.add(new_recipe)
    db.session.commit()

    # Trigger async tasks
    process_recipe_image.delay(new_recipe.id, recipe_data.image)
    generate_recipe_embedding.delay(new_recipe.id)

    return jsonify({'message': 'Recipe created successfully', 'id': new_recipe.id}), 201
