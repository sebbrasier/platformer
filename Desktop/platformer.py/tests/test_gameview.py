import arcade

from gameview import *
from readmap import *
from readmap import Map_game


#test ouverture du fichier map
def test_map() -> None:
    #Bien vérifier que l'on a extrait les bonnes informations du text "map"
    assert Map_game.dim == (20, 7)
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

    # Créer un sprite pour le blob et le positionner
    blob_sprite = arcade.Sprite(":resources:/images/enemies/slimePurple.png", scale=0.5)
    blob_sprite.center_x = 100
    blob_sprite.center_y = 100

    blob_instance = blob(blob_sprite, 1)

    # On s'assure que les listes d'obstacles sont initialisées et vides
    view.wall_list = arcade.SpriteList()
    view.no_go_list = arcade.SpriteList()

    # On force une collision 
    obstacle = arcade.Sprite(":resources:/images/tiles/boxCrate_double.png", scale=0.5)
    obstacle.center_x = blob_sprite.right
    obstacle.center_y = blob_sprite.center_y
    view.wall_list.append(obstacle)

    # Avant la collision, la vitesse est 1
    vitesse_initiale = blob_instance.speed

    # Appeler la méthode qui gère la collision et le changement de direction.
    blob_instance.monster_position(view.no_go_list, view.wall_list)

    # Après collision, on attend que la vitesse soit inversée.
    assert blob_instance.speed == -vitesse_initiale

    
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
    left_edge = cam_i - (WINDOW_WIDTH / 2) + 410
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

    # Créer un sprite pour le blob et le placer à la position du joueur.
    blob_sprite = arcade.Sprite(":resources:/images/enemies/slimePurple.png", scale=0.5)
    blob_sprite.center_x = view.player_sprite.center_x
    blob_sprite.center_y = view.player_sprite.center_y
    view.monster_list.append(blob_sprite)

    # Créer une instance de blob et l'ajouter dans la table des blobs.
    blob_instance = blob(blob_sprite, -1)
    view.monster_TABLE.monsters.append(blob_instance)

    # Récupérer l'épée active via active_weapon (l'épée est à l'indice 0).
    sword = view.active_weapon.weapons[0]

    # Rendre l'épée visible et positionner son sprite sur le blob.
    Sword.can_kill = True
    sword.attribute.visible = True
    sword.attribute.center_x = blob_sprite.center_x
    sword.attribute.center_y = blob_sprite.center_y

    # Simuler l'attaque : l'épée vérifie les collisions et doit retirer le blob.
    sword.check_hit_monsters(view.monster_list)

    # Vérifier que le sprite du blob a bien été retiré de la liste des monstres.
    assert blob_sprite not in view.monster_list


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
    sword = view.active_weapon.weapons[0]  # 0 : indice de l'épée dans la liste

    # S'assurer que l'épée est invisible au début
    assert not sword.attribute.visible

    # Simuler un clic gauche de souris à des coordonnées arbitraires
    view.on_mouse_press(150, 150, arcade.MOUSE_BUTTON_LEFT, 0)

    # Vérifier que l'épée est visible après le clic
    assert sword.attribute.visible
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