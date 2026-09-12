import sys
import os

# Thêm đường dẫn thư mục cha để import module chuẩn xác
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import threading
import customtkinter as ctk
from netscan.core.utils import get_default_local_ip, get_default_subnet
from netscan.core.scanner import NetworkScanner
from netscan.core.vendor import VendorEngine

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NetScanGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NetScan Pro - Network Intelligence Tool")
        self.geometry("960x600")

        self.vendor_engine = VendorEngine()
        self.local_ip = get_default_local_ip()
        self.default_subnet = get_default_subnet(self.local_ip)

        self._build_ui()

    def _build_ui(self):
        header_frame = ctk.CTkFrame(self, corner_radius=10)
        header_frame.pack(fill="x", padx=15, pady=15)

        lbl = ctk.CTkLabel(header_frame, text="Subnet:", font=("Segoe UI", 13, "bold"))
        lbl.pack(side="left", padx=(15, 5), pady=10)

        self.entry_subnet = ctk.CTkEntry(header_frame, width=180)
        self.entry_subnet.insert(0, self.default_subnet)
        self.entry_subnet.pack(side="left", padx=5, pady=10)

        self.check_ports = ctk.CTkCheckBox(header_frame, text="Deep Scan (Cổng dịch vụ)")
        self.check_ports.pack(side="left", padx=15, pady=10)

        self.btn_scan = ctk.CTkButton(header_frame, text="Bắt Đầu Quét", command=self.start_scan_thread, width=130)
        self.btn_scan.pack(side="right", padx=15, pady=10)

        self.progress = ctk.CTkProgressBar(self, mode="indeterminate")
        self.progress.pack(fill="x", padx=15, pady=(0, 10))
        self.progress.set(0)

        self.text_box = ctk.CTkTextbox(self, font=("Consolas", 12), corner_radius=8)
        self.text_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def log(self, text: str):
        self.text_box.insert("end", text + "\n")
        self.text_box.see("end")

    def start_scan_thread(self):
        self.btn_scan.configure(state="disabled", text="Đang Quét...")
        self.progress.start()
        self.text_box.delete("1.0", "end")
        threading.Thread(target=self._scan_process, daemon=True).start()

    def _scan_process(self):
        subnet = self.entry_subnet.get().strip()
        deep_scan = self.check_ports.get() == 1

        self.log(f"[*] Đang quét dải IP: {subnet}...")
        devices = NetworkScanner.run_discovery(subnet)

        if not devices:
            self.log("[-] Không phát hiện thiết bị nào trong dải mạng.")
        else:
            self.log(f"[+] Tìm thấy {len(devices)} thiết bị trực tuyến.\n")
            header = f"{'IP Address':<18} | {'MAC Address':<20} | {'Nhà Sản Xuất (Vendor)':<30} | {'Dịch Vụ Mở'}"
            self.log(header)
            self.log("-" * 95)

            sorted_ips = sorted(devices.keys(), key=lambda x: [int(p) for p in x.split(".")])
            for ip in sorted_ips:
                mac = devices[ip]
                vendor = self.vendor_engine.lookup(mac)
                services_str = ""
                if deep_scan:
                    svcs = NetworkScanner.scan_ports(ip)
                    services_str = ", ".join(svcs) if svcs else "Closed/Filtered"

                row = f"{ip:<18} | {mac:<20} | {vendor:<30} | {services_str}"
                self.log(row)

        self.progress.stop()
        self.btn_scan.configure(state="normal", text="Bắt Đầu Quét")

if __name__ == "__main__":
    app = NetScanGUI()
    app.mainloop()