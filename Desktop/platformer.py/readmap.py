import arcade
from typing import Dict, Any, List, Tuple, Final,Callable
from abc import ABC, abstractmethod
from enum import Enum, auto
import yaml
from typing import Tuple
from All_items.interuptor import *
from All_items.gate import *
from typing import Optional



# separation de la map en une partie yaml et une de la map classique
def split_map_file(filepath: str) -> Tuple[str, str]:
    try:
        with open(filepath, 'r', encoding='utf-8', newline='\n') as f:
            content = f.read()
    except OSError as e:
        raise RuntimeError(f"Impossible de lire le fichier {filepath}: {e}")

    parts = content.split('---', 1)
    if len(parts) < 2:
        raise ValueError("Le fichier ne contient pas le séparateur '---'.")

    yaml_part = parts[0].strip()
    map_part = parts[1]
    return (yaml_part, map_part)


# lecture de la partie yaml

def load_map_config(filepath: str) -> Dict[str, Any]:
    """
    Lit la partie YAML d'un fichier de map et renvoie la config.
    """
    content = split_map_file(filepath)[0]
    config = yaml.safe_load(content)
    if not isinstance(config, dict):
        raise TypeError("Le fichier YAML doit contenir un dictionnaire racine.")
    if 'width' not in config or 'height' not in config:
        raise KeyError("La config YAML doit contenir 'width' et 'height'.")
    return config


def init_gate_states_from_config(
    config: Dict[str, Any],
    gate_list: List[Gate],
    wall_list: arcade.SpriteList[arcade.Sprite]
) -> None:
    """
    Initialise l'état de chaque Gate (open/closed) selon le YAML.
    """
    gate_dict: Dict[Tuple[int,int], Gate] = {(g.x, g.y): g for g in gate_list}
    for gdata in config.get('gates', []):
        gx, gy = int(gdata['x']), int(gdata['y'])
        state = gdata.get('state', 'closed')
        if (gx, gy) not in gate_dict:
            raise ValueError(f"Aucun portail à la position ({gx},{gy}).")
        gate = gate_dict[(gx, gy)]
        if state == 'open':
            gate.open(wall_list)
        elif state == 'closed':
            gate.close(wall_list)
        else:
            raise ValueError(f"État portail inconnu: {state}")


def link_inter_to_gates(
    config: Dict[str, Any],
    inter_list: List[Inter],
    gate_list: List[Gate],
    wall_list: arcade.SpriteList[arcade.Sprite],
) -> None:
    # 1) Construire dict[(x,y) → Gate]
    gate_dict: Dict[Tuple[int, int], Gate] = {
        (g.x, g.y): g for g in gate_list
    }

    for sw in config.get("switches", []):
        sx, sy = int(sw["x"]), int(sw["y"])
        inter_opt = next(
            (i for i in inter_list if (i.x, i.y) == (sx, sy)),
            None
        )
        if inter_opt is None:
            raise ValueError(f"Aucun interrupteur à la position ({sx},{sy})")
        inter: Inter = inter_opt  # narrow type for MyPy

        # Réinitialiser état et listes d’actions
        raw = sw.get("state", False)
        inter.state = bool(raw) if isinstance(raw, bool) else (str(raw).lower() == "on")

        inter.actions_on.clear()
        inter.actions_off.clear()

        # ===== switch_on =====
        for ac in sw.get("switch_on", []):
            action = ac["action"]
            if action == "disable":
                def disable_fn(i: Inter = inter) -> None:
                    i.disable = True
                inter.actions_on.append(disable_fn)

            else:
                ax, ay = int(ac["x"]), int(ac["y"])
                if (ax, ay) not in gate_dict:
                    raise ValueError(f"Aucun portail trouvé à ({ax},{ay})")
                gate_ref: Gate = gate_dict[(ax, ay)]

                if action == "open-gate":
                    def on_open_fn(
                        g: Gate = gate_ref,
                        wl: arcade.SpriteList[arcade.Sprite] = wall_list
                    ) -> None:
                        g.open(wl)
                    inter.actions_on.append(on_open_fn)

                elif action == "close-gate":
                    def on_close_fn(
                        g: Gate = gate_ref,
                        wl: arcade.SpriteList[arcade.Sprite] = wall_list
                    ) -> None:
                        g.close(wl)
                    inter.actions_on.append(on_close_fn)

                else:
                    raise ValueError(f"Action inconnue dans switch_on: {action}")

        # ===== switch_off =====
        for ac in sw.get("switch_off", []):
            action = ac["action"]
            if action == "disable":
                def disable_fn(i: Inter = inter) -> None:
                    i.disable = True
                inter.actions_off.append(disable_fn)

            else:
                ax, ay = int(ac["x"]), int(ac["y"])
                if (ax, ay) not in gate_dict:
                    raise ValueError(f"Aucun portail trouvé à ({ax},{ay})")
                gate_ref2: Gate = gate_dict[(ax, ay)]

                if action == "open-gate":
                    def off_open_fn(
                        g: Gate = gate_ref2,
                        wl: arcade.SpriteList[arcade.Sprite] = wall_list
                    ) -> None:
                        g.open(wl)
                    inter.actions_off.append(off_open_fn)

                elif action == "close-gate":
                    def off_close_fn(
                        g: Gate = gate_ref2,
                        wl: arcade.SpriteList[arcade.Sprite] = wall_list
                    ) -> None:
                        g.close(wl)
                    inter.actions_off.append(off_close_fn)

                else:
                    raise ValueError(f"Action inconnue dans switch_off: {action}")




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
    Inter = auto()
    Gate = auto ()
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
    if char == "^":
        return map_symbols.Inter
    if char == "|":
        return map_symbols.Gate
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
    if char == map_symbols.Inter:
        return ("inter", ":resources:/images/tiles/leverLeft.png")
    if char == map_symbols.Gate:
        return ("gate", ":resources:/images/tiles/stoneCenter_rounded.png")
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
    
    return tableau[1:-1]



#Ouverture et lecture du fichier "map" pour ensuite la placer dans une matrice
def lecture_map(fichier : str) -> list[list[map_symbols]]:

    width = dim(fichier)[0]
    map = split_map_file(fichier)[1]

    #On converti le tableau de char en tableau de enum
    file_matrix = str_to_matrix(map, width)
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
    







