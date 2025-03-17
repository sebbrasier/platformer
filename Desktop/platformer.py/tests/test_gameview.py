import arcade

from gameview import *
from readmap import *
from readmap import Map_game


#test ouverture du fichier map
def test_map() -> None:
    #Bien vérifier que l'on a extrait les bonnes informations du text "map"
    assert Map_game.setup[0][0] == "*"
    assert Map_game.dim == (20, 6)
    #Vérifier que la fonction qui lit des fichier gère correctement les exceptions
    file = "non_existent_file.txt"
    assert(lecture_map(file) == [])
    #Vérifier que cela s'ouvre correctement avec le fichier map1.txt:
    file2 = "maps/map1.txt"
    assert(lecture_map(file2) != [])


# test la collision des blobs
def test_blob(window: arcade.Window) -> None:
    view = GameView()
    window.show_view(view)
    monster_TABLE = view.monster_TABLE.monsters
    window.test(30)
    i = 0
    #Vérifie que les premières secondes, le blob collisionne avec rien
    for monster in monster_TABLE:
        change_x = monster.speed
        assert view.blob_collision(monster.type, change_x) == False
        i += 1
    window.test(15)
    #Vérifie que le blob change de diréction apres collision
    for i in range(60):
        monst = view.monster_TABLE[0]
        if (view.blob_collision(monst.type, monst.speed) == True):
            assert monst.speed == -1
            assert monst.type.scale_x == 0.5
        window.test(1)

    
#test que l'on revient bien au début apres avoir touché un blob et de la lave
def test_death(window: arcade.Window) -> None:
    view = GameView()
    window.show_view(view)
    view.player_sprite.center_y += 128
    view.player_sprite.center_x += 256
    window.test(25)
    assert view.player_sprite.center_x == 64
    assert view.player_sprite.center_y == 128
    view.player_sprite.center_x += 512
    window.test(25)
    assert view.player_sprite.center_x == 64
    assert view.player_sprite.center_y == 128


#test sauts multiples
def test_jump(window: arcade.Window) -> None:
    view = GameView()
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
    window.show_view(view)

    cam_i = view.camera.position[0]
    left_edge = cam_i - (view.WINDOW_WIDTH / 2) + 410
    view.on_key_press(arcade.key.LEFT, 0)
    window.test(10)
    view.on_key_release(arcade.key.LEFT, 0)
    player_x = view.player_sprite.center_x
    cam_f = view.camera.position[0]
    assert (cam_f == cam_i - abs(player_x - left_edge))
    window.test(30)

#test character sprite keeps moving after one key is released

def test_left_right_keys(window: arcade.Window) -> None:
    view = GameView()
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

def test_sword_hits_blob(window: arcade.Window) -> None:
    """
    Test que l'épée tue bien les blobs lorsqu'elle entre en collision.
    """
    view = GameView()
    window.show_view(view)
    
    # Créer un blob et le placer à la même position que le joueur.
    blob = arcade.Sprite(":resources:/images/enemies/slimePurple.png", scale=0.5)
    blob.center_x = view.player_sprite.center_x
    blob.center_y = view.player_sprite.center_y
    view.monster_list.append(blob)
    view.m_speed.append(-1)
    
    # Rendre l'épée visible et la positionner sur le blob.
    view.sword.visible = True
    view.sword.center_x = blob.center_x
    view.sword.center_y = blob.center_y
    
    # Vérifier que la collision supprime le blob
    view.check_sword_hit_monster()
    assert blob not in view.monster_list


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
    assert All_maps.index == 0


def test_sword_appears_on_click(window: arcade.Window) -> None:
    """
    Test que l'épée apparaît bien lors d'un clic de souris.
    """
    view = GameView()
    window.show_view(view)
    
    # S'assurer que l'épée est initialement invisible.
    view.sword.visible = False
    
    # Simuler un clic gauche de souris à des coordonnées arbitraires 
    view.on_mouse_press(150, 150, arcade.MOUSE_BUTTON_LEFT, 0)
    
    # Vérifier que l'épée est visible
    assert view.sword.visible
    window.test(5)


def test_map_transition(window: arcade.Window) -> None:
    """
    Test que la collision avec le panneau de sortie (exit panel) fait passer de la map 1 à la map 2.
    """
    # Forcer l'index de la map à 0 pour démarrer sur map 1
    All_maps.index = 0
    
    view = GameView()
    window.show_view(view)
    
    # Créer un sprite de panneau de sortie et le placer sur le joueur
    exit_panel = arcade.Sprite(":resources:/images/tiles/signExit.png", scale=0.5)
    exit_panel.center_x = view.player_sprite.center_x
    exit_panel.center_y = view.player_sprite.center_y
    view.next_level_list.append(exit_panel)
    
    # Vérifier que la collision avec le panneau incrémente bien l'index de la map
    view.check_for_next_level()
    assert All_maps.index == 1
    window.test(5)