import threading
from functools import partial
from http.server import HTTPServer

from tunnel_master_handler import TunnelMasterHandler
from utils import load_mac_mapping

from http_forwarder_server import PyHTTPForwarderHandler

# port for tunnel master to run on
TUNNEL_PORT = 8080

def get_main_mac_address():
	conf = open('./mac_addrs.conf', 'r')
	return format_mac_address(conf.read())

def format_mac_address(mac_addr: str):
	final_addr = ''
	for char_idx, char in enumerate(mac_addr):
		if (char_idx + 1) % 2 == 0 and char_idx < 11:
			final_addr = final_addr + char + ':'
		else:
			final_addr = final_addr + char
	return final_addr.lower()

def start_server_async(server: HTTPServer):
	print(f"Starting forwarder at port :: {server.server_port}")
	server.serve_forever()


if __name__ == '__main__':
	# local ip is fixed to when handler is instantiated
	# have to make this dynamic
	# have to pass MAC address to handler, have handler do local IP magic instead

	mapping = load_mac_mapping()

	# setup HTTPServers
	servers = []
	for target in mapping:
		handler = partial(PyHTTPForwarderHandler, target)
		server = HTTPServer(('', int(mapping[target])), handler)
		thread = threading.Thread(target=start_server_async, args=(server,))
		thread.start()

	print(f"Starting tunnel master at port :: {TUNNEL_PORT}")
	server = HTTPServer(('', TUNNEL_PORT), TunnelMasterHandler)
	server.serve_forever()

