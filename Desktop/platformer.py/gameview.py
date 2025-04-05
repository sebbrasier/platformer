import arcade
from readmap import *
import math
from typing import Final
from abc import ABC, abstractmethod
from All_monsters.monsters import *
from All_weapons.weapons import *
from pyglet.math import Vec2
import random

#Variables globales
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
#Taille d'un "carreau" de la grille définie dans readmap
Grid_size = 64
#Initialisation du son
hit_sound = arcade.load_sound(":resources:/sounds/hurt4.wav")


#Classe pour voir quelle arme est active:
class Active_Weapon:
    weapons : list[Weapon]
    #index correspond à l'arme qui apparait à l'écran
    index : int

    def __init__(self, weapons : list[Weapon], index : int) -> None:
        self.weapons = weapons
        self.index = index
    
    def change_index(self, new_index : int) -> None:
        self.index = new_index % len(self.weapons)

#classe pour compter le score
class score:
    points: int
    def __init__(self, points : int) -> None:
        self.points = points
    @property
    def erase(self) -> None:
        self.points = 0


#fonction qui convertit les charactères de la map en un type de bloc et son asset:
def char_to_sprite(char: str) -> tuple[str, str]:
     if char == " ":
          return (" ", " ")
     if char == "=":
          return ("Wall", ":resources:/images/tiles/grassMid.png")
     if char == "-":
          return ("Wall", ":resources:/images/tiles/grassHalf_mid.png")
     if char == "x":
          return ("Wall", ":resources:/images/tiles/boxCrate_double.png")
     if char == "*":
          return ("Coin", ":resources:/images/items/coinGold.png")
     if char == "o":
          return ("Blob", ":resources:/images/enemies/slimePurple.png")
     if char == "v":
          return ("Chauve-souris", "assets/kenney-extended-enemies-png/bat.png")
     if char == "£":
          return ("No-go", ":resources:/images/tiles/lava.png")
     if char == "S":
          return ("Player", ":resources:/images/animated_characters/male_person/malePerson_idle.png")
     if char == "E":
          return ("Next_level", ":resources:/images/tiles/signExit.png")
     else:
          raise Exception("Erreur: caractere inconnu")


