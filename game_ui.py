import tkinter as tk
import time
from game_logic import generate_board  #假設你當初在大腦寫的函式叫這個名字


def update_time(game_win,timer,current_time):
    current_time+=1
    curr_min, curr_sec = divmod(int(current_time), 60) #運算後可直接分為商與餘數
    timer.config(text=f'用時{curr_min:02d}:{curr_sec:02d}')
    game_win.after(1000,lambda:update_time(game_win, timer, current_time))

# =============================================================
# 寫在最外面：元件與記帳本通通由「參數」外送進來！
# =============================================================
def update_flag(flag_label, flag_tracker, word=None):
    # 1. 根據玩家的操作，去修改傳進來的list裡面的數字
    if word == 'increase':
        flag_tracker[0] -= 1  # 插了旗子，需要的旗子數減少
    elif word == 'decrease':
        flag_tracker[0] += 1  # 拔了旗子，需要的旗子數增加
        
    # 2. 透過傳進來的 flag_label 元件，更新畫面上的文字
    flag_label.config(text=f"需要🚩: {flag_tracker[0]}")
    
    
def gameover(game_win):
    from main import init_menu
    def goBackToMenu():
        win_over.destroy()
        game_win.destroy()
        init_menu()
    
    win_over = tk.Toplevel(game_win)
    win_over.geometry("200x100")
    win_over_label = tk.Label(win_over,text='失敗！',font=("",14))
    win_over_label.pack(pady=20) 
    over_button = tk.Button(win_over,text="返回",command=goBackToMenu,font=("",12))
    over_button.pack()
    win_over.transient(game_win) #讓附屬視窗浮在主視窗上
    win_over.grab_set()          #讓附屬視窗消失前無法點擊主視窗
    
def victory(game_win):
    from main import init_menu
    def goBackToMenu():
        win_victory.destroy()
        game_win.destroy()
        init_menu()
    
    win_victory = tk.Toplevel(game_win)
    win_victory.geometry("200x100")
    win_victory_label = tk.Label(win_victory,text='成功！',font=("",14))
    win_victory_label.pack(pady=20) 
    victory_button = tk.Button(win_victory,text="返回",command=goBackToMenu,font=("",12))
    victory_button.pack()
    win_victory.transient(game_win)
    win_victory.grab_set()
    

