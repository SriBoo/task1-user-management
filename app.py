from flask import Flask, request, jsonify, render_template
import sqlite3
import json
import os

app = Flask(__name__, template_folder='templates')

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')  # Serves the HTML UI

@app.route('/users', methods=['GET'])
def get_all_users_json():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify([{"id": u[0], "name": u[1], "email": u[2]} for u in users])

@app.route('/all-users', methods=['GET'])
def all_users_html():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template("all_users.html", users=users)

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        return render_template("user.html", user={"id": user[0], "name": user[1], "email": user[2]})
    else:
        return "User not found", 404

@app.route('/users', methods=['POST'])
def create_user():
    data = json.loads(request.get_data())
    name = data['name']
    email = data['email']
    password = data['password']
    
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    
    return "User created", 201

@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = json.loads(request.get_data())
    name = data.get('name')
    email = data.get('email')
    
    if name and email:
        cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        conn.commit()
        return "User updated"
    else:
        return "Invalid data", 400

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    return "User deleted"

@app.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return "Please provide a name to search", 400
    
    cursor.execute("SELECT * FROM users WHERE name LIKE ?", ('%' + name + '%',))
    users = cursor.fetchall()
    return jsonify([{"id": u[0], "name": u[1], "email": u[2]} for u in users])

@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.get_data())
    email = data['email']
    password = data['password']
    
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    
    if user:
        return jsonify({"status": "success", "user_id": user[0]})
    else:
        return jsonify({"status": "failed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
