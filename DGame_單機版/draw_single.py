# 功能有:畫筆、橡皮擦、更改畫筆顏色、撤銷、恢復、清空畫布、計時器(進度條為倒數)、提早結束繪畫(done)
# 繪畫前會先從data.txt中隨機選擇兩個單字，並讓繪畫者從兩者中選擇題目
# 繪畫資料會存放在draw_data.txt，用於guess_single.py呈現畫好的內容
# 此程式會修改shared_data.json中的answer
# 撤銷及恢復的部分是用stack來儲存每筆畫軌跡，以滑鼠按下到放開算一筆畫

# 繪畫原理:
# 當按下滑鼠左鍵時開始一個新的筆畫，當按著滑鼠左鍵移動時代表正在繪畫，放開滑鼠左鍵代表此筆畫完成
# 當開始一個新筆畫時新增一個current_action陣列儲存當前筆畫資訊，並將目前x,y座標設為last_x和last_y
# 在繪畫過程中，是利用last_x, last_y和當前x, y座標來畫出直線，並添加到current_action中，再將當前x, y座標設為last_x, last_y，一直重複此步驟直到放開滑鼠
# 結束一筆畫後，將current_action以及畫筆顏色加入undo_stack，並將redo_stack清空(因為沒有下一筆畫了)

# 發現問題1:若目前使用橡皮擦，更改畫筆顏色後依然是橡皮擦
# 解決方法:在每次更動顏色時將模式改為繪畫模式

# 發現問題2:在撤銷後又恢復時，原畫筆顏色會變成目前畫筆顏色
# 解決方法:將畫筆顏色也一併記錄起來，以便恢復時可以連原本畫筆顏色也恢復

# 發現問題3:若提前結束繪畫，進度條仍會繼續倒數
# 解決方法:多設置一個draw_done狀態，以確認是否有提前結束繪畫

import sys
import random
import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import signal

if "--pno" in sys.argv:
    pno = str(sys.argv[2])
    print("目前的畫家:"+pno)

