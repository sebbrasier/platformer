import arcade
from typing import Final
from abc import ABC, abstractmethod
from enum import Enum, auto
from readmap import *
from collections.abc import Callable

Block_size_x : Final[int] = 64
Block_size_y : Final[int] = 64

platforms  = frozenset({map_symbols.Half_grass, map_symbols.Grass_tile, map_symbols.Box, map_symbols.Lava, map_symbols.Next_level, map_symbols.Inter, map_symbols.Break})
special_plat = frozenset({map_symbols.Lava, map_symbols.Next_level, map_symbols.Inter})

#Classe pour les opérations d'algèbre linéaire :
class LinAlgebra(ABC):
    #donne l'image miroir d'un vecteur
    @staticmethod
    def flip_vector(vec : tuple[int, int], map : Map) -> tuple[int, int]:
        width = map.dim[0]
        return (vec[0], width - (vec[1]+1))

    @staticmethod
    #transpose un vecteur : donne l'image transposée d'un vecteur
    def transpose_vec(vec : tuple[int, int], map : Map) -> tuple[int, int]:
        return (vec[1], vec[0])
    @staticmethod
    #transpose et reflète horizontalement
    def flip_transpose_vec(vec : tuple[int, int], map: Map) -> tuple[int, int]:
        return(LinAlgebra.transpose_vec(LinAlgebra.flip_vector(vec, map), map))

    @staticmethod
    #reflète horizontalement une matrice
    def flip_matrix(map : Map) -> Map:
        width = map.dim[0]

        new_matrix = [[map.setup[i][width - (j+1)] for j in range(len(map.setup[i]))] for i in range(len(map.setup))]
        return Map(map.dim, new_matrix)

    @staticmethod
   #transpose une matrice
    def transpose_matrix(map : Map) -> Map:
        new_matrix= [[map.setup[j][i] for j in range(map.dim[1])] for i in range(map.dim[0])]

        return Map((map.dim[1], map.dim[0]), new_matrix)


