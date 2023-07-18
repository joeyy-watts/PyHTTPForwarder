from http.server import BaseHTTPRequestHandler

import requests

from local_ip_handler import LocalIPHandler

host = 'localhost'
port = 80

class PyHTTPForwarderHandler(BaseHTTPRequestHandler):

    def __init__(self, target_mac_address, *args, **kwargs):
        self.local_ip_handler = LocalIPHandler(target_mac_address)
        super().__init__(*args, **kwargs)

    def __forward_http(self, method="GET"):
        # TODO: support other HTTP methods
        try:
            if method == "GET":
                result = requests.get("http://" + self.local_ip_handler.local_ip + self.path)
            elif method == "POST":
                result = requests.get("http://" + self.local_ip_handler.local_ip + self.path)

            if result.status_code != 200:
                print(f"Target returned non-OK status code, updating local IP and retrying..")
                self.local_ip_handler.refresh_local_ip()
                result = requests.get("http://" + self.local_ip_handler.local_ip + self.path)

                if result.status_code != 200:
                    print(f"Target returned on OK status code :: {result.status_code}")
                else:
                    print(f"Target returned OK, returning result to caller..")

                self.send_response(result.status_code)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(result.text, "utf-8"))
                return result
        except Exception as e:
            print(f"Failed to forward to {self.local_ip_handler.local_ip}{self.path}, due to exception :: {e}")
            raise Exception(e)

    def do_GET(self):
        print(f"GET request at path :: {self.path}")
        print(f"forwarding to {self.local_ip_handler.local_ip}")
        self.__forward_http(method="GET")

    def do_POST(self):
        print(f"POST request at path :: {self.path}")
        print(f"forwarding to {self.local_ip_handler.local_ip}")
        self.__forward_http(method="POST")
