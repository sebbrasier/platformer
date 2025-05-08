import arcade
import pytest
from gameview import *
def test_yaml_height_width() -> None:
    with pytest.raises(KeyError, match="La config YAML doit contenir 'width' et 'height'."):
        load_map_config("maps/map_tests/switch_gate/noheightwidth.txt")

def test_noyaml() -> None:
    with pytest.raises(TypeError, match="Le fichier YAML doit contenir un dictionnaire racine"):
        load_map_config("maps/map_tests/switch_gate/noyaml.txt")

def test_gate_place() -> None:
    view = GameView.__new__(GameView)
    with pytest.raises(ValueError, match="Aucun portail à la position \(1,1\)\."):
        view.setup("maps/map_tests/switch_gate/gate_place.txt")

def test_switch_place(window: arcade.Window) -> None:
    config = {
        "width": 3,
        "height": 3,
        "switches": [
            {"x": 1, "y": 1,
             "switch_on": [],
             "switch_off": []}
        ]
    }
    inter_list : list[Inter] = []
    gate_list : list[Gate]= []      # peu importe pour ce test
    wall_list : arcade.SpriteList[arcade.Sprite]= arcade.SpriteList()
    with pytest.raises(ValueError, match="Aucun interrupteur à la position \(1,1\)\."):
        link_inter_to_gates(config, inter_list, gate_list, wall_list)

def test_switch_gate_place(window: arcade.Window) -> None:
    view = GameView.__new__(GameView)
    with pytest.raises(ValueError, match="Aucun portail trouvé à \(2,2\)\."):
        view.setup("maps/map_tests/switch_gate/switch_gate_place.txt")

def test_gate_state(window: arcade.Window) -> None:
    # Initialiser la vue et la map de test
    view = GameView()
    view.setup("maps/map_tests/switch_gate/gate_state.txt")
    window.show_view(view)

    def find_gate(view: GameView, x: int, y: int) -> Gate:
        for gate in view.gate_class_list:
            if gate.x == x and gate.y == y:
                return gate
        raise ValueError(f"Pas de gate à ({x},{y})")
    
    gate_0 : Gate = find_gate(view,5,1)
    gate_1 : Gate = find_gate(view,5,3)
    gate_2 : Gate = find_gate(view,5,5)
    gate_3 : Gate = find_gate(view,7,5)
    gate_4 : Gate = find_gate(view,5,7)
    gate_5 : Gate = find_gate(view,7,7)
    gate_6 : Gate = find_gate(view,9,7)


    #verifie que la gate du haut est affiché et que celle du bas ne l'est pas
    window.test(25)
    assert gate_0.sprite not in view.wall_list 
    assert gate_1.sprite in view.wall_list
    window.test(25)
    # clique sur linterupteur pour que l'on verifie si la gate du haut disparait puis on reclique pour la remettre, on verifie
    view.on_mouse_press(1000, 500, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(25)
    assert gate_1.sprite not in view.wall_list
    view.on_mouse_press(1000, 500, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(25)
    assert gate_1.sprite in view.wall_list
    #on deplace la joueuse a coté de l'autre interupteur
    view.on_mouse_release(0, 0, arcade.MOUSE_BUTTON_LEFT, 0)
    view.player_sprite.center_y +=128
    window.test(25)
    #on clique sur l'interupteur et on verifie qu'il ne fait rien car il a seulement une action pour switch on mais comme il 
    # apparait en state on cela ne fera rien
    view.on_mouse_press(1000, 500, arcade.MOUSE_BUTTON_LEFT, 0)
    assert gate_0.sprite not in view.wall_list
    window.test(25)
    # on reclique et on verifie que cela ne fait toujours rien car il est disable
    view.on_mouse_press(1000, 500, arcade.MOUSE_BUTTON_LEFT, 0)
    assert gate_0.sprite not in view.wall_list
    #on deplace la joueuse a coté de l'autre interupteur
    view.on_mouse_release(0, 0, arcade.MOUSE_BUTTON_LEFT, 0)
    view.player_sprite.center_y +=128
    window.test(25)
    #on verifie que un des portail est ouvert l'autre fermé
    #puis on clique pour verifier que les actions de lin terupteur fonctionnent bien
    assert gate_3.sprite in view.wall_list 
    assert gate_2.sprite not in view.wall_list
    window.test(25)
    view.on_mouse_press(1000, 1000, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(25)
    assert gate_3.sprite not in view.wall_list 
    assert gate_2.sprite in view.wall_list
    window.test(25)
    view.on_mouse_press(1000, 1000, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(25)
    assert gate_3.sprite in view.wall_list 
    assert gate_2.sprite not in view.wall_list
    window.test(25)
    #on se deplace a coté du dernier interupteur
    view.on_mouse_release(0, 0, arcade.MOUSE_BUTTON_LEFT, 0)
    view.player_sprite.center_y +=128
    window.test(25)
    assert gate_4.sprite in view.wall_list
    assert gate_5.sprite in view.wall_list
    assert gate_6.sprite in view.wall_list
    window.test(25)
    view.on_mouse_press(1000, 1000, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(25)
    assert gate_4.sprite not in view.wall_list
    assert gate_5.sprite not in view.wall_list
    assert gate_6.sprite not in view.wall_list
    window.test(25)



