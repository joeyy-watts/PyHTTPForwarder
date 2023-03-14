import re
import subprocess


class LocalIPHandler:
    def __init__(self, mac_address):
        self.mac_address = mac_address
        self.local_ip = self.__get_local_ip()

    def refresh_local_ip(self):
        self.__refresh_arp_cache()
        self.local_ip = self.__get_local_ip()

    def __refresh_arp_cache(self):
        cmd = 'nmap -sP 192.168.1.0/24'
        print(f'refreshing arp cache with command :: {cmd}')
        subprocess.run(cmd.split(' '))

    def __get_local_ip(self):
        cmd = f"arp -an | grep {self.mac_address}"
        print(f"getting main led controller ip with command :: {cmd}")
        ret = subprocess.check_output((cmd), shell=True, stderr=subprocess.STDOUT).decode()

        print(f'ret is {ret}')
        pattern = "([0-9.])+"
        match = re.search(pattern, ret)
        return match.group()
