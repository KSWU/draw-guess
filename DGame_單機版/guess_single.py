# 單機版 - 猜題
import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox
import sys
import json
import os
import signal

if "--name" in sys.argv:   #從bg.py取得玩家名單
    index = sys.argv.index("--name")
    userlist = sys.argv[index+1:] # 用來儲存有哪些玩家
    print("userlist=", userlist)
    person_num=len(userlist)
    print("len=", str(person_num))

with open('shared_data.json', 'r') as file:
    data = json.load(file)

pno = data['pno'] % person_num

others = userlist.copy() 
others.remove(userlist[pno-1]) # 猜題名單

user="" # 用來儲存現在是哪個使用者
scores=data['score'] # 用來儲存使用者們的得分 每個繪畫結束都要清空
ans=data['answer']

def on_closing():
    root.destroy()
    os.kill(os.getppid(), signal.SIGINT)    # 向父進程發送SIGINT信號

# 定義發送答案的功能
def send_guess(event=None):
    guess = entry_box.get()  # 從輸入框獲取文字
    if guess:  # 如果輸入框有文字
        user=str(val.get()) # 讀取使用者是誰
        if user == "none": # 檢查是否有選擇使用者
            messagebox.showwarning("警告", "請選擇一個使用者！")
            entry_box.delete(0, tk.END)  # 清空輸入框
        else: # 如果有選擇使用者
            answer_area.config(state=tk.NORMAL)  # 啟用文本區域以允許插入文本
            check_answer(user, guess)  # 檢查答案並處理顯示
            answer_area.see(tk.END)  # 滾動到文本區域的底部
            answer_area.config(state=tk.DISABLED)  # 禁用文本區域防止編輯
            entry_box.delete(0, tk.END)  # 清空輸入框

# 新增檢查答案的功能，這樣可以處理來自不同用戶的答案
def check_answer(username, guess):
    if guess == ans:
        answer_area.insert(tk.END, f"✔{username}猜到了答案\n")
        entry_box.delete(0, tk.END)  # 清空輸入框
        entry_box.config(state='disabled')  # 禁用輸入框 => 到radio再判斷
        update_score(username)  # 更新分數
        # score.update_score(user)  # 通知計分板模塊該用戶答對了
    else:
        answer_area.insert(tk.END, f"{username}猜的是: {guess}\n")

# 定義發送聊天消息的功能
def send_message(event=None):
    message = chat_entry_box.get()  # 從聊天輸入框獲取文字
    if message:  # 如果聊天輸入框有文字
        user=str(val.get()) # 讀取使用者是誰
        if user == "none": # 檢查是否有選擇使用者
            messagebox.showwarning("警告", "請選擇一個使用者！")
            chat_entry_box.delete(0, tk.END)  # 清空輸入框
        else: # 如果有選擇使用者
            chat_area.config(state=tk.NORMAL)  # 啟用文本區域以允許插入文本
            # 檢查訊息是否包含答案，不分大小寫
            if ans.lower() in message.lower(): 
                chat_area.insert(tk.END, f"⚠️{user}，你不可以洩漏答案喔！嘻嘻\n")  # 提示不要洩漏答案
            else:
                chat_area.insert(tk.END, f"{user}說：{message}\n")  # 正常顯示消息
            # chat_area.insert(tk.END, f"{user}說：{message}\n")  # 將消息顯示在聊天室區域
            chat_area.see(tk.END)  # 滾動到文本區域的底部
            chat_area.config(state=tk.DISABLED)  # 禁用文本區域防止編輯
            chat_entry_box.delete(0, tk.END)  # 清空聊天輸入框

#----------------------------------------------------
# 【計分板】

correct_order = [] # 紀錄答對的玩家順序

def update_score(username):
    if username not in correct_order:
        correct_order.append(username)  # 添加用戶到答對順序列表
    
    # 計算得分
    if len(correct_order) <= 10:
        score_increment = 11 - len(correct_order)  # 從10分遞減到1分
    else:
        score_increment = 1  # 第10個之後的用戶都只加1分

    for i in range(person_num):
        if userlist[i]==username:
            scores[i] += score_increment

    # 更新GUI的得分板
    update_scoreboard()
    # 可選的：在GUI中顯示更新後的分數


