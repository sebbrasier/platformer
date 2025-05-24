import arcade
from typing import Callable

#class qui gère les interupteurs, qui prend un sprite pour pouvoir faire un lien entre les actions du levier et le sprite 
# qui est draw.
class Inter :
    sprite: arcade.Sprite
    state : bool
    actions_on: list[Callable[[], None]]
    actions_off: list[Callable[[], None]]
    disable : bool
    x :int
    y:int

    def __init__(self, sprite : arcade.Sprite,state : bool,x :int,y:int) -> None :
        self.sprite = sprite
        self.state = state
        self.x=x
        self.y =y
        self.actions_on  = []
        self.actions_off = []
        self.disable = False

    def trigger(self) -> None:
        #change de côté en focntion de son state et si il n'est pas disable
        if self.disable == True:
            return None
        if self.state == False:
            self.sprite.texture = arcade.load_texture(":resources:/images/tiles/leverRight.png")
            for action in self.actions_on :
                action()
            self.state = True
        else: 
            self.sprite.texture = arcade.load_texture(":resources:/images/tiles/leverLeft.png")
            for action in self.actions_off :
                action()
            self.state = False


            

    