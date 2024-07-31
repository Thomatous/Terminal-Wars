from termcolor import colored
from src.world.world import World
from src.simulator import Simulator
from src.player.random_player import RandomPlayer

if __name__ == "__main__":
    world = World(20, 10)

    while world.generating:
        world.wave_function_collapse()
    print("Generated world!")

    simulator = Simulator(world,
                          [RandomPlayer(health=100, sprite=colored("AA", "red")),
                           RandomPlayer(health=130, sprite=colored("GG", "cyan")),
                           RandomPlayer(health=150, sprite=colored("CC", "magenta"))])
    simulator.simulate()

