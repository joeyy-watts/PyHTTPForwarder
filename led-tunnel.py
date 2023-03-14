from functools import partial
from http.server import HTTPServer

from http_forwarder_server import PyHTTPForwarderHandler


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


if __name__ == '__main__':
	port = 8080
	# local ip is fixed to when handler is instantiated
	# have to make this dynamic
	# have to pass MAC address to handler, have handler do local IP magic instead
	handler = partial(PyHTTPForwarderHandler, get_main_mac_address())
	server = HTTPServer(('', port), handler)
	print(f"Started LED Tunnel server at port {port}")
	server.serve_forever()

