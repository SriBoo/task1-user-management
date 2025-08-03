from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
import json
import os

app = Flask(__name__, template_folder='templates')

is_vercel = os.environ.get("VERCEL") == "1"
is_vercel_dev = os.environ.get("VERCEL_DEV") == "1"

local_db = os.path.join(os.path.dirname(__file__), 'users.db')
db_path = '/tmp/users.db' if is_vercel or is_vercel_dev else local_db

if (is_vercel or is_vercel_dev) and os.path.exists(local_db) and not os.path.exists(db_path):
    try:
        with open(local_db, 'rb') as src, open(db_path, 'wb') as dst:
            dst.write(src.read())
    except Exception as e:
        raise RuntimeError(f"Failed to copy database: {e}")

try:
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
except Exception as e:
    raise RuntimeError(f"Failed to connect to database: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        if user_id:
            return redirect(url_for('get_user', user_id=user_id))
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_all_users_json():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify([{"id": u[0], "name": u[1], "email": u[2]} for u in users])

@app.route('/all-users')
def all_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    rows = cursor.fetchall()
    conn.close()
    users = [{'id': r[0], 'name': r[1], 'email': r[2]} for r in rows]
    return render_template('all_users.html', users=users)

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
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()
    return "User created", 201

@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
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
    data = request.get_json()
    email = data['email']
    password = data['password']
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    if user:
        return jsonify({"status": "success", "user_id": user[0]})
    else:
        return jsonify({"status": "failed"})


handler = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)