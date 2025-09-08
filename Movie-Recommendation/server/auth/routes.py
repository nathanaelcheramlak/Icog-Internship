from flask import Blueprint, request, jsonify
from database.sqlite import get_connection, init_db
from .utils import hash_password, check_password, generate_token, generate_uuid

auth_bp = Blueprint("auth", __name__)

# Initialize DB
init_db()

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    hashed = hash_password(password)
    user_uuid = generate_uuid()

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (uuid, username, password) VALUES (?, ?, ?)", (user_uuid, username, hashed))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        token = generate_token(user_id)
        return jsonify({"message": "User created", "token": token, "user": {"id": user_uuid, "username": username}})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        if 'conn' in locals():
            conn.close()

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    try:
        # Use context manager for better connection handling
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Check password
        if not check_password(password, user["password"]):
            return jsonify({"error": "Invalid credentials"}), 401

        # Generate token and return response
        token = generate_token(user["id"])
        return jsonify({
            "message": "Login successful", 
            "token": token, 
            "user": {
                "id": user["uuid"],       
                "username": user["username"]
            }
        })
        
    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500