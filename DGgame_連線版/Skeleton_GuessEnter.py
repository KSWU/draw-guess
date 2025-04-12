import tkinter as tk 

class Skeleton_GuessEnter(tk.Tk):
    
    def __init__(self,ok_act=None,back_act=None):
        
        super().__init__()
        
        self.topic = tk.Label(self,text="輸入房間號", font=("Arial", 30))
        self.topic.pack(pady=20, anchor='center')
        
        self.clue = tk.Label(self,text="ex:192.168.124.107:5555", font=("Arial", 10))
        self.clue.pack(pady=10, anchor='center')
        
        self.ent_room = tk.Entry(self)
        self.ent_room.pack(pady=10, anchor='center')
        
        self.ok_act = ok_act
        self.btn_ok = tk.Button(self,text="ok", font=("Arial", 10),command=self.ok_onclick)
        self.btn_ok.pack(pady=10, anchor='center')
        
        self.back_act = back_act
        self.btn_back = tk.Button(self,text="Back", font=("Arial", 10),command=self.back_onclick)
        self.btn_back.pack(pady=10, anchor='center')
        
    def ok_onclick(self):
        if self.ok_act:
            self.ok_act(self.ent_room.get())
            
    def back_onclick(self):
        if self.back_act:
            self.back_act()
        
if __name__ == '__main__':
    
    def act(stry):
        print(stry)
    
    w = Skeleton_GuessEnter(act)
    w.mainloop()