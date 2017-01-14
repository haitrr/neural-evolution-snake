from enum import Enum
from Block import *
from Constants import *
from NeuralNetwork import *
import numpy as np


class Snake:
    def __init__(self, game_map, head, code, gen):
        self.game_map = game_map
        head.type = BlockType.Snake
        head.owners.append(code)
        self.body = []
        self.body.append(head)
        self.direction = RIGHT
        self.dead = False
        self.code = code
        self.gen = gen
        self.fitness = 0
        self.life_time = 0

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
                input_vector.append(self.game_map[i][j].type.value)
        return np.reshape(input_vector, (GEN_SIZE[0], 1))

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

    def get_turn(self):
        input_vector = self.get_input()
        output = self.gen.feed_forward(input_vector)
        self.turn(output.argmax())

    def move(self):
        if self.dead:
            return

        self.get_turn()
        head = self.body[0]
        to_pos = [
            int(head.position.x / BLOCK_SIZE),
            int(head.position.y / BLOCK_SIZE)
        ]
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
        self.life_time += 1
        if to.type == BlockType.Normal:
            to.type = BlockType.Snake
            to.owners.append(self.code)
            self.body = [to] + self.body
            self.body[-1].remove_owner(self.code)
            self.body.pop()
        elif to.type == BlockType.Wall:
            self.die()
        elif to.type == BlockType.Food:
            to.type = BlockType.Snake
            to.owners.append(self.code)
            self.body.insert(0, to)
        elif self.code in to.owners:
            self.die()
        else:
            to.owners.append(self.code)
            self.body = [to] + self.body
            self.body[-1].remove_owner(self.code)
            self.body.pop()

    def die(self):
        self.fitness = len(self.body) + self.life_time / LIFE_TIME
        for block in self.body:
            block.remove_owner(self.code)
        self.body.clear()
        self.direction = STOP
        self.dead = True
