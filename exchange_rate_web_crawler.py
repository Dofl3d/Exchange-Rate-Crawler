from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import os

# Get current timestamp
current_time = datetime.now()
timestamp = current_time.strftime("%d-%m-%Y_%H:%M:%S")
file_timestamp = current_time.strftime("%d/%m/%Y %H:%M:%S")

# Initialize Chrome driver
driver = webdriver.Chrome()
print("Đang mở trang MB Bank...")

driver.get('https://www.mbbank.com.vn/ExchangeRate')

# Wait for page to load
wait = WebDriverWait(driver, 20)

print("Đang đợi bảng tỷ giá xuất hiện...")

try:
    # Wait for table to appear
    table_element = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table-fee'))
    )
    print("✓ Đã tìm thấy bảng tỷ giá")
    
    # Wait for tbody rows to appear (AngularJS render)
    tbody_rows = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'table.table-fee tbody tr'))
    )
    print(f"✓ Đã phát hiện {len(tbody_rows)} dòng dữ liệu")
    
    # Wait additional 3 seconds to ensure AngularJS finishes rendering
    time.sleep(3)
    
    # Check if data exists in td elements
    td_elements = driver.find_elements(By.CSS_SELECTOR, 'table.table-fee tbody tr td')
    if len(td_elements) > 0:
        print(f"✓ Đã load {len(td_elements)} ô dữ liệu")
    else:
        print("⚠️ Cảnh báo: Chưa có dữ liệu trong các ô")
        time.sleep(5)  # Wait more
    
    print("✓ Bảng tỷ giá đã sẵn sàng!")
    
except Exception as e:
    print(f"❌ Lỗi khi đợi bảng tỷ giá: {e}")
    print("Đang thử đợi thêm 10 giây...")
    time.sleep(10)

# Get HTML after ensuring data is loaded
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
print("✓ Đã lấy HTML của trang")

data = []

# Find the target table
table = soup.find('table', class_='table-fee')

if not table:
    print("❌ KHÔNG TÌM THẤY BẢNG TỶ GIÁ!")
    driver.quit()
else:
    print("✓ Đã tìm thấy table trong HTML")
    
    # Get tbody
    tbody = table.find('tbody')
    
    if tbody:
        rows = tbody.find_all('tr')
        print(f"✓ Tìm thấy {len(rows)} dòng trong tbody")
    else:
        print("⚠️ Không tìm thấy tbody, đang lấy tất cả tr")
        rows = table.find_all('tr')

    def convert_to_float(value):
        cleaned = re.sub(r'[^\d.]', '', value.replace(',', ''))
        try:
            return float(cleaned) if cleaned else 0.0
        except:
            return 0.0
    
    row_count = 0
    for row in rows:
        columns = row.find_all('td')
        if columns and len(columns) >= 5:
            currency = columns[0].text.strip()
            
            # Skip header row if exists
            if currency.lower() in ['ngoại tệ', 'currency', '']:
                continue
                
            buy_rate_cash = convert_to_float(columns[1].text.strip())
            buy_rate_transfer = convert_to_float(columns[2].text.strip())
            sell_rate_cash = convert_to_float(columns[3].text.strip())
            sell_rate_transfer = convert_to_float(columns[4].text.strip())
            
            # Add to list with timestamp
            data.append({
                'Thời gian': timestamp,
                'Ngoại Tệ': currency,
                'Mua vào (Tiền mặt)': buy_rate_cash,
                'Mua vào (Chuyển Khoản)': buy_rate_transfer,
                'Bán ra (Tiền mặt)': sell_rate_cash,
                'Bán ra (Chuyển Khoản)': sell_rate_transfer
            })
            row_count += 1
    
    print(f"\n{'='*60}")
    print(f"✓ Đã crawl thành công {row_count} loại ngoại tệ")
    print(f"{'='*60}\n")

# Create DataFrame
df = pd.DataFrame(data)

if df.empty:
    print("❌ KHÔNG CÓ DỮ LIỆU ĐỂ LƯU!")
    print("Vui lòng kiểm tra lại trang web hoặc thử chạy lại.")
else:
    # Fixed filename
    excel_file = 'Tỷ giá quy đổi ngân hàng MB.xlsx'
    
    # Check if file already exists
    if os.path.exists(excel_file):
        # Read old data
        df_old = pd.read_excel(excel_file)
        # Update with new data
        df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"✓ Đã cập nhật dữ liệu mới vào file: {excel_file}")
    else:
        # Create new file
        df.to_excel(excel_file, index=False, engine='openpyxl')
        print(f"✓ Đã tạo file mới: {excel_file}")
    
    print(f"✓ Thời gian cập nhật: {timestamp}")
    print(f"✓ Tổng số dòng dữ liệu: {len(df)}")

# Close browser
driver.quit()
print("✓ Đã đóng trình duyệt")

