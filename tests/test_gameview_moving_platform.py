import arcade

from gameview import *
import pytest

#tests des fonctions d'analyse de map
def test_read_arrows_right() -> None:
    file = "maps/map_tests/moving_platforms/stuck.txt"
    #on hard code ce que devraient etre les platformes et leurs fleches associées
    platform_set_1 = frozenset({(0,3), (0,4), (0,5), (1,3), (1,5), (2,3), (2,4), (2,5)})
    platform_set_2 = frozenset({(3,6), (3,7), (3,8), (3,9), (3, 10)})
    arrow_tuple_left = (map_symbols.LEFT, map_symbols.LEFT, map_symbols.LEFT)
    arrow_tuple_right = (map_symbols.RIGHT, map_symbols.RIGHT, map_symbols.RIGHT)
    arrow_tuple_up =  (map_symbols.UP, map_symbols.UP)
    arrow_tuple_down = (map_symbols.DOWN, map_symbols.DOWN)

    horizontal_tuple = (arrow_tuple_left, arrow_tuple_right)
    vertical_tuple = (arrow_tuple_down, arrow_tuple_up)

    #Calcul des platformes et de leurs flèches associées
    map = Map(dim(file), lecture_map(file))
    right = AddPlatform.read_arrows_right(map, map_symbols.RIGHT, lambda a,b : a)
    left = AddPlatform.read_arrows_right(LinAlgebra.flip_matrix(map), map_symbols.LEFT, LinAlgebra.flip_vector)
    down = AddPlatform.read_arrows_right(LinAlgebra.transpose_matrix(map), map_symbols.DOWN, LinAlgebra.transpose_vec)
    up = AddPlatform.read_arrows_right(LinAlgebra.flip_matrix(LinAlgebra.transpose_matrix(map)), map_symbols.UP, LinAlgebra.flip_transpose_vec)

    #test si la valeur attendue est bien celle calculéee
    assert right[platform_set_1] == arrow_tuple_right
    assert left[platform_set_1] == arrow_tuple_left
    assert up[platform_set_2] == arrow_tuple_up
    assert down[platform_set_2] == arrow_tuple_down

    #test si les bonnes platformes ont les bonnes flèches gauche et droites associées
    horizontal = AddPlatform.combine_right_left(left, right, map)
    vertical = AddPlatform.combine_right_left(down, up, map)

    assert horizontal[platform_set_1] == horizontal_tuple
    assert vertical[platform_set_2] == vertical_tuple

#test si la fonction qui définit un "bloc" pour les platformes est bien fonctionnelle 
def test_read_platform() -> None:
    file = "maps/map_tests/moving_platforms/block1.txt"
    #test de la fonction avec plusieurs cas de blocs complexes
    block = {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
    (1, 0), (1, 2), (1, 4),
    (2, 0), (2, 1), (2, 2), (2, 3),
    (3, 0), (3, 2), (3, 3), (3, 4),
    (4, 0), (4, 3), (4, 4),
    (5,0), (5,3)}
    map = Map(dim(file), lecture_map(file))
    point_set : set[tuple[int, int]] = set()
    AddPlatform.read_platform(map, (0, 0), lambda a,b : a, point_set)

    #Deuxieme cas avec un bloc complexe
    file2 = "maps/map_tests/moving_platforms/block2.txt"
    map2 = Map(dim(file2), lecture_map(file2))
    block2 = {(0, 1), (2, 4), (1, 2), (3, 4), 
              (0, 10), (4, 3), (4, 9), (2, 7), 
              (1, 8), (0, 2), (1, 0), (0, 8), (2, 5), 
              (1, 3), (0, 11), (2, 8), (3, 5), 
              (4, 4), (4, 10), (3, 8), (0, 0), 
              (0, 9), (2, 0), (2, 3), (2, 6), 
              (4, 8), (4, 11)}
    
    point_set2 : set[tuple[int, int]] = set()
    AddPlatform.read_platform(map2, (0, 0), lambda a,b : a, point_set2)
    assert point_set2 == block2

