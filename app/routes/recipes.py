from flask import Blueprint, jsonify
from app.models.recipe import Recipe

bp = Blueprint('recipes', __name__, url_prefix='/api/recipes')

@bp.route('/', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([recipe.to_dict() for recipe in recipes]), 200
