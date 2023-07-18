import json
from http.server import BaseHTTPRequestHandler
from utils import load_mac_mapping

import requests

from local_ip_handler import LocalIPHandler

host = 'localhost'
port = 80

class TunnelMasterHandler(BaseHTTPRequestHandler):
    def __get_all_mappings(self) -> dict:
        return load_mac_mapping()

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            mapping = self.__get_all_mappings()
            mapping_json = json.dumps(mapping)

            self.wfile.write(mapping_json.encode())
        except:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html>Internal Server Error</html>", "utf-8"))
