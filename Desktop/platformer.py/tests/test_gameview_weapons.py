import arcade

from gameview import *
from readmap import *
import math


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

    # Rendre l'épée visible et positionner son sprite sur le blob.
    Sword.can_kill = True
    sword.attribute.visible = True
    view.on_mouse_press(500,100, arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(100)

    # Vérifier que le sprite du blob a bien été retiré de la liste des monstres.
    assert len(view.monster_list) == 0


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



# Test pour les flèches
def test_arrow(window: arcade.Window) -> None:
    view = GameView()
    view.setup("maps/map_tests/file_test.txt")
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
    view.setup("maps/map_tests/file_test.txt")
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

    



