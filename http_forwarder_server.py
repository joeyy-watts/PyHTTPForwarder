from http.server import BaseHTTPRequestHandler

import requests

host = 'localhost'
port = 80

class PyHTTPForwarderHandler(BaseHTTPRequestHandler):

    def __init__(self, forward_target, *args, **kwargs):
        self.target = forward_target
        super().__init__(*args, **kwargs)

    def __forward_http(self):
        try:
            result = requests.get("http://"+ self.target + self.path)
            print(f"forwarded")
        except Exception as e:
            print(f"Failed to forward to {self.target}{self.path}")
            raise Exception(e)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html>OK</html>", "utf-8"))
        return result

    def do_GET(self):
        print(f"got request at path :: {self.path}")
        print(f"forwarding to {self.target}")
        self.__forward_http()
