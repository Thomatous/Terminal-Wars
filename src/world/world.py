from random import choice
from typing import List
from src.world.tile import Tile
from src.world.data.enums.direction import Direction
from src.world.data.rules import RULES
from src.world.data.sprites import SPRITES

class World:
    def __init__(self, cols: int, rows: int) -> None:
        self.cols = cols
        self.rows = rows
        self.tilemap = self._init_tilemap()
        self._init_neighbours()

    @property
    def generating(self) -> bool:
        for y in range(self.rows):
            for x in range(self.cols):
                if self.tilemap[y][x].entropy > 0:
                    return True
        return False


    def _init_tilemap(self) -> List[List[Tile]]:
        tilemap: List[List[Tile]] = []
        for y in range(self.rows):    
            row: List[Tile] = []
            for x in range(self.cols):
                tile = Tile(x, y)
                row.append(tile)
            tilemap.append(row)
        return tilemap

    def _init_neighbours(self) -> None:
        for y in range(self.rows):
            for x in range(self.cols):
                tile = self.tilemap[y][x]
                if y > 0:
                    tile.add_neighbour(Direction.NORTH, self.tilemap[y - 1][x])
                if x < self.cols - 1:
                    tile.add_neighbour(Direction.EAST, self.tilemap[y][x + 1])
                if y < self.rows - 1:
                    tile.add_neighbour(Direction.SOUTH, self.tilemap[y + 1][x])
                if x > 0:
                    tile.add_neighbour(Direction.WEST, self.tilemap[y][x - 1])
    
    def _get_min_entropy(self) -> int:
        min_entropy = len(list(RULES.keys()))
        for y in range(self.rows):
            for x in range(self.cols):
                entropy = self.tilemap[y][x].entropy
                if entropy > 0:
                    if entropy < min_entropy:
                        min_entropy = entropy
        return min_entropy
    
    def _get_min_entropy_tiles(self) -> List[Tile]:
        min_entropy = self._get_min_entropy()
        min_entropy_tiles = []

        for y in range(self.rows):
            for x in range(self.cols):
                entropy = self.tilemap[y][x].entropy
                if entropy > 0:
                    if entropy < min_entropy:
                        min_entropy_tiles.clear()
                        min_entropy = entropy
                    if entropy == min_entropy:
                        min_entropy_tiles.append(self.tilemap[y][x])
        return min_entropy_tiles
    
    def wave_function_collapse(self):
        min_entropy_tiles = self._get_min_entropy_tiles()

        if min_entropy_tiles == []:
            return 0

        tile_to_collapse: Tile = choice(min_entropy_tiles)
        tile_to_collapse.collapse()

        stack: List[Tile] = []
        stack.append(tile_to_collapse)

        while(len(stack) > 0):
            tile = stack.pop()

            tile_possiblities = tile.possibilities
            directions = tile.directions

            for direction in directions:
                neighbour = tile.neighbours[direction]
                if neighbour.entropy != 0:
                    reduced = neighbour.constrain(tile_possiblities, direction)
                    if reduced == True:
                        stack.append(neighbour)    # When possibilities were reduced need to propagate further
        return 1
