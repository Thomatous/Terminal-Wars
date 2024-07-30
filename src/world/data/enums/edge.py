from enum import Enum

class Edge(Enum):
    GRASS    = 0
    WATER    = 1
    FOREST   = 2
    COAST_N  = 3
    COAST_E  = 4
    COAST_S  = 5
    COAST_W  = 6
    FOREST_N = 7
    FOREST_E = 8
    FOREST_S = 9
    FOREST_W = 10
    ROCK_N   = 11
    ROCK_E   = 12
    ROCK_S   = 13
    ROCK_W   = 14
    ROCK     = 15