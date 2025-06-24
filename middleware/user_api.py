import json
from middleware.auth_required import auth_required
from database.server import get_db
from mysql.connector import Error
# from api.admin.auth.auth import hash_password

class UserAPI:

    @auth_required( permission = "" , roles="")
    def handle_get(self):
        try:
            conn = get_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, email FROM users")
            users = cursor.fetchall()
            return 200, {"Content-Type": "application/json"}, json.dumps({
                "users": users,
                "accessed_by": self.user["email"]
            }).encode()
        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

    