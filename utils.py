import subprocess


def load_mac_mapping(conf="mac_addrs.conf"):
    """
    loads the MAC address to port mapping from config file
    :return:
    """
    conf = open('./mac_addrs.conf', 'r')
    dict = {}
    for each in conf:
        mac, port = each.split(':')
        dict[mac] = port.strip('\n')

    return dict

def refresh_arp_cache():
    cmd = 'nmap -sP 192.168.1.0/24'
    print(f'refreshing arp cache with command :: {cmd}')
    subprocess.run(cmd.split(' '))