#Classe abstraite pour lire et ajouter des plateformes
class AddPlatform(ABC):

    @staticmethod
    #Fonction qui détecte un "bloc" ou une plateforme entière et les ajoute tous dans le même ensemble
    def read_platform( map : Map, point : tuple[int, int], Rearrange : Callable[[tuple[int, int], Map], tuple[int, int]], point_set : set[tuple[int, int]]) -> None:
        """Rajoute tous les blocs qui vont constituer une platforme dans le même set"""
        i, j =point
        matrix = map.setup
        width = map.dim[0]
        height = map.dim[1]
        point_set.add(Rearrange(point, map))
        #Fonction récursive qui détecte si les blocs voisins font partie de la plateforme et les ajoute dans l'ensemble
        #Cette fonction s'arrête selon les conditions sur i et j
        if i+1 < height:
            if Rearrange((i+1, j), map) not in point_set and matrix[i+1][j] in platforms:
                AddPlatform.read_platform(map, (i+1, j), Rearrange, point_set)
        if i-1 >= 0:
            if Rearrange((i-1, j), map) not in point_set and matrix[i-1][j] in platforms:
                AddPlatform.read_platform(map, (i-1, j), Rearrange, point_set)
        if j+1 < width:
                if Rearrange((i, j+1),map) not in point_set and matrix[i][j+1] in platforms:
                    AddPlatform.read_platform(map, (i, j+1), Rearrange, point_set)
        if j-1 >= 0:
            if Rearrange((i, j-1),map) not in point_set and matrix[i][j-1] in platforms:
                AddPlatform.read_platform(map, (i, j-1), Rearrange, point_set)


    #fonction qui retourne les séquences de flèches dans la carte, ainsi que la position du bloc à leur gauche
    #pour que cette fonction détecte toute sorte de chaîne de flèches, on devra transposer et/ou refléter la carte
    @staticmethod
    def read_arrows_right( map: Map, symbol : map_symbols, Rearrange : Callable[[tuple[int, int], Map], tuple[int,int]]) -> dict[frozenset[tuple[int, int]], tuple[map_symbols, ...]]:
        """lit le fichier pour voir si il y a une flèche à droite d'un bloc, elle appelle ensuite read_platforme pour rajouter le platforme toute entière"""
        table = map.setup
        width = map.dim[0]
        stockage: dict[frozenset[tuple[int, int]], tuple[map_symbols, ...]] = {}

        for i in range(len(table)):
            j = 0
            #détecte si une chaîne de flèches est à droite d’un bloc
            while j+1 < len(table[i]):
                if table[i][j+1] == symbol and table[i][j] in platforms:
                    arrow_list: list[map_symbols] = [symbol]
                    h = j+1
                    while h + 1 < width and table[i][h + 1] == symbol:
                        h += 1
                        arrow_list.append(symbol)
                    point_set : set[tuple[int, int]] = set()
                    AddPlatform.read_platform(map, (i, j), Rearrange, point_set)
                    frozen_point = frozenset(point_set)
                    #Erreur si plusieurs chaînes de flèches dans le même sens affectent la plateforme
                    if frozen_point in stockage:
                        raise ValueError("Erreur : une platforme est affectée par plusieurs séries de flèches qui vont dans le même sens")
                    stockage[frozen_point] = tuple(arrow_list)
                    j = h 
                else:
                    j += 1  
        return stockage
    
     #Fonction qui combine deux plateformes en une si elles sont affectées par une séquence de flèches gauche et droite
    #cela garantit qu'une plateforme ne peut pas être affectée par un mouvement horizontal et vertical à la fois
    @staticmethod
    def combine_right_left(left : dict[frozenset[tuple[int, int]], tuple[map_symbols, ...]], 
                        right : dict[frozenset[tuple[int, int]], tuple[map_symbols, ...]], map: Map
                        ) -> dict[frozenset[tuple[int, int]], tuple[tuple[map_symbols, ...], tuple[map_symbols, ...]]]:
        
        """Vérifie si la m6eme platforme est affectée par deux séries de flèches et les combine ensemble"""
        
        left_set = {a for a in left}
        right_set = {a for a in right}
        final : dict[frozenset[tuple[int, int]], tuple[tuple[map_symbols, ...], tuple[map_symbols, ...]]] = {}
        empty : tuple[map_symbols, ...] = ()
        intersection = left_set & right_set
        for a in intersection:
            final[a] = (left[a], right[a])
        
        for a in left_set:
            if a not in final:
                final[a] = (left[a], empty)
                
        for b in right_set:
            if b not in final:
                final[b] = (empty, right[b])
        return final

    #Fonction qui lève une erreur si des flèches horizontales et verticales affectent la même plateforme
    @staticmethod
    def duplicate_checker(horizontal : dict[frozenset[tuple[int, int]], tuple[tuple[map_symbols, ...], tuple[map_symbols, ...]]],
                        vertical : dict[frozenset[tuple[int, int]], tuple[tuple[map_symbols, ...], tuple[map_symbols, ...]]]) -> None:
        for e in horizontal:
            if e in vertical:
                raise ValueError("Erreur : Une platforme est affectée par un mouvement horizontal et vertical")


