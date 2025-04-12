import tkinter as tk
from PIL import Image, ImageTk

# macro
RESAMPLE_METHOD = Image.Resampling.LANCZOS #原為 Image.ANTIALIAS

class Skeleton_EndingFrame(tk.Frame):
    
    def __init__(self,root,winner_lst):
        super().__init__()
        self.configure(width=450,height=400) # 12 9.5
        self.configure(bg="#E1DDBF")  
        
        self.img_pix_0 = 165
        self.img_pix_1 = 120
        self.xb = 30
        
        # 載入圖片
        
        
        
        self.image3 = Image.open("img/winner3.png")
        self.image3 = self.image3.resize((self.img_pix_1, self.img_pix_1), RESAMPLE_METHOD)  
        self.image3_photo = ImageTk.PhotoImage(self.image3)
        self.label3 = tk.Label(self, image=self.image3_photo,bg="#E1DDBF")
        self.label3.config(width=self.img_pix_1, height=self.img_pix_1)  
        if len(winner_lst) >= 3 :
            self.label3.place(x=272+self.xb,y=168)
        
        
        self.image2 = Image.open("img/winner2.png") #3
        self.image2 = self.image2.resize((self.img_pix_1, self.img_pix_1), RESAMPLE_METHOD)  
        self.image2_photo = ImageTk.PhotoImage(self.image2)
        self.label2 = tk.Label(self, image=self.image2_photo,bg="#E1DDBF")
        self.label2.config(width=self.img_pix_1, height=self.img_pix_1)  
        if len(winner_lst) >= 2 :
            self.label2.place(x=58+self.xb,y=168)
                
        
        self.image1 = Image.open("img/winner1.png") #4
        self.image1 = self.image1.resize((self.img_pix_0, self.img_pix_0), RESAMPLE_METHOD)  
        self.image1_photo = ImageTk.PhotoImage(self.image1)
        self.label1 = tk.Label(self, image=self.image1_photo,bg="#E1DDBF")
        self.label1.config(width=self.img_pix_0, height=self.img_pix_0)  
        self.label1.place(x=142+self.xb,y=40)
        
        self.name1 = tk.Label(self,bg="#FF5959",fg="white",text=winner_lst[0], font=("Arial", 15) )
        self.name1.place(x=190+self.xb,y=160)
        
        if len(winner_lst) >= 2 :
            self.name2 = tk.Label(self,bg="#FF5959",fg="white",text=winner_lst[1], font=("Arial", 13) )
            self.name2.place(x=90+self.xb,y=255)
        
        if len(winner_lst) >= 3 :
            self.name3 = tk.Label(self,bg="#FF5959",fg="white",text=winner_lst[2], font=("Arial", 13) )
            self.name3.place(x=292+self.xb,y=255)
        
        
        self.btn = tk.Button(self,text="Play Again",bg="#4C4C7E",fg="white", font=("Arial", 10),command=self.btn_onclick)
        self.btn.place(x=190+self.xb,y=320)
        self.btn_act = None
        
    def btn_onclick(self):
        if self.btn_act :
            self.btn_act()
     



if __name__ == '__main__':
    
    def act():
        print("here")
        root.destroy()
    
    llst = ["player0","player1","player2"] #
    root = tk.Tk()
    r = Skeleton_EndingFrame(root,llst)
    r.pack()
    
    root.mainloop()


   
