import threading

class MyTimerr :
    
    def __init__(self,time=10,timeOut_act=None,preEnd_act=None):
        
        self.__time = time
        self.__timeOut_act = timeOut_act
        self.__preEnd_act = preEnd_act
        self.__event = threading.Event()
        
        
        
    def start_timer(self,time=None,timeOut_act=None,preEnd_act=None):
        
        threading.Thread(target=self.__start_timer_task,args=(time,timeOut_act,preEnd_act)).start()
        
    def __start_timer_task(self,time=None,timeOut_act=None,preEnd_act=None):
        
        #print("start")
        self.__set_time(time)
        self.__set_timeOut_act(timeOut_act)
        self.__set_preEnd_act(preEnd_act)
        
        self.__event = threading.Event()
        isEventOccur = self.__event.wait(self.__time)
    
        if not isEventOccur :
            #print("===timeout")
            if self.__timeOut_act:
                self.__timeOut_act()
        else :
            #print("===preEnd")
            if self.__preEnd_act:
                self.__preEnd_act()
            
    def pre_end_timer(self,preEnd_act=None):
        #print("pre_end_timer")
        self.__set_preEnd_act(preEnd_act)
        self.__event.set()
        
    
        

                    
            
    
    def __set_time(self,time=None):
        if time : 
            self.__time = time
            
    def __set_timeOut_act(self,timeOut_act=None):
        if timeOut_act:
            self.__timeOut_act = timeOut_act
            
    def __set_preEnd_act(self,preEnd_act=None):
        if preEnd_act :
            self.__preEnd_act = preEnd_act
    
            

        
if __name__ == '__main__':
    
    # === testing func ==========================
    def timeout_act():
        print("time out !!")
        
    def event_act():
        print("user !!")
        
    def inputy():
        
        while True :
            n = input()
            if n=="0":
                t.start_timer()
            if n=="1":
                t.pre_end_timer()

    # === testing func bottom ===================
    
    t = MyTimerr()
    t.start_timer(10,timeOut_act=timeout_act,preEnd_act=event_act)
    
    while True :
        n = input()
        if n=="0":
            t.start_timer()
        if n=="1":
            t.pre_end_timer()

            

    
