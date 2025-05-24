import arcade

from gameview import *
from readmap import *
import math
    
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

    #Gauche
    cam_i = view.camera.position[0]
    left_edge = cam_i - (WINDOW_WIDTH / 2) + 410
    window.test(20)
    view.player_sprite.center_x -= 600
    window.test(20)
    player_x = view.player_sprite.center_x
    cam_f = view.camera.position[0]
    assert (cam_f == cam_i - abs(player_x - left_edge))

    #Droite
    cam_i = view.camera.position[0]
    right_edge = cam_i + (WINDOW_WIDTH / 2) - 410  
    window.test(20)
    view.player_sprite.center_x += 600
    window.test(20)
    player_x = view.player_sprite.center_x
    cam_f = view.camera.position[0]
    assert cam_f == cam_i + abs(player_x - right_edge)

    # Haut 
    cam_i = view.camera.position[1]
    upper_edge = cam_i + (WINDOW_HEIGHT / 2) - 300
    window.test(20)
    view.player_sprite.center_y += 400
    window.test(1)
    player_y = view.player_sprite.center_y
    cam_f = view.camera.position[1]
    assert cam_f == cam_i + abs(player_y - upper_edge)
    window.test(20)

    # Bas 
    cam_i = view.camera.position[1]
    down_edge = cam_i - (WINDOW_HEIGHT / 2) + 250
    window.test(20)
    view.player_sprite.center_y -= 1000
    window.test(1)
    player_y = view.player_sprite.center_y
    cam_f = view.camera.position[1]
    assert cam_f == cam_i - abs(player_y - down_edge)


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
    

<<<<<<< HEAD

=======
>>>>>>> f3b1f9b336f89f6b394fc5283b6e28b9e3a6287c
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
