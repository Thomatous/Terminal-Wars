from typing import List

class Spritemap():
    def __init__(self, cols: int, rows: int) -> None:
        self.cols = cols
        self.rows = rows
        self.map: List[List[str]] = []
        for _ in range(self.rows):    
            row: List[str] = []
            for _ in range(self.cols):
                row.append("  ")
            self.map.append(row)
        
    def add_sprite(self, y: int, x: int, sprite: str) -> None:
        self.map[y][x] = sprite
    
    def __repr__(self) -> str:
        map = ""
        for y in range(self.rows):
            row = ""
            for x in range(self.cols):
                row += self.map[y][x]
            map += row + '\n'
        return map
