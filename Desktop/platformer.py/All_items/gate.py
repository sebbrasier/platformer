import arcade
from All_items import interuptor
class Gate :
    sprite: arcade.Sprite

    def __init__(self, sprite : arcade.Sprite) -> None:
        self.sprite = sprite
    
    def appearance(self, interuptor : interuptor):
        if interuptor.acitve == True :
            self.visible = False

    