import arcade
from readmap import *
import math
from typing import Final
from abc import ABC, abstractmethod

#Variables globales
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
#Taille d'un "carreau" de la grille définie dans readmap
Grid_size = 64
#Initialisation du son
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
        
    
    #Méthode qui va etre utile pour les fleches et l'épée
    def check_hit_monsters(self, monster_list : arcade.SpriteList) -> None:
        monsters_hit= []
        if self.attribute.visible == True:
            monsters_hit = arcade.check_for_collision_with_list(self.attribute, monster_list)
            for monster in monsters_hit:
                monster.remove_from_sprite_lists()
                arcade.play_sound(hit_sound)

#Class pour l'épée qui hérite de Weapon
class Sword(Weapon):

    def __init__(self, attribute : arcade.Sprite, player_sprite : arcade.Sprite, camera_position : tuple[float, float]) -> None:
        super().__init__(attribute, player_sprite, camera_position)
    
    #Fonction qui despawn un monstre dès qu'il est touché
    def check_hit_monsters(self, monster_list : arcade.SpriteList) -> None:
        monsters_hit= []
        if self.attribute.visible == True:
            monsters_hit = arcade.check_for_collision_with_list(self.attribute, monster_list)
            for monster in monsters_hit:
                monster.remove_from_sprite_lists()
                arcade.play_sound(hit_sound)

    def update_weapon_position(self) -> None:
        weapon_r = math.radians(self.attribute.angle - 50)
        vec = (25 * math.cos(weapon_r), 25 * math.sin(-weapon_r))
        self.attribute.center_x = self.player_sprite.center_x + vec[0]
        self.attribute.center_y = self.player_sprite.center_y -15 + vec[1]


#Classe pour l'arc qui hérite de Weapon
class Bow(Weapon):

    def __init__(self, attribute : arcade.Sprite, player_sprite : arcade.Sprite, camera_position : tuple[float, float]) -> None:
        super().__init__(attribute, player_sprite, camera_position)
    
    #L'arc se comportant différamment de l'épée, on redéfinit l'orientation avec quelques constantes qui changent
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
        self.attribute.angle = math.degrees(angle) + 120

    def update_weapon_position(self) -> None:
        weapon_r = math.radians(self.attribute.angle - 50)
        vec = (20 * math.cos(weapon_r), 20 * math.sin(-weapon_r))
        self.attribute.center_x = self.player_sprite.center_x + vec[0]
        self.attribute.center_y = self.player_sprite.center_y -15 + vec[1]
    
    #L'arc ne tue personne, c'est la flèche
    def check_hit_monsters(self, monster_list : arcade.SpriteList) -> None:
        pass


class Arrow(Weapon):
    #bool qui vérifie si l'on a le droit de tirer
    Activated : bool

    def __init__(self, attribute : arcade.Sprite, player_sprite : arcade.Sprite, camera_position : tuple[float, float]) -> None:
        super().__init__(attribute, player_sprite, camera_position)
        self.Activated = False

    #Fonction qui permet de tirer
    def shoot(self, mouse_x: float, mouse_y: float) -> None:
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

    #Fonction qui détecte les collisions avec la flèche
    def arrow_collision(self, no_go_list : arcade.SpriteList, monster_list : arcade.SpriteList, wall_list : arcade.SpriteList) -> bool:
        lava_hit = arcade.check_for_collision_with_list(self.attribute, no_go_list)
        monster_hit = arcade.check_for_collision_with_list(self.attribute, monster_list)
        wall_hit = arcade.check_for_collision_with_list(self.attribute, wall_list)
        for lava in lava_hit:
            return True
        for monster in monster_hit:
            return True
        for wall in wall_hit:
            return True
        return False

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


#Les deux classes si-dessous permettent de mieux gérer le déplacement de chaque monstre
class monster:
    type: arcade.Sprite
    speed : int

    def __init__(self, type : arcade.Sprite, speed : int) -> None:
        self.type = type
        self.speed = speed
        
