from curses import raw
import json
import os
import random
from datetime import datetime
from data.cleandata import normalize_text

class SimpleBrain: #the set of permutation and recognition rules for matching user input to intents
    def __init__(self):
        # Xác định đường dẫn tuyệt đối để tránh lỗi khi chạy ở thư mục khác
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(base_dir)
        
        self.log_dir = os.path.join(project_dir, 'logs')
        self.miss_log_path = os.path.join(self.log_dir, 'miss_log.txt')
        
        # Tạo thư mục logs nếu chưa có
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Load dữ liệu từ JSON
        with open(os.path.join(base_dir, 'content.json'), 'r', encoding='utf-8') as f:
            self.content = json.load(f)
            
        with open(os.path.join(base_dir, 'responses.json'), 'r', encoding='utf-8') as f:
            self.responses = json.load(f)

    def log_miss(self, user_input: str):
        """Ghi lại các câu không khớp vào miss_log.txt"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.miss_log_path, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] MISS: {user_input}\n")

    def get_response(self, user_input: str) -> tuple[str, bool]:

        clean_text = normalize_text(user_input)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        address = "abc xyz"
        
        # Duyệt qua các ý định và từ khóa
        for intent, keywords in self.content.items():
            for kw in keywords:
                # Kiểm tra xem từ khóa có nằm trong chuỗi đầu vào không
                if kw in clean_text:
                    # Nếu có, chọn ngẫu nhiên một câu trả lời trong list responses
                    possible_responses = self.responses.get(intent, ["Tôi hiểu ý định nhưng chưa có câu trả lời."])
                    
                    final_response = random.choice(possible_responses).replace("{time}", current_time).replace("{address}", address).replace("{location}", address)

                    final_response = final_response.replace("{time}", current_time.strftime("%Y-%m-%d %H:%M:%S")).replace("{address}", address).replace("{location}", address)
                    final_response = final_response.replace("{date}", current_time.strftime("%Y-%m-%d"))
                    final_response = final_response.replace("{weather}", "nắng")
                    final_response = final_response.replace("{schedule}", current_time.strftime("%Y-%m-%d %H:%M:%S"))  # Nếu muốn chèn câu người dùng vào phản hồi

                    return final_response, True
        
        # NẾU KHÔNG MATCH TỪ KHÓA NÀO
        self.log_miss(user_input)
        return "🤖 AI Cơ Bản không hiểu. [Chuyển sang model phức tạp (LLM)...]", False