import pygame
import sys
import random
import os
import math

class Ship:
    def __init__(self, size_name, positions: list):
        self.size_name = size_name 
        self.size = 4 if size_name == "2x2" else int(size_name)
        self.positions = positions  
        self.hits = 0               

    def isSunk(self) -> bool:
        return self.hits >= self.size

class Board:
    def __init__(self):
        self.grid_size = 10
        self.ships = []   
        self.shots = []  
        self.hits_coords = [] 
        self.miss_coords = [] 
        
    def add_ship(self, ship: Ship):
        self.ships.append(ship)

    def receive_shot(self, x: int, y: int) -> bool:
        if (x, y) in self.shots:
            return False
        
        self.shots.append((x, y))
        for ship in self.ships:
            if (x, y) in ship.positions:
                ship.hits += 1
                self.hits_coords.append((x, y))
                return True
        self.miss_coords.append((x, y))
        return False

    def all_ships_sunk(self) -> bool:
        if not self.ships: return False
        return all(ship.isSunk() for ship in self.ships)

class Player():
    def __init__(self, name: str, board: Board):
        self.name = name
        self.board = board  

class EasyAI(Player):
    def takeShot(self, enemy_board: Board):
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if (x, y) not in enemy_board.shots:
                return x, y 

class HardAI(Player):
    def __init__(self, name: str, board: Board):
        super().__init__(name, board)
        self.target_stack = []  

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 10 and 0 <= ny < 10:
                neighbors.append((nx, ny))
        return neighbors

    def takeShot(self, enemy_board: Board):
        while True:
            if self.target_stack:
                x, y = self.target_stack.pop()
                if (x, y) not in enemy_board.shots:
                    return x, y
            else:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                if (x, y) not in enemy_board.shots:
                    return x, y

def place_random_ships(board: Board):
    ship_sizes = [5, 4, 3, 3, 2, "2x2"]
    for size in ship_sizes:
        placed = False
        while not placed:
            positions = []
            if size == "2x2":
                x = random.randint(0, 8)
                y = random.randint(0, 8)
                positions = [(x, y), (x+1, y), (x, y+1), (x+1, y+1)]
            else:
                horizontal = random.choice([True, False])
                if horizontal:
                    x = random.randint(0, 9 - size)
                    y = random.randint(0, 9)
                    positions = [(x + i, y) for i in range(size)]
                else:
                    x = random.randint(0, 9)
                    y = random.randint(0, 9 - size)
                    positions = [(x, y + i) for i in range(size)]
            
            overlap = False
            for ship in board.ships:
                if any(p in ship.positions for p in positions):
                    overlap = True
                    break
            
            if not overlap:
                board.add_ship(Ship(size, positions))
                placed = True

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.radius = random.randint(4, 7)
        self.color = random.choice([(239, 68, 68), (249, 115, 22), (234, 179, 8)])
        self.lifetime = random.randint(20, 35)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        if self.radius > 0.3:
            self.radius -= 0.15

    def draw(self, screen):
        if self.lifetime > 0 and self.radius > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

class ExplosionManager:
    def __init__(self):
        self.particles = []

    def create_explosion(self, cx, cy):
        for _ in range(25):
            self.particles.append(Particle(cx, cy))

    def update(self):
        for p in self.particles[:]:
            p.update()
            if p.lifetime <= 0:
                self.particles.remove(p)

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)

explosion_manager = ExplosionManager()
