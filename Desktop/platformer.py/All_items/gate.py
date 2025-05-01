import arcade
from All_items.interuptor import *
class Gate :
    sprite: arcade.Sprite
    x :int
    y:int

    def __init__(self, sprite : arcade.Sprite,x :int,y:int) -> None:
        self.sprite = sprite
        self.x=x
        self.y =y
    
    def open(self, wall_list: arcade.SpriteList[arcade.Sprite]) -> None:
        if self.sprite in wall_list:
            wall_list.remove(self.sprite)
        self.sprite.visible = False

    def close(self, wall_list: arcade.SpriteList[arcade.Sprite]) -> None:
        if self.sprite not in wall_list:
            wall_list.append(self.sprite)
        self.sprite.visible = True


    