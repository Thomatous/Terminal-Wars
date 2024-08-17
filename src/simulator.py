import os
import time
from typing import List
from copy import deepcopy
from playsound import playsound
from src.world.tile import Tile
from src.world.world import World
from src.world.spritemap import Spritemap
from src.world.data.sprites import SPRITES
from src.player.player import Player
from src.player.mitosis import Mitosis
from src.player.enum.evolution import Evolution

class Simulator():
    world: World
    players: List[Player]
    spritemap: Spritemap

    def __init__(self, world: World, players: List[Player]) -> None:
        self.world = world
        self.players = players
        self.spritemap = Spritemap(world.cols, world.rows)
    
    @property
    def teams(self) -> set:
        sprites = [p.sprite for p in self.players]
        return set(sprites)
    
    def _get_team_players(self, sprite: str) -> List[Player]:
        team_players = []
        for p in self.players:
            if p.sprite ==  sprite:
                team_players.append(p)
        return team_players
    
    def _get_team_evolutions(self, sprite: str) -> List[Evolution]:
        team_players = self._get_team_players(sprite)
        evolutions = []
        for p in team_players:
            evolutions += p.history
        return evolutions

    def _get_team_health(self, sprite: str) -> List[Evolution]:
        evolutions = self._get_team_evolutions(sprite)
        healths = []
        for e in evolutions:
            if e == Evolution.HEALTH:
                healths.append(e)
        return healths
    
    def _get_team_attack(self, sprite: str) -> List[Evolution]:
        evolutions = self._get_team_evolutions(sprite)
        attacks = []
        for e in evolutions:
            if e == Evolution.ATTACK:
                attacks.append(e)
        return attacks
    
    def _get_team_movement(self, sprite: str) -> List[Evolution]:
        evolutions = self._get_team_evolutions(sprite)
        movement = []
        for e in evolutions:
            if e == Evolution.MOVEMENT:
                movement.append(e)
        return movement
    
    def _get_team_mitosis(self, sprite: str) -> List[Evolution]:
        evolutions = self._get_team_evolutions(sprite)
        mitosis = []
        for e in evolutions:
            if e == Evolution.MITOSIS:
                mitosis.append(e)
        return mitosis
    
    def _get_team_highest_level(self, sprite: str) -> int:
        team_players = self._get_team_players(sprite)
        levels = [p.level for p in team_players]
        return max(levels)
    
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

    def _print_state(self, sleep: int = 0) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        for y in range(self.world.rows):
            for x in range(self.world.cols):
                players_on_tile = self._find_players_by_position(y, x)
                if self._battle_on_tile(players_on_tile):
                    self.spritemap.add_sprite(y, x, "⚔⚔")
                    playsound("/home/thpapa/Projects/Terminal-Wars/assets/sfx/battle.mp3", block=False)
                elif len(players_on_tile) >= 1:
                    self.spritemap.add_sprite(y, x, players_on_tile[0].sprite)
                elif self.world.tilemap[y][x].entropy == 0:
                    self.spritemap.add_sprite(y, x, SPRITES[self.world.tilemap[y][x].possibilities[0]])
                else:
                    self.spritemap.add_sprite(y, x, f" {self.world.tilemap[y][x].entropy}")
        print(self.spritemap)
        print(f"Total players: {len(self.players)}")
        for t in self.teams:
            print(t, 
                  "\tPlayers:",  len(self._get_team_players(t)), 
                  "\tEvolutions:", len(self._get_team_evolutions(t)),
                  "\tHealth:", len(self._get_team_health(t)),
                  "\tAttack:", len(self._get_team_attack(t)), 
                  "\tMovement:", len(self._get_team_movement(t)),
                  "\tMitosis", len(self._get_team_mitosis(t)),
                  "\tHighest level:", self._get_team_highest_level(t)            
                  )

            
        
        time.sleep(sleep)

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
            new_player.level_threshold = 100
            new_player.history = []
            self.players.append(new_player)
            playsound("/home/thpapa/Projects/Terminal-Wars/assets/sfx/mitosis.mp3", block=False)


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
        
        # playsound('/home/thpapa/Projects/Terminal-Wars/assets/soundtracks/world.mp3', block=False)
        while len(self.teams) > 1:
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
            self._print_state(0.3)
            # command = input("Press Enter to continue...")

            self._battle()
            self._update_alive_players()
            self._print_state(0.3)
            # command = input("Press Enter to continue...")
        
        if len(list(self.teams)) > 0:
            print("WINNER:", list(self.teams)[0])
        else:
            print("TIE")
