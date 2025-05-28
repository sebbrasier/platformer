import arcade
import pytest
from gameview import *

def test_zones(window: arcade.Window) -> None:
    """on test les 2 zones, gravité et no_weapon, on verifie que au spawn on a bien la gravité normal,
    puis on déplace le joeur dans la zone gravité et on vérifie quelle est bien inversé. Puis on test la zone no weapon
    avec 2 zones pour s'assurer que notre lecture du yaml marche aussi bien avec plusieurs zones"""
    view = GameView()
    view.setup("maps/map_tests/zone.txt")
    window.show_view(view)

    window.test(25)
    view.player_sprite.center_x = 0
    assert view.physics_engine.gravity_constant == 1
    view.player_sprite.center_x += 200
    window.test(25)
    assert view.physics_engine.gravity_constant == -1
    view.player_sprite.center_x += 200
    window.test(25)
    assert view.physics_engine.gravity_constant == 1
    view.on_mouse_press(150, 150, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(25)
    assert view.sword.attribute.visible == False
    assert view.no_weapon_repr.visible == True
    view.player_sprite.center_x += 200
    window.test(25)
    view.on_mouse_press(150, 150, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(25)
    assert view.sword.attribute.visible == True
    assert view.no_weapon_repr.visible == False
    view.on_mouse_release(0, 0, arcade.MOUSE_BUTTON_LEFT, 0)
    view.player_sprite.center_x += 200
    window.test(25)
    assert view.physics_engine.gravity_constant == 1
    view.on_mouse_press(150, 150, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(25)
    assert view.sword.attribute.visible == False
    assert view.no_weapon_repr.visible == True


