from typing import List, Tuple
from src.world.world import World
from src.world.data.sprites import SPRITES
from src.player.base_player import BasePlayer

class Simulator():
    world: World
    players: List[BasePlayer]

    def __init__(self, world: World, players: List[BasePlayer]) -> None:
        self.world = world
        self.players = players
    
    def _print_state(self) -> None:
        map = ""
        for y in range(self.world.rows):
            row = ""
            for x in range(self.world.cols):
                if any(p.position == (y, x) for p in self.players):
                    row += "PP"
                elif self.world.tilemap[y][x].entropy == 0:
                    row += SPRITES[self.world.tilemap[y][x].possibilities[0]]
                else:
                    row += f" {self.world.tilemap[y][x].entropy}"
            map += row + '\n'
        print(map)

    def simulate(self) -> None:
        for p in self.players:
            p.spawn(self.world)
        while True:
            self._print_state()
            input("Press Enter to continue...")

