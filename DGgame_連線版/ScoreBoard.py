import tkinter as tk
from tkinter import ttk
import threading

class ScoreBoard(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        self.btn_clr = "#FBDF98"#FFEC89
        self.bg_clr = "#D2E8A9"#B4C7E7#E1DDBF
        self.spot_clr = "#CDAEDE"
        
        self.outer_frame = tk.Frame(self)
        self.canvas = tk.Canvas(self.outer_frame, bg=self.bg_clr)
        self.scrollbar = ttk.Scrollbar(self.outer_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_clr)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.outer_frame.pack(side="left", fill="both", expand=True)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.outer_frame.grid_rowconfigure(0, weight=1)
        self.outer_frame.grid_columnconfigure(0, weight=1)
        
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        self.btns = []
        self.spot_guy = []
        
        self.lock = threading.RLock()
        self.version = 0
    
    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=canvas_width))

        for widget in self.scrollable_frame.winfo_children():
            widget.configure(width=canvas_width)
            
    def add_button(self, stry, spot=False):
        with self.lock:
            btn = tk.Button(self.scrollable_frame, bg=self.btn_clr, text=stry,height=3, font=("Arial", 12))
            self.btns.append(btn)
            btn.pack(fill=tk.X, pady=2, padx=10)
            self.canvas.update_idletasks()
            self.canvas.yview_moveto(1)  # 自动滑动到底部    
            if spot:
                btn.config(bg=self.spot_clr) #F7887C
                num = self.version
                self.after(500, lambda: self.spotlight_covery(btn, num))
        
    def update_scores(self, dictt, guy=None):
        with self.lock:
            self.version += 1
            list_data = [[k, v] for k, v in dictt.items()]
            lst = sorted(list_data, key=lambda x: x[1], reverse=True)
            
            spot_guy = None
            
            while len(lst) < len(self.btns):
                btn = self.btns.pop()
                btn.destroy()
                
            i = 0
            for btn in self.btns:
                btn.config(text=lst[i][0] + " : " + str(lst[i][1]))
                if lst[i][0] == guy:
                    spot_guy = i
                i += 1
            
            while len(lst) > len(self.btns):
                self.add_button(lst[i][0] + " : " + str(lst[i][1]))
                if lst[i][0] == guy:
                    spot_guy = i
                i += 1
                
            if spot_guy is not None:
                btn = self.btns[spot_guy]
                btn.config(bg=self.spot_clr) 
                num = self.version
                self.after(500, lambda: self.spotlight_covery(btn, num))
                
    def spotlight_covery(self, btn, num):
        with self.lock:
            if num == self.version:
                btn.config(bg=self.btn_clr)
                
    def remove_all_buttons(self):
        with self.lock:
            self.version += 1
            self.btns.clear()
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            
if __name__ == '__main__':

    def add_to_listbox():
        content = entry.get()
        if content:
            entry.delete(0, tk.END)
            sb.add_button(content, True)
            
    def upd():
        d0 = {"Stephy":29, "Derek":38, "Kevin":73, "Kelly":24}
        sb.update_scores(d0, "Derek")
            
    def remove_all():
        sb.remove_all_buttons()
    
    root = tk.Tk()
    root.title("Listbox with Buttons Example")
    
    sb = ScoreBoard(root)
    sb.pack(pady=10, fill="both", expand=True)
    
    entry = tk.Entry(root, width=50)
    entry.pack(pady=5)
    
    button = tk.Button(root, text="Add to Listbox", command=add_to_listbox)
    button.pack(pady=5)
    
    button = tk.Button(root, text="Update", command=upd)
    button.pack(pady=5)
    
    button = tk.Button(root, text="Remove All", command=remove_all)
    button.pack(pady=5)
    
    root.mainloop()
