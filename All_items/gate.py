import arcade
from All_items.interuptor import *

# Class pour les portails. Elle contient ses coordonnées en attribut pour pouvoir savoir quel switch est en lien avec quel gate.
class Gate :
    sprite: arcade.Sprite
    x :int
    y:int

    def __init__(self, sprite : arcade.Sprite,x :int,y:int) -> None:
        self.sprite = sprite
        self.x=x
        self.y =y
    
    # fonction open et close qui sont appelées dans les Callable des actions des leviers corrsepondants
    def open(self, wall_list: arcade.SpriteList[arcade.Sprite]) -> None:
        if self.sprite in wall_list:
            wall_list.remove(self.sprite)
        self.sprite.visible = False

    def close(self, wall_list: arcade.SpriteList[arcade.Sprite]) -> None:
        if self.sprite not in wall_list:
            wall_list.append(self.sprite)
        self.sprite.visible = True


    