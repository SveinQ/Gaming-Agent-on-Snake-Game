import os, random, time

WIDTH, HEIGHT = 12,12
snake = [(6,6)]
direction = "RIGHT"
last_direction = "RIGHT"

def generate_food():
    while True:
        f = (random.randint(0,WIDTH-1), random.randint(0,HEIGHT-1))
        if f not in snake:
            return f

food = generate_food()

def draw_board():
    lines=[]
    for y in range(HEIGHT):
        row=""
        for x in range(WIDTH):
            if (x,y)==snake[0]:
                row+="S "
            elif (x,y) in snake:
                row+="s "
            elif (x,y)==food:
                row+="F "
            else:
                row+=". "
        lines.append(row)
    os.system("cls" if os.name=="nt" else "clear")
    for r in lines: print(r)
    print("\nLegend: S = Head, s = Body, F = Food")
    with open("board.txt","w") as f:
        f.write("\n".join(lines))

def get_input():
    global direction, last_direction
    try:
        move = open("move.txt").read().strip().upper()
        if move in ("UP", "DOWN", "LEFT", "RIGHT"):
            # Prevent 180° reversal
            if (
                (last_direction == "UP" and move == "DOWN") or
                (last_direction == "DOWN" and move == "UP") or
                (last_direction == "LEFT" and move == "RIGHT") or
                (last_direction == "RIGHT" and move == "LEFT")
            ):
                pass  # Ignore the move, keep current direction
            else:
                direction = move
    except FileNotFoundError:
        pass

def move_snake():
    global food, last_direction
    x, y = snake[0]
    
    if direction == "UP": y -= 1
    elif direction == "DOWN": y += 1
    elif direction == "LEFT": x -= 1
    elif direction == "RIGHT": x += 1

    x %= WIDTH
    y %= HEIGHT
    new_head = (x, y)

    if new_head in snake:
        print("Game Over!")
        exit()

    snake.insert(0, new_head)

    if new_head == food:
        food = generate_food()
    else:
        snake.pop()

    # Records the last direction the snake made
    last_direction = direction


def main():
    for _ in range(200):
        draw_board()
        get_input()
        move_snake()
        time.sleep(0.6)

if __name__=="__main__":
    main()
