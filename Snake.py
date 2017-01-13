from enum import Enum
from Block import *
from Constants import *


class Direction(Enum):
    Left = (-1, 0)
    Up = (0, 1)
    Right = (1, 0)
    Down = (0, -1)
    Stop = (0, 0)


class Snake:
    def __init__(self, game_map, head):
        self.game_map = game_map
        self.body = []
        self.body.append(head)
        self.direction = Direction.Down
        self.dead = False

    def move(self):
        if self.direction == Direction.Stop:
            return
        head = self.body[0]
        to = self.game_map[int(
            head.position.x / BLOCK_SIZE) + self.direction.value[0]][int(
                head.position.y / BLOCK_SIZE) + self.direction.value[1]]
        if to.type == BlockType.Normal:
            to.type = BlockType.Snake
            self.body = [to]+self.body
            self.body[-1].type = BlockType.Normal
            self.body.pop()
        elif to.type == BlockType.Wall:
            self.die()
        elif to.type == BlockType.Food:
            to.type = BlockType.Snake
            self.body.append(0, to)
        else:
            self.die()

    def die(self):
        for block in self.body:
            block.type = BlockType.Normal
            self.direction = Direction.Stop
            self.body.clear()
            self.dead = True
