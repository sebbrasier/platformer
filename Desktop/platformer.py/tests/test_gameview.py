import arcade

from gameview import *
from readmap import *


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