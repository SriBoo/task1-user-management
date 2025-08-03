from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__, template_folder='../templates')

# Connect to SQLite DB
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'users.db')
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_all_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify([{'id': row[0], 'name': row[1], 'email': row[2]} for row in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify({'id': user[0], 'name': user[1], 'email': user[2]})
    return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name, email, password = data.get('name'), data.get('email'), data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'Missing fields'}), 400

    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    return jsonify({'message': 'User deleted successfully'})

# Required for Vercel serverless
def handler(environ, start_response):
    return app(environ, start_response)
