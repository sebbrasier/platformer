import arcade
import math
from abc import abstractmethod
import random


#Variables globales
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
#Taille d'un "carreau" de la grille définie dans readmap
Grid_size = 64

#Les deux classes si-dessous permettent de mieux gérer le déplacement de chaque monstre
class monster:
    sprite: arcade.Sprite

    def __init__(self, sprite : arcade.Sprite) -> None:
        self.sprite = sprite
    
    @abstractmethod
    def monster_position(self, no_go_list : arcade.SpriteList[arcade.Sprite], wall_list : arcade.SpriteList[arcade.Sprite]) -> None:
        """Fonction qui va être définie par les classes enfants pour gérer la position des monstres"""
        ...

#Création d'une classe pour les blobs
class blob(monster):
    #Attribut de vitesse
    speed : int
    def __init__(self, type : arcade.Sprite, speed : int) -> None:
        super().__init__(type)
        self.speed = speed
    
    #Fonction de collision avec l'exterieur: propre aux blobs
    def monster_collision(self, no_go_list : arcade.SpriteList[arcade.Sprite], wall_list : arcade.SpriteList[arcade.Sprite]) -> bool:
        """Fonction de collision avec l'exterieur: propre aux blobs,elle renvoit True si il arrive au bout d'une plateforme ou qu'il percute un obstacle"""
        #point en dessous du blob pour les collision sur les bords
        blob = self.sprite
        change_x = self.speed
        point_y = blob.bottom - (Grid_size / 2)
        if change_x == -1:
             point_x = blob.left
        else:
             point_x = blob.right
        point = (point_x, point_y)
        #detecte les collisions entre le point et l'air, lave et murs
        collided_lava = arcade.get_sprites_at_point(point, no_go_list)
        collided_box = arcade.get_sprites_at_point((point_x, blob.center_y), wall_list)
        collided_air = arcade.get_sprites_at_point(point, wall_list)
        if collided_air == []:
             return True
        for lava in collided_lava:
             return True
        for box in collided_box:
             return True
        return False
    
    def monster_position(self, no_go_list : arcade.SpriteList[arcade.Sprite], wall_list : arcade.SpriteList[arcade.Sprite]) -> None:
        """Cette fonction gère le déplacement du blob, elle utilise monster_collision pour changer de direction si 
        il y a une collision. Elle change l'orientation visuel du sprite selon sa direction"""
        collision = self.monster_collision(no_go_list, wall_list)
        if collision is True:
                #si il y a une collision, la vitesse du blob est inversée ainsi que sa position
                self.speed *= -1
                self.sprite.scale_x *= -1
        self.sprite.change_x = self.speed

#Classe pour les chauves-souris
class chauve_souris(monster):
    speed: float
    start_x: float
    start_y: float
    boundary: float
    vx: float
    vy: float
    random_dir : float

    def __init__(self, sprite: arcade.Sprite, speed: float, boundary: float, random_dir : float) -> None:

        super().__init__(sprite)
        self.speed = speed
        # Enregistrer la position initiale du sprite.
        self.start_x = sprite.center_x
        self.start_y = sprite.center_y
        self.boundary = boundary
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.random_dir = random_dir


    def monster_position(self, no_go_list: arcade.SpriteList[arcade.Sprite], wall_list: arcade.SpriteList[arcade.Sprite]) -> None:
        """ Fonction de déplacement des chauves-souris, avec la fonction random.gauss avec une moyenne à 0 et un écart type a pi/20
            pour que la chauve souris ait une grande probabilité de faire un petit changement de direction et une très petite de faire
            un 180°. Elle fait faire à la chauve souris un 180° quand elle touche sa bordure"""
        if random.random() < self.random_dir:
            current_angle = math.atan2(self.vy, self.vx)
            delta_angle = random.gauss(0, math.pi / 20)
            new_angle = current_angle + delta_angle
            self.vx = math.cos(new_angle) * self.speed
            self.vy = math.sin(new_angle) * self.speed

        # Calcul de la nouvelle position
        new_x = self.sprite.center_x + self.vx
        new_y = self.sprite.center_y + self.vy

        #'Rebondit' sur les limites de sa zone si elle les atteint
        if new_x < self.start_x - self.boundary or new_x > self.start_x + self.boundary:
            self.vx *= -1
            self.sprite.scale_x *= -1
            new_x = self.sprite.center_x + self.vx

        if new_y < self.start_y - self.boundary or new_y > self.start_y + self.boundary:
            self.vy *= -1
            new_y = self.sprite.center_y + self.vy

        # Mettre à jour la position du sprite
        self.sprite.center_x = new_x
        self.sprite.center_y = new_y
        
        
#Cette classe va permettre de ranger les instances des monstres pour pouvoir ensuite manipuler les classes dans GameView
class monster_table:
     monsters : list[monster]

     def __init__(self, monsters : list[monster]) -> None:
          self.monsters = monsters

     def __getitem__(self, i: int) -> monster:
          return self.monsters[i]
