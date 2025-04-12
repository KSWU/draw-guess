# 此程式為遊戲首頁
# 若按開始遊戲會進入player_name.py
# 若按退出遊戲會結束程式

import tkinter as tk
import sys
import signal
import os

def center_window(window, width=400, height=300):
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def start_game():
    home.destroy()
    sys.exit(0)

def exit_game():
    home.destroy()
    os.kill(os.getppid(), signal.SIGINT)    # 向父進程發送 SIGINT 信號

def main():
    global home
    home = tk.Tk()
    home.title("首頁")

    frame = tk.Frame(home)
    frame.pack(expand=True)

    label = tk.Label(frame, text="你畫我猜", font=("Arial", 50))
    label.pack(pady=20, anchor='center')

    start_btn = tk.Button(frame, text="開始遊戲", font=("Arial", 20), command=start_game)
    start_btn.pack(pady=10, anchor='center')

    exit_btn = tk.Button(frame, text="退出遊戲", font=("Arial", 20), command=exit_game)
    exit_btn.pack(pady=10, anchor='center')

    center_window(home, width=600, height=400)

    home.protocol("WM_DELETE_WINDOW", exit_game)
    home.mainloop()

if __name__ == "__main__":
    main()
