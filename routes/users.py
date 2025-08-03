from flask import Blueprint, request, jsonify
from models.user_model import get_all_users, get_user_by_id, add_user

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/')
def index():
    return "User Management System"

@user_routes.route('/users', methods=['GET'])
def get_users():
    return jsonify(get_all_users())

@user_routes.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@user_routes.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    new_id = add_user(data["name"], data["email"], data["password"])
    return jsonify({"id": new_id, **data}), 201
