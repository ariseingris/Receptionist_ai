import os
import json
import re
from google import genai

# 1. Cấu hình Client với thư viện MỚI (google-genai)
# LƯU Ý: Thay dải chữ "YOUR_API_KEY_HERE" bằng API Key thật của bạn
client = genai.Client(api_key="AIzaSyA2sxOE9S2D1pSeTvbrVOiaka1IbNIdsoQ")

# Đường dẫn tới các file dữ liệu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MISS_LOG_PATH = os.path.join(BASE_DIR, 'logs', 'miss_log.txt')
CONTENT_PATH = os.path.join(BASE_DIR, 'data', 'content.json')
RESPONSES_PATH = os.path.join(BASE_DIR, 'data', 'responses.json')

def clean_json_response(text: str) -> str:
    """Xóa bỏ các ký tự Markdown do AI sinh ra để tránh lỗi parse JSON"""
    if not text:
        return "{}"
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def run_auto_update():
    print("🔄 BẮT ĐẦU QUÁ TRÌNH TỰ ĐỘNG HỌC (AUTO-UPDATE)...")
    
    # 1. Đọc file miss_log.txt
    if not os.path.exists(MISS_LOG_PATH):
        print("❌ Không tìm thấy file miss_log.txt.")
        return

    with open(MISS_LOG_PATH, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()
        missed_queries = []
        for line in raw_lines:
            if "MISS" in line:
                query = line.split("): ")[-1].strip() if "): " in line else line.split("MISS: ")[-1].strip()
                if query:
                    missed_queries.append(query)
                    
    missed_queries = list(set(missed_queries))
    
    if not missed_queries:
        print("✨ Không có dữ liệu MISS nào mới. Hệ thống đang hoàn hảo!")
        return
        
    print(f"📄 Đã tìm thấy {len(missed_queries)} câu hỏi chưa hiểu. Đang gửi cho Gemini...")

    # 2. Đọc dữ liệu Intent hiện tại
    with open(CONTENT_PATH, 'r', encoding='utf-8') as f:
        current_intents = json.load(f)
    with open(RESPONSES_PATH, 'r', encoding='utf-8') as f:
        current_responses = json.load(f)
        
    intent_keys = list(current_intents.keys())

    # 3. Ra lệnh cho Gemini API phân tích (Prompt Tiếng Anh)
    prompt = f"""
    Act as an expert NLP Data Annotator.
    I have a Vietnamese chatbot with the following existing Intents: {intent_keys}.
    
    Here is a list of user queries that the bot recently failed to understand (MISS logs):
    {missed_queries}
    
    Your task:
    1. Ignore any queries that are obvious spam, gibberish, or contain offensive language.
    2. Categorize the valid queries into the most appropriate EXISTING Intents.
    3. IF AND ONLY IF a query represents a completely new, valid topic, create a NEW INTENT. 
       - New Intent names MUST be in lowercase, snake_case, and without Vietnamese accents (e.g., 'ask_price', 'hoi_gia_tien').
    4. If you create a new Intent, you MUST provide exactly 1 polite sample response in Vietnamese for that Intent.
    
    Output exactly ONE valid JSON object and nothing else (no markdown, no explanations). Use the following strict schema:
    {{
        "new_training_data": {{
            "existing_or_new_intent_name_1": ["query 1", "query 2"],
            "existing_or_new_intent_name_2": ["query 3"]
        }},
        "new_responses": {{
            "new_intent_name": ["A polite Vietnamese response here."]
        }}
    }}
    """
    
    try:
        # Gọi API bằng cú pháp MỚI của google-genai, sử dụng model gemini-2.5-flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        json_string = clean_json_response(response.text)
        
        # Chuyển string JSON thành Dictionary Python
        ai_analysis = json.loads(json_string)
        
        print("🧠 Gemini đã phân tích xong! Đang cập nhật dữ liệu...")
        
        # 4. Cập nhật vào File Intents.json
        for intent, questions in ai_analysis.get("new_training_data", {}).items():
            if intent in current_intents:
                current_intents[intent].extend(questions)
                current_intents[intent] = list(set(current_intents[intent]))
            else:
                current_intents[intent] = questions
                print(f"🌟 Đã tạo Ý định (Intent) mới: {intent}")
                
        # 5. Cập nhật vào File Responses.json
        for intent, answers in ai_analysis.get("new_responses", {}).items():
            if intent not in current_responses:
                current_responses[intent] = answers
                
        # 6. Ghi đè lại vào file JSON
        with open(CONTENT_PATH, 'w', encoding='utf-8') as f:
            json.dump(current_intents, f, ensure_ascii=False, indent=4)
        with open(RESPONSES_PATH, 'w', encoding='utf-8') as f:
            json.dump(current_responses, f, ensure_ascii=False, indent=4)
            
        # 7. Xóa trắng file miss_log.txt để bắt đầu chu kỳ mới
        open(MISS_LOG_PATH, 'w').close()
        
        print("✅ Đã cập nhật xong JSON thành công!")
        print("🚀 Bạn hãy chạy lại file main.py để AI tự động học lại (train) nhé!")
        
    except json.JSONDecodeError:
        print("❌ Lỗi: Gemini trả về định dạng không phải JSON chuẩn. Vui lòng thử lại.")
        if 'response' in locals():
            print("Chi tiết raw output:\n", response.text)
    except Exception as e:
        print(f"❌ Có lỗi xảy ra trong quá trình gọi API: {e}")

if __name__ == "__main__":
    run_auto_update()