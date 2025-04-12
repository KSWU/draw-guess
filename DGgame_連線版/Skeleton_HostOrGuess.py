import tkinter as tk 

class Skeleton_HostOrGuess(tk.Tk):
    
    def __init__(self,host_act=None,guess_act=None):
        
        super().__init__()
        #self.geometry("400x300")
        
        self.topic = tk.Label(self, text="你畫我猜", font=("Arial", 50))
        self.topic.pack(pady=20, anchor='center')
        
        self.host_act = host_act
        self.btn_host = tk.Button(self,text="Create a Room", font=("Arial", 10),command=self.host_onclick)
        self.btn_host.pack(pady=10, anchor='center')
        
        self.guess_act = guess_act
        self.btn_guess = tk.Button(self,text="Enter a Room", font=("Arial", 10),command=self.guess_onclick)
        self.btn_guess.pack(pady=10, anchor='center')
        
    def host_onclick(self):
        if self.host_act:
            self.host_act()
            
    def guess_onclick(self):
        if self.guess_act:
            self.guess_act()
        
        
if __name__ == '__main__':
    
    def act1():
        print("act1")
    
    def act2():
        print("act2")
    
    root = Skeleton_HostOrGuess(act1,act2)
    
    root.mainloop()
    