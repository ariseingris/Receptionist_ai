import json
import os
import matplotlib.pyplot as plt

def visualize_multi_line_chart():
    print("Đang đọc dữ liệu từ intents.json và responses.json...")
    
    # 1. Định vị file intents.json và responses.json
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    intents_path = os.path.join(base_dir, 'content.json')
    responses_path = os.path.join(base_dir, 'responses.json')
    
    try:
        with open(intents_path, 'r', encoding='utf-8') as f:
            intents_data = json.load(f)
        with open(responses_path, 'r', encoding='utf-8') as f:
            responses_data = json.load(f)
    except FileNotFoundError as e:
        print(f"Cảnh báo: Không tìm thấy file dữ liệu. Chi tiết: {e}")
        return

    # 2. Chuẩn bị dữ liệu để vẽ
    # Lấy danh sách tất cả các ý định (tránh trường hợp file có file không)
    all_intents = list(set(list(intents_data.keys()) + list(responses_data.keys())))
    all_intents.sort() # Sắp xếp alphabet cho dễ nhìn
    
    intent_counts = []
    response_counts = []
    
    for intent in all_intents:
        # Đếm số câu trong mỗi intent, nếu không có thì mặc định là 0
        intent_counts.append(len(intents_data.get(intent, [])))
        response_counts.append(len(responses_data.get(intent, [])))
        
    # 3. Sử dụng Matplotlib để vẽ Biểu đồ đa đường (Multi-line Chart)
    # Cài đặt kích thước khung hình
    plt.figure(figsize=(10, 6))
    
    # Vẽ đường thứ 1: Dữ liệu intents (Câu mẫu)
    plt.plot(all_intents, intent_counts, marker='o', color='blue', linewidth=2, label='Số lượng câu mẫu (Content)')
    
    # Vẽ đường thứ 2: Dữ liệu responses (Câu trả lời)
    plt.plot(all_intents, response_counts, marker='s', color='red', linewidth=2, linestyle='--', label='Số lượng câu trả lời (Responses)')
    
    # Thêm số lượng cụ thể lên các điểm của đường thứ 1
    for i, txt in enumerate(intent_counts):
        plt.annotate(txt, (all_intents[i], intent_counts[i]), textcoords="offset points", xytext=(0,10), ha='center', color='blue')
        
    # Thêm số lượng cụ thể lên các điểm của đường thứ 2
    for i, txt in enumerate(response_counts):
        plt.annotate(txt, (all_intents[i], response_counts[i]), textcoords="offset points", xytext=(0,-15), ha='center', color='red')
    
    # Trang trí biểu đồ
    plt.title('So sánh Số lượng Câu mẫu và Câu trả lời theo Ý định', fontsize=14, fontweight='bold')
    plt.xlabel('Ý định (Intent)', fontsize=12)
    plt.ylabel('Số lượng', fontsize=12)
    
    # Hiển thị chú thích (Legend) để phân biệt 2 đường
    plt.legend(loc ="upper left")
    
    # Xoay nhãn trục x một góc 45 độ để chữ không bị đè lên nhau
    plt.xticks(rotation=45, ha='right')
    
    # Thêm lưới mờ để dễ nhìn
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Tự động căn chỉnh bố cục
    plt.tight_layout()
    
    # Hiển thị biểu đồ lên màn hình
    print("Đang hiển thị biểu đồ...")
    plt.show()

if __name__ == "__main__":
    visualize_multi_line_chart()