#test pour des affectations multiples de flèches
def test_platform_error() -> None:
    #test si on affecte deux fois des flèches à droite, une erreur est bien renvoyée
    file = "maps/map_tests/moving_platforms/block3.txt"
    map = Map(dim(file), lecture_map(file))
    #test si une erreur est bien renvoyée 
    with pytest.raises(ValueError, match="Erreur : une platforme est affectée par plusieurs séries de flèches qui vont dans le même sens"):
        AddPlatform.read_arrows_right(map, map_symbols.RIGHT, lambda a,b : a)
    #Idem pour les flèches à gauche
    with pytest.raises(ValueError, match="Erreur : une platforme est affectée par plusieurs séries de flèches qui vont dans le même sens"):
        AddPlatform.read_arrows_right(LinAlgebra.flip_matrix(map), map_symbols.LEFT, LinAlgebra.flip_vector)
        
    #test pour des fleches verticales
    file2 = "maps/map_tests/moving_platforms/block4.txt"
    map2 = Map(dim(file2), lecture_map(file2))
    #test pour les flèches vers le bas
    with pytest.raises(ValueError, match="Erreur : une platforme est affectée par plusieurs séries de flèches qui vont dans le même sens"):
        AddPlatform.read_arrows_right(LinAlgebra.transpose_matrix(map2), map_symbols.DOWN, LinAlgebra.transpose_vec)
    #test pour les flèches vers le haut
    with pytest.raises(ValueError, match="Erreur : une platforme est affectée par plusieurs séries de flèches qui vont dans le même sens"):
        AddPlatform.read_arrows_right(LinAlgebra.flip_matrix(LinAlgebra.transpose_matrix(map2)), map_symbols.UP, LinAlgebra.flip_transpose_vec)
    
    #test pour des affectations multiples de platformes
    file3 = "maps/map_tests/moving_platforms/block5.txt"
    map3 = Map(dim(file3), lecture_map(file3))
    right = AddPlatform.read_arrows_right(map3, map_symbols.RIGHT, lambda a,b : a)
    left = AddPlatform.read_arrows_right(LinAlgebra.flip_matrix(map3), map_symbols.LEFT, LinAlgebra.flip_vector)
    down = AddPlatform.read_arrows_right(LinAlgebra.transpose_matrix(map3), map_symbols.DOWN, LinAlgebra.transpose_vec)
    up = AddPlatform.read_arrows_right(LinAlgebra.flip_matrix(LinAlgebra.transpose_matrix(map3)), map_symbols.UP, LinAlgebra.flip_transpose_vec)

    #Test qu'une erreur est bien renvoyée dans le cas d'affectations multipels
    horizontal = AddPlatform.combine_right_left(left, right, map3)
    vertical = AddPlatform.combine_right_left(down, up, map3)
    with pytest.raises(ValueError, match="Erreur : Une platforme est affectée par un mouvement horizontal et vertical"):
        AddPlatform.duplicate_checker(horizontal, vertical)

#test pour le calcul de frontières horizontales
def test_boundary_x(window: arcade.Window) -> None:
    file = "maps/map_tests/moving_platforms/block6.txt"
    view = GameView()
    view.setup(file)
    window.show_view(view)
    sprite = view.platform_list[0]
    window.test(20)
    #On s'assure que les calculs sont bons
    right = 224
    left = -32
    assert sprite.boundary_right == right
    assert sprite.boundary_left == left
    window.test(40)

#test pour le calcul de frontières verticales
def test_boundary_y(window: arcade.Window) -> None:
    file = "maps/map_tests/moving_platforms/block7.txt"
    view = GameView()
    view.setup(file)
    window.show_view(view)
    sprite = view.platform_list[0]
    #On s'assure que les frontières du sprite sont bien celles calculées

    #On s'assure que les calculs sont bons
    up = 288
    down = 32
    assert sprite.boundary_top == up
    assert sprite.boundary_bottom == down
    window.test(40)

def test_special_plat(window : arcade.Window) -> None:
    file = "maps/map_tests/moving_platforms/block10.txt"
    view = GameView()
    view.setup(file)
    window.show_view(view)

    #On s'assure que chacune des platformes spéciales est mise dans la boonne liste
    assert len(view.no_go_list) == 1
    assert len(view.inter_list) == 1
    assert len(view.next_level_list) == 1

    lava = view.no_go_list[0]
    inter = view.inter_list[0]
    pannel = view.next_level_list[0]

    #On s'assure que le bon nombre de platformes est ajouté
    assert len(view.platform_list) == 5

    #test des bordures
    assert lava.boundary_right == 160  #valeurs théoriques calculées manuellement
    assert pannel.boundary_right == 224
    assert inter.boundary_right == 284.5
    assert lava.boundary_left == -32
    assert pannel.boundary_left == 32
    assert inter.boundary_left == 97.5

    window.test(10)
    #Test du mouvement
    #Test que les platformes se déplacent vers la droite
    assert lava.change_x == 1
    assert inter.change_x == 1
    assert pannel.change_x == 1

    window.test(100)
    #Test que les platformes se déplacent vers la gauche
    assert lava.change_x == -1
    assert inter.change_x == -1
    assert pannel.change_x == -1