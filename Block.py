from enum import Enum


class BlockType(Enum):
    Normal = -1
    Food = -2
    Wall = -3


class Block:
    def __init__(self, position):
        self.position = position
        self.type = BlockType.Normal

    def draw(self, turtle):
        pass
