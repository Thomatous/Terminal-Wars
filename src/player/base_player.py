from typing import Tuple, List
from random import randint, shuffle
from abc import abstractmethod
from src.world.world import World
from src.world.tile import Tile

class BasePlayer():
    attack: int
    health: int
    movement: int
    y: int
    x: int

    def __init__(self, attack: int = 10, health: int = 100, movement: int = 1, sprite: str = "PP") -> None:
        self.attack = attack
        self.health = health
        self.movement = movement
        self.sprite = sprite
        self.y = None
        self.x = None
    
    @property
    def position(self) -> Tuple[int, int]:
        return (self.y, self.x)

    def spawn(self, world: World) -> None:
        self.y = randint(0, world.rows)
        self.x = randint(0, world.cols)

    def damage(self, damage: int) -> None:
        self.health -= damage

    def move(self, tiles: List[Tile]) -> None:
        moveable_tiles = []
        for t in tiles:
            if t.movement_cost <= self.movement:
                moveable_tiles.append(t)
        shuffle(moveable_tiles)

        if len(moveable_tiles) > 0:
            self.y = moveable_tiles[0].y
            self.x = moveable_tiles[0].x