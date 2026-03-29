import json
import os
import random
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from data.cleandata import normalize_text

class MLBrain:
    def __init__(self):
        """Khởi tạo và huấn luyện mô hình ngay khi bật chương trình (Tính đóng gói)"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(base_dir)
        
        self.miss_log_path = os.path.join(project_dir, 'logs', 'miss_log.txt')
        
        # 1. Load Data
        with open(os.path.join(base_dir, 'content.json'), 'r', encoding='utf-8') as f:
            self.intents = json.load(f)
        with open(os.path.join(base_dir, 'responses.json'), 'r', encoding='utf-8') as f:
            self.responses = json.load(f)
            
        # 2. Train Model (Tự động học ngay khi khởi tạo)
        self.model = self._train_model()

    def _train_model(self):
        """
        Phương thức private (có dấu _ ở đầu) dùng để huấn luyện model.
        Biến file JSON thành X (câu văn) và y (nhãn/ý định).
        """
        X_train = []
        y_train = []
        
        # Chuẩn bị dữ liệu
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
        
        # Ngưỡng tự tin (Threshold): Nếu xác suất < 30% (0.3), coi như không hiểu
        if max_prob < 0.3:
            self.log_miss(user_input, max_prob)
            return f"🤖 AI ML chưa đủ tự tin ({max_prob:.0%} độ chắc chắn). Vui lòng nói rõ hơn!", False
            
        # 3. TReturn res
        possible_responses = self.responses.get(predicted_intent, ["Tôi hiểu nhưng chưa biết nói gì."])
        
        # distinguish ML response with a confidence score
        final_answer = f"[ML {max_prob:.0%}] {random.choice(possible_responses)}"
        return final_answer, True