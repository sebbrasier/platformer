import arcade
from typing import Final
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Final
from readmap import *


Block_size = Final[64]

def create_arrow_chain(map_slice : list[map_symbols], arrow : map_symbols) -> None:
    arrow_chain = [elements for elements in map_slice if elements is arrow]
    return (arrow_chain)



class moving_platform:
    #attributes : Final[arcade.SpriteList[arcade.Sprite]]

    




