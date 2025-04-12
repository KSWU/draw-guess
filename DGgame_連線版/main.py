import socket

import Skeleton_HostOrGuess
import HostStart
import Skeleton_GuessEnter
import GamingWindow
import Umpire
import ClientInterface

wnd_home = None
wnd_enter = None
wnd_gaming = None
wnd_ending = None
ump = None
cln = None
portt = 5555
eeeend = False
lst = None


def home():
    global wnd_home
    wnd_home = Skeleton_HostOrGuess.Skeleton_HostOrGuess(host_onclick,guess_onclick)
    wnd_home.mainloop()
    
def host_onclick():
    global wnd_home,wnd_enter,wnd_gaming,ump,cln
    
    wnd_home.destroy()
    #建立Umpire 啟動server
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    ump = Umpire.Umpire( local_ip, portt)
    ump.svr.start_server()
    
    
    
    
    wnd_enter = HostStart.HostStart(ump,start_onclick)
    wnd_enter.mainloop()

    
    
    
def guess_onclick():
    global wnd_home,wnd_enter,cln
    wnd_home.destroy()
    wnd_enter = Skeleton_GuessEnter.Skeleton_GuessEnter(enter_onclick,back_onclick)
    wnd_enter.mainloop()
    
def start_onclick():
    global wnd_enter,wnd_gaming,ump,cln,wnd_gaming
    ump.outer_accept_act=False
    wnd_enter.destroy()
    
    #啟動作為玩家的client
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    cln = ClientInterface.ClientInterface(local_ip,portt)
    wnd_gaming = GamingWindow.GamingWindow(cln)
    cln.start_client()
    
    wnd_gaming.after(500,aafter)
    wnd_gaming.mainloop()
    
    
def aafter():
    ump.start_game()
    
def enter_onclick(room_str):
    global wnd_enter,wnd_gaming,cln
    wnd_enter.destroy()
    
    hostIP,hostPort = room_str.split(':')
    hostPort = int(hostPort)
    
    cln = ClientInterface.ClientInterface(hostIP,hostPort)
    wnd_gaming = GamingWindow.GamingWindow(cln)
    
    cln.start_client()
    wnd_gaming.mainloop()
    
    
def back_onclick():
    global wnd_enter,wnd_home
    wnd_enter.destroy()
    home()
    

    

if __name__ == '__main__':
    home()
    