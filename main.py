from src.world import World

if __name__ == "__main__":
    world = World(40, 30)

    while world.generating:
        world.wave_function_collapse()
        print(world)

    print("Generated world!")
