import os
from copy import deepcopy
from typing import List, Tuple
from src.world.tile import Tile
from src.world.world import World
from src.world.spritemap import Spritemap
from src.world.data.sprites import SPRITES
from src.player.base_player import Player
from src.player.mitosis import Mitosis

class Simulator():
    world: World
    players: List[Player]
    spritemap: Spritemap

    def __init__(self, world: World, players: List[Player]) -> None:
        self.world = world
        self.players = players
        self.spritemap = Spritemap(world.cols, world.rows)
    
    def _find_players_by_position(self, y: int, x: int) -> List[Player]:
        players_in_position = []
        for p in self.players:
            if p.position == (y, x):
                players_in_position.append(p)
        return players_in_position

    def _battle_on_tile(self, players_on_tile: List[Player]) -> bool:
        if len(players_on_tile) < 2:
            return False
        teams = [p.sprite for p in players_on_tile]
        if len(set(teams)) == 1:
            return False
        return True

    def _print_state(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        for y in range(self.world.rows):
            for x in range(self.world.cols):
                players_on_tile = self._find_players_by_position(y, x)
                if self._battle_on_tile(players_on_tile):
                    self.spritemap.add_sprite(y, x, "⚔⚔")
                elif len(players_on_tile) >= 1:
                    self.spritemap.add_sprite(y, x, players_on_tile[0].sprite)
                elif self.world.tilemap[y][x].entropy == 0:
                    self.spritemap.add_sprite(y, x, SPRITES[self.world.tilemap[y][x].possibilities[0]])
                else:
                    self.spritemap.add_sprite(y, x, f" {self.world.tilemap[y][x].entropy}")
        print(self.spritemap)
        print(f"Players: {len(self.players)}")

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
    
    def _get_available_movement_tiles(self, y: int, x: int) -> List[Tile]:
        available_movement_tiles = []
        for t in self.world.tilemap[y][x].neighbours.values():
            available_movement_tiles.append(t)
        available_movement_tiles.append(self.world.tilemap[y][x])
        return available_movement_tiles
    
    def _duplicate_players(self, players: List[Player]) -> None:
        for p in players:
            new_player = deepcopy(p)
            new_player.level = 1
            new_player.experience = 0
            self.players.append(new_player)

    def simulate(self) -> None:
        while self.world.generating:
            self.world.wave_function_collapse()
            self._print_state()
        print("Generated world!")
        input("Press Enter to continue...")

        for p in self.players:
            p.spawn(self.world)
        self._print_state()
        print("Spawned players!")
        input("Press Enter to continue...")
        
        while True:
            mitosized_players = []
            for p in self.players:
                p.move(self._get_available_movement_tiles(p.y, p.x))
                try:
                    p.gain_experience(self.world.tilemap[p.y][p.x].points)
                except Mitosis:
                    mitosized_players.append(p)    
                p.damage(1)
            self._duplicate_players(mitosized_players)
            self._update_alive_players()
            self._print_state()
            command = input("Press Enter to continue...")

            self._battle()
            self._update_alive_players()
            self._print_state()
            command = input("Press Enter to continue...")

