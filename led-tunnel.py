import os
import re
import subprocess

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

def refresh_arp_cache():
	cmd = 'nmap -sP 192.168.1.0/24'
	print(f'refreshing arp cache with command :: {cmd}')
	subprocess.run(cmd.split(' '))

def get_main_ip():
	# todo: only refresh once every day
	#refresh_arp_cache()
	cmd = f"arp -an | grep {get_main_mac_address()}"
	print(f"getting main led controller ip with command :: {cmd}")
	ret = subprocess.check_output((cmd),shell=True,stderr=subprocess.STDOUT).decode()
	print(f'ret is {ret}')
	pattern = "([0-9.])+"
	match = re.search(pattern, ret)
	return match.group()


if __name__ == '__main__':
	print(get_main_ip())
