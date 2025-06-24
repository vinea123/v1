from http.server import BaseHTTPRequestHandler
from api.welcome import welcome_handler
from api.auth.auth import handle_logout
from api.auth.auth import handle_login
# admin
from api.admin.setting.status import StatusHandler
from api.admin.setting.gender import GenderHandler
from api.admin.setting.roles import RolesHandler
from api.admin.setting.permission import PermissionHandler
from api.admin.setting.roles_permission import Roles_PermissionHandler
from api.admin.users import UsersHandler
from api.admin.brand import BrandHandler
# Users
from api.users.brand import BrandUsersHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def handle_request(self):
        path = self.path
        method = self.command

        # Route for welcome
        if path == "/" and method == "GET":
            status, headers, body = welcome_handler()

        #  Login 

        # Route for login
        elif path == "/login" and method == "POST":
            status, headers, body = handle_login(self)

        # Route for logout
        elif path == "/logout" and method == "POST":
            status, headers, body = handle_logout(self)

        # Admin
        
        # Route for gender        
        elif path.startswith("/admin/gender"):
            status_handler = GenderHandler(self)
            if method == "GET":
                status, headers, body = status_handler.handle_get()
            elif method == "POST":
                status, headers, body = status_handler.handle_post()
            elif method == "PUT":
                status, headers, body = status_handler.handle_put()
            elif method == "DELETE":
                status, headers, body = status_handler.handle_delete()
            else:
                status, headers, body = 405, {"Content-Type": "application/json"}, b'{"error":"Method Not Allowed"}'

        # Route for roles
        elif path.startswith("/admin/roles"):
            status_handler = RolesHandler(self)
            if method == "GET":
                status, headers, body = status_handler.handle_get()
            elif method == "POST":
                status, headers, body = status_handler.handle_post()
            elif method == "PUT":
                status, headers, body = status_handler.handle_put()
            elif method == "DELETE":
                status, headers, body = status_handler.handle_delete()
            else:
                status, headers, body = 405, {"Content-Type": "application/json"}, b'{"error":"Method Not Allowed"}'

        # Route for Permnission
        elif path.startswith("/admin/permission"):
            status_handler = PermissionHandler(self)
            if method == "GET":
                status, headers, body = status_handler.handle_get()
            elif method == "POST":
                status, headers, body = status_handler.handle_post()
            elif method == "PUT":
                status, headers, body = status_handler.handle_put()
            elif method == "DELETE":
                status, headers, body = status_handler.handle_delete()
            else:
                status, headers, body = 405, {"Content-Type": "application/json"}, b'{"error":"Method Not Allowed"}'


        # Route for Roles Permnission
        elif path.startswith("/admin/rolepermission"):
            status_handler = Roles_PermissionHandler(self)
            if method == "GET":
                status, headers, body = status_handler.handle_get()
            elif method == "POST":
                status, headers, body = status_handler.handle_post()
            elif method == "PUT":
                status, headers, body = status_handler.handle_put()
            elif method == "DELETE":
                status, headers, body = status_handler.handle_delete()
            else:
                status, headers, body = 405, {"Content-Type": "application/json"}, b'{"error":"Method Not Allowed"}'



        # Route for users
        elif path.startswith("/admin/users"):
            status_handler = UsersHandler(self)
            if method == "GET":
                status, headers, body = status_handler.handle_get()
            elif method == "POST":
                status, headers, body = status_handler.handle_post()
            elif method == "PUT":
                status, headers, body = status_handler.handle_put()
            elif method == "DELETE":
                status, headers, body = status_handler.handle_delete()
            else:
                status, headers, body = 405, {"Content-Type": "application/json"}, b'{"error":"Method Not Allowed"}'



        # Route for brand
        elif path.startswith("/admin/brand"):
            status_handler = BrandHandler(self)
            if method == "GET":
                status, headers, body = status_handler.handle_get()
            elif method == "POST":
                status, headers, body = status_handler.handle_post()
            elif method == "PUT":
                if path.endswith("/status"):
                    status, headers, body = status_handler.handle_status()
                else:
                    status, headers, body = status_handler.handle_put()
            elif method == "DELETE":
                status, headers, body = status_handler.handle_delete()
            else:
                status, headers, body = 405, {"Content-Type": "application/json"}, b'{"error":"Method Not Allowed"}'


        # User

        # Route for brand
        elif path.startswith("/users/brand"):
            status_handler = BrandUsersHandler(self)
            if method == "GET":
                status, headers, body = status_handler.handle_get()
            elif method == "POST":
                status, headers, body = status_handler.handle_post()
            elif method == "PUT":
                status, headers, body = status_handler.handle_put()
            elif method == "DELETE":
                status, headers, body = status_handler.handle_delete()
            else:
                status, headers, body = 405, {"Content-Type": "application/json"}, b'{"error":"Method Not Allowed"}'


        else:
            status, headers, body = 404, {"Content-Type": "application/json"}, b'{"error": "Not Found"}'

        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def do_DELETE(self):
        self.handle_request()



