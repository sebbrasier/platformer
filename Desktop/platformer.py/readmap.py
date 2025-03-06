
#Ouverture et lecture du fichier "map" pour ensuite la placer dans une matrice
def lecture_map() -> list[list[str]]:
    tableau = []
    try:
        with open("maps/map1.txt", "r", encoding="utf-8", newline="\n") as f:
            line = f.read()
    except OSError as e:
        print("Le fichier n'a pas pu être lu :")
        print(e)

    #On garde seulement le contenu de la map
    for element in line.splitlines():
        ligne = []
        for c in element:
            ligne.append(c)
        tableau.append(ligne)
    
    return tableau[3:-1]

#Calcul des dimensions de la map
def dim() -> tuple[int, int]:
    try:
        with open("maps/map1.txt", "r", encoding="utf-8", newline="\n") as f:
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


#Ceci correspond à la map dans le jeu: initialisée dans gameview
Map_game = Map(dim(), lecture_map())




