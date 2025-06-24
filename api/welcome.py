import json

def welcome_handler():
    status = 200
    headers = {"Content-Type": "application/json"}

    try:
        body_dict = {
            "message": "Successfully!",
            "data": {
                "Welcome": "Python for api !"
            },
        }
        body = json.dumps(body_dict).encode("utf-8")
    except (TypeError, ValueError) as e:
        status = 500
        body = json.dumps({
            "message": "Internal Server Error",
            "error": str(e)
        }).encode("utf-8")

    return status, headers, body