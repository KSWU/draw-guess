# 此程式用於切換各個程式&傳遞各程式所需參數
# 共用變數一律儲存於shared_data.json中，在此程式前段會先初始化
# 若關閉任一視窗，會發送訊號到這並結束程式

import sys
import subprocess
import json
import signal

def init_data():    # 初始化json檔
    with open('shared_data.json', 'r') as file:
        data = json.load(file)

    name_list = data['names']
    num_player = len(name_list)

    data['pno'] = 0
    data['score'] = [0] * num_player
    data['answer'] = ""

    with open('shared_data.json', 'w') as file:
        json.dump(data, file)

def signal_handler(sig, frame):
    print("Exiting program.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

subprocess.run(["python", "home.py"])
subprocess.run(["python", "player_name.py"])

init_data()

while(1):
    with open('shared_data.json', 'r') as file:
        data = json.load(file)

    name_list = data['names']
    num_player = len(name_list)
    pno = data['pno'] % num_player
    subprocess.run(["python", "draw_single.py", "--pno", name_list[pno-1]])

    with open('shared_data.json', 'r') as file:
        data = json.load(file)

    name_list = data['names']
    subprocess.run(["python", "guess_single.py", "--name"] + name_list)

    


