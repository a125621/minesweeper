import tkinter as tk
from game_ui import start_game_ui


def level(level,menu_win):
    if level == 'simple':
        rows = 6
        cols = 6
        mines= 8
    elif level == 'middle':
        rows = 10
        cols = 10
        mines= 15
    elif level == 'hard':
        rows = 15
        cols = 15
        mines= 40
    print(f"【測試】你選擇了 {level} 難度！矩陣大小為：{rows}x{cols}，地雷數：{mines}")
    menu_win.destroy()  # 關掉選單
    start_game_ui(rows, cols, mines)  # 啟動遊戲畫面
    
def init_menu():
    win = tk.Tk()
    win.geometry("300x300")
    win.title("困难度选择")

    title1 = tk.Label(win, text="欢迎游玩踩地雷", font=("", 16))
    title1.pack(pady=(20, 2))  # pady=(上邊距, 下邊距)
    title2 = tk.Label(win, text="请选择难度", font=("", 16))
    title2.pack(pady=(2, 15))  # 這兩個 Label 之間的間距，就是你要的行距！

    simple = tk.Button(win,
                       text='simple',
                       command=lambda:level('simple',win),
                       relief='raised', #边框种类设定，button的预设
                       bd=3,            #边框宽
                       font=('',12))
    simple.pack(pady=10)

    middle = tk.Button(win,
                       text='middle',
                       command=lambda:level('middle',win),
                       relief='raised',
                       bd=3,
                       font=('',12))
    middle.pack(pady=10)

    hard = tk.Button(win,
                       text='hard',
                       command=lambda:level('hard',win),
                       relief='raised',
                       bd=3,
                       font=('',12))
    hard.pack(pady=10)
    win.mainloop()
    
if __name__=="__main__":
    init_menu()