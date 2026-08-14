import random

def generate_board(rows, cols, num_mines, click_row=1, click_col=1):
    # 1. 先建立一個全都是 0 的乾淨地圖 (二維陣列)
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    # board=[]
    # for r in range(0,rows):
    #     rowlist=[]
    #     for _ in range(cols):
    #         rowlist.append(0)
    #     board.append(rowlist)
    
    # 2. 隨機埋雷（地雷為-1，空格為0）
    mines_planted = 0
    while mines_planted < num_mines:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        
        if r==click_row and c==click_col:
            continue
        # 如果這格還不是雷，就把雷埋下去
        if board[r][c] != -1:
            board[r][c] = -1
            mines_planted += 1
            
            # 3.通知這顆雷周圍的8個鄰居，叫他們的數字全部+1
            # 鄰居的相對座標範圍是-1到1
            #d=difference or delta 表差距、位移量
            #n=next or neighbor 表下一個、鄰居
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    # 確保鄰居的座標沒有超出地圖邊界，而且鄰居自己不是雷
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != -1:
                        board[nr][nc] += 1
                        
    return board

# ==========================================
# 測試邏輯運作是否正常
# ==========================================
#__name__ == __main__是用來被import的話不執行，等同於testbench
if __name__ == "__main__":
    # 產生一個9x9，裡面有10顆雷的測試地圖
    test_board = generate_board(9, 9, 10)
    # 外層迴圈：先把test_board拆解成一列一列的row
    for row in test_board:
        # 每處理新的一列，就要準備一個乾淨的空清單放這一列的文字
        new_row_string = []
        # 內層迴圈：這時候才能對row進行一格一格的 cell 拆解！
        for cell in row:
            if cell == -1:
                new_row_string.append('*')
            else:
                new_row_string.append(str(cell))
        #當這一列的 9 個格子都加工完成了，用空格黏起來並「換行印出」
        print(" ".join(new_row_string))
