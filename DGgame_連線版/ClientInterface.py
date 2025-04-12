import socket_c


'''
This is the interface specially for this project (Draw & Guess game)
'''

class ClientInterface(socket_c.SocketClient):

    
    def __init__(self,host,port):
        super().__init__(host,port)
        self.recv_act = self.dealwithType
        self.recv_acts = {
            "init_data":None,
            "canvas":None,
            "ans":None,
            "enter":None,
            "leave":None,
            "stt_choose":None,
            "stt_drawguess":None,
            "stt_rest":None,
            "stt_end":None,
            "stt_again":None
        }

    #-- external func ----------------------------------------
    
    def send_data(self,ty,data):
        data = {"type":ty,"ty_dict":data}
        self.send_dict(data)
        
    def send_canvas(self,data):
        data = {"type":"canvas","ty_dict":data}
        self.send_dict(data)
    
    def send_choice(self,data):
        data = {"type":"choice","ty_dict":data }
        self.send_dict(data)
        
    def send_ans(self,data):
        data = {"type":"ans","ty_dict":data}
        self.send_dict(data)  
        
        
    #-- external func bottom ---------------------------------
    #-- internal func ----------------------------------------
    def dealwithType(self,data):
        #print("dealwithType")
        ty = data["type"]
        data = data["ty_dict"]
        #print(f"recv {ty}")
        if self.recv_acts[ty]:
            self.recv_acts[ty](data)

    #-- internal func bottom ---------------------------------
    #-- testing func ----------------------------------------
    def printRecv(self,data):
        print(data)
    def turnToDict(self,str0):
        arr = str0.split(':')
        data = {arr[0]:arr[1]}
        self.send_dict(data)
    #-- testing func bottom ---------------------------------



if __name__ == '__main__':
    c = ClientInterface('192.168.124.107',5555)
    c.start_client()
    
    while True:
        n = input()
        if n==0:
            break
        c.turnToDict(n)
