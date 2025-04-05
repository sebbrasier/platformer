import arcade

from gameview import *
from readmap import *
import math


#test ouverture du fichier map
def test_map() -> None:
    view = GameView()
    map_test = """
                width: 3
                height: 2
                ---
                S E
                ===
                ---"""
    view.setup(map_test)
    #Bien vérifier que l'on a extrait les bonnes informations du text "map"
    assert(lecture_map(map_test) != [])
    #Vérifier que la fonction qui lit des fichier gère correctement les exceptions
    map_test = "non_existent_file.txt"
    view.setup(map_test)
    assert(lecture_map(map_test) == [])



# test la collision des blobs
def test_blob(window: arcade.Window) -> None:
    view = GameView()
    view.setup("maps/map_tests/blob_colision.txt")
    window.show_view(view)
    window.test(50)
    blob1 : blob
    if isinstance(view.monster_TABLE.monsters[0],blob):
        blob1 = view.monster_TABLE.monsters[0]
    # Avant la collision, la vitesse est 1
    vitesse_initiale = blob1.speed
    window.test(50)
    # Après collision, on attend que la vitesse soit inversée.
    assert blob1.speed == -vitesse_initiale

    
#test que l'on revient bien au début apres avoir touché un blob et de la lave
def test_death(window: arcade.Window) -> None:
    view = GameView()
    view.setup("maps/map_tests/death.txt")
    window.show_view(view)

    window.test(50)
    # on place le joueur sur la lave
    view.player_sprite.center_x += 64
    # on vérifie qu'il est bien revenu a la position initiale
    assert view.player_sprite.center_x == 64
    assert view.player_sprite.center_y == 128
    window.test(25)
    



#test sauts multiples
def test_jump(window: arcade.Window) -> None:
    view = GameView()
    view.setup("maps/map_tests/jump.txt")
    window.show_view(view)
    view.on_key_press(arcade.key.UP, 0)
    view.on_key_release(arcade.key.UP, 0)
    window.test(30)
    view.on_key_press(arcade.key.UP, 0)
    assert (view.player_sprite.change_y != 18)
    view.on_key_release(arcade.key.UP, 0)
    window.test(30)
    view.on_key_press(arcade.key.UP, 0)
    assert (view.player_sprite.change_y == 18)
    window.test(30)

#test camera follow character
def test_camera(window: arcade.Window) -> None:
    view = GameView()
    view.setup("maps/map_tests/camera.txt")
    window.show_view(view)

    cam_i = view.camera.position[0]
    left_edge = cam_i - (WINDOW_WIDTH / 2) + 410
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(50)
    view.on_key_release(arcade.key.LEFT, 0)
    player_x = view.player_sprite.center_x
    cam_f = view.camera.position[0]
    assert (cam_f == cam_i - abs(player_x - left_edge))
    window.test(50)

#test character sprite keeps moving after one key is released

def test_left_right_keys(window: arcade.Window) -> None:
    view = GameView()
    view.setup("maps/map_tests/camera.txt")
    window.show_view(view)
    
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(15)
    view.on_key_press(arcade.key.LEFT, 0)
    view.on_key_release(arcade.key.RIGHT, 0)
    x = view.player_sprite.position
    window.test(15)

    assert(x != view.player_sprite.position)
    

# test que la touche echap pour reset le jeu fonctionne bien

def test_reset_with_escape(window: arcade.Window) -> None:
    view = GameView()
    window.show_view(view)

    # le joueur se déplace
    view.player_sprite.center_x += 200

    # Appuyer sur ECHAP pour réinitialiser
    view.on_key_press(arcade.key.ESCAPE, 0)

    # Vérifier que le joueur est revenu à sa position initiale
    assert view.player_sprite.center_x == 64
    assert view.player_sprite.center_y == 128

