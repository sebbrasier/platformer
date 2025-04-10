import arcade
from typing import Any

class Inter :
    sprite: arcade.Sprite

    def __init__(self, sprite : arcade.Sprite) -> None :
        self.sprite = sprite
        self.active = False
    
    def appearance(self) -> None :
        if self.active == True:
            self.sprite.texture = arcade.load_texture(":resources:/images/tiles/leverRight.png")
        else:
            self.sprite.texture = arcade.load_texture(":resources:/images/tiles/leverLeft.png")



class InterSprite(arcade.Sprite):
    inter_ref: Inter 

    def __init__(self, *args : Any,inter_ref: Inter, **kwargs : Any) -> None:
        super().__init__(*args, **kwargs, )
        self.inter_ref: Inter = inter_ref
    
    def update_inter(self) -> None:
        self.inter_ref.appearance()
    