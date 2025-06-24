from api.auth.auth import verify_token
import json

def auth_required(permission=None, roles=None):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            auth_header = self.request_handler.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return 401, {"Content-Type": "application/json"}, json.dumps({"error": "Unauthorized"}).encode()

            token = auth_header.replace("Bearer ", "").strip()
            user = verify_token(token)
            if not user:
                return 401, {"Content-Type": "application/json"}, json.dumps({"error": "Invalid token"}).encode()  

            # Check roles (support str or list/tuple)
            if roles:
                required_roles = roles if isinstance(roles, (list, tuple)) else [roles]
                user_role = user.get("role", "").lower()
                if user_role not in [r.lower() for r in required_roles]:
                    return 403, {"Content-Type": "application/json"}, json.dumps({"error": "Forbidden: role required"}).encode()

            # Check permission (case-insensitive)
            if permission:
                user_perms = [p.lower() for p in user.get("permissions", [])]
                if permission.lower() not in user_perms:
                    return 403, {"Content-Type": "application/json"}, json.dumps({"error": "Forbidden: permission required"}).encode()

            self.user = user  
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

