import arcade

from gameview import *
from readmap import *
import math



# test la collision des blobs
def test_blob(window: arcade.Window) -> None:
    view = GameView()
    view.setup("maps/map_tests/blob_colision.txt")
    window.show_view(view)
    window.test(50)
    blob1 : blob
    if isinstance(view.monster_TABLE.monsters[0],blob):
        blob1 = view.monster_TABLE.monsters[0]
    # Avant la collision, la vitesse est 1
    vitesse_initiale = blob1.speed
    window.test(50)
    # Après collision, on attend que la vitesse soit inversée.
    assert blob1.speed == -vitesse_initiale



def test_bat(window : arcade.Window) -> None:

    view = GameView()
    view.setup("maps/map_tests/bat.txt")
    window.show_view(view)

    bat1 : chauve_souris
    if isinstance(view.monster_TABLE.monsters[0],chauve_souris):
        bat1 = view.monster_TABLE.monsters[0]

    # on enlève l'effet aléatoire du mouvement de la chauve souris pour tester seulement si les bordures fonctionnent correctement
    #test pour les bordures en x
    bat1.random_dir = 0
    bat1.boundary = 40
    bat1.vx = 1
    bat1.vy = 0
    vitesse_initiale = bat1.vx
    window.test(75)
    # Après collision, on attend que la vitesse soit inversée.
    assert bat1.vx == -vitesse_initiale
    # test pour les bordures en y
    bat1.vx = 0
    bat1.vy = 1
    vitesse_initiale = bat1.vy
    window.test(50)
    # Après collision, on attend que la vitesse soit inversée.
    assert bat1.vy == -vitesse_initiale


    



