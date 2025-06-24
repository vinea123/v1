import json
import datetime
import hashlib
from database.server import get_db
from middleware.user_api import auth_required
from mysql.connector import Error

# Convert DateTime for JSON Serialization
def convert_datetime(obj):
    if isinstance(obj, list):
        return [convert_datetime(item) for item in obj]
    elif isinstance(obj, dict):
        return {
            key: (value.isoformat() if isinstance(value, (datetime.datetime, datetime.date)) else value)
            for key, value in obj.items()
        }
    return obj

# UsersHandler
class UsersHandler:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    # Read JSON Body
    def _read_json(self):
        length = int(self.request_handler.headers.get('Content-Length', 0))
        if length:
            raw = self.request_handler.rfile.read(length).decode()
            try:
                return json.loads(raw)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON: {str(e)}")
        return {}

    # Get ID from URL
    def _get_id(self):
        parts = self.request_handler.path.strip("/").split("/")
        if len(parts) == 3 and parts[0] == "admin" and parts[1] == "users" and parts[2].isdigit():
            return int(parts[2])
        return None

    # GET
    @auth_required(permission="View", roles="Admin")
    def handle_get(self):
        path = self.request_handler.path
        if path == "/favicon.ico":
            return 204, {}, b""

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor(dictionary=True)
            user_id = self._get_id()

            if path == "/admin/users":
                cursor.execute("SELECT * FROM users")
                rows = convert_datetime(cursor.fetchall())
                return 200, {"Content-Type": "application/json"}, json.dumps({
                    "message": "Show all successfully!",
                    "data": rows
                }).encode()
            elif user_id:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                row = cursor.fetchone()
                if row:
                    return 200, {"Content-Type": "application/json"}, json.dumps({
                        "message": "Show successfully!",
                        "data": convert_datetime(row)
                    }).encode()
                else:
                    return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Not found"}).encode()

            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()
        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

    # POST
    @auth_required(permission="Create", roles="Admin")
    def handle_post(self):
        if self.request_handler.path != "/admin/users":
            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

        try:
            data = self._read_json()
        except ValueError as e:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()

        required_fields = ["first_name", "last_name", "email", "password"]
        if not all(data.get(field) for field in required_fields):
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing required fields"}).encode()

        password = data["password"]
        if len(password) != 8:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "The password must be 8 digits."}).encode()

        password_md5 = hashlib.md5(password.encode()).hexdigest()
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        dob = data.get("dob")
        address = data.get("address")
        gender_id = data.get("gender_id")
        roles_id = data.get("roles_id")

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, password, dob, address, gender_id, roles_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, email, password_md5, dob, address, gender_id, roles_id))
            conn.commit()

            user_id = cursor.lastrowid
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            return 201, {"Content-Type": "application/json"}, json.dumps({
                "message": "Created successfully!",
                "data": convert_datetime(row)
            }).encode()
        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

    # PUT
    @auth_required(permission="Update", roles="Admin")
    def handle_put(self):
        user_id = self._get_id()
        if not user_id:
            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

        try:
            data = self._read_json()
        except ValueError as e:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        dob = data.get("dob")
        address = data.get("address")
        gender_id = data.get("gender_id")
        roles_id = data.get("roles_id")

        if not all([first_name, last_name, email]):
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing required fields"}).encode()

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor(dictionary=True)

            if password:
                if len(password) != 8:
                    return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Password must be 8 digits"}).encode()
                password_md5 = hashlib.md5(password.encode()).hexdigest()
                query = """
                    UPDATE users SET first_name=%s, last_name=%s, email=%s, password=%s, dob=%s, address=%s, gender_id=%s, roles_id=%s
                    WHERE id=%s
                """
                params = (first_name, last_name, email, password_md5, dob, address, gender_id, roles_id, user_id)
            else:
                query = """
                    UPDATE users SET first_name=%s, last_name=%s, email=%s, dob=%s, address=%s, gender_id=%s, roles_id=%s
                    WHERE id=%s
                """
                params = (first_name, last_name, email, dob, address, gender_id, roles_id, user_id)

            cursor.execute(query, params)
            conn.commit()

            if cursor.rowcount == 0:
                return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Not found"}).encode()

            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            return 200, {"Content-Type": "application/json"}, json.dumps({
                "message": "Updated successfully!",
                "data": convert_datetime(row)
            }).encode()
        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

    # DELETE
    @auth_required(permission="Delete", roles="Admin")
    def handle_delete(self):
        user_id = self._get_id()
        if not user_id:
            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            row = cursor.fetchone()

            if not row:
                return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Not found"}).encode()

            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            return 200, {"Content-Type": "application/json"}, json.dumps({
                "message": "Deleted successfully!",
                "data": convert_datetime(row)
            }).encode()
        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()
