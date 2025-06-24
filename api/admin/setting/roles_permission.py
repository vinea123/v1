import json
import datetime
from database.server import get_db
from middleware.user_api import auth_required
from mysql.connector import Error

#Convert DateTime for JSON Serialization
def convert_datetime(obj):
    if isinstance(obj, list):
        return [convert_datetime(item) for item in obj]
    elif isinstance(obj, dict):
        return {
            key: (value.isoformat() if isinstance(value, (datetime.datetime, datetime.date)) else value)
            for key, value in obj.items()
        }
    return obj

#PermissionHandler
class Roles_PermissionHandler:
    def __init__(self, request_handler):
        self.request_handler = request_handler

   #Read JSON Body
    def _read_json(self):
        length = int(self.request_handler.headers.get('Content-Length', 0))
        if length:
            raw = self.request_handler.rfile.read(length).decode()
            return json.loads(raw)
        return {}

    #Get ID from URL
    def _get_id(self):
        parts = self.request_handler.path.strip("/").split("/")
        # Expecting: ["admin", "status", "123"]
        if len(parts) == 3 and parts[0] == "admin" and parts[1] == "rolepermission" and parts[2].isdigit():
            return int(parts[2])
        return None

    # Get
    @auth_required(permission="View" , roles="Admin")
    def handle_get(self):
        path = self.request_handler.path

        if path == "/favicon.ico":
            return 204, {}, b""

        if path == "/":
            return 200, {"Content-Type": "application/json"}, json.dumps({"message": "Welcome to Status API"}).encode()

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor(dictionary=True)
            roles_permission_id = self._get_id()

            #  Get all
            if path == "/admin/rolepermission":
                cursor.execute("SELECT * FROM roles_permission")
                rows = convert_datetime(cursor.fetchall())
                return 200, {"Content-Type": "application/json"}, json.dumps({
                    "message": "Show all successfully !", 
                    "data": rows
                }).encode()

            # Get by ID
            elif roles_permission_id:
                cursor.execute("SELECT * FROM roles_permission WHERE id = %s", (roles_permission_id,))
                row = cursor.fetchone()
                if row:
                    row = convert_datetime(row)
                    return 200, {"Content-Type": "application/json"}, json.dumps({
                        "message": "Show successfully !", 
                        "data": row
                    }).encode()
                else:
                    return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Not found"}).encode()
            else:
                return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()
        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

    #Post
    @auth_required(permission="Create" , roles="Admin")
    def handle_post(self):
        if self.request_handler.path != "/admin/rolepermission":
            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

        data = self._read_json()
        roles_id = data.get("roles_id")
        permission_id = data.get("permission_id")


        if not roles_id:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'roles id' field"}).encode()

        if not permission_id:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'permission id' field"}).encode()

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("INSERT INTO roles_permission (roles_id, permission_id) VALUES (%s, %s)", (roles_id, permission_id,))
            conn.commit()
            inserted_id = cursor.lastrowid

            # Now fetch the inserted row
            cursor.execute("SELECT * FROM roles_permission WHERE id = %s", (inserted_id,))
            row = cursor.fetchone()

            if row:
                # Convert datetime if needed (assuming you have convert_datetime)
                row = convert_datetime(row)
                return 201, {"Content-Type": "application/json"}, json.dumps({
                    "message": "Created successfully !",
                    "data": row
                }).encode()
        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

    #Update
    @auth_required(permission="Update" , roles="Admin")
    def handle_put(self):
        roles_permission_id = self._get_id()
        if not  roles_permission_id:
            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

        data = self._read_json()
        roles_id = data.get("roles_id")
        permission_id = data.get("permission_id")

        if not roles_id:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'roles id' field"}).encode()

        if not permission_id:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'permission id' field"}).encode()

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor()
            cursor.execute("""UPDATE roles_permission SET roles_id = %s, permission_id = %s  WHERE id = %s """, (roles_id, permission_id, roles_permission_id))
            conn.commit()

            if cursor.rowcount == 0:
                return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Not found"}).encode()
            else:
                # Fetch the updated row with date fields
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM roles_permission WHERE id = %s", (roles_permission_id,))
                updated_row = cursor.fetchone()

                # Convert datetime fields to string
                updated_row = convert_datetime(updated_row)

                return 200, {"Content-Type": "application/json"}, json.dumps({
                    "message": "Updated successfully !",
                    "data": updated_row
                }).encode()
        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

    #Delete
    @auth_required(permission="Delete" , roles="Admin")
    def handle_delete(self):
        roles_permission_id = self._get_id()
        if not roles_permission_id:
            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor(dictionary=True)

            # Fetch the record before deleting
            cursor.execute("SELECT * FROM roles_permission WHERE id = %s", (roles_permission_id,))
            row = cursor.fetchone()

            if not row:
                return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Not found"}).encode()

            # Delete the record
            cursor.execute("DELETE FROM roles_permission WHERE id = %s", (roles_permission_id,))
            conn.commit()

            # Convert datetime fields to string before returning
            row = convert_datetime(row)

            return 200, {"Content-Type": "application/json"}, json.dumps({
                "message": "Deleted successfully !",
                "data": row
            }).encode()

        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

