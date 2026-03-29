from data.match_key import SimpleBrain
from data.sci_brain import MLBrain

def main():
    print("="*50)
    print("HỆ THỐNG AI CƠ BẢN (KEYWORD MATCHING)")
    print("Gõ 'thoát' để dừng chương trình.")
    print("="*50)
    
    brain = MLBrain()  # Sử dụng mô hình ML thay vì SimpleBrain
    
    while True:
        user_input = input("\nBạn: ")
        
        if user_input.lower() in ['thoát', 'quit', 'exit']:
            print("AI: Tạm biệt nhé!")
            break
            
        response, matched = brain.get_response(user_input)
        print(f"AI: {response}")

if __name__ == "__main__":
    main()