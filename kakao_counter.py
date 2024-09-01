import tkinter as tk
from tkinter import filedialog, messagebox
import re
from collections import Counter

def analyze_chat():
    # 파일 선택
    file_path = filedialog.askopenfilename(title="카카오톡 대화 내역을 선택합니다", filetypes=[("텍스트 파일", "*.txt")])
    if not file_path:
        messagebox.showwarning("파일이 선택되지 않음", "txt 형식의 카카오톡 대화 목록을 선택하세요.")
        return
    
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    
    if not start_date or not end_date:
        messagebox.showwarning("잘못된 날짜", "시작일과 종료일을 입력한 후 파일을 업로드 하세요.")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # 날짜 패턴과 닉네임 패턴 정의
        date_pattern = re.compile(r"\d{4}년 \d{1,2}월 \d{1,2}일")
        nickname_pattern = re.compile(r"\[(.*?)\]")

        # 날짜별로 대화 내용 분리
        dates = date_pattern.findall(text)
        messages = date_pattern.split(text)[1:]

        # 지정된 날짜 범위의 대화만 추출
        selected_messages = []
        for date, message in zip(dates, messages):
            if start_date <= date <= end_date:
                selected_messages.append(message)

        # 닉네임 추출 및 빈도 계산
        nicknames = []
        for message in selected_messages:
            nicknames.extend(nickname_pattern.findall(message))

        nickname_counts = Counter(nicknames)
        top_chatters = nickname_counts.most_common(10)

        # 결과 출력
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "순위:\n")
        for i, (name, count) in enumerate(top_chatters, start=1):
            result_text.insert(tk.END, f"{i}. {name}: {count} 개\n")
    
    except Exception as e:
        messagebox.showerror("오류", str(e))

# GUI
root = tk.Tk()
root.title("카카오톡 대화 분석기")

# 날짜 입력
tk.Label(root, text="시작 지점 (예: 2025년 1월 1일):").pack(pady=5)
start_date_entry = tk.Entry(root)
start_date_entry.pack(pady=5)

tk.Label(root, text="종료 지점 (예: 2025년 1월 31일):").pack(pady=5)
end_date_entry = tk.Entry(root)
end_date_entry.pack(pady=5)

# 분석 버튼
analyze_button = tk.Button(root, text="파일 선택 후 분석하기", command=analyze_chat)
analyze_button.pack(pady=20)

# 결과 출력
result_text = tk.Text(root, height=10, width=50)
result_text.pack(pady=5)

# GUI 실행
root.mainloop()
