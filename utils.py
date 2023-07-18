import subprocess


def format_mac_address(mac_addr: str):
    final_addr = ''
    for char_idx, char in enumerate(mac_addr):
        if (char_idx + 1) % 2 == 0 and char_idx < 11:
            final_addr = final_addr + char + ':'
        else:
            final_addr = final_addr + char
    return final_addr.lower()


def load_mac_mapping(conf="mac_addrs.conf"):
    """
    loads the MAC address to port mapping from config file
    :return:
    """
    conf = open('./mac_addrs.conf', 'r')
    dict = {}
    for each in conf:
        mac, port = each.split(':')
        mac = format_mac_address(mac)
        dict[mac] = port.strip('\n')

    return dict


def refresh_arp_cache():
    cmd = 'nmap -sP 192.168.1.0/24'
    print(f'refreshing arp cache with command :: {cmd}')
    subprocess.run(cmd.split(' '))
