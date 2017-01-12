from enum import Enum


class Direction(Enum):
    Left = 0
    Up = 1
    Right = 2
    Down = 3
    Stop = -1


class Snake:

    def __init__(self, head):
        self.body = []
        self.body.append(head)
        self.direction = Direction.Stop
