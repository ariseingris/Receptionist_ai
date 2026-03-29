import os
import json
import re

# 1. Xác định base_dir (thư mục chứa file cleandata.py)
base_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Đọc file JSON NGAY TỪ ĐẦU (đọc 1 lần duy nhất khi chạy chương trình)
file_path = os.path.join(base_dir, 'teen_dictionary.json')

# Biến STOP_WORDS toàn cục
STOP_WORDS = set() 
TEEN_CODE = {} # Biến toàn cục để lưu mã teen code

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        STOP_WORDS = set(data.get("STOP_WORDS", []))
        TEEN_CODE = data.get("TEEN_CODE_DICT", {})
except FileNotFoundError:
    print(f"Cảnh báo: Không tìm thấy file {file_path}")
except json.JSONDecodeError:
    print(f"Lỗi: File {file_path} không phải là JSON hợp lệ")

def normalize_text(text: str) -> str:
    """
    Chuẩn hóa văn bản và lọc bỏ từ thừa.
    """
    if not text:
        return ""
    
    # Chuyển thành chữ thường
    text = text.lower()
    
    # Xóa dấu câu cơ bản
    text = re.sub(r'[!?,.;:]', '', text)
    
    # Tách câu thành các từ và loại bỏ các từ nằm trong STOP_WORDS (unvital_words)
    words = text.split()
    cleaned_words = [word for word in words if word not in STOP_WORDS]
    text = ' '.join(cleaned_words)
    
    # Xóa khoảng trắng thừa 2 đầu
    return text.strip()