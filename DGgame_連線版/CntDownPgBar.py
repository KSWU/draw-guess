import tkinter as tk
from tkinter import ttk
import threading
import time

'''
提供end_progress() 提前終止progressBar
提供start_progress 開始執行倒數 能指定倒數時間(秒) 能指定終止時執行func 
'''

class CntDownPgBar(ttk.Progressbar):


    def __init__(self,*args,orient="horizontal", mode="determinate", style="red.Horizontal.TProgressbar",**kwargs):
        super().__init__(*args,**kwargs,orient=orient, mode=mode, style=style)
        self.lock = threading.Lock()
        self.time_slot = 10 #sec
        self.update_slot = 100 #ms
        self.finish_func = None
        self.progress_var = tk.DoubleVar()
        self.config(variable=self.progress_var)
        
        self["maximum"] = 10000
        self.progress_var.set(0)
        
        self.print_func = False

    #-- external func ----------------------------------------
    def start_progress(self,time_slot=None,finish_func=None):
        if self.print_func :
            print("pgBar func : start_progress")
        if time_slot :
            self.time_slot = time_slot
        if finish_func:
            self.finish_func = finish_func
        self.progress_var.set(self["maximum"])
        threading.Thread(target=self.decre_progress).start()
        
    def stop_progress(self):
        if self.print_func :
            print("pgBar func : stop_progress")
        self.stop()
        
    def end_progress(self):
        if self.print_func :
            print("pgBar func : end_progress")
        with self.lock:
            self.progress_var.set(0)
            
        
    #-- external func bottom ---------------------------------
    #-- internal func ---------------------------------------- 
    def decre_progress(self):
        
        self.init_time = time.time()
        self.last_time = self.init_time
        
        while True :
            while time.time()-self.last_time < self.update_slot/1000 :
                pass
            self.last_time = time.time()
            with self.lock:
                prgVal = self.progress_var.get()
                if prgVal<=0:
                    if self.finish_func:
                        self.finish_func()
                    return 
                self.progress_var.set( 
                    self["maximum"]-self["maximum"]*((time.time()-self.init_time)/self.time_slot) )
            
    

    #-- internal func bottom ---------------------------------



    

if __name__ == '__main__':
    
    # --- testing function here ----------------

    def btn_onclick():
        pg.end_progress()
        
    def timesUp_action():
        print("timesUp!!")
        
    # --- testing function bottom --------------

        
    root = tk.Tk()
    pg = CntDownPgBar(root,length=300)
    pg.pack()
    
    btn = tk.Button(root,text="end early",command=btn_onclick)
    btn.pack()
    
    pg.start_progress(60,timesUp_action)
    
    root.mainloop()