import os
from src.world.world import World

if __name__ == "__main__":
    world = World(40, 30)

    while world.generating:
        world.wave_function_collapse()
        print(world)
        os.system('cls' if os.name == 'nt' else 'clear')

    print(world)
    print("Generated world!")
