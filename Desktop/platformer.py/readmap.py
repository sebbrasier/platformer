import arcade
from typing import Final
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Final

#Faire un enum pour stocker les éléments de la map
class map_symbols(Enum):
    Space = auto()
    Grass_tile = auto()
    Half_grass = auto()
    Box = auto()
    Coin = auto()
    Blob = auto()
    Chauve_souris = auto()
    Lava = auto()
    Player = auto()
    Next_level = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()

#Fonction qui convertit des char en enum
def char_to_map(char : str) -> map_symbols:
    if  char == " ":
        return map_symbols.Space
    if char == "=":
        return map_symbols.Grass_tile
    if char == "-":
        return map_symbols.Half_grass
    if char == "x":
        return map_symbols.Box
    if char == "*":
        return map_symbols.Coin
    if char == "o":
        return map_symbols.Blob
    if char == "v":
        return map_symbols.Chauve_souris
    if char == "£":
        return map_symbols.Lava
    if char == "S":
        return map_symbols.Player
    if char == "E":
        return map_symbols.Next_level
    if char == "→":
        return map_symbols.RIGHT
    if char == "←":
        return map_symbols.LEFT
    if char == "↓":
        return map_symbols.DOWN
    if char == "↑":
        return map_symbols.UP
    else:
        print(char)
        raise Exception("Erreur: caractere inconnu")
        

#fonction qui convertit les charactères de la map en un type de bloc et son asset:
def enum_to_sprite(char: map_symbols) -> tuple[str, str]:
    if char == map_symbols.Space or char == map_symbols.RIGHT or char == map_symbols.LEFT or char == map_symbols.DOWN or char == map_symbols.UP:
        return (" ", " ")
    if char == map_symbols.Grass_tile:
        return ("Wall", ":resources:/images/tiles/grassMid.png")
    if char == map_symbols.Half_grass:
        return ("Wall", ":resources:/images/tiles/grassHalf_mid.png")
    if char == map_symbols.Box:
        return ("Wall", ":resources:/images/tiles/boxCrate_double.png")
    if char == map_symbols.Coin:
        return ("Coin", ":resources:/images/items/coinGold.png")
    if char == map_symbols.Blob:
        return ("Blob", ":resources:/images/enemies/slimePurple.png")
    if char == map_symbols.Chauve_souris:
        return ("Chauve-souris", "assets/kenney-extended-enemies-png/bat.png")
    if char == map_symbols.Lava:
        return ("No-go", ":resources:/images/tiles/lava.png")
    if char == map_symbols.Player:
        return ("Player", ":resources:/images/animated_characters/male_person/malePerson_idle.png")
    if char == map_symbols.Next_level:
        return ("Next_level", ":resources:/images/tiles/signExit.png")
    else:
        print(char)
        raise ValueError("Erreur: caractere inconnu")
    
    

#Fonction pour stocker un str dans une matrice avec 1  char par coefficient
def str_to_matrix(file : str, width : int) -> list[list[str]]:
    tableau = []
    for element in file.splitlines():
        ligne = []
        for i in range(len(element)):
            ligne.append(element[i])
        for i in range(width - len(element)):
            ligne.append(" ")
        tableau.append(ligne)
    
    return tableau[3:-1]


#Ouverture et lecture du fichier "map" pour ensuite la placer dans une matrice
def lecture_map(fichier : str) -> list[list[map_symbols]]:
    try:
        with open(fichier, "r", encoding="utf-8", newline="\n") as f:
            line = f.read()
    except OSError as e:
        print("Le fichier n'a pas pu être lu :")
        print(e)
        return[]
    
    width = dim(fichier)[0]

    #On converti le tableau de char en tableau de enum
    file_matrix = str_to_matrix(line, width)
    file_map: list[list[map_symbols]] = []
    for row in file_matrix:
        mapped_row = [char_to_map(c) for c in row]
        file_map.append(mapped_row)

    return file_map


#Calcul des dimensions de la map
def dim(fichier : str) -> tuple[int, int]:
    try:
        with open(fichier, "r", encoding="utf-8", newline="\n") as f:
            #largeur de la map
            width_line = f.readline().strip()
            if width_line.startswith("width:"):
                width = int(width_line.split(":")[1].strip())  
            
            #hauteur de la map
            height_line = f.readline().strip()
            if height_line.startswith("height:"):
                height = int(height_line.split(":")[1].strip())  

    except OSError as e:
        print("Le fichier n'a pas pu être lu :")
        print(e)

    return width, height

#Création d'une classe "map" :
class Map:
    dim : tuple[int, int]
    setup : list[list[map_symbols]]

    def __init__(self, dim: tuple[int, int], setup : list[list[map_symbols]]) -> None:
        self.dim = dim
        self.setup = setup
    
    def __str__(self) -> str:
        return f"{self.dim}, {self.setup}" 
    
    def __len__(self) -> int:
        return len(self.setup)
    
    def __getitem__(self, i:int) -> list[map_symbols]:
        return self.setup[i]

#Classe pour classer les maps
class Map_list:
    #Une liste de map, l'index représente la map affichée à l'écran
    Maps : list[str]
    index : int

    def __init__(self, Maps: list[str], index:int) -> None:
        self.Maps = Maps
        self.index = index
    
    def __str__(self) -> str:
        return f"{self.Maps}, {self.index}"
    
    def __len__(self) -> int:
        return len(self.Maps)
    
    def __getitem__(self, i: int) -> str:
        return self.Maps[i]
    







