import MyTimerr
import threading 

class Conductor :
    
    def __init__(self,chapter=4,section=3):
        # define -------------------
        self.CHAPTERS_NUM = chapter
        self.SECTIONS_NUM = section
        self.section_secs = [5,10,5] #
        self.section_funcs = [None,None,None]
        self.finally_section = (section-1)%section   # last chapter will stop at stop_section
        self.finally_func = None
        
        # define bottom ------------
        # game var -----------------
        self.chapter = 0
        self.section = 0
        self.timer = None
        # game var bottom ----------
        self.lock = threading.RLock()
        
    def initiate(self):
        with self.lock:
            self.chapter = 0
            self.section = self.SECTIONS_NUM-1
        
    def start_game(self):
        
        self.initiate()
        self.stt()
        
    def stt(self):
        
        with self.lock:
            self.section = (self.section+1)%(self.SECTIONS_NUM)
            self.chapter = self.chapter+1 if self.section==0 else self.chapter
        
            self.timer = MyTimerr.MyTimerr()
            
        if self.chapter < self.CHAPTERS_NUM or not (self.section == self.finally_section) :
            self.timer.start_timer(self.section_secs[self.section],self.stt,self.stt)        
        else :
            self.timer.start_timer(self.section_secs[self.section],self.finally_func,self.finally_func)
        
        if self.section_funcs[self.section]:
            self.section_funcs[self.section]()
            
    def jump_next_stt(self,section):
        with self.lock:
            if section == self.section:
                self.timer.pre_end_timer()
        
   
# === test =========================================================
if __name__ == '__main__':
    
    import tkinter as tk 
    
    section_names = ["choose","drawguess","rest","qq"]
    stt = 0
    
    def choose():
        global stt
        strr.set(f"chapter #{g.chapter} : {section_names[g.section]}") 
        stt = g.section
        
    def drawguess():
        global stt
        strr.set(f"chapter #{g.chapter} : {section_names[g.section]}") 
        stt = g.section
        
    def rest():
        global stt
        strr.set(f"chapter #{g.chapter} : {section_names[g.section]}") 
        stt = g.section
    
    def qq():
        global stt
        strr.set(f"chapter #{g.chapter} : {section_names[g.section]}")
        stt = g.section
        
    def ending():
        strr.set("The Game is ended")
        
        
    def on_click():
        g.jump_next_stt(stt)
        
    root = tk.Tk()
    strr = tk.StringVar()
    lbl = tk.Label(root,textvariable=strr)
    lbl.pack()
    btn = tk.Button(root,text="pre end",command=on_click)
    btn.pack()
    
    g = Conductor(3,4)
    g.section_secs = [5,10,5,3]
    g.section_funcs = [choose,drawguess,rest,qq]
    g.finally_func = ending
    g.start_game()
    
    root.mainloop()