# Currency conversion function
def convert_currency(amount, from_currency, to_currency, df, rate_type='Bán ra (Chuyển Khoản)'):
    """
    Convert currency using bank's selling rate
    """
    if from_currency == 'VND':
        result = df[df['Ngoại Tệ'] == to_currency][rate_type]
        if result.empty:
            return None, f"Không tìm thấy tỷ giá cho {to_currency}"
        rate = result.values[0]
        if rate == 0:
            return None, f"Tỷ giá {to_currency} không hợp lệ"
        return amount / rate, None
        
    elif to_currency == 'VND':
        result = df[df['Ngoại Tệ'] == from_currency][rate_type]
        if result.empty:
            return None, f"Không tìm thấy tỷ giá cho {from_currency}"
        rate = result.values[0]
        if rate == 0:
            return None, f"Tỷ giá {from_currency} không hợp lệ"
        return amount * rate, None
        
    else:
        result_from = df[df['Ngoại Tệ'] == from_currency][rate_type]
        result_to = df[df['Ngoại Tệ'] == to_currency][rate_type]
        
        if result_from.empty or result_to.empty:
            return None, "Không tìm thấy tỷ giá"
            
        rate_from = result_from.values[0]
        rate_to = result_to.values[0]
        
        if rate_from == 0 or rate_to == 0:
            return None, "Tỷ giá không hợp lệ"
            
        vnd_amount = amount * rate_from
        return vnd_amount / rate_to, None


# ===== CURRENCY CONVERSION PROGRAM =====
print("\n" + "="*60)
print("CHƯƠNG TRÌNH QUY ĐỔI TIỀN TỆ - NGÂN HÀNG MB")
print("="*60)

# Display current exchange rates
print("\n📊 TỶ GIÁ HIỆN TẠI:")
print(f"Thời gian cập nhật: {timestamp}")
print(df[['Ngoại Tệ', 'Bán ra (Tiền mặt)', 'Bán ra (Chuyển Khoản)']].to_string(index=False))

# Get list of currencies
currencies = ['VND'] + list(df['Ngoại Tệ'].unique())

print("\n" + "="*60)
print("QUY ĐỔI TIỀN TỆ")
print("="*60)

# Display currency list
print("\nDanh sách ngoại tệ có sẵn:")
for i, currency in enumerate(currencies, 1):
    print(f"{i}. {currency}")

# Input amount
while True:
    try:
        amount = float(input("\n💰 Nhập số tiền muốn quy đổi: ").replace(',', ''))
        if amount <= 0:
            print("❌ Số tiền phải lớn hơn 0!")
            continue
        break
    except ValueError:
        print("❌ Vui lòng nhập số hợp lệ!")

# Select source currency
print("\n📤 Chọn tiền tệ NGUỒN:")
for i, currency in enumerate(currencies, 1):
    print(f"{i}. {currency}")

while True:
    try:
        choice_from = int(input("Chọn số (1-{}): ".format(len(currencies))))
        if 1 <= choice_from <= len(currencies):
            from_currency = currencies[choice_from - 1]
            break
        print(f"❌ Vui lòng chọn từ 1 đến {len(currencies)}!")
    except ValueError:
        print("❌ Vui lòng nhập số hợp lệ!")

# Select target currency
print("\n📥 Chọn tiền tệ ĐÍCH:")
for i, currency in enumerate(currencies, 1):
    print(f"{i}. {currency}")

while True:
    try:
        choice_to = int(input("Chọn số (1-{}): ".format(len(currencies))))
        if 1 <= choice_to <= len(currencies):
            to_currency = currencies[choice_to - 1]
            break
        print(f"❌ Vui lòng chọn từ 1 đến {len(currencies)}!")
    except ValueError:
        print("❌ Vui lòng nhập số hợp lệ!")

# Check if same currency
if from_currency == to_currency:
    print("\n❌ Không thể quy đổi cùng loại tiền tệ!")
else:
    # Select transaction type
    print("\n💳 Chọn loại giao dịch:")
    print("1. Tiền mặt")
    print("2. Chuyển khoản")
    
    while True:
        try:
            choice_type = int(input("Chọn (1 hoặc 2): "))
            if choice_type == 1:
                rate_type = 'Bán ra (Tiền mặt)'
                break
            elif choice_type == 2:
                rate_type = 'Bán ra (Chuyển Khoản)'
                break
            print("❌ Vui lòng chọn 1 hoặc 2!")
        except ValueError:
            print("❌ Vui lòng nhập số hợp lệ!")
    
    # Perform conversion
    result, error = convert_currency(amount, from_currency, to_currency, df, rate_type)
    
    print("\n" + "="*60)
    print("KẾT QUẢ QUY ĐỔI")
    print("="*60)
    
    if error:
        print(f"\n❌ Lỗi: {error}")
    else:
        print(f"\n✅ Số tiền gốc: {amount:,.2f} {from_currency}")
        print(f"✅ Loại giao dịch: {rate_type}")
        
        if to_currency == 'VND':
            print(f"✅ Kết quả: {result:,.0f} {to_currency}")
        else:
            print(f"✅ Kết quả: {result:,.2f} {to_currency}")
        
        # Display exchange rates used
        if from_currency != 'VND':
            rate_from = df[df['Ngoại Tệ'] == from_currency][rate_type].values[0]
            print(f"\n📊 Tỷ giá {from_currency}: {rate_from:,.2f} VND")
        if to_currency != 'VND':
            rate_to = df[df['Ngoại Tệ'] == to_currency][rate_type].values[0]
            print(f"📊 Tỷ giá {to_currency}: {rate_to:,.2f} VND")

print("\n" + "="*60)
print("CẢM ƠN BẠN ĐÃ SỬ DỤNG!")
print("="*60)