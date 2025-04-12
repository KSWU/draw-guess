import socket

import Skeleton_HostStart
import Umpire

class HostStart(Skeleton_HostStart.Skeleton_HostStart):
    
    def __init__(self,ump,start_act=None,back_act=None):
        
        super().__init__(ump.svr.host,ump.svr.port,start_act,back_act)
        self.ump = ump
        self.show_num(0)
        self.ump.outer_accept_act = self.smb_enter
        
    def smb_enter(self):
        with self.ump.lock_playerlist:
            self.show_num(len(self.ump.player_names))
            
            


if __name__ == '__main__':
    
    
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    u = Umpire.Umpire( local_ip, 5555)
    u.svr.start_server()
    
    root = HostStart(u)
    
    
    
    root.mainloop()
        
        
        
        