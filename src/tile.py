from __future__ import annotations
from typing import List
from src.directions import Direction

class Tile():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.neighbours: List[Tile] = [None, None, None, None]
    
    def add_neighbour(self, direction: Direction, tile: Tile) -> None:
        self.neighbours[direction.value] = tile