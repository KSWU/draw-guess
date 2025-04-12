import threading
import socket
import random

import ServerInterface 
import Conductor

class Umpire:
    
    def __init__(self,hostIP,hostPort):
        
        self.player_names = []
        self.scores = dict()
        self.owner = "player0"
        self.painter = None
        self.get_it = dict()
        self.anss = []#["apple","dog","cat","car","people"]
        self.shuffle_words()
        self.ans = ""
        self.CREDIT_MAX = 10
        self.credit = self.CREDIT_MAX
        
        self.lock_playerlist = threading.Lock()
        
        self.svr = ServerInterface.ServerInterface(hostIP,hostPort)
        self.svr.accept_act = self.accept_new_client
        self.svr.recv_acts["claim_host"] = self.recv_claim_host
        self.svr.recv_acts["start"] = self.recv_start
        self.svr.recv_acts["choose"] = self.recv_choose
        self.svr.recv_acts["canvas"] = self.recv_canvas
        self.svr.recv_acts["ans"] = self.recv_ans
        self.svr.recv_acts["again"] = self.recv_again
        
        self.cond = None
        self.stt_names = ["choose","drawguess","rest"]
        
        self.outer_accept_act = None

    # --- recv action ------------------------------------------------------------
    def recv_claim_host(self,client,addr,data):
        guy, = data.values()
        self.owner = guy
        
    def recv_start(self,client,addr,data):
        guy, = data.values()
        self.start_game()
        
    def recv_again(self,client,addr,data):
        guy, = data.values()
        self.init_game()
        data = {"scores":self.scores}
        self.svr.send_data_all("stt_again", data)
        self.start_game()
        
    def recv_choose(self,client,addr,data):
        guy,ans = data.values()
        #############################
        
    def recv_canvas(self,client,addr,data):
        self.svr.send_data_all("canvas", data, client)
        
        
    def recv_ans(self,client,addr,data):
        guy,ans = data.values()
        
        '''
        if guy == self.owner and ans == "start" :
            self.start_game()
            return 
        '''
        
        with self.cond.lock:
            section = self.cond.section
            if not self.stt_names[section] == "drawguess":
                return
            
            if self.get_it[guy] :
                return 
            
            if ans==self.ans :
                with self.lock_playerlist:
                    self.get_it[guy] = True
                    self.scores[guy] += self.credit
                    self.credit = self.credit-1 if self.credit>1 else 1
                    data = {"scores":self.scores,"guy":guy,"ans":ans,"isRight":True}
                    self.svr.send_data_all("ans", data)
                    if sum(self.get_it.values()) == len(self.get_it)-1 :
                        self.cond.jump_next_stt(section)
            else :
                with self.lock_playerlist:
                    data = {"scores":self.scores,"guy":guy,"ans":ans,"isRight":False}
                    self.svr.send_data_all("ans", data)
                    
                    
                    
                    
                    
    # ----- recv action bottom ------------------------------------------------------------------
    
    
            
    def start_game(self):
        self.init_game()
        
        self.cond = Conductor.Conductor(5,3)
        self.cond.section_secs = [7,60,10]
        self.cond.section_funcs = [self.choose,self.drawguess,self.rest]
        self.cond.finally_func = self.ending
        self.cond.start_game()

    def init_game(self):
        
        with self.lock_playerlist:
            self.painter = self.player_names[-1]
            for k,v in self.scores.items():
                self.scores[k] = 0
                self.get_it[k] = False
        self.shuffle_words()
        

        
        
    def choose(self):
        with self.lock_playerlist:
            try:
                ii = (self.player_names.index(self.painter)+1)%(len(self.player_names))
            except ValueError:
                ii = 0
            self.painter = self.player_names[ii]
            
            for k,v in self.get_it.items():
                self.get_it[k] = False 
        self.ans = self.anss[self.cond.chapter-1]
        self.credit = self.CREDIT_MAX
        
        data = {"guy":self.painter,"ans":self.ans,"sec":self.cond.section_secs[self.cond.section]}
        self.svr.send_data_all("stt_choose",data)
        print("umpire | stt choose")
        
    def drawguess(self):
        
        data = {"guy":self.painter,"ans":self.ans,"sec":self.cond.section_secs[self.cond.section]}
        self.svr.send_data_all("stt_drawguess",data)
        print("umpire | stt drawguess ")
        
    def rest(self):
        
        with self.lock_playerlist:
            cnt = 0 
            tot = len(self.get_it)-1
            for k,v in self.get_it.items():
                if self.get_it[k] :
                    cnt += 1
        data = {"cnt":cnt,"tot":tot,"sec":self.cond.section_secs[self.cond.section]}
        self.svr.send_data_all("stt_rest",data)
        print("umpire | stt rest ")
        
    def ending(self):
        
        with self.lock_playerlist:
            data = {"scores":self.scores}
            self.svr.send_data_all("stt_end",data)
            
        print("umpire | stt ending ")
    
    
        
        
    
        
    def accept_new_client(self,client,addr):
        
        with self.lock_playerlist :
            num = len(self.player_names)
            name = 'player'+str(num)
            self.player_names.append(name)
            self.scores[name] = 0
            
        data = {"name":name}
        self.svr.send_data(client,"init_data",data)
        data = {"scores":self.scores,"guy":name}
        self.svr.send_data_all("enter",data)
        '''
        data = {"type":"init_data","ty_dict":{"name":name}}
        self.svr.send_dict(client, data)
        data = {"type":"enter","ty_dict":{"scores":self.scores,"guy":name}}
        self.svr.broadcast(data)
        '''
        if self.outer_accept_act:
            self.outer_accept_act()
    # =====================================
    # other ================================
    
    def shuffle_words(self):
        with open("data.txt", "r") as file:
            words = file.readlines()
        self.anss = [word.strip() for word in words]
        
        # 随机打乱列表中的单词
        random.shuffle(self.anss)
        
        # 下面是测试输出，可以删除或修改为其他用途
        #print(words)
    # =========================================

if __name__ == '__main__':
    
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    u = Umpire( local_ip, 5555)
    
    u.svr.start_server()
    
    '''
    while True:
        n = input()
        if n == 0:
            break
    '''