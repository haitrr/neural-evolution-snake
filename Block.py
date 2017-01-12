from enum import Enum


class BlockType(Enum):
    Normal = 0
    Food = -1
    Wall = -2
    Snake = 1


class Block:
    def __init__(self, position):
        self.position = position
        self.type = BlockType.Normal

    def draw(self, turtle):
        pass
