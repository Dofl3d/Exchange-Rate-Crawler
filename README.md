# 💱 Exchange Rate Web Crawler - MB Bank

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0+-green.svg)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Công cụ crawl tỷ giá ngoại tệ real-time từ MB Bank và chuyển đổi tiền tệ tự động với giao diện console thân thiện.

## 📸 Demo

```
============================================================
CHƯƠNG TRÌNH QUY ĐỔI TIỀN TỆ - NGÂN HÀNG MB
============================================================

📊 TỶ GIÁ HIỆN TẠI:
Thời gian cập nhật: 12-11-2024_14:30:00

Ngoại Tệ  Bán ra (Tiền mặt)  Bán ra (Chuyển Khoản)
USD                25,450.00                  25,350.00
EUR                27,800.00                  27,650.00
GBP                32,100.00                  31,950.00
```

## 🚀 Tính năng

- ✅ **Crawl tỷ giá real-time** từ MB Bank
- ✅ **Tự động đợi** trang load và render AngularJS
- ✅ **Lưu dữ liệu** vào file Excel tự động
- ✅ **Chuyển đổi tiền tệ** tương tác (VND ↔ Ngoại tệ ↔ Ngoại tệ)
- ✅ **Hỗ trợ 2 loại giao dịch**: Tiền mặt & Chuyển khoản
- ✅ **Giao diện console** đẹp mắt với emoji và màu sắc
- ✅ **Xử lý lỗi** thông minh

## 📋 Yêu cầu hệ thống

- **Python**: 3.8 trở lên
- **Chrome Browser**: Phiên bản mới nhất
- **ChromeDriver**: Tự động cài đặt
- **Windows**: 10/11 (hoặc Linux/macOS)

## 🔧 Cài đặt

### 1. Clone repository

```bash
git clone https://github.com/Dofl3d/Exchange-Rate-Crawler.git
cd Exchange-Rate-Crawler
```

### 2. Tạo Virtual Environment

```bash
python -m venv .venv
```

### 3. Kích hoạt Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### 4. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

## 🎯 Cách sử dụng

### Phương pháp 1: Chạy file Python

```bash
python exchange_rate_web_crawler.py
```

### Phương pháp 2: Chạy file Batch (Windows)

```bash
run.bat
```

### Phương pháp 3: Jupyter Notebook

```bash
jupyter notebook Exchange-rate_web_crawller.ipynb
```

## 📊 Cấu trúc dữ liệu

File Excel được tạo ra sẽ có cấu trúc:

| Thời gian | Ngoại Tệ | Mua vào (Tiền mặt) | Mua vào (Chuyển Khoản) | Bán ra (Tiền mặt) | Bán ra (Chuyển Khoản) |
|-----------|----------|-------------------|----------------------|------------------|---------------------|
| 12-11-2024 14:30:00 | USD | 25,200.00 | 25,100.00 | 25,450.00 | 25,350.00 |
| 12-11-2024 14:30:00 | EUR | 27,500.00 | 27,400.00 | 27,800.00 | 27,650.00 |

## 💡 Ví dụ sử dụng

### Quy đổi USD sang VND

```
💰 Nhập số tiền muốn quy đổi: 100

📤 Chọn tiền tệ NGUỒN: USD
📥 Chọn tiền tệ ĐÍCH: VND
💳 Chọn loại giao dịch: Chuyển khoản

✅ Kết quả: 2,535,000 VND
```

### Quy đổi VND sang EUR

```
💰 Nhập số tiền muốn quy đổi: 10000000

📤 Chọn tiền tệ NGUỒN: VND
📥 Chọn tiền tệ ĐÍCH: EUR
💳 Chọn loại giao dịch: Chuyển khoản

✅ Kết quả: 361.66 EUR
```

## 🛠️ Công nghệ sử dụng

| Công nghệ | Mục đích |
|-----------|----------|
| **Selenium** | Điều khiển trình duyệt Chrome, đợi AngularJS render |
| **BeautifulSoup4** | Parse và trích xuất dữ liệu HTML |
| **Pandas** | Xử lý và phân tích dữ liệu |
| **openpyxl** | Đọc/ghi file Excel |
| **WebDriverWait** | Đợi element xuất hiện trên trang |

## 📁 Cấu trúc thư mục

```
Exchange-Rate-Crawler/
│
├── exchange_rate_web_crawler.py   # File Python chính
├── Exchange-rate_web_crawller.ipynb  # Jupyter Notebook
├── run.bat                        # File batch chạy nhanh
├── requirements.txt               # Danh sách thư viện
├── .gitignore                     # Loại trừ file không cần thiết
├── README.md                      # Tài liệu hướng dẫn
│
├── .venv/                         # Virtual environment (không upload)
└── Tỷ giá quy đổi ngân hàng MB.xlsx  # File Excel kết quả (không upload)
```

## 🔍 Chi tiết kỹ thuật

### Crawling Strategy

1. **Mở trang MB Bank** với Selenium
2. **Đợi table xuất hiện** với WebDriverWait (tối đa 20 giây)
3. **Đợi AngularJS render** tbody và tr
4. **Kiểm tra dữ liệu** trong td elements
5. **Parse HTML** với BeautifulSoup
6. **Trích xuất dữ liệu** tỷ giá
7. **Lưu vào Excel** với Pandas

### Currency Conversion Logic

- **VND → Ngoại tệ**: `amount / tỷ_giá_bán_ra`
- **Ngoại tệ → VND**: `amount * tỷ_giá_bán_ra`
- **Ngoại tệ A → Ngoại tệ B**: `(amount * tỷ_giá_A) / tỷ_giá_B`

## ⚠️ Lưu ý

- Chương trình cần **Chrome Browser** đã cài đặt
- Cần **kết nối Internet** để crawl dữ liệu
- Tỷ giá **cập nhật real-time** từ MB Bank
- **Không** sử dụng cho mục đích thương mại

## 🐛 Xử lý lỗi

### Lỗi: "Module not found"
```bash
pip install -r requirements.txt
```

### Lỗi: "ChromeDriver not found"
```bash
pip install webdriver-manager
```

### Lỗi: "No data crawled"
- Kiểm tra kết nối Internet
- Đợi thêm thời gian (tăng `time.sleep()`)
- Kiểm tra lại URL MB Bank

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📝 License

Dự án này được phát hành dưới giấy phép [MIT License](LICENSE).

## 👨‍💻 Tác giả

**Dofl3d**
- GitHub: [@Dofl3d](https://github.com/Dofl3d)
- Repository: [Exchange-Rate-Crawler](https://github.com/Dofl3d/Exchange-Rate-Crawler)

## 🌟 Hỗ trợ

Nếu thấy dự án hữu ích, hãy cho một ⭐️ trên GitHub!

---

**Lưu ý**: Dự án này chỉ dành cho mục đích học tập và nghiên cứu. Không sử dụng cho mục đích thương mại.