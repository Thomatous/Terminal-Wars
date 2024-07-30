from typing import List
from src.tile import Tile
from src.directions import Direction

class World:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.tilemap = self._init_tilemap()
        self._init_neighbours()

    def _init_tilemap(self) -> List[List[Tile]]:
        tilemap: List[List[Tile]] = []
        for y in range(self.height):    
            row: List[Tile] = []
            for x in range(self.width):
                tile = Tile(x, y)
                row.append(tile)
            tilemap.append(row)
        return tilemap

    def _init_neighbours(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                tile = self.tilemap[y][x]
                if y > 0:
                    tile.add_neighbour(Direction.NORTH, self.tilemap[y - 1][x])
                if x < self.width - 1:
                    tile.add_neighbour(Direction.EAST, self.tilemap[y][x + 1])
                if y < self.height - 1:
                    tile.add_neighbour(Direction.SOUTH, self.tilemap[y + 1][x])
                if x > 0:
                    tile.add_neighbour(Direction.WEST, self.tilemap[y][x - 1])