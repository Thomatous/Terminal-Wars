from typing import Tuple, List
from random import randint, shuffle
from abc import abstractmethod
from src.world.world import World
from src.world.tile import Tile
from src.player.enum.evolution import Evolution
from src.player.mitosis import Mitosis

class Player():
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
    history: List[Evolution]

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
        self.history = []
    
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
    
    @abstractmethod
    def evolve(self, evolution_history: List[Evolution], level: int) -> Evolution:
        """
        Return one of the following evolutions:
        Evolution.ATTACK:   Increases your attack
        Evolution.HEALTH:   Increases your health
        Evolution.MOVEMENT: Increases your movement
        Evolution.MITOSIS:  Splits your creature into two creatures with halved stats
        """
        raise NotImplementedError("Base players can't evolve.")

    def _increase_level_threshold(self, rate: float) -> None:
        self.level_threshold = self.level_threshold * rate

    def _get_modified_stats(self) -> Tuple[int, int, int]:
        return (self.attack // 10, self.health // 10, self.movement)
    
    def _apply_evolution(self, evolution: Evolution) -> None:
        self.history.append(evolution)
        if evolution == Evolution.ATTACK:
            self.attack += 15
        elif evolution == Evolution.HEALTH:
            self.health += 10
        elif evolution == Evolution.MOVEMENT:
            self.movement += 1
        elif evolution == Evolution.MITOSIS:
            self.attack = self.attack // 2
            self.health = self.health // 2
            self.movement = self.movement // 2
            raise Mitosis
    
    def _level_up(self) -> NameError:
        self.level += 1
        a, h, m = self._get_modified_stats()
        evolution = self.evolve(self.history, self.level)
        self._apply_evolution(evolution)


    def gain_experience(self, experience: int) -> None:
        self.experience += experience
        if self.experience >= self.level_threshold:
            self._increase_level_threshold(1.2)
            self.experience = self.experience - self.level_threshold
            self._level_up()