import threading 
import socket
import json

class SocketClient:
    MSG_LENGTH = 1024

    
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.sock = None
        self.client_port = None
        self.recv_act = None
        self.dbg = False
        
    #-- external func ----------------------------------------
    def start_client(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((self.host,self.port))
        self.client_port = self.sock.getsockname()[1]
        threading.Thread(target=self.listen_server).start()
        
        
    def send_dict(self,data):
        self.send_fixed_length_message(data)
        
    #-- external func bottom ---------------------------------
    #-- internal func ----------------------------------------
    def listen_server(self):
        while True:
            self.dbg = not self.dbg
            try :
                message = self.sock.recv(self.MSG_LENGTH).decode('utf-8').strip()
                if message:
                    data = json.loads(message)
                    if self.recv_act:
                        self.recv_act(data)
                #print(self.dbg)
            except:
                #print("haha")
                #print(self.dbg)
                print("Recieving ERROR")
                
                
    def send_fixed_length_message(self, message):
        json_message = json.dumps(message)
        if len(json_message) < self.MSG_LENGTH:
            json_message = json_message.ljust(self.MSG_LENGTH)
        elif len(json_message) > self.MSG_LENGTH:
            json_message = json_message[:self.MSG_LENGTH]
        self.sock.sendall(json_message.encode('utf-8'))

    #-- internal func bottom ---------------------------------