# 定義更新記分板
def update_scoreboard(event=None):
    scoreboard_area.config(state=tk.NORMAL)  # 啟用文本區域以允許插入文本
    scoreboard_area.delete('1.0','end')

    # 根據得分排序玩家
    sorted_scores=scores.copy()
    sorted_scores_dic = {userlist[i]: scores[i] for i in range(person_num)}
    sorted_scores_dic = sorted(sorted_scores_dic.items(), key=lambda x: x[1], reverse=True)
    # 更新得分板
    for i, (username, score) in enumerate(sorted_scores_dic):
        scoreboard_area.insert(tk.END,f"#{i+1} {username}: {score} 分\n")

    scoreboard_area.see(tk.END)  # 滾動到文本區域的底部
    scoreboard_area.config(state=tk.DISABLED)  # 禁用文本區域防止編輯

# 選擇使用者的radio buuton，如果該使用者已經答對了，則不能回答問題
def radio_detect():
    user=str(val.get()) # 讀取使用者是誰
    username=user
    # print("gi")
    if username in correct_order: # 已經答對，不讓他輸入
        # entry_box.delete(0, tk.END)  # 清空輸入框
        entry_box.config(state='disabled')  # 禁用輸入框
    else:
        entry_box.config(state='normal')  # 開啟輸入框
        entry_box.delete(0, tk.END)  # 清空輸入框
        
#----------------------------------------------------
# 【計時】
time_elapsed=60 # 倒數計時的秒數
all_correct = False  # 用來記錄是不是所有人都答對
timer_id = None  # 用於存儲計時器事件的標識符
def start_timer():
    global timer_id
    timer_id = root.after(time_elapsed*1000, timer_event)  # 開始計時，30秒後執行timer_event
    update_progress_bar()  # 每秒更新一次進度條

def exit_win():
    root.destroy()
    data['pno'] = pno+1
    print("更新繪畫者:", data['pno'])

    data['score'] = scores
    print("更新分數:", data['score'])

    with open('shared_data.json', 'w') as file:
        json.dump(data, file)

    sys.exit(0)

def timer_event():  # 計時器事件  時間到
    # 清空答對的玩家順序列表
    correct_order.clear()
    messagebox.showinfo("Messagebox","答題結束，這題答案是"+ans)
    exit_win()

def update_progress_bar(): 
    global time_elapsed, timer_id
    if len(correct_order)==len(others):  # 全部人答出來=>提前結束
        # 清空答對的玩家順序列表
        correct_order.clear()
        if timer_id:
            root.after_cancel(timer_id)  # 取消計時器事件
            timer_id = None
        messagebox.showinfo("Messagebox","所有人都猜到了！")
        exit_win()

    time_elapsed-=1
    progress['value'] = time_elapsed

    if time_elapsed > 0:  
        root.after(1000, update_progress_bar)

