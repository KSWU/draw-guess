# 目前功能有:畫筆、橡皮擦、更改畫筆顏色、撤銷、恢復、清空畫布

# 以drawing_mode更改繪畫/橡皮擦模式
# 發現問題:若目前使用橡皮擦，更改畫筆顏色後依然是橡皮擦
# 解決方法:在每次更動顏色時將模式改為繪畫模式

# 撤銷及恢復的部分是用stack來儲存每筆畫軌跡，以滑鼠按下到放開算一筆畫
# 發現問題:在撤銷後又恢復時，原畫筆顏色會變成目前畫筆顏色
# 解決方法:將畫筆顏色也一併記錄起來，以便恢復時可以連原本畫筆顏色也恢復

# 繪畫原理:
# 當按下滑鼠左鍵時開始一個新的筆畫，當按著滑鼠左鍵移動時代表正在繪畫，放開滑鼠左鍵代表此筆畫完成
# 當開始一個新筆畫時新增一個current_action陣列儲存當前筆畫資訊，並將目前x,y座標設為last_x和last_y
# 在繪畫過程中，是利用last_x, last_y和當前x, y座標來畫出直線，並添加到current_action中，再將當前x, y座標設為last_x, last_y，一直重複此步驟直到放開滑鼠
# 結束一筆畫後，將current_action以及畫筆顏色加入undo_stack，並將redo_stack清空(因為沒有下一筆畫了)

'''
canvas收到server的指令有4種:
{"canvas_action":"draw_start","dict":{"action_id":self.current_action_id,"x1":event.x, "y1":event.y}}
{"canvas_action":"draw_end","dict":{"action_id":self.current_action_id}}
{"canvas_action":"drawing","dict":{"action_id":self.current_action_id,"x1":x1,"y1":y1,"x2":x2,"y2":y2,"color":color}}
{"canvas_action":"erase","dict":{"action_id":self.current_action_id,"x1":x1,"y1":y1,"x2":x2,"y2":y2,"color":"white"}}
{"canvas_action":"undo","dict":{"action_id":action_id}}
{"canvas_action":"redo","dict":{"action_id":action_id}}
{"canvas_action":"clear","dict":0}

'''

'''
此class應該提供func:


'''

import tkinter as tk
from tkinter import colorchooser

import Skeleton_MyCanvasFrame

