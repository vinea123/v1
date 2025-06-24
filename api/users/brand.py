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
# class BrandUsersHandler:
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
#         # Expecting ["users", "brand", "123"]
#         if len(parts) == 3 and parts[0] == "users" and parts[1] == "brand" and parts[2].isdigit():
#             return int(parts[2])
#         return None


#     # Get
#     @auth_required(permission="View" , roles="")
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
#             if path == "/users/brand":
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
#     @auth_required(permission="Create" , roles="")
#     def handle_post(self):
#         if self.request_handler.path != "/users/brand":
#             return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

#         data = self._read_json()
#         name = data.get("name")
#         status_id = data.get("status_id")


#         if not name:
#             return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'name' field"}).encode()
        
#         if not status_id:
#             return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'status id' field"}).encode()

#         conn = get_db()
#         if not conn:
#             return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

#         try:
#             cursor = conn.cursor(dictionary=True)  
#             cursor.execute("INSERT INTO brand (name ,status_id) VALUES (%s, %s)", (name,status_id,))
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
#     @auth_required(permission="Update" , roles="")
#     def handle_put(self):
#         brand_id = self._get_id()
#         if not brand_id:
#             return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

#         data = self._read_json()
#         name = data.get("name")
#         status_id = data.get("status_id")

        
#         if not name:
#             return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'name' field"}).encode()
        
#         if not status_id:
#             return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'status id' field"}).encode()
        
#         conn = get_db()
#         if not conn:
#             return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

#         try:
#             cursor = conn.cursor()
#             cursor.execute("UPDATE brand SET name = %s , status_id = %s WHERE id = %s", (name, status_id , brand_id  ))
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
#     @auth_required(permission="Delete" , roles="")
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

# JSON date converter
def convert_datetime(obj):
    if isinstance(obj, list):
        return [convert_datetime(item) for item in obj]
    elif isinstance(obj, dict):
        return {
            key: (value.isoformat() if isinstance(value, (datetime.datetime, datetime.date)) else value)
            for key, value in obj.items()
        }
    return obj


class BrandUsersHandler:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def _read_json(self):
        length = int(self.request_handler.headers.get('Content-Length', 0))
        if length:
            raw = self.request_handler.rfile.read(length).decode()
            return json.loads(raw)
        return {}

    def _get_path_parts(self):
        return self.request_handler.path.strip("/").split("/")

    def _get_brand_id(self):
        parts = self._get_path_parts()
        return int(parts[1]) if len(parts) == 2 and parts[0] == "brand" and parts[1].isdigit() else None

    @auth_required(permission="View", roles=["staff", "Manager"])
    def handle_get(self):
        path = self.request_handler.path
        if path == "/favicon.ico":
            return 204, {}, b""

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor(dictionary=True)
            brand_id = self._get_brand_id()

            if path == "/users/brand":
                cursor.execute("SELECT * FROM brand WHERE status = 'active'")
                rows = convert_datetime(cursor.fetchall())
                return 200, {"Content-Type": "application/json"}, json.dumps({
                    "message": "Active brands listed.",
                    "data": rows
                }).encode()

            elif brand_id:
                cursor.execute("SELECT * FROM brand WHERE id = %s", (brand_id,))
                row = cursor.fetchone()

                if not row:
                    return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Brand not found"}).encode()

                if row["status"].lower() != "active":
                    return 403, {"Content-Type": "application/json"}, json.dumps({"error": "Brand is inactive"}).encode()

                return 200, {"Content-Type": "application/json"}, json.dumps({
                    "message": "Brand retrieved.",
                    "data": convert_datetime(row)
                }).encode()

            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

    @auth_required(permission="Create", roles=["staff", "Manager"])
    def handle_post(self):
        if self.request_handler.path != "/users/brand":
            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid URL"}).encode()

        data = self._read_json()
        name = data.get("name")
        status = data.get("status", "active")

        if not name:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing 'name' field"}).encode()

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("INSERT INTO brand (name, status) VALUES (%s, %s)", (name, status))
            conn.commit()
            brand_id = cursor.lastrowid

            cursor.execute("SELECT * FROM brand WHERE id = %s", (brand_id,))
            row = convert_datetime(cursor.fetchone())

            return 201, {"Content-Type": "application/json"}, json.dumps({
                "message": "Brand created successfully!",
                "data": row
            }).encode()

        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

    @auth_required(permission="Update", roles=["staff", "Manager"])
    def handle_put(self):
        brand_id = self._get_brand_id()
        if not brand_id:
            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid or missing brand ID"}).encode()

        data = self._read_json()
        name = data.get("name")
        status = data.get("status", "active")

        if not name or not status:
            return 400, {"Content-Type": "application/json"}, json.dumps({"error": "Missing required fields"}).encode()

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE brand SET name = %s, status = %s WHERE id = %s", (name, status, brand_id))
            conn.commit()

            if cursor.rowcount == 0:
                return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Brand not found"}).encode()

            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM brand WHERE id = %s", (brand_id,))
            updated = convert_datetime(cursor.fetchone())

            return 200, {"Content-Type": "application/json"}, json.dumps({
                "message": "Brand updated successfully!",
                "data": updated
            }).encode()
        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()

    @auth_required(permission="Delete", roles=["staff", "Manager"])
    def handle_delete(self):
        brand_id = self._get_brand_id()
        if not brand_id:
            return 404, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid or missing brand ID"}).encode()

        conn = get_db()
        if not conn:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": "DB connection failed"}).encode()

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM brand WHERE id = %s", (brand_id,))
            row = cursor.fetchone()

            if not row:
                return 404, {"Content-Type": "application/json"}, json.dumps({"message": "Brand not found"}).encode()

            cursor.execute("DELETE FROM brand WHERE id = %s", (brand_id,))
            conn.commit()

            return 200, {"Content-Type": "application/json"}, json.dumps({
                "message": "Brand deleted successfully!",
                "data": convert_datetime(row)
            }).encode()
        except Error as e:
            return 500, {"Content-Type": "application/json"}, json.dumps({"error": str(e)}).encode()
        finally:
            conn.close()
