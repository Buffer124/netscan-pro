import socket

def get_default_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def get_default_subnet(local_ip: str) -> str:
    parts = local_ip.split(".")
    if len(parts) == 4 and local_ip != "127.0.0.1":
        return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
    return "192.168.1.0/24"