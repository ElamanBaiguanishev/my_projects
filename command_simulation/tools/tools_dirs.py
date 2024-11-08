import random


def get_serial_tome() -> str:
    return '{:04X}-{:04X}'.format(random.randint(0, 65535), random.randint(0, 65535))


def get_DUID() -> str:
    DUID = "00-01-00-01-" + '-'.join([hex(random.randint(0, 255))[2:].upper() for _ in range(10)])
    if len(DUID) == 41:
        return DUID
    else:
        return get_DUID()


def get_ip6() -> str:
    ip6 = "fe80::" + hex(random.randint(0, 255))[2:] + hex(random.randint(0, 255))[2:] + ":" \
          + hex(random.randint(0, 255))[2:] + hex(random.randint(0, 255))[2:] + ":" \
          + hex(random.randint(0, 255))[2:] + hex(random.randint(0, 255))[2:] + ":" \
          + hex(random.randint(0, 255))[2:] + hex(random.randint(0, 255))[2:] + "%" + str(random.randint(6, 12))
    if len(ip6) in (27, 28):
        return ip6
    else:
        return get_ip6()


def get_mac_address() -> str:
    mac_address = '-'.join([hex(random.randint(0, 255))[2:].upper() for _ in range(6)])
    if len(mac_address) == 17:
        return mac_address
    else:
        return get_mac_address()


def get_min(M: int):
    if M > 60:
        return res_m[M % 60]
    else:
        return res_m[M]
