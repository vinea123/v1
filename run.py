from http.server import HTTPServer
from routes.api import SimpleHTTPRequestHandler

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on http://127.0.0.1:{port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stop!")
    finally:
        httpd.server_close()

if __name__ == "__main__":
    run()