class GameView(arcade.View):

    #Initialisation de toutes les listes
    next_level_list : arcade.SpriteList[arcade.Sprite]
    player_sprite : arcade.Sprite
    player_sprite_list : arcade.SpriteList[arcade.Sprite]

    wall_list : arcade.SpriteList[arcade.Sprite]
    coin_list : arcade.SpriteList[arcade.Sprite]
    no_go_list : arcade.SpriteList[arcade.Sprite]
    monster_list : arcade.SpriteList[arcade.Sprite]
    weapon_icon_list : arcade.SpriteList[arcade.Sprite]
    weapon_list : arcade.SpriteList[arcade.Sprite] 

    arrow_list : arcade.SpriteList[arcade.Sprite]
    arrow_class_list : list[Arrow]

    #Cette liste va permettre de ranger les instances de la class "monster"
    monster_TABLE : monster_table

    #UI elements
    camera: arcade.camera.Camera2D
    UI_camera : arcade.camera.Camera2D

    #ajout des armes
    sword : Sword
    bow : Bow

    #Initialiser la liste de fichiers
    file_list : Map_list

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        #Rajout du score
        self.coin_score = score(0)

        #Chargement des polices
        arcade.resources.load_kenney_fonts()

        #Allow change weapon
        self.Allow_change_weapon = True

        # initialisation des variables pour le son 
        self.coin_sound = arcade.load_sound(":resources:/sounds/coin4.wav")
        self.jump_sound = arcade.load_sound(":resources:/sounds/jump3.wav")
        self.game_over_sound = arcade.load_sound(":resources:/sounds/gameover3.wav")
        self.hit_sound = arcade.load_sound(":resources:/sounds/hurt4.wav")

        #Initialisation des listes de fichiers
        self.file_list = Map_list(["maps/map1.txt", "maps/map2.txt", "maps/map3.txt"], 0)

        # Setup our game
        self.setup(self.file_list.Maps[self.file_list.index])

    def setup(self, MAP_file : str) -> None:
        """Set up the game here."""
        PLAYER_GRAVITY = 1

        #Initialiser les listes d'objets
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.weapon_icon_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.no_go_list = arcade.SpriteList(use_spatial_hash=True)
        self.monster_list = arcade.SpriteList(use_spatial_hash=True)
        self.next_level_list = arcade.SpriteList(use_spatial_hash=True)
        self.player_sprite_list = arcade.SpriteList()
        self.arrow_list = arcade.SpriteList()
        self.weapon_list = arcade.SpriteList()
        self.arrow_class_list = []
        self.monster_TABLE = monster_table([])
        
        MAP = lecture_map(MAP_file)
        #Création de la map
        for i in  range(len(MAP)):
            for j in range(len(MAP[i])):
                sprite = MAP[i][j] 
                if char_to_sprite(sprite) != (" ", " "):
                    asset = arcade.Sprite(char_to_sprite(sprite)[1],
                        center_y = (len(MAP) - i) * Grid_size,
                        center_x = j * Grid_size,
                        scale = 0.5
                    )
                    self.sprite_type(char_to_sprite(sprite)[0], asset)
                
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls = self.wall_list,
            gravity_constant=PLAYER_GRAVITY,
        )
        #initialisation de la caméra
        self.camera = arcade.camera.Camera2D()
        self.UI_camera = arcade.camera.Camera2D()

        #initialisation des armes
        self.sword = Sword(arcade.Sprite("assets/kenney-voxel-items-png/axe_gold.png",scale=0.5 * 0.7), self.player_sprite, self.camera.position)
        self.bow = Bow(arcade.Sprite("assets/kenney-voxel-items-png/bowArrow.png",scale=0.5 * 0.7), self.player_sprite, self.camera.position)

        self.weapon_list.append(self.sword.attribute)
        self.weapon_list.append(self.bow.attribute)
    
        #Active l'arme qui va apparaitre à l'écran
        self.active_weapon = Active_Weapon([self.sword, self.bow], 0)
        for weapon in self.active_weapon.weapons:
            weapon.attribute.visible = False
        
        #Initialisation de l'icone des armes
        self.sword_repr = arcade.Sprite("assets/kenney-voxel-items-png/axe_gold.png", scale = 0.5, center_x=60, center_y = 550)
        self.bow_repr = arcade.Sprite("assets/kenney-voxel-items-png/bowArrow.png", scale = 0.5, center_x=60, center_y = 550)

        self.weapon_icon_list.append(self.sword_repr)
        self.weapon_icon_list.append(self.bow_repr)
        for icon in self.weapon_icon_list:
            icon.visible = False
        self.weapon_icon_list[self.active_weapon.index].visible = True

    
    #Fonction qui détecte si le joueur collisionne avec le paneau
    def check_for_next_level(self) -> None:
        exit_list = arcade.check_for_collision_with_list(self.player_sprite, self.next_level_list)
        for exit in exit_list:
             self.file_list.index += 1
             self.setup(self.file_list.Maps[self.file_list.index])
    
     #Ranger les sprites dans la bonne liste selon son asset
    def sprite_type(self, type : str, sprite: arcade.Sprite) -> None:
        if type == "Wall":
            self.wall_list.append(sprite)
        if type == "Coin":
              self.coin_list.append(sprite)
        if type == "Chauve-souris":
            self.monster_list.append(sprite)
            chauve_S = chauve_souris(sprite,-1, 100)
            self.monster_TABLE.monsters.append(chauve_S)
        if type == "Blob":
            self.monster_list.append(sprite)
            blob_monster = blob(sprite, -1)
            self.monster_TABLE.monsters.append(blob_monster)
        if type == "No-go":
            self.no_go_list.append(sprite)
        if type == "Player":
            self.player_sprite = sprite
            self.player_sprite_list.append(self.player_sprite)
        if type == "Next_level":
            self.next_level_list.append(sprite)
        
    #Variables booléennes qui détectent quand les touches sont appuyées
    key_right : bool = False
    key_left : bool = False

    #Fonction qui "crée" une flèche
    def create_arrow(self) -> arcade.Sprite:
        arrow = arcade.Sprite("assets/kenney-voxel-items-png/arrow.png",scale=0.3)
        arrow.visible = False
        self.arrow_list.append(arrow)
        return arrow
    
    #Définit tout ce qui se passe quand le joueur appuye sur le ckick gauche
    def on_mouse_press(self, x:int, y:int, button:int, modifiers: int) -> None :
        if button == arcade.MOUSE_BUTTON_LEFT:
            #Fait appraitre l'arme que l'on a sélectionné, indiqué par active_weapon.index
            weapon : Weapon
            weapon = self.active_weapon.weapons[self.active_weapon.index]
            self.Allow_change_weapon = False
            #S'assurer que l'épée ne peut que tuer le blob pendait le click
            Sword.can_kill = True
            if self.active_weapon.index == 1:
                #Fait appraitre la flèche si on a séléctionné l'arc
                arrow = Arrow(self.create_arrow(), self.player_sprite, self.camera.position)
                arrow.Activated = True
                arrow.shoot(x, y)
                self.arrow_class_list.append(arrow)

            # Positionner l'épée en fonction de l'angle
            weapon.update_weapon_orientation(x,y)
            weapon.attribute.visible = True
        
        # Clic droit pour changer d'arme
        if button == arcade.MOUSE_BUTTON_RIGHT and self.Allow_change_weapon:
            #Fait disparaitre l'icon de l'arme qui était affichée
            weapon_repr = self.weapon_icon_list[self.active_weapon.index]
            weapon_repr.visible = False
            self.active_weapon.change_index(self.active_weapon.index + 1)
            weapon_repr = self.weapon_icon_list[self.active_weapon.index]
            weapon_repr.visible = True

            
    def on_mouse_release(self, x:int, y:int, button:int, modifiers:int) -> None :
            #Fait disparaitre l'arme que l'on a en main
            weapon = self.active_weapon.weapons[self.active_weapon.index]
            weapon.attribute.visible = False
            self.Allow_change_weapon = True
        
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""
        PLAYER_MOVEMENT_SPEED = 3
        PLAYER_JUMP_SPEED = 18
        
        if key == arcade.key.RIGHT:
            # start moving to the right
            self.player_sprite.change_x = + PLAYER_MOVEMENT_SPEED
            self.key_right = True
    
        if key == arcade.key.LEFT:
            # start moving to the left
            self.player_sprite.change_x = - PLAYER_MOVEMENT_SPEED
            self.key_left = True

        if key == arcade.key.UP and self.physics_engine.can_jump(): 
            # start moving to the left
            self.player_sprite.change_y = PLAYER_JUMP_SPEED

            #son
            arcade.play_sound(self.jump_sound)

        if key == arcade.key.ESCAPE:
            self.setup(self.file_list.Maps[self.file_list.index])
            

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""
        if key == arcade.key.RIGHT:
            self.key_right = False
        if key == arcade.key.LEFT:
            self.key_left = False
        if (key == arcade.key.RIGHT or key == arcade.key.LEFT) and (self.key_right == False and self.key_left == False):
            #stop later mouvement
            self.player_sprite.change_x = 0

    def on_draw(self) -> None:
        """Render the screen"""
        self.clear()
        with self.camera.activate():
            self.player_sprite_list.draw()
            self.wall_list.draw()
            self.no_go_list.draw()
            self.coin_list.draw()
            self.monster_list.draw()
            self.weapon_list.draw()
            self.next_level_list.draw()
            self.arrow_list.draw()
            
        with self.UI_camera.activate():
            arcade.draw_text(f"SCORE: {self.coin_score.points}", 10,650, arcade.color.WHITE, 20,font_name="Kenney Future")
            self.weapon_icon_list.draw()


    #fonction de control de camera
    def cam_control(self) -> None:
         player_x = self.player_sprite.center_x
         player_y = self.player_sprite.center_y
         #Calcule des "Bords" de la caméra:
         right_edge = self.camera.position[0] + (WINDOW_WIDTH / 2) - 410
         left_edge = self.camera.position[0] - (WINDOW_WIDTH / 2) + 410
         upper_edge = self.camera.position[1] + (WINDOW_HEIGHT / 2) - 300
         down_edge = self.camera.position[1] - (WINDOW_HEIGHT / 2) + 250

        #La caméra se déplace avec le joueur
         if player_x >= right_edge:
              self.camera.position = Vec2(self.camera.position[0] + abs(player_x - right_edge) , self.camera.position[1]) 
         if player_x <= left_edge:
              self.camera.position = Vec2(self.camera.position[0]  - abs(player_x - left_edge) , self.camera.position[1])
         if player_y >= upper_edge:
              self.camera.position = Vec2(self.camera.position[0], self.camera.position[1] + abs(player_y - upper_edge))
         if player_y <= down_edge:
              self.camera.position = Vec2(self.camera.position[0], self.camera.position[1] - abs(player_y - down_edge))

    def game_over(self, danger : arcade.SpriteList[arcade.Sprite]) -> None:
        hit : list[arcade.Sprite]
        hit = arcade.check_for_collision_with_list(self.player_sprite, danger)
        for elements in hit:
            #On appelle setup dès que l'on meurt
            self.file_list.index = 0
            self.setup(self.file_list.Maps[self.file_list.index])
            self.coin_score.erase
        # son 
            arcade.play_sound(self.game_over_sound)
            
    """Main in-game view."""
    def on_update(self, delta_time: float) -> None:
        self.player_sprite.center_x += self.player_sprite.change_x
        self.physics_engine.update()

        self.check_for_next_level()
        self.cam_control()


        coin_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hit:
            coin.remove_from_sprite_lists()
            self.coin_score.points += 1
        #son
            arcade.play_sound(self.coin_sound)

        #update position de l'arme sur l'écran
        weapon = self.active_weapon.weapons[self.active_weapon.index]
        weapon.camera_position = self.camera.position
        weapon.player_sprite = self.player_sprite
        weapon.update_weapon_position()
        
        #check si l'épée touche un monstre
        weapon.check_hit_monsters(self.monster_list)
        
        #Update position des flèches:
        for arrow in self.arrow_list:
            arrow.change_y -= 1.5
        self.arrow_list.update()

        #Check si les flèches touchent les monstres
        for arrows in self.arrow_class_list:
            if arrows.arrow_collision(self.no_go_list, self.monster_list, self.wall_list) is True:
                self.arrow_class_list.remove(arrows)
                self.arrow_list.remove(arrows.attribute)
            arrows.check_hit_monsters(self.monster_list)
            
        #position du blob
        for monster in self.monster_TABLE.monsters:
            monster.monster_position(self.no_go_list, self.wall_list)

        self.monster_list.update()
                    

        #Detection de la collision avec la lave et les blobs:
        self.game_over(self.no_go_list)
        self.game_over(self.monster_list)