#Cette classe va permettre de ranger les monster avec leur vitesse
class monster_table:
     monsters : list[monster]

     def __init__(self, monsters : list[monster]) -> None:
          self.monsters = monsters

     def __getitem__(self, i: int) -> monster:
          return self.monsters[i]


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
          return ("Monster", ":resources:/images/enemies/slimePurple.png")
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
    weapon_list = arcade.SpriteList() #type ignore

    arrow_list : arcade.SpriteList[arcade.Sprite]
    arrow_class_list : list[Arrow]
    arrow_class_list = []

    #Cette liste va permettre de ranger les instances de la class "monster"
    monster_TABLE = monster_table([])

    # declaration des variables utilisées pour l'épée
    sword_timer: float = 0.0

    #UI elements
    camera: arcade.camera.Camera2D
    UI_camera : arcade.camera.Camera2D

    #Rajout du score
    coin_score = score(0)

    #Chargement des polices
    arcade.resources.load_kenney_fonts()

    #Allow change weapon
    Allow_change_weapon = True

    # initialisation des variables pour le son 
    coin_sound = arcade.load_sound(":resources:/sounds/coin4.wav")
    jump_sound = arcade.load_sound(":resources:/sounds/jump3.wav")
    game_over_sound = arcade.load_sound(":resources:/sounds/gameover3.wav")
    hit_sound = arcade.load_sound(":resources:/sounds/hurt4.wav")

    # ajout des représentation des armes à gauch
   
    #ajoute des armes
    sword = Sword(arcade.Sprite("assets/kenney-voxel-items-png/axe_gold.png",scale=0.5 * 0.7), arcade.Sprite("assets/kenney-voxel-items-png/axe_gold.png",scale=0.5 * 0.7), (0.0, 0.0))
    bow = Bow(arcade.Sprite("assets/kenney-voxel-items-png/bowArrow.png",scale=0.5 * 0.7), arcade.Sprite("assets/kenney-voxel-items-png/bowArrow.png",scale=0.5 * 0.7), (0.0, 0.0))

    weapon_list.append(sword.attribute)
    weapon_list.append(bow.attribute)

    sword.attribute.visible = False
    bow.attribute.visible = False 
    
    #Active l'arme qui va apparaitre à l'écran
    active_weapon = Active_Weapon([sword, bow], 0)
   
    """Lateral speed of the player, in pixels per frame."""
    
    #Ranger les sprites dans la bonne liste selon son asset
    def sprite_type(self, type : str, sprite: arcade.Sprite) -> None:
        if type == "Wall":
            self.wall_list.append(sprite)
        if type == "Coin":
              self.coin_list.append(sprite)
        if type == "Monster":
            self.monster_list.append(sprite)
            monsters = monster(sprite, -1)
            self.monster_TABLE.monsters.append(monsters)

        if type == "No-go":
            self.no_go_list.append(sprite)
        if type == "Player":
            self.player_sprite = sprite
            self.player_sprite_list = arcade.SpriteList()
            self.player_sprite_list.append(self.player_sprite)
        if type == "Next_level":
            self.next_level_list.append(sprite)
             

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Setup our game
        self.setup()
    
    def check_for_next_level(self) -> None:
        exit_list = arcade.check_for_collision_with_list(self.player_sprite, self.next_level_list)
        for exit in exit_list:
             All_maps.index += 1
             self.setup()

    def setup(self) -> None:
        """Set up the game here."""
        PLAYER_GRAVITY = 1

        #Initialiser les listes d'objets
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.weapon_icon_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.no_go_list = arcade.SpriteList(use_spatial_hash=True)
        self.monster_list = arcade.SpriteList(use_spatial_hash=True)
        self.next_level_list = arcade.SpriteList(use_spatial_hash=True)
        self.arrow_list = arcade.SpriteList()
        self.arrow_class_list = []
        
        MAP = All_maps.Maps[All_maps.index]
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

        #Initialisation de l'icone des armes
        self.sword_repr = arcade.Sprite("assets/kenney-voxel-items-png/axe_gold.png", scale = 0.5, center_x=60, center_y = 550)
        self.bow_repr = arcade.Sprite("assets/kenney-voxel-items-png/bowArrow.png", scale = 0.5, center_x=60, center_y = 550)
        self.sword_repr.visible = True
        self.bow_repr.visible = False

        #Initialisation 
        self.weapon_icon_list.append(self.sword_repr)
        self.weapon_icon_list.append(self.bow_repr)
        
        
    #Variables booléennes qui détectent quand les touches sont appuyées
    key_right : bool = False
    key_left : bool = False

    #Fonction qui "crée" une flèche
    def create_arrow(self) -> arcade.Sprite:
        arrow = arcade.Sprite("assets/kenney-voxel-items-png/arrow.png",scale=0.3)
        arrow.visible = False
        self.arrow_list.append(arrow)
        return arrow
    

    def on_mouse_press(self, x:int, y:int, button:int, modifiers: int) -> None :
        if arcade.MOUSE_BUTTON_LEFT:
            weapon : Weapon
            weapon = self.active_weapon.weapons[self.active_weapon.index]
            #self.sword_timer = 0.2
            if self.active_weapon.index == 1:
                self.Allow_change_weapon = False
                arrow = Arrow(self.create_arrow(), self.player_sprite, self.camera.position)
                arrow.Activated = True
                arrow.shoot(x, y)
                self.arrow_class_list.append(arrow)

            # Positionner l'épée en fonction de l'angle
            weapon.update_weapon_orientation(x,y)
            weapon.attribute.visible = True
            
    def on_mouse_release(self, x:int, y:int, button:int, modifiers:int) -> None :
            weapon = self.active_weapon.weapons[self.active_weapon.index]
            weapon.attribute.visible = False
            self.Allow_change_weapon = True
        
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""
        PLAYER_MOVEMENT_SPEED = 4
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
            self.setup()

        #change weapon
        if key == arcade.key.P and self.Allow_change_weapon == True:
            weapon_repr = self.weapon_icon_list[self.active_weapon.index]
            weapon_repr.visible = False
            self.active_weapon.change_index(self.active_weapon.index + 1)
            weapon_repr = self.weapon_icon_list[self.active_weapon.index]
            weapon_repr.visible = True
            

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
            self.coin_list.draw()
            self.monster_list.draw()
            self.no_go_list.draw()
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
              self.camera.position = (self.camera.position[0] + abs(player_x - right_edge) , self.camera.position[1]) #type ignore
         if player_x <= left_edge:
              self.camera.position = (self.camera.position[0]  - abs(player_x - left_edge) , self.camera.position[1]) #type ignore
         if player_y >= upper_edge:
              self.camera.position = (self.camera.position[0], self.camera.position[1] + abs(player_y - upper_edge))#type ignore
         if player_y <= down_edge:
              self.camera.position = (self.camera.position[0], self.camera.position[1] - abs(player_y - down_edge))#type ignore

    #Fonction qui déplace le blob
    def blob_position(self) -> None:
         for blob in self.monster_TABLE.monsters:
            collision = self.blob_collision(blob.type, blob.speed)
            if collision == True:
                 #si il y a une collision, la vitesse du blob est inversée ainsi que sa position
                 blob.speed *= -1
                 blob.type.scale_x *= -1
            blob.type.change_x = blob.speed
         self.monster_list.update()
    
    #Fonction qui détecte les collisions
    def blob_collision(self, blob: arcade.Sprite, change_x : int) -> bool:
        #point en dessous du blob pour les collision sur les bords
        point_y = blob.bottom - (Grid_size / 2)
        if change_x == -1:
             point_x = blob.left
        else:
             point_x = blob.right
        point = (point_x, point_y)
        #detecte les collisions entre le point et l'air, lave et murs
        collided_lava = arcade.get_sprites_at_point(point, self.no_go_list)
        collided_box = arcade.get_sprites_at_point((point_x, blob.center_y), self.wall_list)
        collided_air = arcade.get_sprites_at_point(point, self.wall_list)
        if collided_air == []:
             return True
        for lava in collided_lava:
             return True
        for box in collided_box:
             return True
        return False
    
    def game_over(self, danger : arcade.sprite_list) -> None:
        hit = arcade.check_for_collision_with_list(self.player_sprite, danger)
        for elements in hit:
            All_maps.index = 0
            self.setup()
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
        if self.sword_timer > 0:
            self.sword_timer -= delta_time
            if self.sword_timer <= 0:
                self.sword.attribute.visible = False
        
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
        self.blob_position()

        #Detection de la collision avec la lave et les blobs:
        self.game_over(self.no_go_list)
        self.game_over(self.monster_list)
        
    
             



