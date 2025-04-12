import tkinter as tk
from PIL import Image, ImageTk

# macro
RESAMPLE_METHOD = Image.Resampling.LANCZOS #原為 Image.ANTIALIAS

class Skeleton_MyCanvasFrame(tk.Canvas):
    
    #title_word = tk.StringVar()
    
    
    def __init__(self,root,**args):
        super().__init__(root,**args)
        self.all_btn = []
        self.canvas = tk.Canvas(self ,bg="white", width=400, height=400)
        self.canvas.grid(row=1, column=2, rowspan=10) 
        

        # 顯示選定的單字
        self.word_label = tk.Label(self, text="dog", font=("Helvetica", 14))
        self.word_label.grid(row=0, column=2, pady=5)
        
        
        # 添加按鈕
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0, pady=10)
        
        
        # 加載圖片並設置為按鈕圖標
        self.draw_image = Image.open("img/pencil.jpg")
        self.draw_image = self.draw_image.resize((30, 30), RESAMPLE_METHOD)  
        self.draw_photo = ImageTk.PhotoImage(self.draw_image)
        self.draw_button = tk.Button(self.button_frame, image=self.draw_photo)
        self.draw_button.config(width=30, height=30)  
        self.draw_button.grid(row=0, column=0, padx=5, pady=5)
        self.all_btn.append(self.draw_button)

        self.erase_image = Image.open("img/eraser.jpg")
        self.erase_image = self.erase_image.resize((30, 30), RESAMPLE_METHOD) 
        self.erase_photo = ImageTk.PhotoImage(self.erase_image)
        self.erase_button = tk.Button(self.button_frame, image=self.erase_photo)
        self.erase_button.config(width=30, height=30)
        self.erase_button.grid(row=1, column=0, padx=5, pady=5)
        self.all_btn.append(self.erase_button)

        self.color_image = Image.open("img/palette.jpg")
        self.color_image = self.color_image.resize((30, 30), RESAMPLE_METHOD)  
        self.color_photo = ImageTk.PhotoImage(self.color_image)
        self.color_button = tk.Button(self.button_frame, image=self.color_photo)
        self.color_button.config(width=30, height=30)
        self.color_button.grid(row=2, column=0, padx=5, pady=5)
        self.all_btn.append(self.color_button)

        self.undo_image = Image.open("img/undo.jpg")
        self.undo_image = self.undo_image.resize((30, 30), RESAMPLE_METHOD) 
        self.undo_photo = ImageTk.PhotoImage(self.undo_image)
        self.undo_button = tk.Button(self.button_frame, image=self.undo_photo)
        self.undo_button.config(width=30, height=30)
        self.undo_button.grid(row=3, column=0, padx=5, pady=5)
        self.all_btn.append(self.undo_button)

        self.redo_image = Image.open("img/redo.jpg")
        self.redo_image = self.redo_image.resize((30, 30), RESAMPLE_METHOD)
        self.redo_photo = ImageTk.PhotoImage(self.redo_image)
        self.redo_button = tk.Button(self.button_frame, image=self.redo_photo)
        self.redo_button.config(width=30, height=30)
        self.redo_button.grid(row=4, column=0, padx=5, pady=5)
        self.all_btn.append(self.redo_button)

        self.clear_button = tk.Button(self.button_frame, bg="white", text="Clear")
        self.clear_button.grid(row=5, column=0, padx=5, pady=5)
        self.all_btn.append(self.clear_button)
        
#-------------------------------------------------
        # 新增顏色按鈕
        self.color_button_frame = tk.Frame(self)
        self.color_button_frame.grid(row=1, column=1, pady=10)
        
        self.red_button = tk.Button(self.color_button_frame, bg="red")
        self.red_button.config(width=4, height=2)
        self.red_button.grid(row=0, column=1, padx=5, pady=5)
        self.all_btn.append(self.red_button)

        self.orange_button = tk.Button(self.color_button_frame, bg="orange")
        self.orange_button.config(width=4, height=2)
        self.orange_button.grid(row=1, column=1, padx=5, pady=5)
        self.all_btn.append(self.orange_button)

        self.yellow_button = tk.Button(self.color_button_frame, bg="yellow")
        self.yellow_button.config(width=4, height=2)
        self.yellow_button.grid(row=2, column=1, padx=5, pady=5)
        self.all_btn.append(self.yellow_button)

        self.green_button = tk.Button(self.color_button_frame, bg="green")
        self.green_button.config(width=4, height=2)
        self.green_button.grid(row=3, column=1, padx=5, pady=5)
        self.all_btn.append(self.green_button)

        self.blue_button = tk.Button(self.color_button_frame, bg="blue")
        self.blue_button.config(width=4, height=2)
        self.blue_button.grid(row=4, column=1, padx=5, pady=5)
        self.all_btn.append(self.blue_button)

        self.purple_button = tk.Button(self.color_button_frame, bg="purple")
        self.purple_button.config(width=4, height=2)
        self.purple_button.grid(row=5, column=1, padx=5, pady=5)
        self.all_btn.append(self.purple_button)

        self.black_button = tk.Button(self.color_button_frame, bg="black", fg="white")
        self.black_button.config(width=4, height=2)
        self.black_button.grid(row=6, column=1, padx=5, pady=5)
        self.all_btn.append(self.black_button)
        
        
    
if __name__ == '__main__':
    root = tk.Tk()
    mf = Skeleton_MyCanvasFrame(root)
    mf.pack()
    root.mainloop()