#Classe pour les plateformes mobiles
class moving_platform:
    platform : Final[arcade.Sprite]
    speed : float
    arrow_sequence1 : Final[tuple[map_symbols, ...]]
    arrow_sequence2 : Final[tuple[map_symbols, ...]]
    boundary_right : float
    boundary_left : float
    is_dropped : bool 
    ref_y: float
    timer : float
    start_timer : bool
    can_go_up : bool

    def __init__(self, platform : arcade.Sprite, speed : float, arrow_sequence1 : tuple[map_symbols, ...], arrow_sequence2 : tuple[map_symbols, ...]) -> None:
        self.platform = platform
        self.arrow_sequence1 = arrow_sequence1
        self.arrow_sequence2 = arrow_sequence2
        self.speed = speed
        self.is_dropped = False
        self.ref_y = self.platform.center_y
        self.timer = 0.0
        self.start_timer = False
        self.can_go_up = False
        

    @abstractmethod
    def calculate_boundary_right(self, block_size : int) -> float:
        ...
    
    @abstractmethod
    def calculate_boundary_left(self, block_size : int) -> float:
        ...
    
    @abstractmethod
    def move(self) -> None:
        ...

   #Méthode pour faire tomber les plateformes lorsque le joueur est dessus
    def drop(self) -> None:
        pass

    def go_up(self) -> None:
        pass
    
    #Méthode qui détecte si une plateforme est sous le joueur
    def is_under(self, player : arcade.Sprite) -> bool:
        #Crée un point sous le joueur
        point_y = player.bottom - 12
        point_x = player.center_x

        if self.platform.left <= point_x and point_x <= self.platform.right and self.platform.bottom <= point_y and point_y <= self.platform.top:
            return True
        return False
    
    

#Classe pour les plateformes qui se déplacent horizontalement
class moving_platform_x(moving_platform):

    grid_x : float
    def __init__(self, platform : arcade.Sprite, speed : float, arrow_sequence1 : tuple[map_symbols, ...], arrow_sequence2 : tuple[map_symbols, ...]) -> None:
        super().__init__(platform, speed, arrow_sequence1, arrow_sequence2)
        self.grid_x = self.platform.center_x
        self.boundary_right = self.calculate_boundary_right(Block_size_x)
        self.boundary_left = self.calculate_boundary_left(Block_size_x)

    def calculate_boundary_right(self, block_size : int) -> float:
        return (self.platform.right ) + len(self.arrow_sequence1) * block_size
    
    def calculate_boundary_left(self, block_size : int) -> float:
        return (self.platform.left ) - len(self.arrow_sequence2) * block_size
    
    def move(self) -> None:
        
        if self.platform.right >= self.boundary_right and self.platform.change_x > 0 :
            self.platform.change_x *= -1
        if self.platform.left <= self.boundary_left and self.platform.change_x < 0 :
            self.platform.change_x *= -1
    
    #Méthode pour faire tomber les plateformes lorsque le joueur est dessus
    #Nous ne définissons cela que pour les plateformes horizontales
    def drop(self) -> None:
        if self.can_go_up is False:
            if self.is_dropped is True:
                self.platform.center_y -= 10
            if self.platform.center_y <= -1200:
                self.can_go_up = True
                self.is_dropped = False
    
    def go_up(self) -> None:
        if self.can_go_up is True:
            self.platform.center_y += 10
            if self.platform.center_y >= self.ref_y:
                self.platform.center_y = self.ref_y
                self.can_go_up = False

#Classe pour les plateformes qui se déplacent verticalement
class moving_platform_y(moving_platform):
    grid_y : float

    def __init__(self, platform : arcade.Sprite, speed : float, arrow_sequence1 : tuple[map_symbols, ...], arrow_sequence2 : tuple[map_symbols, ...]) -> None:
        super().__init__(platform, speed, arrow_sequence1, arrow_sequence2)
        self.grid_y = self.platform.center_y
            
        self.grid_y = self.platform.center_y
        self.boundary_right = self.calculate_boundary_right(Block_size_x)
        
        self.boundary_left = self.calculate_boundary_left(Block_size_x)

    def calculate_boundary_right(self, block_size : int) -> float:
        return (self.platform.top) + len(self.arrow_sequence1) * block_size
    
    def calculate_boundary_left(self, block_size : int) -> float:
        return (self.platform.bottom) - len(self.arrow_sequence2) * block_size
    
    def move(self) -> None:
        
        if self.platform.top >= self.boundary_right and self.platform.change_y > 0 :
            self.platform.change_y *= -1
        if self.platform.bottom <= self.boundary_left and self.platform.change_y < 0 :
            self.platform.change_y *= -1

        
