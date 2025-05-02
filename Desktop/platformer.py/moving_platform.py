import arcade
from typing import Final
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Final
from readmap import *
from collections.abc import Callable

Block_size_x : Final[int] = 64
Block_size_y : Final[int] = 64

platforms : frozenset[map_symbols] = frozenset({map_symbols.Half_grass, map_symbols.Grass_tile, map_symbols.Box})

#Function that returns a set of all the points in a platforms
def read_platform(map : Map, point : tuple[int, int], Rearrange : Callable[[tuple[int, int], Map], tuple[int, int]], point_set : set[tuple[int, int]]) -> None:
    i = point[0]
    j = point[1]
    matrix = map.setup
    width = map.dim[0]
    height = map.dim[1]
    point_set.add(Rearrange(point, map))
    if i-1 >= 0 and i+1 < height and j-1 >=0 and j+1 < width:
        #Recursive function that detects if all nieghboring blocks are part of the block and adds them to the platform set if they are
        if Rearrange((i+1, j), map) not in point_set and matrix[i+1][j] in platforms:
            point_set.add(Rearrange((i+1, j), map))
            read_platform(map, (i+1, j), Rearrange, point_set)
        if Rearrange((i-1, j), map) not in point_set and matrix[i-1][j] in platforms:
            point_set.add(Rearrange((i-1, j), map))
            read_platform(map, (i-1, j), Rearrange, point_set)
        if Rearrange((i, j+1),map) not in point_set and matrix[i][j+1] in platforms:
            point_set.add(Rearrange((i, j+1), map))
            read_platform(map, (i, j+1), Rearrange, point_set)
        if Rearrange((i, j-1),map) not in point_set and matrix[i][j-1] in platforms:
            point_set.add(Rearrange((i, j-1), map))
            read_platform(map, (i, j-1), Rearrange, point_set)


#Write a function that returns the sequences of arrows in the map, along with the position of the grass block they are left to
#for this function to detect any type of arrow chain, we will need to transpose and/or flip the maps
def read_arrows_right(map: Map, symbol : map_symbols, Rearrange : Callable[[tuple[int, int], Map], tuple[int,int]]) -> dict[frozenset[tuple[int, int]], tuple[map_symbols, ...]]:
    table = map.setup
    width = map.dim[0]
    stockage: dict[frozenset[tuple[int, int]], tuple[map_symbols, ...]] = {}

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
                point_set : set[tuple[int, int]] = set()
                read_platform(map, (i, j), Rearrange, point_set)
                frozen_point = frozenset(point_set)
                stockage[frozen_point] = tuple(arrow_list)
                j = h + 1  
            else:
                j += 1  
    return stockage

#gives the mirror image of a vector
def flip_vector(vec : tuple[int, int], map : Map) -> tuple[int, int]:
    width = map.dim[0]
    return (vec[0], width - (vec[1]+1))

#transpose vector : gives the transposed image of a vector
def transpose_vec(vec : tuple[int, int], map : Map) -> tuple[int, int]:
    return (vec[1], vec[0])

#transposes and flips:
def flip_transpose_vec(vec : tuple[int, int], map: Map) -> tuple[int, int]:
    return(transpose_vec(flip_vector(vec, map), map))

#Function that combines two platforms into one if both a left and right sequence of arrows touch the platforms
def combine_right_left(left : dict[frozenset[tuple[int, int]], tuple[map_symbols, ...]], 
                       right : dict[frozenset[tuple[int, int]], tuple[map_symbols, ...]], map: Map
                       ) -> dict[frozenset[tuple[int, int]], tuple[tuple[map_symbols, ...], tuple[map_symbols, ...]]]:
    
    left_set = {a for a in left}
    right_set = {a for a in right}
    final : dict[frozenset[tuple[int, int]], tuple[tuple[map_symbols, ...], tuple[map_symbols, ...]]] = {}
    empty : tuple[map_symbols, ...] = ()
    for a in left_set:
        for b in right_set:
            if a == b:
                final[b] = (left[a], right[b])
    
    for a in left_set:
        if a not in final:
            final[a] = (left[a], empty)
            
    for b in right_set:
        if b not in final:
            final[b] = (empty, right[b])
    return final

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
    speed : float
    arrow_sequence1 : Final[tuple[map_symbols, ...]]
    arrow_sequence2 : Final[tuple[map_symbols, ...]]
    boundary_right : float
    boundary_left : float

    def __init__(self, platform : arcade.Sprite, speed : float, arrow_sequence1 : tuple[map_symbols, ...], arrow_sequence2 : tuple[map_symbols, ...]) -> None:
        self.platform = platform
        self.arrow_sequence1 = arrow_sequence1
        self.arrow_sequence2 = arrow_sequence2
        self.speed = speed
        

    @abstractmethod
    def calculate_boundary_right(self, block_size : int) -> float:
        ...
    
    @abstractmethod
    def calculate_boundary_left(self, block_size : int) -> float:
        ...

#Class for platforms that move horizontally
class moving_platform_x(moving_platform):

    grid_x : float
    def __init__(self, platform : arcade.Sprite, speed : float, arrow_sequence1 : tuple[map_symbols, ...], arrow_sequence2 : tuple[map_symbols, ...]) -> None:
        super().__init__(platform, speed, arrow_sequence1, arrow_sequence2)
        self.grid_x = self.platform.center_x
        self.boundary_right = self.calculate_boundary_right(Block_size_x)
        self.boundary_left = self.calculate_boundary_left(Block_size_x)

    def calculate_boundary_right(self, block_size : int) -> float:
        return (self.grid_x + block_size/2) + len(self.arrow_sequence1) * block_size
    
    def calculate_boundary_left(self, block_size : int) -> float:
        return (self.grid_x - block_size/2) - len(self.arrow_sequence2) * block_size

#Class for platforms that move vertically
class moving_platform_y(moving_platform):
    grid_y : float

    def __init__(self, platform : arcade.Sprite, speed : float, arrow_sequence1 : tuple[map_symbols, ...], arrow_sequence2 : tuple[map_symbols, ...]) -> None:
        super().__init__(platform, speed, arrow_sequence1, arrow_sequence2)
        self.grid_y = self.platform.center_y
            
        self.grid_y = self.platform.center_y
        self.boundary_right = self.calculate_boundary_right(Block_size_x)
        
        self.boundary_left = self.calculate_boundary_left(Block_size_x)

    def calculate_boundary_right(self, block_size : int) -> float:
        return (self.grid_y + block_size/2) + len(self.arrow_sequence1) * block_size
    
    def calculate_boundary_left(self, block_size : int) -> float:
        return (self.grid_y - block_size/2) - len(self.arrow_sequence2) * block_size
    
