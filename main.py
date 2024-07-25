import os
from flask import jsonify
from app import create_app

app = create_app()

@app.route('/', methods=['GET'])
def welcome():
    return jsonify({"message": "Welcome to Sanza!"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get("PORT", default=5000))
