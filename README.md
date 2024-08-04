### Version 0.0.1

# Terminal Wars

### Overview 
This repository contains a python implementation of the [Wave Function Collapse](https://github.com/mxgmn/WaveFunctionCollapse) algorithm in [Python](https://www.python.org/) with the tile implementation presented on [this video](https://www.youtube.com/watch?v=qRtrj6Pua2A).  

This mini project can best be described as a simplistic terminal based battle simulator. Where the battling entities are inherited instances of the included `base_player.py` containing an implementation of the evolution function:
```Python
def evolve(self, curr_attack: int, curr_health: int, curr_movement: int, level: int) -> Evolution:
        """
        Return one of the following evolutions:
        Evolution.ATTACK:   Increases your attack
        Evolution.HEALTH:   Increases your health
        Evolution.MOVEMENT: Incereases your movement
        Evolution.MITOSIS:  Splits your creature into two creatures with halved stats
        """
        pass
```
### Requirements
1. Make sure you have python3 installed in your system
2. Install the dependencies using: `pip install -r requirements.txt`
> It is recommended that you use a [python virtual enviroment](https://docs.python.org/3/library/venv.html) in order to not clutter your system python.

### How to play
Create some player classes as described above and simply add them to the Simulator object in main.py like so:
```Python
    ...
    simulator = Simulator(world,
                          [RandomPlayer(sprite=colored("AA", "red")),
                           RandomPlayer(sprite=colored("GG", "cyan")),
                           RandomPlayer(sprite=colored("CC", "magenta"))])
    ...
```
Then simply run `python main.py`

