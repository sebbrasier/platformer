import arcade
from enum import Enum, auto
from typing import Callable

class States(Enum):
    on = auto()
    off = auto()

class Inter :
    sprite: arcade.Sprite
    state : States
    actions_on: list[Callable[[], None]]
    actions_off: list[Callable[[], None]]
    disable : bool
    x :int
    y:int

    def __init__(self, sprite : arcade.Sprite,state : States,x :int,y:int) -> None :
        self.sprite = sprite
        self.state = state
        self.x=x
        self.y =y
        self.actions_on  = []
        self.actions_off = []
        self.disable = False

    def trigger(self) -> None:
        if self.disable == True:
            return None
        
        if self.state == States.off:
            self.sprite.texture = arcade.load_texture(":resources:/images/tiles/leverRight.png")
            for action in self.actions_on :
                action()
            self.state = States.on
        else: 
            self.sprite.texture = arcade.load_texture(":resources:/images/tiles/leverLeft.png")
            for action in self.actions_off :
                action()
            self.state = States.off


            

    