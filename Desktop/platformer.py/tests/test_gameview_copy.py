import arcade

from gameview import *
from readmap import *
import pytest
import math

# Test de l'ouverture du fichier map
def test_map() -> None:
    # Bien vérifier que l'on a extrait les bonnes informations du fichier "map"
    file = "maps/map_test.txt"
    dimension = dim(file)
    assert dimension == (7, 4)
    assert len(lecture_map(file)) == 4
    # Vérifier que la fonction qui lit les fichiers gère correctement les exceptions
    file = "non_existent_file.txt"
    assert(lecture_map(file) == [])

# Test de la fonction char_to_sprite
def test_char_to_sprite() -> None:
    # Tester si char_to_sprite retourne la bonne paire pour chaque caractère
    assert char_to_sprite("*") == ("Coin", ":resources:/images/items/coinGold.png")
    assert char_to_sprite(" ") == (" ", " ")
    assert char_to_sprite("=") == ("Wall", ":resources:/images/tiles/grassMid.png")
    assert char_to_sprite("-") == ("Wall", ":resources:/images/tiles/grassHalf_mid.png")
    assert char_to_sprite("x") == ("Wall", ":resources:/images/tiles/boxCrate_double.png")
    assert char_to_sprite("o") == ("Blob", ":resources:/images/enemies/slimePurple.png")
    assert char_to_sprite("v") == ("Chauve-souris", "assets/kenney-extended-enemies-png/bat.png")
    assert char_to_sprite("£") == ("No-go", ":resources:/images/tiles/lava.png")
    assert char_to_sprite("S") == ("Player", ":resources:/images/animated_characters/male_person/malePerson_idle.png")
    assert char_to_sprite("E") == ("Next_level", ":resources:/images/tiles/signExit.png")
    # Tester si une exception est bien levée pour un caractère inconnu
    with pytest.raises(Exception, match="Erreur: caractere inconnu"):
        char_to_sprite("Z")  # Caractère inconnu
    with pytest.raises(Exception, match="Erreur: caractere inconnu"):
        char_to_sprite("9")  # Autre caractère inconnu

# Test de la fonction sprite_type
def test_sprite_type(window: arcade.Window) -> None:
    view = GameView()
    window.show_view(view)
    mock_sprite = arcade.Sprite()
    # Vérifie que le sprite est bien ajouté à la bonne liste selon son type
    view.sprite_type("Wall", mock_sprite)
    assert mock_sprite in view.wall_list
    view.sprite_type("Coin", mock_sprite)
    assert mock_sprite in view.coin_list
    view.sprite_type("Player", mock_sprite)
    assert mock_sprite in view.player_sprite_list
    view.sprite_type("Chauve-souris", mock_sprite)
    assert mock_sprite in view.monster_list
    view.sprite_type("No-go", mock_sprite)
    assert mock_sprite in view.no_go_list
    view.sprite_type("Next_level", mock_sprite)
    assert mock_sprite in view.next_level_list

# Test pour les flèches
def test_arrow(window: arcade.Window) -> None:
    view = GameView()
    view.setup("maps/map_test.txt")
    window.show_view(view)
    window.test(20)
    view.on_mouse_press(500, 500, arcade.MOUSE_BUTTON_RIGHT, 0)
    view.on_mouse_press(500, 500, arcade.MOUSE_BUTTON_LEFT, 0)
    arrow = view.arrow_class_list[0]
    # Test que la flèche apparaisse bien sur le personnage et est visible
    assert arrow.attribute.visible is True
    assert arrow.attribute.position == view.player_sprite.position
    world_x = 500 + view.camera.position[0] - (WINDOW_WIDTH / 2)
    world_y = 500 + view.camera.position[1] - (WINDOW_HEIGHT / 2)
    ref_x = view.player_sprite.center_x
    ref_y = view.player_sprite.center_y   
    angle = math.atan2(ref_x - world_x,ref_y - world_y)
    # Test que la flèche apparaisse avec le bon angle
    assert arrow.attribute.angle == math.degrees(angle) + 140
    old_y = arrow.attribute.change_y
    window.test(1)
    # Test que la gravité est bien appliquée
    assert arrow.attribute.change_y == old_y - 1.5
    
    #Vérifier que la flèche disparait quand elle rentre en collision avec un monstre
    for i in range(30):
        collision_list = arcade.check_for_collision_with_list(arrow.attribute, view.monster_list)
        if len(collision_list) != 0:
            assert len(view.arrow_list) == 0
            assert len(view.arrow_class_list) == 0
        window.test(1)
    # Vérifier que le monstre a bien été tué
    assert len(view.monster_list) == 0

    # Test que plusieurs flèches ont été tirées
    for i in range(5):
        view.on_mouse_press(500, 500, arcade.MOUSE_BUTTON_LEFT, 0)
    assert len(view.arrow_class_list) == 5
    assert len(view.arrow_list) == 5
    window.test(30)

    #Test que la flèche disparait quand elle touche un mur
    view.on_mouse_press(500, 500, arcade.MOUSE_BUTTON_LEFT, 0)
    assert len(view.arrow_class_list) == 1
    assert len(view.arrow_list) == 1
    arrow = view.arrow_class_list[0]
    for i in range(30):
        collision_list = arcade.check_for_collision_with_list(arrow.attribute, view.wall_list)
        if len(collision_list) != 0:
            assert len(view.arrow_list) == 0
            assert len(view.arrow_class_list) == 0
        window.test(1)
    
    #Test que la flèche disparait si elle tombe plus bas que la hauteur de l'écran
    view.on_mouse_press(-500, 500, arcade.MOUSE_BUTTON_LEFT, 0)
    arrow = view.arrow_class_list[0]
    for i in range(30):
        if arrow.attribute.center_y < (view.camera.position[1] - 720/2 ):
            assert(len(view.arrow_list) == 0)
            assert(len(view.arrow_class_list) == 0)
        window.test(1)


#Test pour changer d'armes
def test_change_weapon(window: arcade.Window) -> None:
    view = GameView()
    view.setup("maps/map_test.txt")
    window.show_view(view)
    #Test que l'on a  bien l'épée en main
    assert view.active_weapon.index == 0
    view.on_mouse_press(500, 500, arcade.MOUSE_BUTTON_LEFT, 0)
    #Vérifier que l'icone ainsi que l'épée sont bien visibles
    assert view.sword.attribute.visible is True
    assert view.sword_repr.visible is True
    window.test(20)
    view.on_mouse_release(500, 500,arcade.MOUSE_BUTTON_LEFT, 0)
    view.on_mouse_press(500, 500, arcade.MOUSE_BUTTON_RIGHT, 0)
    #Vérifier que l'on a bien changé d'arme
    view.on_mouse_press(500, 500,arcade.MOUSE_BUTTON_LEFT, 0)
    assert view.active_weapon.index == 1
    assert view.bow.attribute.visible is True
    assert view.bow_repr.visible is True
    #Vérifier que l'épée et son icone ont bien disparu
    assert view.sword.attribute.visible is False
    assert view.sword_repr.visible is False
    window.test(10)