class DrawingApp:
    def __init__(self, pno):
        self.drawing_mode = True  # 畫筆模式，True表示畫筆模式，False表示橡皮擦模式
        self.takeabreak = False
        self.pen_color = "black"  # 畫筆顏色預設為黑色
        self.undo_stack = []      # 用於儲存每筆畫的軌跡，以便撤銷操作
        self.redo_stack = []      # 用於儲存被撤銷的筆畫，以便恢復操作
        self.time_elapsed = 30     # 用於計時的變量
        self.draw_done = False
        self.pno=pno
        self.load_words_and_prompt_choice()  # 從文件中隨機選擇兩個單字，並讓繪畫者選擇

    ###題目選擇################################################

    def load_words_and_prompt_choice(self): #開啟題目資料檔。並隨機選擇兩個單字
        with open("data.txt", "r", encoding='utf-8') as file:
            words = file.readlines()
        words = [word.strip() for word in words]
        self.word1, self.word2 = random.sample(words, 2)
        self.prompt_user_for_word_choice()

    def prompt_user_for_word_choice(self):  # 提示用戶選擇一個單字
        self.choice_window = tk.Tk()
        self.choice_window.title("Choose a Word")
        
        # 計算中心位置
        screen_width = self.choice_window.winfo_screenwidth()
        screen_height = self.choice_window.winfo_screenheight()
        window_width = 280
        window_height = 120
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.choice_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        prompt_label = tk.Label(self.choice_window, text=str(self.pno)+"開始繪畫\n請選擇題目", font=("Helvetica", 14))
        prompt_label.pack(pady=10)

        button_frame = tk.Frame(self.choice_window)
        button_frame.pack(pady=10)

        word1_button = tk.Button(button_frame, text=self.word1, command=lambda: self.select_word(self.word1))
        word1_button.pack(side=tk.LEFT, padx=10)

        word2_button = tk.Button(button_frame, text=self.word2, command=lambda: self.select_word(self.word2))
        word2_button.pack(side=tk.LEFT, padx=10)

        self.choice_window.protocol("WM_DELETE_WINDOW", self.on_closing_1)
        self.choice_window.mainloop()

    def select_word(self, word):    # 選擇單字後，將選定的單字設為題目，並創建畫家和玩家視窗
        self.word = word
        self.choice_window.destroy()
        self.create_painter_windows()

    ###設置視窗################################################

    def create_painter_windows(self):    # 創建畫家視窗
        self.painter = tk.Tk()
        self.painter.title("Painter")
        self.setup_painter()
        self.painter.protocol("WM_DELETE_WINDOW", self.on_closing_2)

        # 計算中心位置
        screen_width = self.painter.winfo_screenwidth()
        screen_height = self.painter.winfo_screenheight()
        window_width = 625
        window_height = 500
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.painter.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.start_timer()  # 開始計時
        
    def setup_painter(self):    #設置畫家視窗
        self.canvas_a_frame = tk.Frame(self.painter)
        self.canvas_a_frame.grid(row=0, column=1, pady=10, sticky=tk.N)

        # 題目
        self.word_label = tk.Label(self.canvas_a_frame, text=self.word, font=("Helvetica", 14))
        self.word_label.config(width=4, height=2)
        self.word_label.grid(row=0, column=0, padx=5, pady=5, sticky="we")

        # 畫布
        self.canvas_a = tk.Canvas(self.canvas_a_frame, bg="white", width=500, height=380)
        self.canvas_a.grid(row=1, column=0, rowspan=10) 

        # 綁定畫布的事件
        self.canvas_a.bind("<B1-Motion>", self.draw_or_erase)
        self.canvas_a.bind("<Button-1>", self.start_action)
        self.canvas_a.bind("<ButtonRelease-1>", self.end_action)

        # 進度條
        self.progress = ttk.Progressbar(self.canvas_a_frame, orient=tk.HORIZONTAL, length=200, mode='determinate', maximum=30)
        self.progress.grid(row=11, column=0, pady=10, sticky=tk.E+tk.W)

        #【button_frame】
        self.button_frame = tk.Frame(self.painter)
        self.button_frame.grid(row=0, column=0, pady=10, sticky=tk.N)
        
        #----------------------第一行----------------------#
        # 排版用label
        self.invisible_label = tk.Label(self.button_frame, text="", font=("Helvetica", 14))
        self.invisible_label.config(width=4, height=2)
        self.invisible_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # 畫筆
        self.draw_image = Image.open("img/pencil.jpg")
        self.draw_image = self.draw_image.resize((30, 30), Image.ANTIALIAS)  
        self.draw_photo = ImageTk.PhotoImage(self.draw_image)
        self.draw_button = tk.Button(self.button_frame, image=self.draw_photo, command=self.set_draw_mode)
        self.draw_button.config(width=30, height=30)  
        self.draw_button.grid(row=1, column=0, padx=5, pady=5)

        # 橡皮擦
        self.erase_image = Image.open("img/eraser.jpg")
        self.erase_image = self.erase_image.resize((30, 30), Image.ANTIALIAS) 
        self.erase_photo = ImageTk.PhotoImage(self.erase_image)
        self.erase_button = tk.Button(self.button_frame, image=self.erase_photo, command=self.set_erase_mode)
        self.erase_button.config(width=30, height=30)
        self.erase_button.grid(row=2, column=0, padx=5, pady=5)
        
        # 調色盤
        self.color_image = Image.open("img/palette.jpg")
        self.color_image = self.color_image.resize((30, 30), Image.ANTIALIAS)  
        self.color_photo = ImageTk.PhotoImage(self.color_image)
        self.color_button = tk.Button(self.button_frame, image=self.color_photo, command=self.choose_color)
        self.color_button.config(width=30, height=30)
        self.color_button.grid(row=3, column=0, padx=5, pady=5)

        # 撤銷
        self.undo_image = Image.open("img/undo.jpg")
        self.undo_image = self.undo_image.resize((30, 30), Image.ANTIALIAS) 
        self.undo_photo = ImageTk.PhotoImage(self.undo_image)
        self.undo_button = tk.Button(self.button_frame, image=self.undo_photo, command=self.undo_last_action)
        self.undo_button.config(width=30, height=30)
        self.undo_button.grid(row=4, column=0, padx=5, pady=5)

        # 恢復
        self.redo_image = Image.open("img/redo.jpg")
        self.redo_image = self.redo_image.resize((30, 30), Image.ANTIALIAS)
        self.redo_photo = ImageTk.PhotoImage(self.redo_image)
        self.redo_button = tk.Button(self.button_frame, image=self.redo_photo, command=self.redo_last_action)
        self.redo_button.config(width=30, height=30)
        self.redo_button.grid(row=5, column=0, padx=5, pady=5)

        #清空畫布
        self.clear_button = tk.Button(self.button_frame, bg="white", text="Clear", command=self.clear_canvas)
        self.clear_button.grid(row=6, column=0, padx=5, pady=5)

        #繪畫完畢
        self.done_button = tk.Button(self.button_frame, bg="white", text="Done", command=self.timer_event)
        self.done_button.grid(row=7, column=0, padx=5, pady=5)

        #----------------------第二行----------------------#
        # 各種顏色按鈕
        self.red_button = tk.Button(self.button_frame, bg="red", command=lambda: self.set_pen_color("red"))
        self.red_button.config(width=4, height=2)
        self.red_button.grid(row=1, column=1, padx=5, pady=5)

        self.orange_button = tk.Button(self.button_frame, bg="orange", command=lambda: self.set_pen_color("orange"))
        self.orange_button.config(width=4, height=2)
        self.orange_button.grid(row=2, column=1, padx=5, pady=5)

        self.yellow_button = tk.Button(self.button_frame, bg="yellow", command=lambda: self.set_pen_color("yellow"))
        self.yellow_button.config(width=4, height=2)
        self.yellow_button.grid(row=3, column=1, padx=5, pady=5)

        self.green_button = tk.Button(self.button_frame, bg="green", command=lambda: self.set_pen_color("green"))
        self.green_button.config(width=4, height=2)
        self.green_button.grid(row=4, column=1, padx=5, pady=5)

        self.blue_button = tk.Button(self.button_frame, bg="blue", command=lambda: self.set_pen_color("blue"))
        self.blue_button.config(width=4, height=2)
        self.blue_button.grid(row=5, column=1, padx=5, pady=5)

        self.purple_button = tk.Button(self.button_frame, bg="purple", command=lambda: self.set_pen_color("purple"))
        self.purple_button.config(width=4, height=2)
        self.purple_button.grid(row=6, column=1, padx=5, pady=5)

        self.black_button = tk.Button(self.button_frame, bg="black", fg="white", command=lambda: self.set_pen_color("black"))
        self.black_button.config(width=4, height=2)
        self.black_button.grid(row=7, column=1, padx=5, pady=5)

    ###模式設置################################################

    def set_draw_mode(self):    # 設置為畫筆模式
        self.drawing_mode = True

    def set_erase_mode(self):   # 設置為橡皮擦模式
        self.drawing_mode = False

    ###更改畫筆顏色################################################

    def set_pen_color(self, color): # 更改畫筆顏色並設置為畫筆模式
        self.pen_color = color
        self.set_draw_mode() 

    def choose_color(self): # 彈出顏色選擇器(調色盤)以更改畫筆顏色
        color = colorchooser.askcolor()[1]
        if color:
            self.pen_color = color
            self.set_draw_mode()  

    ###繪畫################################################

    def start_action(self, event):  # 開始一個新的筆畫
        self.current_action = []
        self.update_position(event)

    def end_action(self, event):    # 結束當前筆畫，並將其加到undo_stack中
        if self.current_action:
            self.undo_stack.append((self.current_action, self.pen_color))  # 儲存動作和顏色
            self.redo_stack.clear()  # 每次執行新操作時清除redo_stack

    def update_position(self, event):   # 更新最後一個座標
        self.last_x, self.last_y = event.x, event.y

    def draw_or_erase(self, event): # 根據當前模式決定動作
        x, y = event.x, event.y
        if self.takeabreak:
            return
        
        elif self.drawing_mode: # 畫線
            line_id_a = self.canvas_a.create_line(self.last_x, self.last_y, x, y, fill=self.pen_color, width=2)

            # 儲存動作和顏色
            self.current_action.append(((line_id_a), (self.last_x, self.last_y, x, y), self.pen_color))  
        
        else:   # 擦除(畫筆顏色為白)
            line_id_a = self.canvas_a.create_line(self.last_x, self.last_y, x, y, fill="white", width=10)

            # 儲存動作和顏色
            self.current_action.append(((line_id_a), (self.last_x, self.last_y, x, y), "white"))  
        self.update_position(event)

    ###清除畫布################################################

    def clear_canvas(self): 
        self.canvas_a.delete("all")
        self.undo_stack.clear()
        self.redo_stack.clear()

    ###撤銷/恢復################################################

    def undo_last_action(self): # 撤銷上一個筆畫
        if self.undo_stack:
            last_action, _ = self.undo_stack.pop()  
            for (line_id_a), coords, color in last_action:
                self.canvas_a.delete(line_id_a)
            self.redo_stack.append((last_action, color))  

    def redo_last_action(self): # 恢復上一個撤銷的筆畫
        if self.redo_stack:
            last_action, color = self.redo_stack.pop()  
            new_action = []
            for (line_id_a), coords, color in last_action:
                line_id_a_new = self.canvas_a.create_line(*coords, fill=color, width=2 if color != "white" else 10)
                new_action.append(((line_id_a_new), coords, color))  # 儲存動作和顏色
            self.undo_stack.append((new_action, color))  

    ###計時器################################################
    
    def start_timer(self):
        self.painter.after(self.time_elapsed*1000, self.timer_event) # 開始計時，30秒後執行timer_event
        self.update_progress_bar()  # 每秒更新一次進度條

    def timer_event(self):  # 計時器事件
        if not self.draw_done:
            self.draw_done = True
            self.takeabreak = True
            messagebox.showinfo("Messagebox", self.pno+"繪畫結束")
            self.save_undo_stack_to_file()  
            self.painter.destroy()

            with open('shared_data.json', 'r') as file:
                data = json.load(file)
            
            data['answer'] = self.word
            print("更新答案:" + data['answer'])

            with open('shared_data.json', 'w') as file:
                json.dump(data, file)

            sys.exit(0)

    def update_progress_bar(self):
        if self.draw_done:  # 提前結束就跳出
            return
        
        self.time_elapsed -= 1
        self.progress['value'] = self.time_elapsed

        if self.time_elapsed > 0:  
            self.painter.after(1000, self.update_progress_bar)  
    
    def save_undo_stack_to_file(self):
        with open('draw_data.txt', 'w') as file:
            for action, color in self.undo_stack:
                for (line_id_a), coords, color in action:
                    file.write(f'{coords},{color}\n')
    
    def on_closing_1(self):
        self.choice_window.destroy()   
        os.kill(os.getppid(), signal.SIGINT)    # 向父進程發送 SIGINT 信號    

    def on_closing_2(self):
        self.painter.destroy()   
        os.kill(os.getppid(), signal.SIGINT)    # 向父進程發送 SIGINT 信號    

if __name__ == "__main__":
    app = DrawingApp(pno)  

