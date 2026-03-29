import sys
import os

# Thêm đường dẫn thư mục gốc vào sys.path để import được module brain
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.match_key import SimpleBrain
from data.sci_brain import MLBrain

def run_tests():
    brain = MLBrain()
    
    # 15 câu hỏi thông thường và hóc búa
    test_cases = [
        "Xin chào shop",                      # 1. Chào hỏi bình thường
        "Ê có ai ở đây không?",               # 2. Chào hỏi suồng sã
        "Bây giờ là mấy giờ rồi nhỉ?",        # 3. Hỏi giờ
        "Cho mình xin địa chỉ ở đâu vậy?",    # 4. Hỏi địa điểm
        "Tôi muốn đặt lịch hẹn ngày mai",     # 5. Đặt lịch chuẩn
        "Tạm biệt nhé",                       # 6. Chào tạm biệt
        "Đặt cho tôi 1 bàn 2 người",          # 7. Đặt lịch (dùng từ đặt bàn)
        "Shop mở cửa lúc mấy giờ?",           # 8. Cố tình nhầm lẫn (vừa có "mấy giờ", ý định hỏi lịch hoạt động)
        
        # Các câu dễ gây MISS
        "Thời tiết Hà Nội hôm nay thế nào?",  # 9. Miss (Không có trong từ khóa)
        "Bạn có thể làm toán không?",         # 10. Miss
        "Cho hỏi shop có chi nhánh ở HCM không?", # 11. Có "ở đâu" không? Không có, sẽ Miss nếu không rèn kỹ.
        "Ai là tổng thống Mỹ hiện tại?",      # 12. Miss (Câu hỏi kiến thức)
        "Tôi bị đau đầu quá",                 # 13. Miss (Trò chuyện phiếm)
        "bôk lịch cho anh em ơi",             # 14. Viết sai chính tả chữ "book" -> Miss
        "Mai tớ ghé lấy đồ nha"               # 15. Ý định thông báo -> Miss
    ]
    
    print("🚀 BẮT ĐẦU CHẠY TEST 15 CÂU HỎI...\n")
    
    match_count = 0
    miss_count = 0
    
    for i, question in enumerate(test_cases, 1):
        print(f"Câu {i}: '{question}'")
        response, is_matched = brain.get_response(question)
        
        if is_matched:
            print(f"  -> ✅ MATCH: {response}")
            match_count += 1
        else:
            print(f"  -> ❌ MISS: {response}")
            miss_count += 1
        print("-" * 40)
            
    print("\n📊 BÁO CÁO TỔNG KẾT:")
    print(f"Tổng số câu: {len(test_cases)}")
    print(f"Số câu Match: {match_count}")
    print(f"Số câu Miss : {miss_count}")
    print("\nCác câu Miss đã được ghi vào file logs/miss_log.txt")

if __name__ == "__main__":
    run_tests()