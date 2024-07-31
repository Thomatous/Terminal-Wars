import os
from typing import List, Tuple
from src.world.world import World
from src.world.spritemap import Spritemap
from src.world.data.sprites import SPRITES
from src.player.base_player import BasePlayer

class Simulator():
    world: World
    players: List[BasePlayer]
    spritemap: Spritemap

    def __init__(self, world: World, players: List[BasePlayer]) -> None:
        self.world = world
        self.players = players
        self.spritemap = Spritemap(world.cols, world.rows)
    
    def _find_players_by_position(self, y: int, x: int) -> List[BasePlayer]:
        players_in_position = []
        for p in self.players:
            if p.position == (y, x):
                players_in_position.append(p)
        return players_in_position

    def _print_state(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        for y in range(self.world.rows):
            for x in range(self.world.cols):
                players_on_tile = self._find_players_by_position(y, x)
                if len(players_on_tile) == 1:
                    self.spritemap.add_sprite(y, x, players_on_tile[0].sprite)
                elif len(players_on_tile) > 1:
                    self.spritemap.add_sprite(y, x, "⚔⚔")
                elif self.world.tilemap[y][x].entropy == 0:
                    self.spritemap.add_sprite(y, x, SPRITES[self.world.tilemap[y][x].possibilities[0]])
                else:
                    self.spritemap.add_sprite(y, x, f" {self.world.tilemap[y][x].entropy}")
        print(self.spritemap)
    
    def _update_alive_players(self):
        alive_playes = []
        for p in self.players:
            if p.health > 0:
                alive_playes.append(p)
        self.players = alive_playes
    
    def _battle(self) -> None:
        for p1 in self.players:
            for p2 in self.players:
                if p1.sprite != p2.sprite and p1.position == p2.position:
                    p1.damage(p2.attack)
                    p2.damage(p1.attack)

    def simulate(self) -> None:
        self._print_state()
        input("Press Enter to continue...")

        for p in self.players:
            p.spawn(self.world)
        self._print_state()
        print("Spawned players!")
        input("Press Enter to continue...")
        
        while True:
            for p in self.players:
                p.move(self.world.tilemap[p.y][p.x].neighbours.values())
                p.damage(1)
            self._battle()
            self._update_alive_players()
            self._print_state()
            input("Press Enter to continue...")

