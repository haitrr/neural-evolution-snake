from enum import Enum


class BlockType(Enum):
    Normal = 5
    Food = 10
    Wall = 0
    Snake = 2

class Block:
    def __init__(self, position):
        self.position = position
        self.type = BlockType.Normal
        self.owners = []
    
    def remove_owner(self,code):
        self.owners.remove(code)
        if self.owners == []:
            self.type=BlockType.Normal
