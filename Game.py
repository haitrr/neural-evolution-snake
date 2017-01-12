"""UI of the game"""

from tkinter import *
from Constants import *
from Block import *
from Point import Point
from random import randint
from Snake import *


def init_blocks():
    blocks = []
    for i in range(MAP_HEIGHT):
        temp = []
        for j in range(MAP_WIDTH):
            block = Block(Point(i * BLOCK_SIZE, j * BLOCK_SIZE))
            if randint(1, 10) > 9:
                block.type = BlockType.Wall
            temp.append(block)
        blocks.append(temp)
    return blocks


def create_food():
    pos = Point(randint(0, MAP_HEIGHT - 1), randint(0, MAP_WIDTH - 1))
    while map_blocks[pos.x][pos.y].type != BlockType.Normal:
        pos = Point(randint(0, MAP_HEIGHT - 1), randint(0, MAP_WIDTH - 1))
    map_blocks[pos.x][pos.y].type = BlockType.Food
    return map_blocks[pos.x][pos.y]


def create_snake():
    pos = Point(randint(0, MAP_HEIGHT - 1), randint(0, MAP_WIDTH - 1))
    while map_blocks[pos.x][pos.y].type != BlockType.Normal:
        pos = Point(randint(0, MAP_HEIGHT - 1), randint(0, MAP_WIDTH - 1))
    map_blocks[pos.x][pos.y].type = BlockType.Snake
    new_snake = Snake(map_blocks[pos.x][pos.y])


def draw_game():
    game_canvas.delete()
    for blocks in map_blocks:
        for block in blocks:
            if block.type == BlockType.Normal:
                pass
            elif block.type == BlockType.Food:
                game_canvas.create_rectangle(
                    (block.position.x, block.position.y), (block.position.x + BLOCK_SIZE, block.position.y + BLOCK_SIZE), fill='red', outline='black')
            elif block.type == BlockType.Wall:
                game_canvas.create_rectangle(
                    (block.position.x, block.position.y), (block.position.x + BLOCK_SIZE, block.position.y + BLOCK_SIZE), fill='blue', outline='black')
            else:
                game_canvas.create_rectangle(
                    (block.position.x, block.position.y), (block.position.x + BLOCK_SIZE, block.position.y + BLOCK_SIZE), fill='white', outline='black')
root = Tk()
root.resizable(width=False, height=False)
root.grid()


game_canvas = Canvas(root, width=MAP_WIDTH * BLOCK_SIZE,
                     height=MAP_HEIGHT * BLOCK_SIZE, background="black")
game_canvas.grid(row=0, column=0)

map_blocks = init_blocks()
food = create_food()
snake = create_snake()
draw_game()

root.title("Snake evolution")
root.mainloop()
