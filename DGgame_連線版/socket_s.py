import socket
import threading
import json

class SocketServer:
    
    MSG_LENGTH = 1024
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        self.clients = []
        self.addrs = []
        self.lock_clients = threading.Lock()
        self.recv_act = None
        self.accept_act = None
        self.recv_from_agent = None
        self.running = False
        self.server_thread = None
        
    #-- external func ----------------------------------------
    def start_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.running = True
        self.server_thread = threading.Thread(target=self.accepting_client)
        self.server_thread.start()
        
    def stop_server(self):
        self.running = False
        self.sock.close()
        with self.lock_clients:
            for client in self.clients:
                client.close()
        self.server_thread.join()
        
    def broadcast(self, data, exclude_client=None):
        with self.lock_clients:
            for client in self.clients:
                if not client == exclude_client:
                    self.send_fixed_length_message(client, data)
    
    def send_dict(self, client, data):
        self.send_fixed_length_message(client, data)
        
    #-- external func bottom ---------------------------------
    #-- internal func ----------------------------------------
    def accepting_client(self):
        while self.running:
            try:
                client, addr = self.sock.accept()
                with self.lock_clients:
                    self.clients.append(client)
                    self.addrs.append(addr)
                if self.accept_act:
                    self.accept_act(client, addr)
                threading.Thread(target=self.listen_client, args=(client, addr)).start()
            except OSError:
                break
    
    def listen_client(self, client, addr):
        while self.running:
            try:
                message = client.recv(self.MSG_LENGTH).decode('utf-8').strip()
                if message:
                    data = json.loads(message)
                    if self.recv_act:
                        self.recv_act(client, addr, data)
            except:
                if self.recv_from_agent:
                    error_msg = {"error_type": "client_lost", "dict": {"client": client, "addr": addr}}
                    self.recv_from_agent(error_msg)
                with self.lock_clients:
                    self.clients.remove(client)
                    self.addrs.remove(addr)
                break

    def send_fixed_length_message(self, sock, message):
        json_message = json.dumps(message)
        if len(json_message) < self.MSG_LENGTH:
            json_message = json_message.ljust(self.MSG_LENGTH)
        elif len(json_message) > self.MSG_LENGTH:
            json_message = json_message[:self.MSG_LENGTH]
        sock.sendall(json_message.encode('utf-8'))

    #-- internal func bottom ---------------------------------

if __name__ == '__main__':
    
    def sample_recv_act(client, addr, data):
        svr.broadcast(data, client)
        
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    svr = SocketServer(local_ip, 5555)
    svr.recv_act = sample_recv_act
    svr.start_server()
    
    while True:
        n = input("Enter 0 to stop the server: ")
        if n == "0":
            svr.stop_server()
            print("Server stopped.")
            break
'''
if __name__ == '__main__' :
    
    def sample_recv_act(client,addr,data):
        svr.broadcast(data,client)
        
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    svr = SocketServer(local_ip, 5555)
    svr.recv_act = sample_recv_act
    svr.start_server()
    while True:
        n = input()
        if n == 0:
            break
'''