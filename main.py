from src.world import World

if __name__ == "__main__":
    world = World(10, 10)

    is_running = True
    while is_running:
        world.wave_function_collapse()
        print(world)
        input("Press Enter to continue...")
