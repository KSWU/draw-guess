import tkinter as tk
from tkinter import ttk
import MyCanvasFrame 
import CntDownPgBar
import ScoreBoard
import Skeleton_EndingFrame

class Skeleton_GamingWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.bg_clr = "#A4DFE7"#3A76C6#B4C7E7
        self.inner_clr = "#F5F5ED"#638FA9#E1DDBF
        
        self.title("Gaming Window")
        self.geometry("1000x500+100+50")
        self.configure(bg=self.bg_clr)
        
        self.end_frame = None

        # 左侧Frame
        '''
        self.left_frame = tk.Frame(self, bg="#FFEC89", bd=2, relief=tk.SOLID)
        self.left_frame.place(relx=0.02, rely=0.02, relwidth=0.2, relheight=0.96)
        
        self.player_label = tk.Label(self.left_frame, text="You:", bg="white", font=("Arial", 14))
        self.player_label.pack(pady=10)

        self.players_listbox = tk.Listbox(self.left_frame, font=("Arial", 12))
        self.players_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        
        # 添加一些示例玩家
        self.players_listbox.insert(tk.END, "User2374 (房主)")
        self.players_listbox.insert(tk.END, "User2230")
        self.players_listbox.delete(0,tk.END)
        for _ in range(5):
            self.players_listbox.insert(tk.END, "空的玩家欄位")
            
        '''
        self.left_frame = tk.Frame(self, bg="green") # , bd=2, relief=tk.SOLID
        self.left_frame.place(relx=0.02, rely=0.02, relwidth=0.2, relheight=0.96)
        
        self.player_label = tk.Label(self.left_frame, text="玩家列表", bg="white", font=("Arial", 14))
        self.player_label.place(relx=0,rely=0,relwidth=1.0,relheight=0.1)# pady=10
        
        self.score_board = ScoreBoard.ScoreBoard(self.left_frame)
        self.score_board.place(relx=0,rely=0.1,relwidth=1.0,relheight=0.9)
        
        # 右上name_label
        self.name_label = tk.Label(self,bg=self.bg_clr,text="player?", font=("Arial", 20))
        self.name_label.place(relx=0.78, rely=0.08, relwidth=0.2, relheight=0.1)
            
        # 右下Frame
        self.right_frame = tk.Frame(self, bg=self.inner_clr, bd=2) #, relief=tk.SOLID
        self.right_frame.place(relx=0.78, rely=0.26, relwidth=0.2, relheight=0.72)
        self.chat_listbox = tk.Listbox(self.right_frame, font=("Arial", 12))
        self.chat_listbox.place(relx=0.02, rely=0.02, relwidth=0.91, relheight=0.88)
        self.scr_chat = ttk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.chat_listbox.yview)
        self.scr_chat.place(relx=0.93, rely=0.02, relwidth=0.08, relheight=0.88) #pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_listbox.config(yscrollcommand=self.scr_chat.set)
        self.ans_entry = tk.Entry(self.right_frame)
        self.ans_entry.place(relx=0.02, rely=0.92, relwidth=0.75, relheight=0.07)
        self.ans_btn =  tk.Button(self.right_frame, text="Send")
        self.ans_btn.place(relx=0.78, rely=0.92, relwidth=0.20, relheight=0.07)
        #self.chat_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        

        # 中上Frame
        '''
        self.center_top_frame = tk.Frame(self, bg="white")
        self.center_top_frame.place(relx=0.24, rely=0.02, relwidth=0.52, relheight=0.89)
        '''
        self.cnv = MyCanvasFrame.MyCanvasFrame(self)
        self.cnv.place(relx=0.24, rely=0.02, relwidth=0.52, relheight=0.89)

        # 中下Frame
        self.center_bottom_frame = tk.Frame(self, bg=self.inner_clr, bd=2) #, relief=tk.SOLID
        self.center_bottom_frame.place(relx=0.24, rely=0.91, relwidth=0.52, relheight=0.07)
        
        self.pgb = CntDownPgBar.CntDownPgBar(self.center_bottom_frame)
        self.pgb.place(relx=0.00, rely=0.05, relwidth=1.00, relheight=0.90)
        
    def switch_end(self,llst):
        
        self.end_frame = Skeleton_EndingFrame.Skeleton_EndingFrame(self,llst)
        
        self.end_frame.place(relx=0.24, rely=0.02, relwidth=0.52, relheight=0.89)
        
    def switch_back(self):
        if self.end_frame :
            self.end_frame.destroy()
            self.end_frame = None

if __name__ == "__main__":
    
    def change():
        global ff
        if ff:
            lst = ["player0","player1","player2"]
            wnd.switch_end(lst)
            ff = False
        else :
            wnd.end_frame.destroy()
            ff = True
    
    ff = True
    wnd = Skeleton_GamingWindow()
    wnd.ans_btn.config(command=change)
    #line_id_a =  wnd.canvas.create_line(0, 0, 100, 100, fill="white", width=10)
    
    wnd.mainloop()
