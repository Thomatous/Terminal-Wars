from termcolor import colored
from src.world.world import World
from src.simulator import Simulator
from src.player.random_player import RandomPlayer

if __name__ == "__main__":
    world = World(10, 10)
    simulator = Simulator(world,
                          [RandomPlayer(sprite=colored("AA", "red")),
                           RandomPlayer(sprite=colored("GG", "cyan")),
                           RandomPlayer(sprite=colored("CC", "magenta"))])
    simulator.simulate()

