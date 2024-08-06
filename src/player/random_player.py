from random import randint
from src.player.enum.evolution import Evolution
from src.player.player import Player

class RandomPlayer(Player):
    def evolve(self, curr_attack: int, curr_health: int, curr_movement: int, level: int) -> Evolution:
        """
        Return one of the following evolutions:
        Evolution.ATTACK:   Increases your attack
        Evolution.HEALTH:   Increases your health
        Evolution.MOVEMENT: Incereases your movement
        Evolution.MITOSIS:  Splits your creature into two creatures with halved stats
        """
        evolutions = [Evolution.ATTACK, Evolution.HEALTH, Evolution.MOVEMENT, Evolution.MITOSIS]
        return evolutions[randint(0, 3)]
