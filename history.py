import pygame
import os
import random
import math
import json

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battleship Game")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

def load_match_history():
    if not os.path.exists(HISTORY_FILE):
        default_data = {"player_wins": 0, "ai_wins": 0, "total_matches": 0}
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error: {e}")
        return default_data
    
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"player_wins": 0, "ai_wins": 0, "total_matches": 0}

def save_match_history(winner):
    data = load_match_history()
    data["total_matches"] += 1
    if winner == "Player":
        data["player_wins"] += 1
    elif winner == "AI":
        data["ai_wins"] += 1
        
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Saved: {winner} won match {data['total_matches']}")
    except Exception as e:
        print(f"Error: {e}")

match_data = load_match_history()

COLOR_BG = (15, 23, 42)
COLOR_PANEL = (30, 41, 59, 200)
COLOR_TEXT = (248, 250, 252)
COLOR_GRID = (71, 85, 105)
COLOR_SHIP = (148, 163, 184)
COLOR_HIT = (239, 68, 68)
COLOR_MISS = (100, 116, 139)
COLOR_HOLE_BORDER = (30, 41, 59)
COLOR_HOLE_FIRE = (249, 115, 22)
COLOR_HOLE_CORE = (15, 23, 42)
COLOR_BTN = (51, 65, 85)
COLOR_HOVER = (71, 85, 105)
COLOR_ACTIVE = (34, 197, 94)

CELL_SIZE = int(SCREEN_HEIGHT * 0.052)
GRID_SIZE_PX = 10 * CELL_SIZE

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.radius = random.uniform(3.0, 5.0)
        self.lifetime = random.randint(20, 35)
        self.color = random.choice([(239, 68, 68), (249, 115, 22), (234, 179, 8)])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        if self.radius > 0.3:
            self.radius -= 0.15

    def draw(self, surface):
        if self.radius > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))

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

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

def draw_grid(surface, x_offset, y_offset, grid, show_ships=True):
    for i in range(11):
        pygame.draw.line(surface, COLOR_GRID, (x_offset + i * CELL_SIZE, y_offset), (x_offset + i * CELL_SIZE, y_offset + GRID_SIZE_PX), 1)
        pygame.draw.line(surface, COLOR_GRID, (x_offset, y_offset + i * CELL_SIZE), (x_offset + GRID_SIZE_PX, y_offset + i * CELL_SIZE), 1)

def draw_ui(surface):
    panel_rect = pygame.Rect(900, 50, 260, 600)
    pygame.draw.rect(surface, COLOR_PANEL, panel_rect, border_radius=12)
    
    font = pygame.font.SysFont("Arial", 20)
    txt_total = font.render(f"Total Matches: {match_data['total_matches']}", True, COLOR_TEXT)
    txt_wins = font.render(f"Player Wins: {match_data['player_wins']}", True, COLOR_ACTIVE)
    txt_loss = font.render(f"AI Wins: {match_data['ai_wins']}", True, COLOR_HIT)
    
    surface.blit(txt_total, (920, 80))
    surface.blit(txt_wins, (920, 120))
    surface.blit(txt_loss, (920, 150))

explosion_manager = ExplosionManager()
clock = pygame.time.Clock()

player_ships_left = 5
ai_ships_left = 5
game_over = False
winner = None
history_saved = False 
has_bg = False

running = True
while running:
    clock.tick(60)
    
    if has_bg: 
        screen.blit(bg_image, (0, 0))
    else: 
        screen.fill(COLOR_BG)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t: 
                ai_ships_left = 0

    if not game_over:
        if player_ships_left == 0:
            game_over = True
            winner = "AI"
        elif ai_ships_left == 0:
            game_over = True
            winner = "Player"
            
    if game_over and not history_saved:
        save_match_history(winner)
        match_data = load_match_history()
        history_saved = True

    draw_grid(screen, 50, 100, None)
    draw_grid(screen, 500, 100, None)
    draw_ui(screen)
    
    explosion_manager.update()
    explosion_manager.draw(screen)
    
    if game_over:
        font_end = pygame.font.SysFont("Arial", 40, bold=True)
        txt_end = font_end.render(f"{winner.upper()} WINS!", True, COLOR_ACTIVE if winner == "Player" else COLOR_HIT)
        screen.blit(txt_end, (250, 20))

    pygame.display.flip()

pygame.quit()
