import arcade
from readmap import Map
from readmap import *
import math


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
          return ("Monster", ":resources:/images/enemies/slimeBlue.png")
     if char == "£":
          return ("No-go", ":resources:/images/tiles/lava.png")
     if char == "S":
          return ("Player", ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png")
     if char == "E":
          return ("Next_level", ":resources:/images/tiles/signExit.png")
     else:
          raise Exception("Erreur: caractere inconnu")
     
class GameView(arcade.View):

    #Liste pour les objets situés à la fin du niveau
    next_level_list : arcade.SpriteList[arcade.Sprite]
    
    player_sprite : arcade.Sprite
    player_sprite_list : arcade.SpriteList[arcade.Sprite]

    wall_list : arcade.SpriteList[arcade.Sprite]
    coin_list : arcade.SpriteList[arcade.Sprite]
    no_go_list : arcade.SpriteList[arcade.Sprite]
    monster_list : arcade.SpriteList[arcade.Sprite]
    #variable qui va stocker les vitesses de chaque monstre
    m_speed : list[int]
    m_speed = [] 
    camera: arcade.camera.Camera2D
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    #Taille d'un "carreau" de la grille définie dans readmap
    Grid_size = 64


    
    # initialisation des variables pour le son 

    coin_sound = arcade.load_sound(":resources:/sounds/coin4.wav")
    jump_sound = arcade.load_sound(":resources:/sounds/jump3.wav")
    game_over_sound = arcade.load_sound(":resources:/sounds/gameover3.wav")

   
    """Lateral speed of the player, in pixels per frame."""
    
    #Ranger les sprites dans la bonne liste selon son asset
    def sprite_type(self, type : str, sprite: arcade.Sprite) -> None:
        if type == "Wall":
            self.wall_list.append(sprite)
        if type == "Coin":
              self.coin_list.append(sprite)
        if type == "Monster":
            self.monster_list.append(sprite)
            self.m_speed.append(-1)
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

        # ajout de l'épée
        self.sword = arcade.Sprite("assets/kenney-voxel-items-png/axe_gold.png",scale=0.5 * 0.7,)
        self.sword.visible = False
        self.sword_list = arcade.SpriteList()
        self.sword_list.append(self.sword)

        # declaration des variables utilisées pour l'épée
        self.sword_angle: float = 0.0
        self.sword_timer: float = 0.0
        self.SWORD_RADIUS_X = 20
        self.SWORD_RADIUS_Y = 30

        # Setup our game
        self.setup()
    
    def check_for_next_level(self) -> None:
        exit_list = arcade.check_for_collision_with_list(self.player_sprite, self.next_level_list)
        for exit in exit_list:
             All_maps.index += 1
             self.setup()

    def setup(self) -> None:
        """Set up the game here."""
        self.m_speed = []
        PLAYER_GRAVITY = 1

        #Initialiser les listes d'objets
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.no_go_list = arcade.SpriteList(use_spatial_hash=True)
        self.monster_list = arcade.SpriteList(use_spatial_hash=True)
        self.next_level_list = arcade.SpriteList(use_spatial_hash=True)
        
        MAP = All_maps.Maps[All_maps.index]
        #Création de la map
        for i in  range(len(MAP)):
            for j in range(len(MAP[i])):
                sprite = MAP[i][j] 
                if char_to_sprite(sprite) != (" ", " "):
                    asset = arcade.Sprite(char_to_sprite(sprite)[1],
                        center_y = (len(MAP) - i) * self.Grid_size,
                        center_x = j * self.Grid_size,
                        scale = 0.5
                    )
                    self.sprite_type(char_to_sprite(sprite)[0], asset)
                
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls = self.wall_list,
            gravity_constant=PLAYER_GRAVITY,
        )
        self.camera = arcade.camera.Camera2D()
        

    #Variables booléennes qui détectent quand les touches sont appuyées
    key_right : bool = False
    key_left : bool = False

    

    def on_mouse_press(self, x:int, y:int, button:int, modifiers: int) -> None :
        if arcade.MOUSE_BUTTON_LEFT :
            self.sword.visible = True
            #self.sword_timer = 0.2

            # Positionner l'épée en fonction de l'angle
            self.update_sword_orientation(x,y)
            
    def on_mouse_release(self, x:int, y:int, button:int, modifiers:int) -> None :
            self.sword.visible = False

    def update_sword_orientation(self,mouse_x: float, mouse_y: float) -> float:
        """
        Calcule la position et l'angle de l'épée pour que le manche reste fixé
        vers le personnage et que le placement se fasse le long d'un ovale.
        """
        # Conversion des coordonnées de la souris (écran) en coordonnées du monde
        world_x = mouse_x + self.camera.position[0] - (self.WINDOW_WIDTH / 2)
        world_y = mouse_y + self.camera.position[1] - (self.WINDOW_HEIGHT / 2)
        # Point de référence pour le personnage (on décale verticalement si besoin)
        ref_x = self.player_sprite.center_x
        ref_y = self.player_sprite.center_y   # ajustez ce décalage pour "baisser" le point de référence
        # Calcul de l'angle entre le point de référence et le clic (en radians)
        angle = math.atan2(ref_x - world_x,ref_y - world_y)
        # Appliquer la rotation à l'image (toujours +45° pour correspondre à l'orientation de l'image de base)
        self.sword.angle = math.degrees(angle) + 135
        return angle
    
    def update_sword_position(self) -> None:
         
        sword_r = math.radians(self.sword.angle - 45)
        vec = (30 * math.cos(sword_r), 30 * math.sin(-sword_r))
        self.sword.center_x = self.player_sprite.center_x + vec[0]
        self.sword.center_y = self.player_sprite.center_y + vec[1]
    
    # fonction qui detecte si l'épée touche un blob

    def check_sword_hit_monster(self)->None:
        monsters_hit= []
        if self.sword.visible == True:
            monsters_hit = arcade.check_for_collision_with_list(self.sword,self.monster_list)
            for monster in monsters_hit:
                monster.remove_from_sprite_lists()
        
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
            self.sword_list.draw()
            self.next_level_list.draw()


    #fonction de control de camera
    def cam_control(self) -> None:
         player_x = self.player_sprite.center_x
         player_y = self.player_sprite.center_y
         #Calcule des "Bords" de la caméra:
         right_edge = self.camera.position[0] + (self.WINDOW_WIDTH / 2) - 410
         left_edge = self.camera.position[0] - (self.WINDOW_WIDTH / 2) + 410
         upper_edge = self.camera.position[1] + (self.WINDOW_HEIGHT / 2) - 300
         down_edge = self.camera.position[1] - (self.WINDOW_HEIGHT / 2) + 250

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
         i = 0
         for blob in self.monster_list:
            collision = self.blob_collision(blob, self.m_speed[i])
            if collision == True:
                 #si il y a une collision, la vitesse du blob est inversée ainsi que sa position
                 self.m_speed[i] *= -1
                 blob.scale_x *= -1
            blob.change_x = self.m_speed[i]
            i += 1
         self.monster_list.update()
    
    #Fonction qui détecte les collisions
    def blob_collision(self, blob: arcade.Sprite, change_x : int) -> bool:
        #point en dessous du blob pour les collision sur les bords
        point_y = blob.bottom - (self.Grid_size / 2)
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
    
    """Main in-game view."""
    def on_update(self, delta_time: float) -> None:
        self.player_sprite.center_x += self.player_sprite.change_x
        self.physics_engine.update()

        self.check_for_next_level()
        self.cam_control()

        coin_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hit:
            coin.remove_from_sprite_lists()
        #son
            arcade.play_sound(self.coin_sound)

        #update position de l'épée 
        self.update_sword_position()

        #check si l'épée touche un monstre
        self.check_sword_hit_monster()
        if self.sword_timer > 0:
            self.sword_timer -= delta_time
            if self.sword_timer <= 0:
                self.sword.visible = False

        #position du blob
        self.blob_position()

        # game over si le joueur entre en collsion avec la lave
        lava_hit =  arcade.check_for_collision_with_list(self.player_sprite, self.no_go_list)
        for lava in lava_hit:
            self.setup()
        # son 
            arcade.play_sound(self.game_over_sound)

        # game over si le joueur entre en collision un monstre
        monster_hit =  arcade.check_for_collision_with_list(self.player_sprite, self.monster_list)
        for monster in monster_hit:
            self.setup()
        # son 
            arcade.play_sound(self.game_over_sound)
    
             



