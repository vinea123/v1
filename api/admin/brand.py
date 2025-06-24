# import json
# import datetime
# from database.server import get_db
# from middleware.user_api import auth_required
# from mysql.connector import Error

# #Convert DateTime for JSON Serialization
# def convert_datetime(obj):
#     if isinstance(obj, list):
#         return [convert_datetime(item) for item in obj]
#     elif isinstance(obj, dict):
#         return {
#             key: (value.isoformat() if isinstance(value, (datetime.datetime, datetime.date)) else value)
#             for key, value in obj.items()
#         }
#     return obj

# #GenderHandler
# class BrandHandler:
#     def __init__(self, request_handler):
#         self.request_handler = request_handler

#    #Read JSON Body
#     def _read_json(self):
#         length = int(self.request_handler.headers.get('Content-Length', 0))
#         if length:
#             raw = self.request_handler.rfile.read(length).decode()
#             return json.loads(raw)
#         return {}

#     #Get ID from URL
#     def _get_id(self):
#         parts = self.request_handler.path.strip("/").split("/")
#         if len(parts) == 3 and parts[0] == "admin" and parts[1] == "brand" and parts[2].isdigit():
#             return int(parts[2])
#         return None


#     # Get
#     @auth_required(permission="View" , roles="Admin")
#     def handle_get(self):
#         path = self.request_handler.path

#         if path == "/favicon.ico":
#             return 204, {}, b""

#         if path == "/":
#             return 200, {"Content-Type": "application/json"}, json.dumps({"message": "Welcome to Status API"}).encode()

#         conn = get_db()
#         if not conn:
#             return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()
            

#         try:
#             cursor = conn.cursor(dictionary=True)
#             brand_id = self._get_id()

#             #  Get all
#             if path == "/admin/brand":
#                 cursor.execute("SELECT * FROM brand")
#                 rows = convert_datetime(cursor.fetchall())
#                 return 200, {"Content-Type": "application/json"}, json.dumps({
#                     "message": "Show all successfully !", 
#                     "data": rows
#                 }).encode()

#             # Get by ID
#             elif brand_id:
#                 cursor.execute("SELECT * FROM brand WHERE id = %s", (brand_id,))
#                 row = cursor.fetchone()
#                 if row:
#                     row = convert_datetime(row)
#                     return 200, {"Content-Type": "application/json"}, json.dumps({
#                         "message": "Show successfully !", 
#                         "data": row
#                     }).encode()
#                 else:
#                     return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Not found"}).encode()
#             else:
#                 return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()
#         except Error as e:
#             return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
#         finally:
#             conn.close()

#     #Post
#     @auth_required(permission="Create" , roles="Admin")
#     def handle_post(self):
#         if self.request_handler.path != "/admin/brand":
#             return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

#         data = self._read_json()
#         name = data.get("name")
#         status = data.get("status", "active")


#         if not name:
#             return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'name' field"}).encode()
        
#         if not status:
#             return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'status' field"}).encode()

#         conn = get_db()
#         if not conn:
#             return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

#         try:
#             cursor = conn.cursor(dictionary=True)  
#             cursor.execute("INSERT INTO brand (name ,status) VALUES (%s, %s)", (name,status,))
#             conn.commit()
#             inserted_id = cursor.lastrowid

#             # Now fetch the inserted row
#             cursor.execute("SELECT * FROM brand WHERE id = %s", (inserted_id,))
#             row = cursor.fetchone()

#             if row:
#                 row = convert_datetime(row)
#                 return 201, {"Content-Type": "application/json"}, json.dumps({
#                     "message": "Created successfully !",
#                     "data": row
#                 }).encode()
#         except Error as e:
#             return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
#         finally:
#             conn.close()

#     #Update
#     @auth_required(permission="Update" , roles="Admin")
#     def handle_put(self):
#         brand_id = self._get_id()
#         if not brand_id:
#             return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

#         data = self._read_json()
#         name = data.get("name")
#         status = data.get("status", "active")

        
#         if not name:
#             return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'name' field"}).encode()
        
#         if not status:
#             return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'status' field"}).encode()
        
#         conn = get_db()
#         if not conn:
#             return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

#         try:
#             cursor = conn.cursor()
#             cursor.execute("UPDATE brand SET name = %s , status = %s WHERE id = %s", (name, status , brand_id  ))
#             conn.commit()

#             if cursor.rowcount == 0:
#                 return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Not found"}).encode()
#             else:
#                 # Fetch the updated row with date fields
#                 cursor = conn.cursor(dictionary=True)
#                 cursor.execute("SELECT * FROM brand WHERE id = %s", (brand_id,))
#                 updated_row = cursor.fetchone()

#                 # Convert datetime fields to string
#                 updated_row = convert_datetime(updated_row)

#                 return 200, {"Content-Type": "application/json"}, json.dumps({
#                     "message": "Updated successfully !",
#                     "data": updated_row
#                 }).encode()
#         except Error as e:
#             return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
#         finally:
#             conn.close()

