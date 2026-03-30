import json
import os
import random
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from data.cleandata import normalize_text
from data.match_key import SimpleBrain

class MLBrain:
    def __init__(self):
        """Khởi tạo và huấn luyện mô hình ngay khi bật chương trình (Tính đóng gói)"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(base_dir)
        
        self.miss_log_path = os.path.join(project_dir, 'logs', 'miss_log.txt')
        os.makedirs(os.path.dirname(self.miss_log_path), exist_ok=True)
        
        # 1. Load Data
        with open(os.path.join(base_dir, 'content.json'), 'r', encoding='utf-8') as f:
            self.intents = json.load(f)
        with open(os.path.join(base_dir, 'responses.json'), 'r', encoding='utf-8') as f:
            self.responses = json.load(f)
            
        # 2. Train Model (Tự động học ngay khi khởi tạo)
        self.model = self._train_model()

    def _train_model(self):
        """
        Phương thức private (có dấu _ ở đầu) dùng for train model.
        Biến file JSON thành X (câu văn) và y (nhãn/ý định).
        """
        X_train = []
        y_train = []
        
        # prepare
        for intent, sentences in self.intents.items():
            for sentence in sentences:
                # Nên normalize luôn data huấn luyện để đồng bộ với lúc test
                X_train.append(normalize_text(sentence))
                y_train.append(intent)
                
        # Tạo một Pipeline: 
        # Bước 1: Biến chữ thành Ma trận tần suất (TF-IDF)
        # Bước 2: Dùng thuật toán Naive Bayes để phân loại
        model = make_pipeline(TfidfVectorizer(), MultinomialNB())
        
        # start train (fit)
        model.fit(X_train, y_train)
        return model

    def log_miss(self, user_input: str, max_prob: float):
        """record the command that have low confindence"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.miss_log_path, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] MISS (Prob: {max_prob:.2f}): {user_input}\n")

    def get_response(self, user_input: str) -> tuple[str, bool]:
        """
        Thay vì dùng for loop tìm keyword, ta dùng Model ML để dự đoán
        """
        clean_text = normalize_text(user_input)
        if not clean_text:
            return "Bạn hãy nói gì đó đi!", False

        # 1. Dự đoán Ý định (Intent)
        predicted_intent = self.model.predict([clean_text])[0]
        
        # 2. Lấy xác suất tự tin (Confidence Score) của dự đoán đó
        # (Để tránh trường hợp người dùng gõ linh tinh máy cũng cố đoán)
        probabilities = self.model.predict_proba([clean_text])[0]
        max_prob = max(probabilities)
        
        # Ngưỡng tự tin (Threshold): Nếu xác suất < 50% (0.5), coi như không hiểu
        if max_prob < 0.5:
            self.log_miss(user_input, max_prob)
            return f"Chuyển sang model phức tạp [confidence: {max_prob:.2f}]", False
            
        # 3. TReturn res
        possible_responses = self.responses.get(predicted_intent, ["Tôi hiểu nhưng chưa biết nói gì."])
        now = datetime.now()
        current_time = now.strftime("%H:%M")          # Lấy giờ phút (VD: 14:30)
        current_date = now.strftime("%d/%m/%Y")       # Lấy ngày tháng năm (VD: 30/03/2026)
        
        # Phân loại Sáng / Chiều / Tối
        hour = now.hour
        if hour < 12:
            session = "sáng"
        elif hour < 18:
            session = "chiều"
        else:
            session = "tối"
            
        address = "18 Đường Hoang Quoc Viet, Vien Han Lam va Công Nghệ, TP Hà Nội"
        
        # 3. Thay thế các biến động vào chuỗi
        # Pick once — reuse the same selection for substitution
        raw_response = random.choice(possible_responses)

        final_answer = raw_response.replace("{time}", current_time) \
                                .replace("{date}", current_date) \
                                .replace("{session}", session) \
                                .replace("{location}", address) \
                                .replace("{address}", address)

        # Prefix with confidence score
        final_answer = f"[ML {max_prob:.0%}] {final_answer}"
        return final_answer, True