import random
import tkinter as tk

# 게임 화면 크기 설정
WIDTH = 20
HEIGHT = 10
CELL_SIZE = 30  # 각 셀 크기 (픽셀)

# 플레이어 초기 위치
player_x = WIDTH // 2
bullets = []
enemies = []
score = 0

# Tkinter 윈도우 생성
root = tk.Tk()
root.title("Shooting Game")
canvas = tk.Canvas(root, width=WIDTH * CELL_SIZE, height=HEIGHT * CELL_SIZE, bg="black")
canvas.pack()
score_label = tk.Label(root, text=f"Score: {score}", font=("Arial", 14), fg="white", bg="black")
score_label.pack()

# 게임 화면 업데이트 함수
def draw_screen():
    canvas.delete("all")
    
    # 적 그리기
    for ex, ey in enemies:
        canvas.create_rectangle(ex * CELL_SIZE, ey * CELL_SIZE, (ex + 1) * CELL_SIZE, (ey + 1) * CELL_SIZE, fill="red")
    
    # 총알 그리기
    for bx, by in bullets:
        canvas.create_rectangle(bx * CELL_SIZE + 10, by * CELL_SIZE, bx * CELL_SIZE + 20, (by + 1) * CELL_SIZE, fill="yellow")
    
    # 플레이어 그리기
    canvas.create_rectangle(player_x * CELL_SIZE, (HEIGHT - 1) * CELL_SIZE, (player_x + 1) * CELL_SIZE, HEIGHT * CELL_SIZE, fill="green")
    
    score_label.config(text=f"Score: {score}")
    root.update()

# 키 입력 처리 함수
def key_press(event):
    global player_x, bullets
    if event.keysym == "Left" and player_x > 0:
        player_x -= 1
    elif event.keysym == "Right" and player_x < WIDTH - 1:
        player_x += 1
    elif event.keysym == "space":
        bullets.append([player_x, HEIGHT - 2])

def update_game():
    global bullets, enemies, score
    
    # 총알 이동
    bullets = [[bx, by - 1] for bx, by in bullets if by > 0]
    
    # 적 이동 및 생성
    if random.randint(1, 3) == 1:
        enemies.append([random.randint(0, WIDTH - 1), 0])
    enemies = [[ex, ey + 1] for ex, ey in enemies if ey < HEIGHT - 1]
    
    # 충돌 감지
    global score
    new_bullets = []
    new_enemies = []
    for ex, ey in enemies:
        hit = False
        for bx, by in bullets:
            if bx == ex and by == ey:
                hit = True
                score += 1
        if not hit:
            new_enemies.append([ex, ey])
    
    bullets = new_bullets
    enemies = new_enemies
    draw_screen()
    root.after(300, update_game)

# 키 입력 바인딩
root.bind("<KeyPress>", key_press)

# 게임 시작
update_game()
root.mainloop()