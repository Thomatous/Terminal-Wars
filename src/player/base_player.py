from random import randint
from abc import abstractmethod
from src.world.world import World

class BasePlayer():
    attack: int
    health: int
    movement: int

    def __init__(self, attack: int = 10, health: int = 100, movement: int = 1,) -> None:
        self.attack = attack
        self.health = health
        self.movement = health

    def spawn(world: World):
        self.y = randint(0, world.rows)
        self.x = randint(0, world.cols)

    def damage(self, damage: int) -> None:
        self.health -= health
