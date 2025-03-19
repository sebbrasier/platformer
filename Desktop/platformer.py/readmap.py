
#Ouverture et lecture du fichier "map" pour ensuite la placer dans une matrice
def lecture_map(fichier : str) -> list[list[str]]:
    tableau = []
    try:
        with open(fichier, "r", encoding="utf-8", newline="\n") as f:
            line = f.read()
    except OSError as e:
        print("Le fichier n'a pas pu être lu :")
        print(e)
        return[]

    #On garde seulement le contenu de la map
    for element in line.splitlines():
        ligne = []
        for c in element:
            ligne.append(c)
        tableau.append(ligne)
    
    return tableau[3:-1]


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
    setup : list[list[str]]

    def __init__(self, dim: tuple[int, int], setup : list[list[str]]) -> None:
        self.dim = dim
        self.setup = setup
    
    def __str__(self) -> str:
        return f"{self.dim}, {self.setup}" 
    
    def __len__(self) -> int:
        return len(self.setup)
    
    def __getitem__(self, i:int) -> list[str]:
        return self.setup[i]

#Classe pour classer les maps
class Map_list:
    #Une liste de map, l'index représente la map affichée à l'écran
    Maps : list[Map]
    index : int

    def __init__(self, Maps: list[Map], index:int) -> None:
        self.Maps = Maps
        self.index = index
    
    def __str__(self) -> str:
        return f"{self.Maps}, {self.index}"
    
    def __len__(self) -> int:
        return len(self.Maps)
    
    def __getitem__(self, i: int) -> Map:
        return self.Maps[i]
    

All_maps = Map_list([], 0)
#Ceci correspond à la map dans le jeu: initialisée dans gameview
Map_game = Map(dim("maps/map1.txt"), lecture_map("maps/map1.txt"))
Map_game2 = Map(dim("maps/map2.txt"), lecture_map("maps/map2.txt"))
Map_game3 = Map(dim("maps/map3.txt"), lecture_map("maps/map3.txt"))


All_maps.Maps.append(Map_game)
All_maps.Maps.append(Map_game2)
All_maps.Maps.append(Map_game3)




