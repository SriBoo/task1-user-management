from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user list to simulate a database
users = []
user_id_counter = 1

@app.route('/')
def index():
    return "✅ User Management API is live!"

@app.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    global user_id_counter
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    user = {
        "id": user_id_counter,
        "name": name,
        "email": email,
        "password": password
    }
    user_id_counter += 1
    users.append(user)
    return jsonify({"message": "User created", "user": user}), 201

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in users:
        if user['id'] == user_id:
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    for user in users:
        if user['id'] == user_id:
            user['name'] = data.get('name', user['name'])
            user['email'] = data.get('email', user['email'])
            return jsonify({"message": "User updated", "user": user})
    return jsonify({"error": "User not found"}), 404

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [u for u in users if u['id'] != user_id]
    return jsonify({"message": "User deleted"})

@app.route('/search', methods=['GET'])
def search_users():
    name_query = request.args.get('name', '')
    matched_users = [u for u in users if name_query.lower() in u['name'].lower()]
    return jsonify(matched_users)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    for user in users:
        if user['email'] == email and user['password'] == password:
            return jsonify({"status": "success", "user_id": user['id']})
    return jsonify({"status": "failed"}), 401
