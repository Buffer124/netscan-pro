import os
import re
from typing import Dict

class VendorEngine:
    def __init__(self, db_path: str = None):
        self.vendors: Dict[str, str] = {}
        if db_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, "data", "manuf")
        self.load_manuf_db(db_path)

    def load_manuf_db(self, path: str):
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = re.split(r"\s+", line, maxsplit=2)
                if len(parts) >= 2:
                    mac_prefix = parts[0].upper().replace("-", ":")
                    if len(mac_prefix.split(":")) == 3:
                        vendor_name = parts[2] if len(parts) >= 3 else parts[1]
                        self.vendors[mac_prefix] = vendor_name

    def lookup(self, mac: str) -> str:
        if not mac:
            return "Unknown"
        clean_mac = re.sub(r"[^A-Fa-f0-9]", ":", mac).upper()
        parts = clean_mac.split(":")
        if len(parts) >= 3:
            oui = ":".join(parts[:3])
            return self.vendors.get(oui, "Unknown Vendor")
        return "Unknown"