from enum import Enum
from Block import *
from Constants import *
from NeuralNetwork import *
import numpy as np


class Snake:
    def __init__(self, game_map, head, code):
        self.game_map = game_map
        head.type = code
        self.body = []
        self.body.append(head)
        self.direction = RIGHT
        self.dead = False
        self.code = code
        self.gen = NeuralNetwork(GEN_SIZE)

    def get_input(self):
        head = self.body[0]
        input_vector = []
        for i in range(
                int(head.position.x / BLOCK_SIZE) - INPUT_SIZE,
                int(head.position.x / BLOCK_SIZE) + INPUT_SIZE):
            if i >= MAP_HEIGHT:
                i = i - MAP_HEIGHT
            if i < 0:
                i = i + MAP_HEIGHT
            for j in range(
                    int(head.position.y / BLOCK_SIZE) - INPUT_SIZE,
                    int(head.position.y / BLOCK_SIZE) + INPUT_SIZE):
                if j >= MAP_WIDTH:
                    j = j - MAP_WIDTH
                if j < 0:
                    j = j + MAP_WIDTH
                if self.game_map[i][j].type is BlockType:
                    input_vector.append(self.game_map[i][j].type.value)
                elif self.game_map[i][j].type == self.code:
                    input_vector.append(0)
                else:
                    input_vector.append(BlockType.Normal.value)
        return np.reshape(input_vector, (INPUT_SIZE * INPUT_SIZE * 4, 1))

    def turn(self, x):
        """
        Turn the snake direction
        x values:
        0: turn left
        1: go straight
        2: turn right
        """
        if x == 1:
            pass
        elif x == 0:
            if self.direction == UP:
                self.direction = LEFT
            elif self.direction == LEFT:
                self.direction = DOWN
            elif self.direction == DOWN:
                self.direction = RIGHT
            elif self.direction == RIGHT:
                self.direction = UP
            else:
                print("ERROR")
        elif x == 2:
            if self.direction == UP:
                self.direction = RIGHT
            elif self.direction == LEFT:
                self.direction = UP
            elif self.direction == DOWN:
                self.direction = LEFT
            elif self.direction == RIGHT:
                self.direction = DOWN
            else:
                print("ERROR")
        else:
            print("ERROR")

    def move(self):
        input_vector = self.get_input()
        output = self.gen.feed_forward(input_vector)
        self.turn(output.argmax())
        head = self.body[0]
        to_pos = [int(head.position.x / BLOCK_SIZE), int(head.position.y / BLOCK_SIZE)]
        to_pos[0] = to_pos[0] + self.direction[0]
        if to_pos[0] >= MAP_HEIGHT:
            to_pos[0] = to_pos[0] - MAP_HEIGHT
        if to_pos[0] < 0:
            to_pos[0] = to_pos[0] + MAP_HEIGHT
        to_pos[1] = to_pos[1] + self.direction[1]
        if to_pos[1] >= MAP_WIDTH:
            to_pos[1] = to_pos[1] - MAP_WIDTH
        if to_pos[1] < 0:
            to_pos[1] = to_pos[1] + MAP_WIDTH
        to = self.game_map[to_pos[0]][to_pos[1]]
        if to.type == BlockType.Normal:
            to.type = self.code
            self.body = [to] + self.body
            self.body[-1].type = BlockType.Normal
            self.body.pop()
        elif to.type == BlockType.Wall:
            self.die()
        elif to.type == BlockType.Food:
            to.type = self.code
            self.body.append(0, to)
        elif to.type == self.code:
            self.die()
        else:
            pass

    def die(self):
        for block in self.body:
            block.type = BlockType.Normal
            self.direction = STOP
            self.body.clear()
            self.dead = True
