import arcade
from readmap import *
import math
from typing import Tuple
from abc import abstractmethod
from All_monsters.monsters import *
from All_weapons.weapons import *
from All_items.interuptor import *
from All_items.gate import *
from pyglet.math import Vec2
from moving_platform import *

#Variables globales
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
#Taille d'un "carreau" de la grille définie dans readmap
Grid_size = 64
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

    #Initialisation des listes pour stocker les sprites ainsi que la classe de platformes
    platform_list : arcade.SpriteList[arcade.Sprite]
    platform_class_list : list[moving_platform]

    #Initialisation des listes pour stocker les sprites ainsi que la classe des flèches
    arrow_list : arcade.SpriteList[arcade.Sprite]
    arrow_class_list : list[Arrow]
    gate_list : arcade.SpriteList[arcade.Sprite]
    inter_list : arcade.SpriteList[arcade.Sprite]
    inter_class_list :list[Inter]
    gate_class_list : list[Gate]

    #liste pour platformes qui se cassent
    drop_platform_list : list[moving_platform]
    drop_bool : bool 
    timer_started : bool 
    timer : float
    

    #Cette liste va permettre de ranger les instances de la class "monster"
    monster_TABLE : monster_table

    #UI elements
    camera: arcade.camera.Camera2D
    UI_camera : arcade.camera.Camera2D
    level_score : int

    #ajout des armes
    sword : Sword
    bow : Bow

    #Initialiser la liste de fichiers
    file_list : Map_list

    def __init__(self) -> None:
        super().__init__()
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
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
        self.error_sound = arcade.load_sound(":resources:/sounds/error5.wav")

        #Initialisation des listes de fichiers
        self.file_list = Map_list([ "maps/map5.txt","maps/map4.txt", "maps/map1.txt", "maps/map2.txt", "maps/map3.txt"], 0) 

        # Setup our game
        self.setup(self.file_list.Maps[self.file_list.index])

    def setup(self, MAP_file : str) -> None:
    
        # lecture de la partie yaml du fichier map
        config  = load_map_config(MAP_file)
        self.weapon_disable_zones: list[Tuple[int,int,int,int]] = []
        # ajoute les coordonnées de chaque zone dans une list de Tuple différentes pour les 2 types de zones
        for z in config.get("weapon_disable_zones", []):
            self.weapon_disable_zones.append((
                int(z["x1"]),
                int(z["y1"]),
                int(z["x2"]),
                int(z["y2"]),
            ))
        self.gravity_inverse: list[Tuple[int,int,int,int]] = []
        for z in config.get("gravity_inverse_zones", []):
            self.gravity_inverse.append((
                int(z["x1"]),
                int(z["y1"]),
                int(z["x2"]),
                int(z["y2"]),
            ))

        """Set up the game here."""
        PLAYER_GRAVITY = 1

        #Initialiser les listes d'objets
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.weapon_icon_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.no_go_list = arcade.SpriteList(use_spatial_hash=True)
        self.monster_list = arcade.SpriteList()
        self.next_level_list = arcade.SpriteList(use_spatial_hash=True)
        self.player_sprite_list = arcade.SpriteList()
        self.arrow_list = arcade.SpriteList()
        self.weapon_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.platform_class_list = []
        self.arrow_class_list = []
        self.monster_TABLE = monster_table([])
        self.gate_list = arcade.SpriteList()
        self.inter_list = arcade.SpriteList()
        self.inter_class_list = []
        self.gate_class_list = []
        self.drop_platform_list = []
        self.level_score = 0
        
        MAP = Map(dim(MAP_file), lecture_map(MAP_file))
        #Ajout des platformes qui bougent
        moving_arrow_dict_RIGHT = AddPlatform.read_arrows_right(MAP, map_symbols.RIGHT, lambda a, b : a)
        moving_arrow_dict_LEFT = AddPlatform.read_arrows_right(LinAlgebra.flip_matrix(MAP), map_symbols.LEFT, LinAlgebra.flip_vector)
        horizontal = AddPlatform.combine_right_left(moving_arrow_dict_LEFT, moving_arrow_dict_RIGHT, MAP)
        moving_arrow_dict_DOWN = AddPlatform.read_arrows_right(LinAlgebra.transpose_matrix(MAP), map_symbols.DOWN, LinAlgebra.transpose_vec)
        moving_arrow_dict_UP = AddPlatform.read_arrows_right(LinAlgebra.flip_matrix(LinAlgebra.transpose_matrix(MAP)), map_symbols.UP, LinAlgebra.flip_transpose_vec)
        vertical = AddPlatform.combine_right_left(moving_arrow_dict_DOWN, moving_arrow_dict_UP, MAP)
        #Check pour des erreurs
        AddPlatform.duplicate_checker(horizontal, vertical)
        platform_set : set[tuple[int, int]] = {a for e in horizontal for a in e} | {a for e in vertical for a in e}
        #On rajoute tout d'abord toutes les platformes
        self.add_platform_x(horizontal, MAP)
        self.add_platform_y(vertical, MAP)

        #Création de la map
        #On place les sprites au bon endroit
        for i in  range(len(MAP.setup)):
            for j in range(len(MAP.setup[i])):
                if (i, j) not in platform_set:
                    sprite = MAP.setup[i][j] 
                    if enum_to_sprite(sprite) != (" ", " "):
                        #Créer un sprite par rapport au (i, j)ième élément de la map
                        asset = arcade.Sprite(enum_to_sprite(sprite)[1],
                            center_y = (len(MAP.setup) - i) * Grid_size,
                            center_x = j * Grid_size,
                            scale = 0.5
                        )
                        map_x = j
                        map_y = len(MAP) - 1 - i
                        self.sprite_type(enum_to_sprite(sprite)[0], asset, map_x, map_y)
         
        #Physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=  self.player_sprite,
            platforms=self.platform_list,
            walls = self.wall_list,
            gravity_constant=PLAYER_GRAVITY,
        )
        #ajoute les gate à la liste des wall pour qu'ils aient le même effet
        self.wall_list.extend(self.gate_list)

        #fait le lien entre les switch et gate comme indiqué dans le yaml  
        init_gate_states_from_config(config,self.gate_class_list,self.wall_list)
        link_inter_to_gates(config,self.inter_class_list,self.gate_class_list,self.wall_list)     

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
        
        #Initialisation des icones
        self.sword_repr = arcade.Sprite("assets/kenney-voxel-items-png/axe_gold.png", scale = 0.5, center_x=60, center_y = 550)
        self.bow_repr = arcade.Sprite("assets/kenney-voxel-items-png/bowArrow.png", scale = 0.5, center_x=60, center_y = 550)
        self.no_weapon_repr = arcade.Sprite("assets/kenney_board-game-icons/PNG/hand_cross.png", scale = 0.5, center_x=60, center_y = 450)
        self.gravity_change = arcade.Sprite("assets/kenney_board-game-icons/PNG/character_lift.png", scale = 0.5, center_x=60, center_y = 350)

        self.weapon_icon_list.append(self.sword_repr)
        self.weapon_icon_list.append(self.bow_repr)
        self.weapon_icon_list.append(self.no_weapon_repr)
        self.weapon_icon_list.append(self.gravity_change)

        for icon in self.weapon_icon_list:
            icon.visible = False
        self.weapon_icon_list[self.active_weapon.index].visible = True

    
    def add_platform_x(self, platforms : dict[frozenset[tuple[int, int]], tuple[tuple[map_symbols, ...], tuple[map_symbols, ...]]], MAP : Map) -> None:
        """Fonction qui rajoute toutes les platformes verticales"""
        for a in platforms:
            sequence = platforms[a]
            for vec in a:
                i = vec[0]
                j = vec[1]
                sprite = MAP.setup[i][j] 
        
                if enum_to_sprite(sprite) != (" ", " "):
                    #Créer un sprite par rapport au (i, j)ième élément de la map
                    asset = arcade.Sprite(enum_to_sprite(sprite)[1],
                        center_y = (len(MAP.setup) - i) * Grid_size,
                        center_x = j * Grid_size,
                        scale = 0.5
                    )
                    
                    asset_class = moving_platform_x(asset, 1, sequence[1], sequence[0])
                    asset_class.platform.boundary_right = asset_class.boundary_right
                    asset_class.platform.boundary_left = asset_class.boundary_left
                    asset_class.platform.change_x = asset_class.speed
                    #selon le type de sprite, il est ajouté ou non dans la liste de platformes
                    if sprite in special_plat:
                        map_x = j
                        map_y = len(MAP) - 1 - i
                        self.sprite_type(enum_to_sprite(sprite)[0], asset, map_x, map_y)
                        self.platform_class_list.append(asset_class)
                    else:
                        self.platform_list.append(asset_class.platform)
                    if sprite == map_symbols.Break:
                        self.drop_platform_list.append(asset_class)
                
    
    def add_platform_y(self, platforms : dict[frozenset[tuple[int, int]], tuple[tuple[map_symbols, ...], tuple[map_symbols, ...]]], MAP : Map) -> None:
        """Fonction qui rajoute les platformes horizontales
           Un peu de duplication de code quand il s'agit de créer le sprite, mais il n'y a pas moyen de rajouter les platformes
           verticales et horizontales en meme temps avec le code actuel"""
        for a in platforms:
            sequence = platforms[a]
            for vec in a:
                i = vec[0]
                j = vec[1]
                sprite = MAP.setup[i][j] 
                if enum_to_sprite(sprite) != (" ", " "):
                    #Créer un sprite par rapport au (i, j)ième élément de la map
                    asset = arcade.Sprite(enum_to_sprite(sprite)[1],
                        center_y = (len(MAP.setup) - i) * Grid_size,
                        center_x = j * Grid_size,
                        scale = 0.5
                    )
                    asset_class = moving_platform_y(asset, 1, sequence[1], sequence[0])
                    asset_class.platform.boundary_top = asset_class.boundary_right
                    asset_class.platform.boundary_bottom = asset_class.boundary_left
                    asset_class.platform.change_y = asset_class.speed
                    #selon le type de sprite, il est ajouté ou non dans la liste de platformes
                    if sprite in special_plat:
                        map_x = j
                        map_y = len(MAP) - 1 - i
                        self.sprite_type(enum_to_sprite(sprite)[0], asset, map_x, map_y)
                        self.platform_class_list.append(asset_class)
                    else:
                        self.platform_list.append(asset_class.platform)
                    if sprite == map_symbols.Break:
                        self.drop_platform_list.append(asset_class)
    
    def check_for_next_level(self) -> None:
        """Fonction qui détecte si le joueur collisionne avec le paneau"""
        exit_list = arcade.check_for_collision_with_list(self.player_sprite, self.next_level_list)
        for exit in exit_list:
             self.file_list.index = (1 + self.file_list.index) % len(self.file_list)
             #reset maps once we hit the end
             self.setup(self.file_list.Maps[self.file_list.index])
    
    def sprite_type(self, type: str, sprite: arcade.Sprite, map_x: int, map_y: int) -> None:
        """Cette fonction range les sprites selon son asset"""
        if type == "Wall":
            self.wall_list.append(sprite)
        if type == "Coin":
              self.coin_list.append(sprite)
        if type == "Chauve-souris":
            self.monster_list.append(sprite)
            chauve_S = chauve_souris(sprite,1, 100, 0.01)
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
        # pour gate et inter on les ajoute aussi dans des "class_list" pour pouvoir les gérer en tant que sprite ET gate/Inter
        if type == "gate":
            gate = Gate(sprite,map_x, map_y)
            self.gate_list.append(sprite)
            self.gate_class_list.append(gate)
        if type == "inter": 
            lever = Inter(sprite,False,map_x,map_y)
            self.inter_list.append(lever.sprite)        
            self.inter_class_list.append(lever)
        if type == "Break":
            empt : tuple[map_symbols, ...] = ()
            asset_class = moving_platform_x(sprite, 0, empt,empt) 
            self.drop_platform_list.append(asset_class)
            self.wall_list.append(asset_class.platform)

        
    #Variables booléennes qui détectent quand les touches sont appuyées
    key_right : bool = False
    key_left : bool = False

    
    def create_arrow(self) -> arcade.Sprite:
        """Fonction qui "crée" une flèche"""
        arrow = arcade.Sprite("assets/kenney-voxel-items-png/arrow.png",scale=0.3)
        arrow.visible = False
        self.arrow_list.append(arrow)
        return arrow
    
    
    def can_jump_homemade(self,gravity_index : int, y_distance: float = 5.0) -> bool:
        """Fonction qui fait comme le can_jump de arcade de base mais qui marche aussi quand le joueur est à l'envers dû à la gravité inverse"""
        offset = - y_distance * gravity_index
        self.player_sprite.center_y += offset

        hits = arcade.check_for_collision_with_list(self.player_sprite,self.wall_list)
        hits += arcade.check_for_collision_with_list(self.player_sprite,self.platform_list)
        self.player_sprite.center_y -= offset
        
        return len(hits) > 0
    
    
    def on_mouse_press(self, x:int, y:int, button:int, modifiers: int) -> None :
        """Définit tout ce qui se passe quand le joueur appuye sur le click gauche"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            #calcul de la zone de non arme
            position_x = int(self.player_sprite.center_x // Grid_size)
            position_y = int(self.player_sprite.center_y // Grid_size)
            for x1, y1, x2, y2 in self.weapon_disable_zones:
                if x1 <= position_x <= x2 and y1 <= position_y <= y2:
                    arcade.play_sound(self.error_sound)
                    self.no_weapon_repr.color = arcade.color.RED
                    self.no_weapon_repr.visible = True
                    # on est dans une zone où l'arme est désactivée
                    return
            #Fait appraitre l'arme que l'on a sélectionné, indiqué par active_weapon.index
            weapon : Weapon
            weapon = self.active_weapon.weapons[self.active_weapon.index]
            self.Allow_change_weapon = False
            # active le fait que l'épée puisse fonctionner lors de la frame du clic
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
            self.no_weapon_repr.visible = False
            self.no_weapon_repr.color = arcade.color.WHITE
        
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""
        PLAYER_MOVEMENT_SPEED = 6
        PLAYER_JUMP_SPEED = 18
        
        if key == arcade.key.RIGHT:
            # se déplace à droite
            self.player_sprite.change_x = + PLAYER_MOVEMENT_SPEED
            self.key_right = True
    
        if key == arcade.key.LEFT:
            # se déplace à gauche
            self.player_sprite.change_x = - PLAYER_MOVEMENT_SPEED
            self.key_left = True

        gravity_constant : int = 1
        position_x = int(self.player_sprite.center_x // Grid_size)
        position_y = int(self.player_sprite.center_y // Grid_size)
        for x1, y1, x2, y2 in self.gravity_inverse:
            if x1 <= position_x <= x2 and y1 <= position_y <= y2:
                gravity_constant = -1
                break
        if key == arcade.key.UP and self.can_jump_homemade(gravity_constant): 

            self.player_sprite.change_y = PLAYER_JUMP_SPEED * gravity_constant 
            #son
            arcade.play_sound(self.jump_sound)

        if key == arcade.key.ESCAPE:
            self.coin_score.points = max(self.coin_score.points - self.level_score, 0)
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
            self.platform_list.draw()
            self.no_go_list.draw()
            self.coin_list.draw()
            self.weapon_list.draw()
            self.next_level_list.draw()
            self.arrow_list.draw()
            self.gate_list.draw()
            self.inter_list.draw()
            self.monster_list.draw()
            
        with self.UI_camera.activate():
            arcade.draw_text(f"SCORE: {self.coin_score.points}", 10,650, arcade.color.WHITE, 20,font_name="Kenney Future")
            self.weapon_icon_list.draw()


    #fonction de control de camera
    def cam_control(self) -> None:
         """ Cette fonction adapte la camera selon la position du joueur"""
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
        """ Cette fonction relance set up si le joueur touche un sprite de la liste danger ou si le joueur tombre trop bas """
        hit : list[arcade.Sprite]
        hit = arcade.check_for_collision_with_list(self.player_sprite, danger)
        for elements in hit:
            #On appelle setup dès que l'on meurt
            self.file_list.index = 0
            self.setup(self.file_list.Maps[self.file_list.index])
            self.coin_score.erase
            arcade.play_sound(self.game_over_sound)
        # son 
        if self.player_sprite.center_y <= -300:
            self.file_list.index = 0
            self.setup(self.file_list.Maps[self.file_list.index])
            self.coin_score.erase
            arcade.play_sound(self.game_over_sound)

 
    def in_zone(self)->None:
        """ Cette fonction vérifie si on est dans une zones et met à jour la gravité et les icones en fonction """
        # savoir si on rentre dans la no_weapon zone
        position_x = int(self.player_sprite.center_x // Grid_size)
        position_y = int(self.player_sprite.center_y // Grid_size)

        self.physics_engine.gravity_constant = 1
        self.player_sprite.angle = 0
        self.no_weapon_repr.visible = False
        self.gravity_change.visible = False

        # verification de si le joueur est dans une des zones
        for x1, y1, x2, y2 in self.weapon_disable_zones:
            if x1 <= position_x <= x2 and y1 <= position_y <= y2:
                self.no_weapon_repr.visible = True
        for x1, y1, x2, y2 in self.gravity_inverse:
            if x1 <= position_x <= x2 and y1 <= position_y <= y2:
                self.physics_engine.gravity_constant = - self.physics_engine.gravity_constant
                self.player_sprite.angle = 180
                self.gravity_change.visible = True
                break
    
    def coin_hit(self)->None:
        """Fonction qui verifi si le joueur touche une pièce et qui change le score en fonction"""
        coin_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hit:
            coin.remove_from_sprite_lists()
            self.coin_score.points += 1
            self.level_score += 1
        
            arcade.play_sound(self.coin_sound)

    """Main in-game view."""
    def on_update(self, delta_time: float) -> None:
        self.physics_engine.update()
        # update des listes
        self.monster_list.update()
        self.no_go_list.update()
        self.inter_list.update()
        self.next_level_list.update()
        self.in_zone() 
        self.check_for_next_level()
        self.cam_control()
        self.coin_hit()

        #update position de l'arme sur l'écran
        weapon = self.active_weapon.weapons[self.active_weapon.index]
        weapon.camera_position = self.camera.position
        weapon.player_sprite = self.player_sprite
        weapon.update_weapon_position()
        weapon.check_hit_monsters(self.monster_list)

        #Update la position des platformes non-controlées par arcade
        for e in self.platform_class_list:
            e.move()
        
        #Update position des flèches:
        for arrow in self.arrow_list:
            arrow.change_y -= 1.5
        self.arrow_list.update()

        #check si on touche un interupteur
        for inter in self.inter_class_list:
            if weapon.check_hit_inter(inter.sprite) == True and self.active_weapon.index == 0:
                inter.trigger()
            for arrows in self.arrow_class_list:
                if arrows.check_hit_inter(inter.sprite) == True:
                    inter.trigger()
            
        #Check si les flèches touchent les monstres
        for arrows in self.arrow_class_list:
            if arrows.arrow_collision(self.no_go_list, self.monster_list, self.wall_list, self.platform_list, self.inter_list) is True:
                self.arrow_class_list.remove(arrows)
                self.arrow_list.remove(arrows.attribute)
            arrows.check_hit_monsters(self.monster_list)
        
        #position du blob
        for monster in self.monster_TABLE.monsters:
            monster.monster_position(self.no_go_list, self.wall_list)

        #platformes qui se cassent
        for e in self.drop_platform_list:
            if e.is_under(self.player_sprite) is True:
                e.start_timer = True
            if e.start_timer:
                e.timer += delta_time
            if e.timer >= 0.5:
                e.is_dropped = True
                e.start_timer = False
                e.timer = 0.0
            if e.is_dropped is True:
                e.drop()
            e.go_up()          

        #Detection de la collision avec la lave et les blobs:
        self.game_over(self.no_go_list)
        self.game_over(self.monster_list)
        # reintialise le can_kill a False pour que l'épée puisse faire des actions seulement pendant l'image du clic
        Sword.can_kill = False




