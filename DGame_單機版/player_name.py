# 此程式用於選擇玩家人數及輸入玩家姓名
# 會根據玩家人數動態調整玩家姓名欄位個數
# 若未填入姓名or姓名重複會跳出警告
# 開始遊戲後會進到draw_single.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import sys
import os
import signal

def on_closing():
    player_setting.destroy()
    os.kill(os.getppid(), signal.SIGINT)    # 向父進程發送 SIGINT 信號

def center_window(window, width=400, height=300):
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def combobox_selected(event):
    global num_players
    selected_value = choose_com.get()
    print("選擇的遊玩人數:", selected_value)
    
    entry_label.grid()

    # 顯示相應的玩家輸入框
    num_players = int(selected_value[0])  # 取得玩家數量
    for i in range(num_players):
        player_labels[i].grid()
        player_entries[i].grid()

    # 顯示開始遊戲按鈕
    start_btn.grid()

def start_game():
    name_list = []  # 存放玩家姓名
    name_set = set()    # 用於檢查名字是否重複
    for i in range(num_players):
        name = player_entries[i].get().strip()  # 取得玩家名稱並去除前後空格
        if name == "":
            messagebox.showwarning("警告", "玩家名稱不能為空！")
            return
        elif name in name_set:
            messagebox.showwarning("警告", "玩家名稱重複！")
            return
        else:
            name_set.add(name) 
            name_list.append(name)  

    # 將玩家名單存入shared_data.json中
    with open('shared_data.json', 'r') as file:
        data = json.load(file)
    
    data['names'] = name_list   

    with open('shared_data.json', 'w') as file:
        data = json.dump(data, file, indent=4)

    player_setting.destroy()
    sys.exit(0)

def main():
    global player_setting, choose_com, start_btn, entry_label
    global player_labels, player_entries

    player_setting = tk.Tk()
    player_setting.title("遊戲視窗")
    
    choose_frame = tk.Frame(player_setting)
    choose_frame.grid(row=0, column=0, columnspan=4, pady=5, sticky=tk.W)
    choose_label = tk.Label(choose_frame, text="請選擇遊玩人數:", font=("Arial", 20))
    choose_label.grid(row=0, column=0, padx=5, pady=5)
    choose_com = ttk.Combobox(choose_frame, values=['2人', '3人', '4人'])
    choose_com.grid(row=0, column=1, padx=5, pady=5)
    choose_com.bind("<<ComboboxSelected>>", combobox_selected)

    name_frame = tk.Frame(player_setting)
    name_frame.grid(row=1, column=0, pady=10, sticky=tk.W)
    entry_label = tk.Label(name_frame, text="請輸入玩家名稱(最多10字):", font=("Arial", 18))
    entry_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    entry_label.grid_remove()

    player_labels = []  # 玩家標籤
    player_entries = [] # 玩家姓名輸入欄位

    for i in range(4):
        label = tk.Label(name_frame, text=f"玩家{i+1}:", font=("Arial", 18))
        label.grid(row=i+1, column=0, padx=5, pady=5)
        entry = tk.Entry(name_frame, font=("Arial", 18), width=10)
        entry.grid(row=i+1, column=1, padx=5, pady=5)
        
        player_labels.append(label)
        player_entries.append(entry)

        label.grid_remove()
        entry.grid_remove()

    start_btn = tk.Button(player_setting, text="開始遊戲", font=("Arial", 20), command=start_game)
    start_btn.grid(row=2, column=0, pady=5, columnspan=4)
    start_btn.grid_remove()

    center_window(player_setting, width=400, height=400)

    player_setting.protocol("WM_DELETE_WINDOW", on_closing)
    player_setting.mainloop()

if __name__ == "__main__":
    main()
