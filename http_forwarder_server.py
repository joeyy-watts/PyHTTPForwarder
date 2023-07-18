from http.server import BaseHTTPRequestHandler

import requests

from local_ip_handler import LocalIPHandler

host = 'localhost'
port = 80

class PyHTTPForwarderHandler(BaseHTTPRequestHandler):

    def __init__(self, target_mac_address, *args, **kwargs):
        self.local_ip_handler = LocalIPHandler(target_mac_address)
        super().__init__(*args, **kwargs)

    def __forward_http(self):
        # TODO: support other HTTP methods
        # TODO: return result from target to caller
        try:
            result = requests.get("http://" + self.local_ip_handler.local_ip + self.path)

            if result.status_code != 200:
                print(f"Target returned non-OK status code, updating local IP and retrying..")
                self.local_ip_handler.refresh_local_ip()
                result = requests.get("http://" + self.local_ip_handler.local_ip + self.path)
                if result.status_code != 200:
                    print(f"Failed to forward")

            print(f"forwarded, result is :: {result}")
        except Exception as e:
            print(f"Failed to forward to {self.local_ip_handler.local_ip}{self.path}")
            raise Exception(e)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html>OK</html>", "utf-8"))
        return result

    def do_GET(self):
        print(f"got request at path :: {self.path}")
        print(f"forwarding to {self.local_ip_handler.local_ip}")
        self.__forward_http()
