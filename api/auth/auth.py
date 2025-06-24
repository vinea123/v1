import json, hashlib, uuid, base64
from database.server import get_db
from mysql.connector import Error

# Store tokens with full user info (email, role, permissions)
tokens = {}

def hash_password(password: str) -> str:
    """Hash password with MD5 (consider upgrading to stronger hashing)."""
    return hashlib.md5(password.encode()).hexdigest()

def generate_token(user_info: dict) -> str:
    """Generate a unique token for the user and store their info."""
    token = base64.urlsafe_b64encode(f"{user_info['email']}:{uuid.uuid4()}".encode()).decode()
    tokens[token] = user_info
    return token

def verify_token(token: str) -> dict | None:
    """Verify the token and return user info or None if invalid."""
    return tokens.get(token)

def handle_login(request_handler):
    length = int(request_handler.headers.get("Content-Length", 0))
    body = json.loads(request_handler.rfile.read(length).decode()) if length else {}

    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing email or password"}).encode()
    
    conn = get_db()
    if not conn:
        return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

    try:
        cursor = conn.cursor(dictionary=True)

        # Get user + role using updated roles_id column
        cursor.execute("""
            SELECT u.id, u.email, r.id AS role_id, r.name AS role_name
            FROM users u
            JOIN roles r ON u.roles_id = r.id
            WHERE u.email = %s AND u.password = %s
        """, (email, hash_password(password)))
        user = cursor.fetchone()

        if not user:
            return 401, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid credentials"}).encode()

        # Get permissions based on roles_id 
        cursor.execute("""
            SELECT p.name FROM permission p
            JOIN roles_permission rp ON rp.permission_id = p.id
            WHERE rp.roles_id = %s
        """, (user["role_id"],))
        permissions = [row["name"] for row in cursor.fetchall()]

        user_info = {
            "email": user["email"],
            "role": user["role_name"],
            "permissions": permissions
        }

        token = generate_token(user_info)

        return 200, {"Content-Type": "application/json"}, json.dumps({
            "message": "Login successfully!",
            "token": token
            # "role": user["role_name"],
            # "permissions": permissions
        }).encode()

    except Error as e:
        return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
    finally:
        conn.close()

def handle_logout(request_handler):
    auth_header = request_handler.headers.get("Authorization")
    if not auth_header:
        return 401, {"Content-Type": "application/json"}, json.dumps({"error": "Missing token"}).encode()

    token = auth_header.replace("Bearer ", "").strip()
    if token in tokens:
        del tokens[token]
        return 200, {"Content-Type": "application/json"}, json.dumps({"message": "Logout successfully!"}).encode()

    return 401, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid token"}).encode()
