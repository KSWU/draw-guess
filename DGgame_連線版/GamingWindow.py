import tkinter as tk 

import Skeleton_GamingWindow
import ClientInterface


class GamingWindow(Skeleton_GamingWindow.Skeleton_GamingWindow):
    
    def __init__(self,cln):
        super().__init__()
        self.myName = None
        self.cln = cln
        self.cln.recv_acts["init_data"] = self.recv_init_data
        self.cln.recv_acts["canvas"] = self.recv_canvas 
        self.cln.recv_acts["ans"] = self.recv_ans 
        self.cln.recv_acts["enter"] = self.recv_enter
        self.cln.recv_acts["leave"] = self.recv_leave
        self.cln.recv_acts["stt_choose"] = self.recv_stt_choose
        self.cln.recv_acts["stt_drawguess"] = self.recv_stt_drawguess 
        self.cln.recv_acts["stt_rest"] = self.recv_stt_rest 
        self.cln.recv_acts["stt_end"] = self.recv_stt_end
        self.cln.recv_acts["stt_again"] = self.recv_again
        
        self.cnv.bind("<<drawing>>",self.on_draw)
        self.ans_btn.config(command=self.send_onclick)
        

        
        self.debug_print = False
        
     
    # ---recv action------------------------------------------------------------
    def recv_canvas(self,data):
        self.cnv.show_by_dict(data)
        
    def recv_ans(self,data):
        if self.debug_print :
            print("GamingWindow | recv_ans")
        scores,guy,ans,isRight = data.values()
        #print(scores_str)
        str0 = ""
        if isRight :
            str0 = guy+" got it !"
            self.update_players_board(scores,guy)
        else:
            str0 = guy+" guess : "+ans
        self.add_chat(str0)
        
    def recv_enter(self,data):
        if self.debug_print :
            print("GamingWindow | recv_enter")
        scores,guy = data.values()
        print(scores,guy)
        self.update_players_board(scores,guy)
        if self.myName == guy:
            self.add_chat("You enter the room")
        else :
            self.add_chat(guy+" enter the room")
            
    def recv_leave(self,data):
        if self.debug_print :
            print("GamingWindow | recv_leave")
        scores,guy = data.values()
        self.update_players_board(scores)
        self.add_chat(guy+" leave the room")        
          
        
    def recv_stt_choose(self,data):
        if self.debug_print :
            print("GamingWindow | recv_stt_choose")
        guy,ans,sec = data.values()
        self.pgb.end_progress()
        self.pgb.start_progress(sec,self.pgb_timesup)
        
        self.cnv.clear_canvas()
        self.cnv.disable()
        self.ans_entry.config(state=tk.DISABLED)
        self.ans_btn.config(state=tk.DISABLED)
        
        
        if guy == self.myName :
            str0 = "You are painter\n"+"Topic : "+ans
        else :
            str0 = guy+" is painter"
        self.cnv.show_string(str0)
        self.cnv.word_label.config(text=str0)
        
    def recv_stt_drawguess(self,data):
        if self.debug_print :
            print("GamingWindow | recv_stt_drawguess")
        guy,ans,sec = data.values()
        self.pgb.end_progress()
        self.pgb.start_progress(sec,self.pgb_timesup)
        
        self.cnv.clear_canvas()
        self.cnv.disable()
        self.ans_entry.config(state=tk.NORMAL)
        self.ans_btn.config(state=tk.NORMAL)
        
        if guy == self.myName :
            stry = ans
            self.cnv.restart()
            self.ans_entry.config(state=tk.DISABLED)
            self.ans_btn.config(state=tk.DISABLED)
        else :
            stry = guy+" is painter"
            
        self.cnv.word_label.config(text=stry)
        
        
        
    def recv_stt_rest(self,data):
        if self.debug_print :
            print("GamingWindow | recv_stt_rest")
        cnt,tot,sec = data.values()
        self.pgb.end_progress()
        self.pgb.start_progress(sec,self.pgb_timesup)
        self.cnv.clear_canvas()
        self.cnv.disable()
        self.ans_entry.config(state=tk.DISABLED)
        self.ans_btn.config(state=tk.DISABLED)
        
        if cnt==tot:
            str0 = "All people get the answer!!"
        else :
            str0 = str(cnt) +" people get the answer"
        self.cnv.show_string(str0)
        self.cnv.word_label.config(text="")
        
    def recv_stt_end(self,data):
        if self.debug_print :
            print("GamingWindow | recv_stt_end")
        scores, = data.values()
        self.pgb.end_progress()
        self.update_players_board(scores)
        self.cnv.clear_canvas()
        self.cnv.disable()
        str0 = "The game is ended"
        '''
        self.cnv.show_string(str0)
        '''
        list_data = [[k, v] for k, v in scores.items()]
        lst = sorted(list_data, key=lambda x: x[1], reverse=True)
        lst = [fir for fir,secd in lst]
        self.switch_end(lst)
        self.end_frame.btn.config(command=self.again_onclick)
        self.cnv.word_label.config(text="")
        self.ans_entry.config(state=tk.DISABLED)
        self.ans_btn.config(state=tk.DISABLED)
        
    def recv_init_data(self,data):
        if self.debug_print :
            print("GamingWindow | recv_init_data")
        self.myName, = data.values()
        self.name_label.config(text=self.myName)
        # 初始視窗權限
        self.cnv.disable()
        self.ans_entry.config(state=tk.DISABLED)
        self.ans_btn.config(state=tk.DISABLED)
        
        self.cnv.word_label.config(text="")
        self.cnv.show_string("Waiting for Owner to Start...")
        
    def recv_again(self,data):
        scores, = data.values()
        self.update_players_board(scores)
        self.switch_back()
        
    # --- recv action bottom-----------------------------------------------------------
    # --- command func ----------------------------------------------------------------
    def send_onclick(self):
        if self.debug_print :
            print("GamingWindow | send_onclick")
        stry = self.ans_entry.get()
        if not stry:
            return 
        data = {"guy":self.myName,"ans":stry}
        self.cln.send_data("ans",data)
        self.ans_entry.delete(0, tk.END)
        
    def on_draw(self,event):
        data = self.cnv.event_data
        self.cln.send_data("canvas",data)
        
    def pgb_timesup(self):
        if self.debug_print :
            print("GamingWindow | pgb_timesup")
        '''
        self.cnv.clear_canvas()
        self.cnv.disable()
        self.ans_entry.config(state=tk.DISABLED)
        self.ans_btn.config(state=tk.DISABLED)
        '''
        
        self.cnv.word_label.config(text="--")
        
    def again_onclick(self):
        data = {"name":self.myName}
        self.cln.send_data("again",data)
        
        
    
    # --- command func bottom ---------------------------------------------------------
    # --- other func ------------------------------------------------------------------
    def update_players_board(self,dictt,guy=None):
        self.score_board.update_scores(dictt,guy)
         
          
    def add_chat(self,str0):
        self.chat_listbox.insert(tk.END, str0)
        self.chat_listbox.yview(tk.END)  # 自动滑动到底部
    
    # --- other func bottom ----------------------------------------------------------
    
     

if __name__ == '__main__':
    

    hostIP,hostPort = '192.168.128.107', 5555
    c = ClientInterface.ClientInterface(hostIP,hostPort)
    g = GamingWindow(c)
    
    c.start_client()
    g.mainloop()
    