def load_undo_stack_from_file():
    actions = []
    with open('draw_data.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            coords, color = line.strip().rsplit(',', 1)
            coords = coords.strip('()').split(',')
            coords = tuple(map(int, coords))
            actions.append((coords, color))
    return actions

def draw_from_undo_stack(canvas, actions):
    for coords, color in actions:
        x1, y1, x2, y2 = coords
        canvas.create_line(x1, y1, x2, y2, fill=color, width=2 if color != "white" else 10)

#####################################################

root = tk.Tk()
root.title("你畫我猜 - 聊天室")
window_width=1250
window_height=650
# root.geometry("950x650")
root.geometry(f"{window_width}x{window_height}")

hey = tk.Toplevel(root)
canvas_b = tk.Canvas(hey, bg="white", width=400, height=400)
canvas_b.pack()
actions = load_undo_stack_from_file()
draw_from_undo_stack(canvas_b, actions)

# 使用Grid佈局管理器設定兩個主區域
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

# 【答題區】
# 外框
answer_frame = tk.LabelFrame(root, text="答題區")
answer_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# 顯示回答紀錄
answer_area = tk.Text(answer_frame, state='disabled')
answer_area.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
answer_frame.grid_rowconfigure(1, weight=1)  # 確保Text控件所在的行可以擴展
answer_frame.grid_columnconfigure(0, weight=1)  # 確保Text控件所在的列可以擴展

# 回答紀錄的scroll bar
scrollbar_answer = tk.Scrollbar(answer_frame, command=answer_area.yview)
scrollbar_answer.grid(row=1, column=1, sticky='ns')
answer_area.config(yscrollcommand=scrollbar_answer.set,padx=10)

# 選擇使用者身分
user_frame = tk.Frame(root) # 使用者框框 
user_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

val = tk.StringVar(value="none") # 現在是哪個使用者
radio_btn=[]
for i in range(len(others)):
    print(i)
    radio_btnn = tk.Radiobutton(user_frame, text=others[i], variable=val, value=others[i], command=radio_detect)  # 放入第一個單選按鈕
    radio_btn.append(radio_btnn)
    radio_btn[i].grid(row=0, column=i, padx=5, pady=5)
    
user_frame.grid_rowconfigure(0, weight=1)  # 確保Text控件所在的行可以擴展
user_frame.grid_columnconfigure(0, weight=1)  # 確保Text控件所在的列可以擴展
user_frame.grid_columnconfigure(1, weight=1)  # 確保Text控件所在的列可以擴展
user_frame.grid_columnconfigure(2, weight=1)  # 確保Text控件所在的列可以擴展
user_frame.grid_columnconfigure(3, weight=1)  # 確保Text控件所在的列可以擴展

# 輸入文字框
entry_box = tk.Entry(answer_frame,width=30)
entry_box.grid(row=2, column=0, padx=10, pady=5,sticky="w")
entry_box.bind("<Return>", send_guess)

# 提交答案 按鈕
send_button = tk.Button(answer_frame, text="提交答案", width=8,command=send_guess)
send_button.grid(row=2, column=0, padx=5, pady=5,sticky="ne")

#---------------------------------------------------------
# 目前先將聊天室註解掉
# 【聊天室】
# 外框
chat_frame = tk.LabelFrame(root, text="聊天室")
chat_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
chat_frame.grid_rowconfigure(1, weight=1)  # 確保Text控件所在的行可以擴展
chat_frame.grid_columnconfigure(2, weight=1)  # 確保Text控件所在的列可以擴展

# 顯示聊天紀錄
chat_area = tk.Text(chat_frame, state='disabled')
chat_area.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
answer_frame.grid_columnconfigure(2, weight=1)  # 確保Text控件所在的列可以擴展

# 聊天紀錄的scroll bar
scrollbar_chat = tk.Scrollbar(chat_frame, command=chat_area.yview)
scrollbar_chat.grid(row=1, column=3, sticky='ns')
chat_area.config(yscrollcommand=scrollbar_chat.set)

# 輸入文字框
chat_entry_box = tk.Entry(chat_frame,width=30)
chat_entry_box.grid(row=2, column=2, sticky="w", padx=5)
chat_entry_box.bind("<Return>", send_message)

# 發送 按鈕
send_chat_button = tk.Button(chat_frame, text="發送",width=8, command=send_message)
send_chat_button.grid(row=2, column=2, padx=5, pady=5,sticky="e")

#----------------------------------------------------------------

# 【計分版】
# 外框
scoreboard_frame = tk.LabelFrame(root, text="計分板")
scoreboard_frame.grid(row=0, column=4, sticky="nsew", padx=5, pady=5)
scoreboard_frame.grid_rowconfigure(0, weight=1)  # 確保Text控件所在的行可以擴展
scoreboard_frame.grid_columnconfigure(4, weight=1)  # 確保Text控件所在的列可以擴展

# 顯示記分板
scoreboard_area = tk.Text(scoreboard_frame, state='disabled')
scoreboard_area.grid(row=1, column=4, sticky="nsew", padx=5, pady=5)
scoreboard_frame.grid_rowconfigure(1, weight=1)
scoreboard_frame.grid_columnconfigure(4, weight=1)  # 確保Text控件所在的列可以擴展

# 記分板的scroll bar
scrollbar_scoreboard = tk.Scrollbar(scoreboard_frame, command=scoreboard_area.yview)
scrollbar_scoreboard.grid(row=1, column=5, sticky='ns')
scoreboard_area.config(yscrollcommand=scrollbar_scoreboard.set)

#----------------------------------------------------------------

# 【進度條】
progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate', maximum=time_elapsed)
progress.grid(row=3, column=0,columnspan=5, padx=5,pady=10, sticky=tk.E+tk.W)

update_scoreboard()

start_timer()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

