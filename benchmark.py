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
        view.setup(map_file)
    
    res = timeit.timeit(lambda: add_map(), number=nb)
    print(f"{nbr} : {res/nb}")

def benchmark_enemies(map_file : str, nbr : int) -> None:
    arcade.open_window(800, 600, "Benchmark Window")
    view = GameView()
    view.setup(map_file) 
    nb = 1000

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

print_benchmark_plat()

