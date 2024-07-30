from __future__ import annotations
from random import choices
from typing import Dict, List
from src.world.enums.direction import Direction
from src.world.rules import RULES
from src.world.weights import WEIGHTS

class Tile():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.neighbours: Dict[Tile] = {}
        self.possibilities = list(RULES.keys())
        self.entropy = len(self.possibilities)

    @property
    def directions(self) -> List[Direction]:
        return list(self.neighbours.keys())
    
    def collapse(self):
        weights = [WEIGHTS[possibility] for possibility in self.possibilities]
        self.possibilities = choices(self.possibilities, weights=weights, k=1)
        self.entropy = 0

    def add_neighbour(self, direction: Direction, tile: Tile) -> None:
        self.neighbours[direction] = tile
    
    def constrain(self, neighbour_possibilities: List, direction: Direction):
        reduced = False

        if self.entropy > 0:
            connectors = []
            for neighbour_possibility in neighbour_possibilities:
                connectors.append(RULES[neighbour_possibility][direction.value])

            # check opposite side
            if direction == Direction.NORTH: opposite = Direction.SOUTH
            if direction == Direction.EAST:  opposite = Direction.WEST
            if direction == Direction.SOUTH: opposite = Direction.NORTH
            if direction == Direction.WEST:  opposite = Direction.EAST

            for possibility in self.possibilities.copy():
                if RULES[possibility][opposite.value] not in connectors:
                    self.possibilities.remove(possibility)
                    reduced = True

            self.entropy = len(self.possibilities)

        return reduced