#     #Delete
#     @auth_required(permission="Delete" , roles="Admin")
#     def handle_delete(self):
#         brand_id = self._get_id()
#         if not brand_id:
#             return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

#         conn = get_db()
#         if not conn:
#             return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

#         try:
#             cursor = conn.cursor(dictionary=True)

#             # Fetch the record before deleting
#             cursor.execute("SELECT * FROM brand WHERE id = %s", (brand_id,))
#             row = cursor.fetchone()

#             if not row:
#                 return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Not found"}).encode()

#             # Delete the record
#             cursor.execute("DELETE FROM brand WHERE id = %s", (brand_id,))
#             conn.commit()

#             # Convert datetime fields to string before returning
#             row = convert_datetime(row)

#             return 200, {"Content-Type": "application/json"}, json.dumps({
#                 "message": "Deleted successfully !",
#                 "data": row
#             }).encode()

#         except Error as e:
#             return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
#         finally:
#             conn.close()



import json
import datetime
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

# BrandHandler
class BrandHandler:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def _read_json(self):
        length = int(self.request_handler.headers.get('Content-Length', 0))
        if length:
            raw = self.request_handler.rfile.read(length).decode()
            return json.loads(raw)
        return {}

    def _get_id(self):
        parts = self.request_handler.path.strip("/").split("/")
        if len(parts) >= 3 and parts[0] == "admin" and parts[1] == "brand" and parts[2].isdigit():
            return int(parts[2])
        return None

    @auth_required(permission="View", roles="Admin")
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
            brand_id = self._get_id()

            if path == "/admin/brand":
                cursor.execute("SELECT * FROM brand")
                rows = convert_datetime(cursor.fetchall())
                return 200, {"Content-Type": "application/json"}, json.dumps({
                    "message": "Show all successfully !",
                    "data": rows
                }).encode()

            elif brand_id:
                cursor.execute("SELECT * FROM brand WHERE id = %s", (brand_id,))
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

    @auth_required(permission="Create", roles="Admin")
    def handle_post(self):
        if self.request_handler.path != "/admin/brand":
            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

        data = self._read_json()
        name = data.get("name")
        status = data.get("status", "active")

        if not name:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'name' field"}).encode()

        if not status:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'status' field"}).encode()

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("INSERT INTO brand (name, status) VALUES (%s, %s)", (name, status))
            conn.commit()
            inserted_id = cursor.lastrowid

            cursor.execute("SELECT * FROM brand WHERE id = %s", (inserted_id,))
            row = cursor.fetchone()

            if row:
                row = convert_datetime(row)
                return 201, {"Content-Type": "application/json"}, json.dumps({
                    "message": "Created successfully !",
                    "data": row
                }).encode()
        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

    @auth_required(permission="Update", roles="Admin")
    def handle_put(self):
        brand_id = self._get_id()
        if not brand_id:
            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

        data = self._read_json()
        name = data.get("name")
        status = data.get("status", "active")

        if not name:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'name' field"}).encode()

        if not status:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'status' field"}).encode()

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE brand SET name = %s, status = %s WHERE id = %s", (name, status, brand_id))
            conn.commit()

            if cursor.rowcount == 0:
                return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Not found"}).encode()

            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM brand WHERE id = %s", (brand_id,))
            updated_row = cursor.fetchone()
            updated_row = convert_datetime(updated_row)

            return 200, {"Content-Type": "application/json"}, json.dumps({
                "message": "Updated successfully !",
                "data": updated_row
            }).encode()
        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

    @auth_required(permission="Delete", roles="Admin")
    def handle_delete(self):
        brand_id = self._get_id()
        if not brand_id:
            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM brand WHERE id = %s", (brand_id,))
            row = cursor.fetchone()

            if not row:
                return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Not found"}).encode()

            cursor.execute("DELETE FROM brand WHERE id = %s", (brand_id,))
            conn.commit()

            row = convert_datetime(row)
            return 200, {"Content-Type": "application/json"}, json.dumps({
                "message": "Deleted successfully !",
                "data": row
            }).encode()
        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

    @auth_required(permission="Update", roles="Admin")
    def handle_status(self):
        brand_id = self._get_id()
        if not brand_id:
            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

        data = self._read_json()
        status = data.get("status")

        if not status:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'status' field"}).encode()

        status = status.strip().lower()
        if status not in ["active", "inactive"]:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid 'status' value"}).encode()

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE brand SET status = %s, modify_date = CURRENT_TIMESTAMP WHERE id = %s", (status, brand_id))
            conn.commit()

            if cursor.rowcount == 0:
                return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Not found"}).encode()

            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM brand WHERE id = %s", (brand_id,))
            updated_row = cursor.fetchone()

            return 200, {"Content-Type": "application/json"}, json.dumps({
                "message": "Status updated successfully!",
                "data": convert_datetime(updated_row)
            }).encode()
        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

            