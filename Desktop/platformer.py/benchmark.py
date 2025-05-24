import arcade
import timeit
from gameview import *

#Mesure le temps pour créer les platformes
def benchmark_platforms(map_file : str, nbr : int) -> None:
    MAP = Map(dim(map_file), lecture_map(map_file))
    arcade.open_window(800, 600, "Benchmark Window")
    view = GameView()
    nb = 1000
    def add_map() -> None:
        #Ajout des platformes qui bougent
        moving_arrow_dict_RIGHT = AddPlatform.read_arrows_right(MAP, map_symbols.RIGHT, lambda a, b : a)
        moving_arrow_dict_LEFT = AddPlatform.read_arrows_right(LinAlgebra.flip_matrix(MAP), map_symbols.LEFT, LinAlgebra.flip_vector)
        horizontal = AddPlatform.combine_right_left(moving_arrow_dict_LEFT, moving_arrow_dict_RIGHT, MAP)
        moving_arrow_dict_DOWN = AddPlatform.read_arrows_right(LinAlgebra.transpose_matrix(MAP), map_symbols.DOWN, LinAlgebra.transpose_vec)
        moving_arrow_dict_UP = AddPlatform.read_arrows_right(LinAlgebra.flip_matrix(LinAlgebra.transpose_matrix(MAP)), map_symbols.UP, LinAlgebra.flip_transpose_vec)
        vertical = AddPlatform.combine_right_left(moving_arrow_dict_DOWN, moving_arrow_dict_UP, MAP)
        #Check pour des erreurs
        AddPlatform.duplicate_checker(horizontal, vertical)
        #On rajoute tout d'abord toutes les platformes
        view.add_platform_x(horizontal, MAP)
        view.add_platform_y(vertical, MAP)
    
    res = timeit.timeit(lambda: add_map(), number=nb)
    print(f"{nbr} : {res/nb}")

def benchmark_enemies(map_file : str, nbr : int) -> None:
    arcade.open_window(800, 600, "Benchmark Window")
    view = GameView()
    view.setup(map_file) 
    nb = 100

    res= timeit.timeit(
        lambda: view.on_update(1/60),
        number=nb
    )
    print(f"{nbr} : {res/nb}")


def print_benchmark_plat() -> None:
    maps = {"maps/benchmark_maps/platforms1.txt" : 1, "maps/benchmark_maps/platforms5.txt" : 5, "maps/benchmark_maps/platforms50.txt" : 50,
        "maps/benchmark_maps/platforms100.txt" : 100, "maps/benchmark_maps/platforms500.txt" : 500, "maps/benchmark_maps/platforms1000.txt" : 1000}
    
    for e in maps:
        benchmark_platforms(e, maps[e])

def print_benchmark_en() -> None:
    maps = {"maps/benchmark_maps/enemies1.txt" : 1, "maps/benchmark_maps/enemies5.txt" : 5, "maps/benchmark_maps/enemies50.txt" : 50,
        "maps/benchmark_maps/enemies100.txt" : 100, "maps/benchmark_maps/enemies500.txt" : 500, "maps/benchmark_maps/enemies1000.txt" : 1000,
          "maps/benchmark_maps/enemies10000.txt" : 10000}
    
    for e in maps:
        benchmark_enemies(e, maps[e])


