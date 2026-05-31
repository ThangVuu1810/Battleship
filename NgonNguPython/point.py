import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battleship Game - Menu UI")
clock = pygame.time.Clock()

COLOR_BG = (22, 36, 71)        
COLOR_PANEL = (31, 64, 104)     
COLOR_TEXT = (255, 255, 255)    
COLOR_BTN = (74, 119, 161)      
COLOR_HOVER = (142, 168, 157)   
COLOR_ACTIVE = (46, 204, 113)   

font_title = pygame.font.SysFont("algerian", 45, bold=True)
font_menu = pygame.font.SysFont("algerian", 26, bold=True)
font_sub = pygame.font.SysFont("arial", 20) 

current_state = 'MAIN'

game_settings = {
    "sound": True,
    "music": True,
    "score": 1200,
    "difficulty": "Chua chon"
}

history_data = [
    "Tran 1: Thang - Du doan: 15 luot - Diem: +200",
    "Tran 2: Thua  - Du doan: 25 luot - Diem: -100",
    "Tran 3: Thang - Du doan: 18 luot - Diem: +150"
]

def draw_button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, active_color, (x, y, w, h), border_radius=10)
        if click[0] == 1 and action is not None:
            pygame.time.delay(150) 
            return action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h), border_radius=10)
        
    text_surf = font_menu.render(text, True, COLOR_TEXT)
    text_rect = text_surf.get_rect(center=((x + w/2), (y + h/2)))
    screen.blit(text_surf, text_rect)
    return None

def set_state(state_name):
    global current_state
    current_state = state_name

def toggle_sound(): game_settings["sound"] = not game_settings["sound"]
def toggle_music(): game_settings["music"] = not game_settings["music"]
def reset_score(): game_settings["score"] = 0
def choose_diff(diff):
    game_settings["difficulty"] = diff
    set_state('PLAYING')

def draw_main_menu():
    title_surf = font_title.render("BAN TAU CHIEN - BATTLESHIP", True, COLOR_TEXT)
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 80))
    
    draw_button("CHOI GAME", 300, 200, 200, 50, COLOR_BTN, COLOR_HOVER, lambda: set_state('DIFFICULTY'))
    draw_button("LICH SU", 300, 280, 200, 50, COLOR_BTN, COLOR_HOVER, lambda: set_state('HISTORY'))
    draw_button("CAU HINH", 300, 360, 200, 50, COLOR_BTN, COLOR_HOVER, lambda: set_state('SETTINGS'))
    draw_button("THOAT", 300, 440, 200, 50, (192, 57, 43), (231, 76, 60), sys.exit)

def draw_difficulty_menu():
    title_surf = font_title.render("CHON DO KHO CUA MAY", True, COLOR_TEXT)
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 100))
    
    draw_button("DE (Easy AI)", 300, 220, 200, 60, COLOR_BTN, COLOR_HOVER, lambda: choose_diff("De"))
    draw_button("KHO (Hard AI)", 300, 310, 200, 60, COLOR_BTN, COLOR_HOVER, lambda: choose_diff("Kho"))
    draw_button("QUAY LAI", 300, 420, 200, 50, (127, 140, 141), (149, 165, 166), lambda: set_state('MAIN'))

def draw_settings_menu():
    title_surf = font_title.render("CAU HINH TRO CHOI", True, COLOR_TEXT)
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 80))
    
    sound_txt = f"AM THANH: {'BAT' if game_settings['sound'] else 'TAT'}"
    music_txt = f"NHAC NEN: {'BAT' if game_settings['music'] else 'TAT'}"
    score_txt = f"DIEM SO HIEN TAI: {game_settings['score']}"
    
    draw_button(sound_txt, 250, 180, 300, 50, COLOR_BTN, COLOR_HOVER, toggle_sound)
    draw_button(music_txt, 250, 250, 300, 50, COLOR_BTN, COLOR_HOVER, toggle_music)
    draw_button("RESET DIEM SO", 250, 320, 300, 50, (230, 126, 34), (211, 84, 0), reset_score)
    
    score_surf = font_sub.render(score_txt, True, COLOR_TEXT)
    screen.blit(score_surf, (SCREEN_WIDTH//2 - score_surf.get_width()//2, 400))
    
    draw_button("QUAY LAI", 300, 480, 200, 50, (127, 140, 141), (149, 165, 166), lambda: set_state('MAIN'))

def draw_history_menu():
    title_surf = font_title.render("LICH SU TRAN CHIEN", True, COLOR_TEXT)
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 80))
    
    pygame.draw.rect(screen, COLOR_PANEL, (150, 160, 500, 250), border_radius=10)
    
    for i, records in enumerate(history_data):
        rec_surf = font_sub.render(records, True, COLOR_TEXT)
        screen.blit(rec_surf, (180, 190 + i * 40))
        
    draw_button("QUAY LAI", 300, 460, 200, 50, (127, 140, 141), (149, 165, 166), lambda: set_state('MAIN'))

def draw_playing_placeholder():
    title_surf = font_title.render("MAN HINH GAMEPLAY", True, COLOR_ACTIVE)
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, 150))
    
    info_txt = f"Dang chuan bi tran dau voi may do kho: {game_settings['difficulty'].upper()}"
    info_surf = font_sub.render(info_txt, True, COLOR_TEXT)
    screen.blit(info_surf, (SCREEN_WIDTH//2 - info_surf.get_width()//2, 250))
    
    hint_txt = "(Tai day se ve luoi 10x10 chon tau, sap xep doi hinh va ban)"
    hint_surf = font_sub.render(hint_txt, True, COLOR_TEXT)
    screen.blit(hint_surf, (SCREEN_WIDTH//2 - hint_surf.get_width()//2, 320))
    
    draw_button("QUAY LAI MENU", 300, 450, 200, 50, (192, 57, 43), (231, 76, 60), lambda: set_state('MAIN'))

running = True
while running:
    screen.fill(COLOR_BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if current_state == 'MAIN':
        draw_main_menu()
    elif current_state == 'DIFFICULTY':
        draw_difficulty_menu()
    elif current_state == 'SETTINGS':
        draw_settings_menu()
    elif current_state == 'HISTORY':
        draw_history_menu()
    elif current_state == 'PLAYING':
        draw_playing_placeholder()
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()