def start_game_ui(rows, cols, num_mines):
    # 建立全域防禦變數：記錄上一次人類「左鍵」與「右鍵」點擊的時間
    last_click_time = [0.0]
    #記錄需要多少旗子
    remaining_flags = [num_mines]
    #記錄是不是第一次按
    first_click = [True]
    board_container = [None]  #建立一個外送箱，用來永久裝地圖
    
    #建立一個叫button_grid的列表去填入空表示被蓋起來的地雷圖
    buttons_grid=[]
    for r in range(rows):
        row_list=[]
        for c in range(cols):
            row_list.append(None)
        buttons_grid.append(row_list)
        
        
    def left_click(event, r, c):
        # ---------------------------------------------------------
        # 寫在裡面：負責算數學的內層函式，直接共享外部變數
        # ---------------------------------------------------------
        def check_win():
            unopened_count = 0
            for r_idx in range(rows):
                for c_idx in range(cols):
                    if buttons_grid[r_idx][c_idx]["state"] == "normal":#normal就是沒有被disable的
                        unopened_count += 1                             #還有一種叫active是懸停或點擊中
            return unopened_count == num_mines
        
        # 1. 邊界防護罩
        if not (0 <= r < rows and 0 <= c < cols):
            return
            
        current_btn = buttons_grid[r][c]
        
        # 2. 左鍵Debounce檢查（只對人類手動點擊有效）
        if event is not None:
            current_time = time.time()
            if current_time - last_click_time[0] < 0.15:
                print("偵測到連點，已被Debounce攔截！")
                return
            last_click_time[0] = current_time 

        # 3. 旗子防護罩：有旗子的格子不能按左鍵
        if current_btn["text"] == "🚩":
            return
            
        nonlocal first_click
        if first_click[0]:
            #將產生的地圖塞入外送箱的 [0] 位置
            board_container[0] = generate_board(rows, cols, num_mines, r, c)
            first_click[0] = False
        # =============================================================
        # 大路 A：這格「已經翻開了」（Chording 雙擊解鎖鄰居）
        # =============================================================
        board = board_container[0]
        if current_btn["state"] == "disabled":
            # 只有當玩家「手動點擊」一個已經翻開的「數字格」時，才觸發解鎖
            # 雖然button被disable但它只能封鎖掉command，用bind還是可以作動
            if board[r][c] > 0 and event is not None:
                val = board[r][c]
                
                # 精準計算周圍 8 個鄰居共有幾支旗子
                flag_num = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if buttons_grid[nr][nc]["text"] == "🚩":
                                flag_num += 1
                                
                # 如果周圍旗子數剛好等於這格的數字，連鎖戳周圍鄰居
                if flag_num == val:
                    print(f"觸發雙擊解鎖！點擊了數字 {val} 的周圍")
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            left_click(None, r + dr, c + dc) # 遞迴傳 None 安全通過
            return # 已經翻開的格子處理完解鎖就必須 return，不能往下走！

        # =============================================================
        # 大路 B：這格「尚未翻開」（第一次翻開格子的原本邏輯）
        # =============================================================
        print(f"左鍵點擊了{r},{c}")
        if board[r][c] == -1:
            gameover(game_win)
            
        elif board[r][c] == 0:
            print('擴充到有數字')
            current_btn.config(text="", relief="flat", state="disabled", bg="#e6e6e6")
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue  
                    left_click(None, r + dr, c + dc) # 遞迴傳 None 安全通過
        
                            
        elif board[r][c] > 0:
            val = board[r][c]
            colors = {1: "blue", 2: "green", 3: "red", 4: "purple", 5: "maroon"}
            btn_color = colors.get(val, "black") 
            current_btn.config(
                text=str(val), 
                fg=btn_color,
                #disable會把顏色都變成灰的所以要設定，並還要先寫font
                disabledforeground=btn_color, 
                relief="flat", 
                state="disabled", 
                bg="#e6e6e6"
            )
        #呼叫判斷成功的function
        if check_win():
            victory(game_win)  # 條件成立，呼叫最外面的轉場積木！
            return
    
    def right_click(event,r,c):
        current_btn = buttons_grid[r][c]
        if current_btn["state"] == "disabled":
            return
        
        # 右鍵 Debounce 檢查
        if event is not None:
            current_time = time.time()
            # 如果距離上次點擊小於 0.15 秒（150毫秒），就直接當作沒看見
            if current_time - last_click_time[0] < 0.15:
                print("偵測到連點，已被Debounce攔截！")
                return
            last_click_time[0] = current_time # 更新最後點擊時間
            
        
        if current_btn["text"] == " ":
            current_btn.config(text="🚩",fg='red')
            update_flag(flag, remaining_flags, 'increase')
        elif current_btn["text"] == "🚩":
            current_btn.config(text=" ",fg="black")
            update_flag(flag, remaining_flags, 'decrease')
        
    
    # 1. 建立遊戲的主視窗
    game_win = tk.Tk()
    game_win.title(f"踩地雷 - 遊戲中 ({rows}x{cols})")
    
    info_frame = tk.Frame(game_win)
    info_frame.pack(side='top',fill='x',pady=5)
    game_frame = tk.Frame(game_win)
    game_frame.pack(side='bottom')
    
    use_time = tk.Label(info_frame,text='用時:0s')#text這裡會被上面的覆蓋掉所以寫不寫沒關係
    use_time.pack(side='left')
    update_time(game_win, use_time, 0)
    flag = tk.Label(info_frame,text="🚩:")
    flag.pack(side='right')
    update_flag(flag, remaining_flags)
    
    for r in range(rows):
        for c in range(cols):
            btn = tk.Button(game_frame, text=" ", width=5, height=2)
            btn.grid(row=r, column=c)
            buttons_grid[r][c] = btn
            btn.bind("<Button-1>", lambda event, row=r, col=c: left_click(event, row, col))
            btn.bind("<Button-3>", lambda event, row=r, col=c: right_click(event, row, col))
            # def lambda(event,row=r,col=c):
            #     left_click(event, r, c)
    
    game_win.mainloop()