class MyCanvasFrame(Skeleton_MyCanvasFrame.Skeleton_MyCanvasFrame):
    
    def __init__(self,root,**args):
        super().__init__(root,**args)
        
        self.instance_name = ""
        self.can_paint = True
        self.drawing_mode = True  # 畫筆模式，True表示畫筆模式，False表示橡皮擦模式
        self.pen_color = "black"  # 畫筆顏色預設為黑色
        self.undo_stack = []      # 用於儲存每筆畫的軌跡，以便撤銷操作
        self.redo_stack = []      # 用於儲存被撤銷的筆畫，以便恢復操作
        self.current_action = []
        self.current_action_id = None
        self.event_data = None
        # event_datas = []
        
        # 綁定畫布的事件
        self.canvas.bind("<B1-Motion>", self.draw_or_erase)
        self.canvas.bind("<Button-1>", self.start_action)
        self.canvas.bind("<ButtonRelease-1>", self.end_action)
        
        self.draw_button.config(command=self.set_draw_mode)
        self.erase_button.config(command=self.set_erase_mode)
        self.color_button.config(command=self.choose_color)
        self.undo_button.config(command=self.undo_last_action)
        self.redo_button.config(command=self.redo_last_action)
        self.clear_button.config(command=self.clear_onclick)

        self.red_button.config(command=lambda: self.set_pen_color("red"))
        self.orange_button.config(command=lambda: self.set_pen_color("orange"))
        self.yellow_button.config(command=lambda: self.set_pen_color("yellow"))
        self.green_button.config(command=lambda: self.set_pen_color("green"))
        self.blue_button.config(command=lambda: self.set_pen_color("blue"))
        self.purple_button.config(command=lambda: self.set_pen_color("purple"))
        self.black_button.config(command=lambda: self.set_pen_color("black"))
        
        self.debug_print = False
        
    #-- external func ----------------------------------------
    def disable(self):
        if self.debug_print :
            print("MyCanvasFrame | func disable")
        self.can_paint = False
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        for btn in self.all_btn:
            btn.config(state=tk.DISABLED)
        
            
    def enable(self):
        if self.debug_print :
            print("MyCanvasFrame | func enable")
        self.can_paint = True
        self.canvas.bind("<B1-Motion>", self.draw_or_erase)
        self.canvas.bind("<Button-1>", self.start_action)
        self.canvas.bind("<ButtonRelease-1>", self.end_action)
        for btn in self.all_btn:
            btn.config(state=tk.NORMAL)
            
    def restart(self):
        if self.debug_print :
            print("MyCanvasFrame | func restart")
        self.clear_canvas()
        self.can_paint = True
        self.drawing_mode = True  # 畫筆模式，True表示畫筆模式，False表示橡皮擦模式
        self.pen_color = "black"  # 畫筆顏色預設為黑色
        self.event_data = None      
        self.enable()
        
    def clear_canvas(self):
        # 清除畫布
        if self.debug_print :
            print("MyCanvasFrame | clear canvas")
        self.canvas.delete("all")
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.current_action.clear()
        self.current_action_id = None
            
        
        
    def show_string(self,str0=""):
        if self.debug_print :
            print("MyCanvasFrame | show_string")
        self.disable()
        self.clear_canvas()
        self.canvas.update_idletasks()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_width()
        #print(f"{width}x{height}")
        #print(str0)
        self.canvas.create_text(width/2, height/2, text=str0, font=("Arial", 24), fill="black")

    def show_by_dict(self,data):
        if data:
            act = data.get("canvas_action")
            if act=="draw_start":
                self.recv_start(data)
            if act=="draw_end":
                self.recv_end(data)
            if act=="drawing" :
                self.recv_draw(data)
            if act=="erase":
                self.recv_erase(data)
            if act=="undo":
                self.recv_undo(data)
            if act=="redo":
                self.recv_redo(data)
            if act=="clear":
                self.clear_canvas() 
    
    #-- external func bottom ---------------------------------
    #-- internal func ----------------------------------------
    def set_draw_mode(self):
        # 設置為畫筆模式
        self.drawing_mode = True

    def set_erase_mode(self):
        # 設置為橡皮擦模式
        self.drawing_mode = False
    
    def set_pen_color(self, color):
        # 設置畫筆顏色並設置為畫筆模式
        self.pen_color = color
        self.set_draw_mode()  # 設置為畫筆模式
        
    def choose_color(self):
        # 彈出顏色選擇器以更改畫筆顏色
        color = colorchooser.askcolor()[1]
        if color:
            self.pen_color = color
            self.set_draw_mode()  # 設置為畫筆模式
            
    def clear_onclick(self):
        # 清除畫布
        if self.debug_print :
            print("MyCanvasFrame | clear_onclick")
        self.clear_canvas()
        if self.can_paint :
            self.gen_event({"canvas_action":"clear"})
        
    
    def start_action(self, event):
        # 開始一個新的操作
        self.current_action = []
        if not self.current_action_id:
            self.current_action_id = 0
        self.current_action_id += 1
        self.update_position(event)
        self.gen_event({"canvas_action":"draw_start","dict":{"action_id":self.current_action_id,"x1":event.x, "y1":event.y}})

    def recv_start(self,data):
        data = data.get("dict")
        if data :
            action_id,x1,y1 = data.values()
            self.current_action = []
            self.current_action_id = action_id

    def end_action(self, event):
        # 結束當前操作，將其添加到操作列表中
        if self.current_action:
            self.undo_stack.append((self.current_action, self.current_action_id))  # 儲存動作和颜色
            self.redo_stack.clear()  # 每次執行新操作時清除redo_stack
            self.gen_event({"canvas_action":"draw_end","dict":{"action_id":self.current_action_id}})

    def recv_end(self,data):
        data = data.get("dict")
        if data :
            action_id = data.values()
            if self.current_action:
                self.undo_stack.append((self.current_action, self.current_action_id))  # 儲存動作和颜色
                self.current_action = []
                self.redo_stack.clear()  # 每次執行新操作時清除redo_stack
                

    def update_position(self, event):
        # 更新最後一個座標
        self.last_x, self.last_y = event.x, event.y

    def draw_or_erase(self, event):
        # 畫或擦除根據當前模式
        x, y = event.x, event.y 
        #if abs(x-self.last_x)>10 or abs(y-self.last_y)>10:
        #    return 
        if not self.current_action_id:
            return 
            
        if self.drawing_mode:
            # 畫線
            x1,y1,x2,y2 = self.last_x, self.last_y, x, y
            color = self.pen_color
            line_id = self.canvas.create_line(x1,y1,x2,y2, fill=color, width=2)
            self.current_action.append( line_id )  # 儲存動作
            self.gen_event({"canvas_action":"drawing","dict":{"action_id":self.current_action_id,"x1":x1,"y1":y1,"x2":x2,"y2":y2,"color":color}})
        else:
            # 擦除(畫筆顏色為白)
            x1,y1,x2,y2 = self.last_x, self.last_y, x, y
            color = "white"
            line_id = self.canvas.create_line(x1,y1,x2,y2, fill=color, width=10)
            self.current_action.append( line_id )  # 儲存動作
            self.gen_event({"canvas_action":"erase","dict":{"action_id":self.current_action_id,"x1":x1,"y1":y1,"x2":x2,"y2":y2,"color":color}})

        self.update_position(event)
        
    def recv_draw(self,data):
        data = data.get("dict")
        if data :
            action_id,x1,y1,x2,y2,color = data.values()
            if not (action_id==self.current_action_id) :
                self.recv_end({"dict":{"action_id":self.current_action_id}})
                self.current_action_id = action_id
            line_id = self.canvas.create_line(x1,y1,x2,y2, fill=color, width=2)
            self.current_action.append( line_id )  # 儲存動作
            
    def recv_erase(self,data):
        data = data.get("dict")
        if data :
            action_id,x1,y1,x2,y2,color = data.values()
            if not (action_id==self.current_action_id) :
                self.recv_end({"dict":{"action_id":self.current_action_id}})
                self.current_action_id = action_id
            line_id = self.canvas.create_line(x1,y1,x2,y2, fill=color, width=10)
            self.current_action.append( line_id )  # 儲存動作


    def undo_last_action(self):
        # 撤銷上一個操作
        if self.undo_stack:
            last_action, action_id = self.undo_stack.pop()  # 获取动作和id
            self.gen_event({"canvas_action":"undo","dict":{"action_id":action_id}})
            last_action_detail = []
            for line_id in last_action:
                x1, y1, x2, y2 = self.canvas.coords(line_id)
                color = self.canvas.itemcget(line_id, 'fill')
                last_action_detail.append((x1, y1, x2, y2, color))
                self.canvas.delete(line_id)
            self.redo_stack.append((last_action_detail, action_id))  # 存储动作和id

    def recv_undo(self,data):
        if self.undo_stack:
            data = data.get("dict")
            if data :
                action_id, = data.values()
                _,iid = self.undo_stack[len(self.undo_stack)-1]
                if not(iid==action_id):
                    return 
                last_action, action_id = self.undo_stack.pop()  # 获取动作和id
                last_action_detail = []
                for line_id in last_action:
                    x1, y1, x2, y2 = self.canvas.coords(line_id)
                    color = self.canvas.itemcget(line_id, 'fill')
                    last_action_detail.append((x1, y1, x2, y2, color))
                    self.canvas.delete(line_id)
                self.redo_stack.append((last_action_detail, action_id))  # 存储动作和id

    def redo_last_action(self):
        # 恢復上一個撤銷的操作
        if self.redo_stack:
            last_action, action_id = self.redo_stack.pop()  # 获取动作和颜色
            self.gen_event({"canvas_action":"redo","dict":{"action_id":action_id}})
            new_action = []
            for line_detail in last_action:
                x1, y1, x2, y2, color = line_detail
                line_id_new = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2 if color != "white" else 10)
                new_action.append(line_id_new)  # 存储动作和颜色
            self.undo_stack.append((new_action, action_id))  # 存储动作和颜色
            
    def recv_redo(self,data):
        if self.redo_stack:
            data = data.get("dict")
            if data :
                action_id, = data.values()    
                while self.redo_stack:
                    last_action,iid = self.redo_stack.pop()
                    if (iid==action_id):
                        break
                if not(iid==action_id):
                    return 
                new_action = []
                for line_detail in last_action:
                    x1, y1, x2, y2, color = line_detail
                    line_id_new = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2 if color != "white" else 10)
                    new_action.append(line_id_new)  # 存储动作和颜色
                self.undo_stack.append((new_action, action_id))  # 存储动作和颜色
    
            

    def gen_event(self,event_data):
        #self.event_datas.append(event_data)
        self.event_data=event_data
        self.event_generate("<<drawing>>")
        


            
    #-- internal func bottom ---------------------------------



    
if __name__ == '__main__':
    
    def simul_send(event):
        wid = event.widget
        datadata = wid.event_data
        cnvs1.show_by_dict(datadata)
        
    root0 = tk.Tk()
    cnvs0 = MyCanvasFrame(root0)
    cnvs0.instance_name = "Jeff"
    cnvs0.pack()
    
    wnd1 = tk.Toplevel(root0)
    
    cnvs1 = MyCanvasFrame(wnd1)
    cnvs1.pack()
    cnvs1.instance_name = "Stephy"
    cnvs1.disable()
    cnvs0.bind("<<drawing>>",simul_send)
    
    
    root0.mainloop()   




