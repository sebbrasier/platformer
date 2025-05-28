import arcade

from gameview import *
from readmap import *
import pytest
import math

# Test de l'ouverture du fichier map
def test_map() -> None:
    # Bien vérifier que l'on a extrait les bonnes informations du fichier "map"
    file = "maps/map_tests/file_test.txt"
    dimension = dim(file)
    print(lecture_map(file))
    assert dimension == (7, 4)
    assert len(lecture_map(file)) == 4
    #on s'assure que le fichier est bien stocké sous forme de matrice 7x4
    for i in range(4):
        assert len(lecture_map(file)[i]) == 7

def test_str_to_matrix() -> None:
    input_str = (
        "abc\n"
        "de\n"
        "fghi\n"
        "j"
    )
    width = 5
    result = str_to_matrix(input_str, width)

    # Doit supprimer la première et la dernière ligne : ne garder que ["de", "fghi"]
    expected = [
        ['d', 'e', ' ', ' ', ' '],    # "de" complété avec des espaces jusqu'à une largeur de 5
        ['f', 'g', 'h', 'i', ' ']     # "fghi" complété avec un espace
    ]
    assert result == expected

    # Vérification supplémentaire : lorsque toutes les lignes font exactement la largeur demandée
    input_str_2 = (
        "aaaaa\n"
        "bbbbb\n"
        "ccccc"
    )
    result2 = str_to_matrix(input_str_2, 5)
    expected2 = [['b', 'b', 'b', 'b', 'b']]  # On ne garde que la ligne du milieu
    assert result2 == expected2

    # Cas limite : si l'entrée contient seulement deux lignes, le résultat doit être vide
    input_str_3 = "line1\nline2"
    assert str_to_matrix(input_str_3, 5) == []

#test enum_to_sprite
def test_enum_to_sprite() -> None:
    # Test if enum_to_sprite returns correct tuples
    assert enum_to_sprite(map_symbols.Coin) == ("Coin", ":resources:/images/items/coinGold.png")
    assert enum_to_sprite(map_symbols.Space) == (" ", " ")
    assert enum_to_sprite(map_symbols.Grass_tile) == ("Wall", ":resources:/images/tiles/grassMid.png")
    assert enum_to_sprite(map_symbols.Half_grass) == ("Wall", ":resources:/images/tiles/grassHalf_mid.png")
    assert enum_to_sprite(map_symbols.Box) == ("Wall", ":resources:/images/tiles/boxCrate_double.png")
    assert enum_to_sprite(map_symbols.Blob) == ("Blob", ":resources:/images/enemies/slimePurple.png")
    assert enum_to_sprite(map_symbols.Chauve_souris) == ("Chauve-souris", "assets/kenney-extended-enemies-png/bat.png")
    assert enum_to_sprite(map_symbols.Lava) == ("No-go", ":resources:/images/tiles/lava.png")
    assert enum_to_sprite(map_symbols.Player) == ("Player", ":resources:/images/animated_characters/male_person/malePerson_idle.png")
    assert enum_to_sprite(map_symbols.Next_level) == ("Next_level", ":resources:/images/tiles/signExit.png")

def test_char_to_map() -> None:
    # Valid character mapping tests
    assert char_to_map(" ") == map_symbols.Space
    assert char_to_map("=") == map_symbols.Grass_tile
    assert char_to_map("-") == map_symbols.Half_grass
    assert char_to_map("x") == map_symbols.Box
    assert char_to_map("*") == map_symbols.Coin
    assert char_to_map("o") == map_symbols.Blob
    assert char_to_map("v") == map_symbols.Chauve_souris
    assert char_to_map("£") == map_symbols.Lava
    assert char_to_map("S") == map_symbols.Player
    assert char_to_map("E") == map_symbols.Next_level
    assert char_to_map("→") == map_symbols.RIGHT
    assert char_to_map("←") == map_symbols.LEFT
    assert char_to_map("↓") == map_symbols.DOWN
    assert char_to_map("↑") == map_symbols.UP
    assert char_to_map("^") == map_symbols.Inter
    assert char_to_map("|") == map_symbols.Gate

    # Invalid characters should raise Exception
    with pytest.raises(Exception, match="Erreur: caractere inconnu"):
        char_to_map("z")
    with pytest.raises(Exception, match="Erreur: caractere inconnu"):
        char_to_map("9")
    with pytest.raises(Exception, match="Erreur: caractere inconnu"):
        char_to_map("!")

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

