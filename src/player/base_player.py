from typing import Tuple, List
from random import randint, shuffle
from abc import abstractmethod
from src.world.world import World
from src.world.tile import Tile

class BasePlayer():
    name: str
    attack: int
    health: int
    movement: int
    sprite: str
    y: int
    x: int
    level: int
    level_threshold: int
    experience: int

    def __init__(self,
                 name: str = "Player",
                 attack: int = 10,
                 health: int = 100,
                 movement: int = 1,
                 sprite: str = "PP",
                 level_threshold: int = 100) -> None:
        self.attack = attack
        self.health = health
        self.movement = movement
        self.sprite = sprite
        self.y = None
        self.x = None
        self.level = 1
        self.level_threshold = level_threshold
        self.experience = 0
    
    @property
    def position(self) -> Tuple[int, int]:
        return (self.y, self.x)

    def spawn(self, world: World) -> None:
        self.y = randint(1, world.rows - 1)
        self.x = randint(1, world.cols - 1)

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
    
    @staticmethod
    @abstractmethod
    def level_up(pips: int, curr_level: int):
        pass

    def gain_experience(self, experience: int) -> None:
        self.experience += experience
        if self.experience >= self.level_threshold:
            BasePlayer.level_up(1, 1)
            self.level_threshold *= 1.3
            self.experience = self.experience - self.level_threshold