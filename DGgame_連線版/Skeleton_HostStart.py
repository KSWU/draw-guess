import tkinter as tk 

class Skeleton_HostStart(tk.Tk):
    
    def __init__(self,hostIP,hostPort,start_act=None,back_act=None):
        super().__init__()
        
        self.topic = tk.Label(self, text="等待其他玩家進入", font=("Arial", 30))
        self.topic.pack(pady=20, anchor='center')
        
        self.clue = tk.Label(self, text="請其他玩家輸入你的房間號 : ", font=("Arial", 10))
        self.clue.pack(pady=5, anchor='center')
        
        self.hostIP = tk.StringVar()
        self.hostIP.set(hostIP+":"+str(hostPort))
        self.lbl_hostIP = tk.Label(self, textvariable=self.hostIP, font=("Arial", 10))
        self.lbl_hostIP.pack(pady=5, anchor='center')
        
        self.lbl_num = tk.Label(self, text="已有0人", font=("Arial", 10))
        self.lbl_num.pack(pady=5, anchor='center')
        
        self.start_act = start_act
        self.btn_start = tk.Button(self,text="Start !!", font=("Arial", 10),command=self.start_onclick)
        self.btn_start.pack(pady=10, anchor='center')
        
        
        self.back_act = back_act
        self.btn_back = tk.Button(self,text="Back", font=("Arial", 10),command=self.back_onclick)
        #self.btn_back.pack(pady=10, anchor='center')
        
    
    def show_num(self,n):
        self.lbl_num.config(text=f"已有{n}人")
        
    def start_onclick(self):
        if self.start_act:
            self.start_act()
            
    def back_onclick(self):
        if self.back_act:
            self.back_act()
    
        
if __name__ == '__main__':
    root = Skeleton_HostStart('192.168.128.107',5555)
    root.mainloop()
        
    