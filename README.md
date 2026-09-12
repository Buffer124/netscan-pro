Set-Content -Path README.md -Value @"
# ⚡ NetScan Pro - Network Intelligence Tool

Công cụ quét mạng nội bộ (LAN Scanner) tốc độ cao dành cho Desktop, hỗ trợ phát hiện thiết bị và nhận diện thương hiệu phần cứng hoàn toàn ngoại tuyến (Offline IEEE OUI Database).

## ✨ Tính Năng Nổi Bật

- ⚡ **Quét mạng siêu tốc:** Quét dải subnet \`/24\` (254 host) bằng ThreadPool song song.
- 🔍 **Nhận diện Vendor tự động:** Tra cứu tên nhà sản xuất từ địa chỉ MAC (Hikvision, Dahua, Kbvision, DrayTek, Apple, Microsoft,...).
- 🛡️ **Deep Scan:** Tùy chọn kiểm tra các cổng dịch vụ mở (HTTP, HTTPS, RTSP Camera, RDP, Printer).
- 🌙 **Giao diện hiện đại:** Hỗ trợ Dark Mode xây dựng trên nền CustomTkinter.

## 🚀 Cài Đặt & Chạy Từ Mã Nguồn

\`\`\`bash
git clone https://github.com/Buffer124/netscan-pro.git
cd netscan-pro
pip install customtkinter rich requests
python netscan/gui.py
\`\`\`

## 📦 Tải Bản Cài Đặt Sẵn (.EXE)
Tải trực tiếp file \`NetScanPro.exe\` tại mục [Releases](https://github.com/Buffer124/netscan-pro/releases).
"@

git add README.md
git commit -m "docs: add project README"
git push origin main
