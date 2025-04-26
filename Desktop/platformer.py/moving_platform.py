import arcade
from typing import Final
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Final
from readmap import *

Block_size_x : Final[int] = 32
Block_size_y : Final[int] = 64

#Write a function that returns the sequences of arrows in the map, along with the position of the grass block they are left to
#for this function to detect any type of arrow chain, we will need to transpose and/or flip the maps
def read_arrows_right(map: Map, symbol : map_symbols) -> dict[tuple[int, int], tuple[map_symbols, ...]]:
    table = map.setup
    width = map.dim[0]
    stockage: dict[tuple[int, int], tuple[map_symbols, ...]] = {}

    for i in range(len(table)):
        j = 0
        #detects if a chain of arrows is right to a block
        while j+1 < len(table[i]):
            if table[i][j+1] == symbol:
                arrow_list: list[map_symbols] = [symbol]
                h = j+1
                while h + 1 < width and table[i][h + 1] == symbol:
                    h += 1
                    arrow_list.append(symbol)
                stockage[(i, j)] = tuple(arrow_list)
                j = h + 1  
            else:
                j += 1  
    return stockage

#mirror flips a matrix 
def flip_matrix(map : Map) -> Map:
    width = map.dim[0]

    new_matrix = [[map.setup[i][width - (j+1)] for j in range(len(map.setup[i]))] for i in range(len(map.setup))]
    return Map(map.dim, new_matrix)

#Transposes a matrix
def transpose_matrix(map : Map) -> Map:
    new_matrix= [[map.setup[j][i] for j in range(map.dim[1])] for i in range(map.dim[0])]

    return Map((map.dim[1], map.dim[0]), new_matrix)

#Class for moving platforms
class moving_platform:
    platform : Final[arcade.Sprite]
    grid_x : float
    grid_y : float
    speed : int
    arrow_sequence : Final[tuple[map_symbols, ...]]

    def __init__(self, platform : arcade.Sprite, speed : int, arrow_sequence : tuple[map_symbols, ...]) -> None:
        self.platform = platform
        self.grid_x = self.platform.center_x
        self.grid_y = self.platform.center_y
        self.arrow_sequence = arrow_sequence
        self.speed = speed
    
    @abstractmethod
    def calculate_boundary(self, block_size : int) -> float:
        ...
    
    @abstractmethod
    def move(self) -> None:
        ...

#We seperate platforms that move up and down or left and right
#Child class for platforms that move left and right
class moving_platform_x(moving_platform):
    #This value is based on how many arrows there are in the chain 
    boundary_x : float

    def __init__(self, platform : arcade.Sprite, speed : int, arrow_sequence : tuple[map_symbols, ...]) -> None:
        super().__init__(platform, speed, arrow_sequence)
        self.boundary_x = self.calculate_boundary(Block_size_x)

    def calculate_boundary(self, block_size : int) -> float:
        return self.grid_x + (self.speed/abs(self.speed)) * len(self.arrow_sequence) * block_size
        
    def move(self) -> None:
        self.platform.center_x += self.speed
        if self.platform.center_x == self.grid_x or self.platform.center_x == self.boundary_x:
            self.speed *= -1

#Child class for platforms that move up and down
class moving_platform_y(moving_platform):
    boundary_y : float

    def __init__(self, platform : arcade.Sprite, speed : int, arrow_sequence : tuple[map_symbols, ...]) -> None:
        super().__init__(platform, speed, arrow_sequence)
        self.boundary_y = self.calculate_boundary(Block_size_y)

    def calculate_boundary(self, block_size : int) -> float:
        return self.grid_y + (self.speed/abs(self.speed)) * len(self.arrow_sequence) * block_size
        
    def move(self) -> None:
        self.platform.center_y += self.speed
        if self.platform.center_y == self.grid_y or self.platform.center_y == self.boundary_y:
            self.speed *= -1
