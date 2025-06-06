import arcade
from readmap import *
import math
from abc import abstractmethod
from All_monsters.monsters import *
from All_items.interuptor import *

hit_sound = arcade.load_sound(":resources:/sounds/hurt4.wav")

#Créer une classe pour les armes
class Weapon:
    attribute : arcade.Sprite
    player_sprite : arcade.Sprite
    camera_position : tuple[float, float]

    #Initialisation
    def __init__(self, attribute : arcade.Sprite, player_sprite : arcade.Sprite, camera_position : tuple[float, float]) -> None:
        self.attribute = attribute
        self.player_sprite = player_sprite
        self.camera_position = camera_position

    #Definit l'orientation "générale" des armes
    def update_weapon_orientation(self, mouse_x: float, mouse_y: float) -> None:
        """
        Calcule la position et l'angle de l'arme pour que le manche reste fixé
        vers le personnage et que le placement se fasse le long d'un cercle.
        """
        world_x = mouse_x + self.camera_position[0] - (WINDOW_WIDTH / 2)
        world_y = mouse_y + self.camera_position[1] - (WINDOW_HEIGHT / 2)
        ref_x = self.player_sprite.center_x
        ref_y = self.player_sprite.center_y   
        angle = math.atan2(ref_x - world_x,ref_y - world_y)
        self.attribute.angle = math.degrees(angle) + 140
    
    #Définit la position (et non l'orientation) des armes à tout moment
    @abstractmethod
    def update_weapon_position(self) -> None:
        ...

    def check_hit_monsters(self, monster_list : arcade.SpriteList[arcade.Sprite]) -> None:
        """Cette fonction check si le weapon (sword/arrow uniquement) touche un monstre et l'enlève de la liste si
        c'est le cas. Elle sera surchargé dans Sword pour que cela ne se produise que pendant la frame du clic."""
        monsters_hit= []
        if self.attribute.visible == True:
            monsters_hit = arcade.check_for_collision_with_list(self.attribute, monster_list)
            for monster in monsters_hit:
                monster.remove_from_sprite_lists()
                arcade.play_sound(hit_sound)
    def check_hit_inter(self, inter : arcade.Sprite) ->bool:
        """Cette fonction check si le weapon (sword/arrow uniquement) touche un interupteur et renvoit True si
        c'est le cas. Elle sera surchargé dans Sword pour que cela ne se produise que pendant la frame du clic."""
        if self.attribute.visible == True:
            inter_hit = arcade.check_for_collision(self.attribute, inter)
            return inter_hit
        return False

#Class pour l'épée qui hérite de Weapon
class Sword(Weapon):
    # initialisation d'un booléen qui sera True seulement pendant la frame du clic
    can_kill = False
    def __init__(self, attribute : arcade.Sprite, player_sprite : arcade.Sprite, camera_position : tuple[float, float]) -> None:
        super().__init__(attribute, player_sprite, camera_position)

    def update_weapon_position(self) -> None:
        """Cette fonction calcul la position de l'épée"""
        weapon_r = math.radians(self.attribute.angle - 50)
        vec = (25 * math.cos(weapon_r), 25 * math.sin(-weapon_r))
        self.attribute.center_x = self.player_sprite.center_x + vec[0]
        self.attribute.center_y = self.player_sprite.center_y -15 + vec[1]

    def check_hit_monsters(self, monster_list: arcade.SpriteList[arcade.Sprite]) -> None:
        """
        L'épée ne tue les monstres que si can_kill est True, juste pendant l'image du clic
        """
        if Sword.can_kill == True:
            super().check_hit_monsters(monster_list)

            
    def check_hit_inter(self, inter: arcade.Sprite) -> bool:
        if Sword.can_kill:
            self.update_weapon_position() 
            return super().check_hit_inter(inter)
        return False

#Class pour l'arc qui hérite de Weapon
class Bow(Weapon):

    def __init__(self, attribute : arcade.Sprite, player_sprite : arcade.Sprite, camera_position : tuple[float, float]) -> None:
        super().__init__(attribute, player_sprite, camera_position)
    

    def update_weapon_position(self) -> None:
        """Cette fonction calcul la position de l'arc"""
        weapon_r = math.radians(self.attribute.angle - 50)
        vec = (20 * math.cos(weapon_r), 20 * math.sin(-weapon_r))
        self.attribute.center_x = self.player_sprite.center_x + vec[0]
        self.attribute.center_y = self.player_sprite.center_y -15 + vec[1]

        #L'arc se comportant différamment de l'épée, on redéfinit l'orientation avec quelques constantes qui changent
    def update_weapon_orientation(self, mouse_x: float, mouse_y: float) -> None:
        """
        Calcule la position et l'angle de l'arme pour que le manche reste fixé
        vers le personnage et que le placement se fasse le long d'un cercle. Elle difère d'une constante comparé à celle de Sword.
        """
        world_x = mouse_x + self.camera_position[0] - (WINDOW_WIDTH / 2)
        world_y = mouse_y + self.camera_position[1] - (WINDOW_HEIGHT / 2)
        ref_x = self.player_sprite.center_x
        ref_y = self.player_sprite.center_y   
        angle = math.atan2(ref_x - world_x,ref_y - world_y)
        self.attribute.angle = math.degrees(angle) + 120
    
    #L'arc ne tue personne, c'est la flèche
    def check_hit_monsters(self, monster_list : arcade.SpriteList[arcade.Sprite]) -> None:
        pass

    def check_hit_inter(self, inter: arcade.Sprite) -> bool:
        return False


class Arrow(Weapon):
    #bool qui vérifie si l'on a le droit de tirer
    Activated : bool

    def __init__(self, attribute : arcade.Sprite, player_sprite : arcade.Sprite, camera_position : tuple[float, float]) -> None:
        super().__init__(attribute, player_sprite, camera_position)
        self.Activated = False

    def shoot(self, mouse_x: float, mouse_y: float) -> None:
        """Fonction qui permet de tirer"""
        if self.Activated == True:
            self.attribute.position = self.player_sprite.position
            self.update_weapon_orientation(mouse_x, mouse_y)
            self.attribute.visible = True
            weapon_r = math.radians(self.attribute.angle - 50)
            vec = (25 * math.cos(weapon_r), 25 * math.sin(-weapon_r))
            self.attribute.change_x = vec[0]
            self.attribute.change_y = vec[1]

    #Ici, on n'a pas besoin de suivre le personnage
    def update_weapon_position(self) -> None:
        pass

    def arrow_collision(self, no_go_list : arcade.SpriteList[arcade.Sprite], monster_list : arcade.SpriteList[arcade.Sprite], wall_list : arcade.SpriteList[arcade.Sprite],
                        platforms : arcade.SpriteList[arcade.Sprite], inter_list : arcade.SpriteList[arcade.Sprite]) -> bool:
        """Cette fonction détècte les collisions entre les flèches et les sprites necessaires"""
        
        lava_hit = arcade.check_for_collision_with_list(self.attribute, no_go_list)
        monster_hit = arcade.check_for_collision_with_list(self.attribute, monster_list)
        wall_hit = arcade.check_for_collision_with_list(self.attribute, wall_list)
        platform_hit = arcade.check_for_collision_with_list(self.attribute, platforms)
        inter_hit = arcade.check_for_collision_with_list(self.attribute, inter_list)

        for lava in lava_hit:
            return True
        for monster in monster_hit:
            return True
        for wall in wall_hit:
            return True
        for plat in platform_hit:
            return True
        for inter in inter_hit:
            return True
        if self.attribute.center_y <= (self.camera_position[1] - 720/2 ):
            return True
        return False



