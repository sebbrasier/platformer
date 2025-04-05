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