def test_sword(window: arcade.Window) -> None:
    
    view = GameView()
    view.setup("maps/map_tests/sword.txt")
    window.show_view(view)

    # Récupérer l'épée active via active_weapon (l'épée est à l'indice 0).
    sword = view.active_weapon.weapons[0]
    # S'assurer que l'épée est invisible au début
    assert not sword.attribute.visible
    window.test(25)
    # Simuler un clic gauche de souris à des coordonnées arbitraires
    view.on_mouse_press(150, 150, arcade.MOUSE_BUTTON_LEFT, 0)

    # Vérifier que l'épée est visible après le clic
    assert sword.attribute.visible
    window.test(25)
    view.player_sprite.center_x += 250
    window.test(50)

    blob1 : blob
    if isinstance(view.monster_TABLE.monsters[0],blob):
        blob1 = view.monster_TABLE.monsters[0]

    # Rendre l'épée visible et positionner son sprite sur le blob.
    Sword.can_kill = True
    sword.attribute.visible = True
    view.on_mouse_press(500,100, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(100)

    # Vérifier que le sprite du blob a bien été retiré de la liste des monstres.
    assert len(view.monster_list) == 0


def test_score_reset_after_game_over(window: arcade.Window) -> None:
    """
    Test que le score se réinitialise après un game over.
    """
    view = GameView()
    window.show_view(view)
    
    # Donner un score non nul
    view.coin_score.points = 10
    
    # Créer de la lave au même endroit que le joueur
    danger = arcade.Sprite(":resources:/images/tiles/lava.png", scale=0.5)
    danger.center_x = view.player_sprite.center_x
    danger.center_y = view.player_sprite.center_y
    view.no_go_list.append(danger)
    
    view.game_over(view.no_go_list)
    
    # Vérifier que le score est remis à zéro et que la map est réinitialisée 
    assert view.coin_score.points == 0
    assert view.file_list.index == 0


def test_map_transition(window: arcade.Window) -> None:
    """
    Test que la collision avec le panneau de sortie (exit panel) fait passer de la map 1 à la map 2.
    """
    # Forcer l'index de la map à 0 pour démarrer sur map 1
 
    
    view = GameView()
    view.file_list.index = 0
    window.show_view(view)
    
    # Créer un sprite de panneau de sortie et le placer sur le joueur
    exit_panel = arcade.Sprite(":resources:/images/tiles/signExit.png", scale=0.5)
    exit_panel.center_x = view.player_sprite.center_x
    exit_panel.center_y = view.player_sprite.center_y
    view.next_level_list.append(exit_panel)
    
    # Vérifier que la collision avec le panneau incrémente bien l'index de la map
    view.check_for_next_level()
    assert view.file_list.index == 1
    window.test(5)

def test_bat(window : arcade.Window) -> None:

    view = GameView()
    view.setup("maps/map_tests/bat.txt")
    window.show_view(view)

    bat1 : chauve_souris
    if isinstance(view.monster_TABLE.monsters[0],chauve_souris):
        bat1 = view.monster_TABLE.monsters[0]


    # on enlève l'effet aléatoire du mouvement de la chauve souris pour tester seulement si les bordures fonctionnent correctement
    #test pour les bordures en x
    bat1.random_dir = 0
    bat1.boundary = 40
    bat1.vx = 1
    bat1.vy = 0

    vitesse_initiale = bat1.vx
    window.test(50)
    # Après collision, on attend que la vitesse soit inversée.
    assert bat1.speed == -vitesse_initiale

    # test pour les bordures en y

    bat1.vx = 0
    bat1.vy = 1

    vitesse_initiale = bat1.vy
    window.test(50)
    # Après collision, on attend que la vitesse soit inversée.
    assert bat1.speed == -vitesse_initiale

def test_sword_orientation(window: arcade.Window) -> None:
    # Initialiser la vue et la map de test
    view = GameView()
    view.setup("maps/map_tests/jump.txt")
    window.show_view(view)
    
    # Forcer l'épée comme arme active (index 0)
    view.active_weapon.index = 0
    weapon = view.active_weapon.weapons[0]
    

    window.test(25)
    
    # Liste de cas à tester comme clic de souris
    test_cases = [
        (0, 0),
        (100, 100),
        (-100, -50),
        (200, -150),
        (-250, 300),
        (1000, 1000),
        (500, 0),
        (700, -150),
        (500, 300)
    ]
    # on calcul d'abord les coordonnées prévu avec nos calculs puis on verifie si c'est bien ou se trouve l'épée
    for mouse_x, mouse_y in test_cases:
        view.on_mouse_press(mouse_x, mouse_y, arcade.MOUSE_BUTTON_LEFT, 0)
        
        world_x = mouse_x + view.camera.position[0] - (WINDOW_WIDTH / 2)
        world_y = mouse_y + view.camera.position[1] - (WINDOW_HEIGHT / 2)
        ref_x = view.player_sprite.center_x
        ref_y = view.player_sprite.center_y
        angle = math.atan2(ref_x - world_x, ref_y - world_y)
        expected_angle = math.degrees(angle) + 140
        #on verifie si l'orientation est bonne avec une tolerance de 0,01 car on manipule des float
        assert math.isclose(weapon.attribute.angle, expected_angle, abs_tol=0.001)
        weapon.update_weapon_position()

        expected_weapon_r = math.radians(expected_angle - 50)
        expected_vec = (25 * math.cos(expected_weapon_r), 25 * math.sin(-expected_weapon_r))
        expected_center_x = view.player_sprite.center_x + expected_vec[0]
        expected_center_y = view.player_sprite.center_y - 15 + expected_vec[1]
        #on verifie si la direction est bonne avec une tolerance de 0,01 car on manipule des float
        assert math.isclose(weapon.attribute.center_x, expected_center_x, abs_tol=0.001)
        assert math.isclose(weapon.attribute.center_y, expected_center_y, abs_tol=0.001)
        window.test(10)

def test_bow_orientation(window: arcade.Window) -> None:
    # Initialiser la vue et la map de test
    view = GameView()
    view.setup("maps/map_tests/jump.txt")
    window.show_view(view)
    
    # Forcer l'arc comme arme active (indice 1, supposant que 0 est l'épée)
    view.active_weapon.index = 1
    weapon = view.active_weapon.weapons[1]
    
    window.test(25)
    
    # Liste de cas à tester comme clic de souris
    test_cases = [
        (0, 0),
        (100, 100),
        (-100, -50),
        (200, -150),
        (-250, 300),
        (1000, 1000),
        (500, 0),
        (700, -150),
        (500, 300)
    ]
    # on calcul d'abord les coordonnées prévu avec nos calculs puis on verifie si c'est bien ou se trouve l'arc
    for mouse_x, mouse_y in test_cases:
        view.on_mouse_press(mouse_x, mouse_y, arcade.MOUSE_BUTTON_LEFT, 0)
        
        world_x = mouse_x + view.camera.position[0] - (WINDOW_WIDTH / 2)
        world_y = mouse_y + view.camera.position[1] - (WINDOW_HEIGHT / 2)
        ref_x = view.player_sprite.center_x
        ref_y = view.player_sprite.center_y
        angle = math.atan2(ref_x - world_x, ref_y - world_y)
        expected_angle = math.degrees(angle) + 120
        
        #on verifie si l'orientation' est bonne avec une tolerance de 0,01 car on manipule des float
        assert math.isclose(weapon.attribute.angle, expected_angle, abs_tol=0.001)
        weapon.update_weapon_position()

        expected_weapon_r = math.radians(expected_angle - 50)
        expected_vec = (20 * math.cos(expected_weapon_r), 20 * math.sin(-expected_weapon_r))
        expected_center_x = view.player_sprite.center_x + expected_vec[0]
        expected_center_y = view.player_sprite.center_y - 15 + expected_vec[1]
        
        #on verifie si la direction est bonne avec une tolerance de 0,01 car on manipule des float
        assert math.isclose(weapon.attribute.center_x, expected_center_x, abs_tol=0.001)
        assert math.isclose(weapon.attribute.center_y, expected_center_y, abs_tol=0.001)
        window.test(10)



    



