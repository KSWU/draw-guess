import socket_s


'''
This is the interface specially for this project (Draw & Guess game)
'''

class ServerInterface(socket_s.SocketServer):

    
    def __init__(self,host,port):
        super().__init__(host,port)
        self.recv_act = self.dealwithType
        self.recv_acts = {
            "claim_host":None,
            "start":None,
            "choose":None,
            "canvas":None,
            "ans":None,
        }


    #-- external func ----------------------------------------
    
    def send_data(self,client,ty,data):
        data = {"type":ty,"ty_dict":data}
        self.send_dict(client,data)
        
    def send_data_all(self,ty,data,exclude_client=None):
        data = {"type":ty,"ty_dict":data}
        self.broadcast(data,exclude_client)
        
        
        
        
    #-- external func bottom ---------------------------------
    #-- internal func ----------------------------------------
    def dealwithType(self,client,addr,data):
        #print("dealwithType")
        ty = data["type"]
        data = data["ty_dict"]
        #print(f"recv {ty}")
        if self.recv_acts[ty]:
            self.recv_acts[ty](client,addr,data)

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
    s = ServerInterface('192.168.124.107',5555)
    s.start_server()
    
    while True:
        n = input()
        if n==0:
            break
        s.turnToDict(n)
