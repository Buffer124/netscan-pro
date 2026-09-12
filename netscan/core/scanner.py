import concurrent.futures
import ipaddress
import platform
import re
import socket
import subprocess
from typing import Dict, List

SERVICES_MAP = {
    21: "FTP", 22: "SSH", 23: "Telnet", 53: "DNS",
    80: "HTTP Web Admin", 443: "HTTPS", 445: "SMB/Fileshare",
    554: "RTSP (Camera IP)", 3389: "RDP", 8080: "HTTP Alt", 9100: "Printer"
}

class NetworkScanner:
    @staticmethod
    def _ping_worker(ip: str):
        is_win = platform.system().lower() == "windows"
        cmd = ["ping", "-n", "1", "-w", "250", ip] if is_win else ["ping", "-c", "1", "-W", "1", ip]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        except Exception:
            pass

    @staticmethod
    def _read_arp_table() -> Dict[str, str]:
        devices = {}
        try:
            output = subprocess.check_output(["arp", "-a"]).decode("utf-8", errors="ignore")
            mac_pattern = re.compile(
                r"(\d{1,3}(?:\.\d{1,3}){3})\s+([0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2})"
            )
            for line in output.splitlines():
                match = mac_pattern.search(line)
                if match:
                    ip, mac = match.groups()
                    mac = mac.replace("-", ":").upper()
                    if mac != "FF:FF:FF:FF:FF:FF" and not ip.startswith("224.") and not ip.endswith(".255"):
                        devices[ip] = mac
        except Exception:
            pass
        return devices

    @staticmethod
    def scan_ports(ip: str, ports: List[int] = list(SERVICES_MAP.keys()), timeout: float = 0.25) -> List[str]:
        open_svcs = []
        for port in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                if s.connect_ex((ip, port)) == 0:
                    open_svcs.append(f"{port}/{SERVICES_MAP.get(port, 'Unknown')}")
        return open_svcs

    @classmethod
    def run_discovery(cls, subnet_cidr: str, threads: int = 80) -> Dict[str, str]:
        net = ipaddress.ip_network(subnet_cidr, strict=False)
        target_ips = [str(ip) for ip in net.hosts()]

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(cls._ping_worker, target_ips)

        arp_dict = cls._read_arp_table()
        return {ip: mac for ip, mac in arp_dict.items() if ipaddress.ip_address(ip) in net}