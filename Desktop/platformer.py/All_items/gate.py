import arcade
from All_items.interuptor import *
class Gate :
    sprite: arcade.Sprite

    def __init__(self, sprite : arcade.Sprite) -> None:
        self.sprite = sprite
    
    def appearance(self, interuptor : Inter)->None:
        if interuptor.active == True :
            self.visible = False

    