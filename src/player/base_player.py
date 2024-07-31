from typing import Tuple
from random import randint
from abc import abstractmethod
from src.world.world import World

class BasePlayer():
    attack: int
    health: int
    movement: int
    y: int
    x: int

    def __init__(self, attack: int = 10, health: int = 100, movement: int = 1,) -> None:
        self.attack = attack
        self.health = health
        self.movement = movement
    
    @property
    def position(self) -> Tuple[int, int]:
        return (self.y, self.x)

    def spawn(self, world: World) -> None:
        self.y = randint(0, world.rows)
        self.x = randint(0, world.cols)

    def damage(self, damage: int) -> None:
        self.health -= damage
