def save_match_history(is_human_win):
    global history_data, game_settings, board_human, board_ai
    
    human_alive = sum(1 for ship in board_human.ships if not ship.isSunk())
    ai_alive = sum(1 for ship in board_ai.ships if not ship.isSunk())
    diff = game_settings["difficulty"]
    
    if is_human_win:
        result = "THANG"
        ship_diff = human_alive  
        score_change = 200 if diff == "Kho" else 100
    else:
        result = "THUA"
        ship_diff = ai_alive     
        score_change = -100 if diff == "Kho" else -50
        
    game_settings["score"] += score_change
    record = f"KQ: {result} | May: {diff.upper()} | Tau con lai: {ship_diff} | Diem: {score_change:+d}"
    history_data.insert(0, record)
    if len(history_data) > 7:
        history_data.pop()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

music_file = os.path.join(BASE_DIR, "They Sold Their Souls - Bonnie Grace.mp3")
if not os.path.exists(music_file):
    music_file = os.path.join(BASE_DIR, "assets", "They Sold Their Souls - Bonnie Grace.mp3")

cannon_file = os.path.join(BASE_DIR, "Cannon sound effect for ships.mp3")
if not os.path.exists(cannon_file):
    cannon_file = os.path.join(BASE_DIR, "assets", "Cannon sound effect for ships.mp3")

try:
    if os.path.exists(music_file):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(0.4) 
        if game_settings["music"]:
            pygame.mixer.music.play(-1) 
except Exception as e:
    print(f"Không thể tải nhạc nền: {e}")

try:
    if os.path.exists(cannon_file):
        cannon_sound = pygame.mixer.Sound(cannon_file)
        cannon_sound.set_volume(0.8) 
    else:
        cannon_sound = None
except Exception as e:
    print(f"Không thể tải âm thanh pháo: {e}")
    cannon_sound = None


monitor_info = pygame.display.Info()
SCREEN_WIDTH = monitor_info.current_w 
SCREEN_HEIGHT = monitor_info.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Battleship Game")
clock = pygame.time.Clock() 

try:
    bg_path = os.path.join(BASE_DIR, "background.jpg")
    if not os.path.exists(bg_path):
        bg_path = os.path.join(BASE_DIR, "assets", "background.jpg")
    if os.path.exists(bg_path):
        bg_image_raw = pygame.image.load(bg_path)
        bg_image = pygame.transform.scale(bg_image_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_image.set_alpha(160) 
        has_bg = True
    else:
        has_bg = False
except:
    has_bg = False 

COLOR_BG = (15, 23, 42)        
COLOR_PANEL = (30, 41, 59, 200) 
COLOR_TEXT = (255, 255, 255)    
COLOR_BTN = (51, 65, 85)      
COLOR_HOVER = (71, 85, 105)   
COLOR_ACTIVE = (34, 197, 94)   
COLOR_MISS = (203, 213, 225)

COLOR_HOLE_BORDER = (40, 40, 45)  
COLOR_HOLE_FIRE = (220, 38, 38)   
COLOR_HOLE_CORE = (10, 10, 12)    

CELL_SIZE = int(SCREEN_HEIGHT * 0.052) 
GRID_SIZE_PX = 10 * CELL_SIZE

def load_ship_images():
    images = {}
    ship_files = {2: "1x2.png", 3: "1x3.png", 4: "1x4.png", 5: "1x5.png", "2x2": "2x2.png"}
    
    for key, filename in ship_files.items():
        path = os.path.join(BASE_DIR, filename) 
        if not os.path.exists(path):
            path = os.path.join(BASE_DIR, "assets", filename)
            
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            if key == "2x2":
                images[key] = pygame.transform.scale(img, (CELL_SIZE * 2, CELL_SIZE * 2))
            else:
                images[key] = pygame.transform.scale(img, (CELL_SIZE * int(key), CELL_SIZE))
        else:
            if key == "2x2":
                surf = pygame.Surface((CELL_SIZE * 2, CELL_SIZE * 2), pygame.SRCALPHA)
                surf.fill((148, 163, 184, 200))
            else:
                surf = pygame.Surface((CELL_SIZE * int(key), CELL_SIZE), pygame.SRCALPHA)
                surf.fill((100, 116, 139, 200))
            images[key] = surf
    return images

SHIP_IMAGES = load_ship_images()

def load_custom_assets():
    assets = {"water": None, "human_avatar": None, "ai_avatar": None}
    
    water_path = os.path.join(BASE_DIR, "Water_tiles.jpg")
    if not os.path.exists(water_path):
        water_path = os.path.join(BASE_DIR, "assets", "Water_tiles.jpg")
    if os.path.exists(water_path):
        raw_water = pygame.image.load(water_path).convert()
        assets["water"] = pygame.transform.scale(raw_water, (GRID_SIZE_PX, GRID_SIZE_PX))
        
    human_path = os.path.join(BASE_DIR, "Jack_sparrow(human).png")
    if not os.path.exists(human_path):
        human_path = os.path.join(BASE_DIR, "assets", "Jack_sparrow(human).png")
    if os.path.exists(human_path):
        raw_human = pygame.image.load(human_path).convert_alpha()
        assets["human_avatar"] = pygame.transform.scale(raw_human, (120, 180))
        
    ai_path = os.path.join(BASE_DIR, "red_pirate(AI).png")
    if not os.path.exists(ai_path):
        ai_path = os.path.join(BASE_DIR, "assets", "red_pirate(AI).png")
    if os.path.exists(ai_path):
        raw_ai = pygame.image.load(ai_path).convert_alpha()
        assets["ai_avatar"] = pygame.transform.scale(raw_ai, (120, 180))
        
    return assets

CUSTOM_ASSETS = load_custom_assets()

font_title = pygame.font.SysFont("algerian", int(SCREEN_HEIGHT * 0.06), bold=True)
font_menu = pygame.font.SysFont("algerian", int(SCREEN_HEIGHT * 0.035), bold=True)
font_sub = pygame.font.SysFont("arial", int(SCREEN_HEIGHT * 0.025), bold=True) 

current_state = 'MAIN'
board_human = None
board_ai = None
ai_player = None
current_turn = "HUMAN"
game_over = False
winner_text = ""

GRID_OFFSET_X_HUMAN = (SCREEN_WIDTH // 2) - GRID_SIZE_PX - int(SCREEN_WIDTH * 0.06)
GRID_OFFSET_X_AI = (SCREEN_WIDTH // 2) + int(SCREEN_WIDTH * 0.06)
GRID_OFFSET_Y = (SCREEN_HEIGHT // 2) - (GRID_SIZE_PX // 2) - 20

placement_sizes = [5, 4, 3, 3, 2, "2x2"]
placement_index = 0          
placement_horizontal = True  

def draw_button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, active_color, (x, y, w, h), border_radius=12)
        if click[0] == 1 and action is not None:
            pygame.time.delay(250) 
            return action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h), border_radius=12)
    text_surf = font_menu.render(text, True, COLOR_TEXT)
    text_rect = text_surf.get_rect(center=((x + w/2), (y + h/2)))
    screen.blit(text_surf, text_rect)

def set_state(state_name):
    global current_state
    current_state = state_name

def toggle_sound(): game_settings["sound"] = not game_settings["sound"]
def toggle_music(): 
    game_settings["music"] = not game_settings["music"]
    if game_settings["music"]: pygame.mixer.music.unpause()
    else: pygame.mixer.music.pause()
def reset_score(): game_settings["score"] = 0

def start_game(diff):
    global board_human, board_ai, ai_player, current_turn, game_over, winner_text, placement_index
    game_settings["difficulty"] = diff
    board_human = Board() 
    board_ai = Board()
    place_random_ships(board_ai) 
    if diff == "Kho": ai_player = HardAI("AI Khó", board_ai)
    else: ai_player = EasyAI("AI Dễ", board_ai)
    current_turn = "HUMAN"
    game_over = False
    winner_text = ""
    placement_index = 0 
    set_state('PLACEMENT')

def draw_main_menu():
    panel_w, panel_h = int(SCREEN_WIDTH * 0.4), int(SCREEN_HEIGHT * 0.65)
    panel_x, panel_y = (SCREEN_WIDTH // 2) - (panel_w // 2), (SCREEN_HEIGHT // 2) - (panel_h // 2) + 30
    s = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    s.fill((30, 41, 59, 220))
    screen.blit(s, (panel_x, panel_y))
    pygame.draw.rect(screen, (100, 116, 139), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=4)
    title_surf = font_title.render("BAN TAU CHIEN - BATTLESHIP", True, COLOR_TEXT)
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, panel_y - int(SCREEN_HEIGHT * 0.12)))
    btn_w, btn_h = int(panel_w * 0.7), int(SCREEN_HEIGHT * 0.08)
    btn_x = (SCREEN_WIDTH // 2) - (btn_w // 2)
    start_y = panel_y + int(panel_h * 0.1)
    gap = btn_h + int(SCREEN_HEIGHT * 0.03)
    draw_button("CHOI GAME", btn_x, start_y, btn_w, btn_h, COLOR_BTN, COLOR_HOVER, lambda: set_state('DIFFICULTY'))
    draw_button("LICH SU", btn_x, start_y + gap, btn_w, btn_h, COLOR_BTN, COLOR_HOVER, lambda: set_state('HISTORY'))
    draw_button("CAU HINH", btn_x, start_y + gap*2, btn_w, btn_h, COLOR_BTN, COLOR_HOVER, lambda: set_state('SETTINGS'))
    draw_button("THOAT GAME", btn_x, start_y + gap*3, btn_w, btn_h, (185, 28, 28), (220, 38, 38), sys.exit)

def draw_difficulty_menu():
    panel_w, panel_h = int(SCREEN_WIDTH * 0.4), int(SCREEN_HEIGHT * 0.5)
    panel_x, panel_y = (SCREEN_WIDTH // 2) - (panel_w // 2), (SCREEN_HEIGHT // 2) - (panel_h // 2) + 40
    s = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    s.fill((30, 41, 59, 220))
    screen.blit(s, (panel_x, panel_y))
    pygame.draw.rect(screen, (100, 116, 139), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=4)
    title_surf = font_title.render("CHON DO KHO CUA MAY", True, COLOR_TEXT)
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, panel_y - int(SCREEN_HEIGHT * 0.12)))
    btn_w, btn_h = int(panel_w * 0.7), int(SCREEN_HEIGHT * 0.08)
    btn_x = (SCREEN_WIDTH // 2) - (btn_w // 2)
    draw_button("DE (Easy AI)", btn_x, panel_y + int(panel_h * 0.15), btn_w, btn_h, COLOR_BTN, COLOR_HOVER, lambda: start_game("De"))
    draw_button("KHO (Hard AI)", btn_x, panel_y + int(panel_h * 0.4), btn_w, btn_h, COLOR_BTN, COLOR_HOVER, lambda: start_game("Kho"))
    draw_button("QUAY LAI", btn_x, panel_y + int(panel_h * 0.7), btn_w, btn_h, (100, 116, 139), (148, 163, 184), lambda: set_state('MAIN'))

def draw_settings_menu():
    panel_w, panel_h = int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.6)
    panel_x, panel_y = (SCREEN_WIDTH // 2) - (panel_w // 2), (SCREEN_HEIGHT // 2) - (panel_h // 2) + 40
    s = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    s.fill((30, 41, 59, 220))
    screen.blit(s, (panel_x, panel_y))
    pygame.draw.rect(screen, (100, 116, 139), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=4)
    title_surf = font_title.render("CAU HINH TRO CHOI", True, COLOR_TEXT)
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, panel_y - int(SCREEN_HEIGHT * 0.12)))
    sound_txt = f"AM THANH: {'BAT' if game_settings['sound'] else 'TAT'}"
    music_txt = f"NHAC NEN: {'BAT' if game_settings['music'] else 'TAT'}"
    score_txt = f"DIEM SO HIEN TAI: {game_settings['score']}"
    btn_w, btn_h = int(panel_w * 0.7), int(SCREEN_HEIGHT * 0.07)
    btn_x = (SCREEN_WIDTH // 2) - (btn_w // 2)
    draw_button(sound_txt, btn_x, panel_y + int(panel_h * 0.12), btn_w, btn_h, COLOR_BTN, COLOR_HOVER, toggle_sound)
    draw_button(music_txt, btn_x, panel_y + int(panel_h * 0.3), btn_w, btn_h, COLOR_BTN, COLOR_HOVER, toggle_music)
    draw_button("RESET DIEM SO", btn_x, panel_y + int(panel_h * 0.48), btn_w, btn_h, (217, 119, 6), (245, 158, 11), reset_score)
    score_surf = font_sub.render(score_txt, True, COLOR_TEXT)
    screen.blit(score_surf, (SCREEN_WIDTH//2 - score_surf.get_width()//2, panel_y + int(panel_h * 0.68)))
    draw_button("QUAY LAI", btn_x, panel_y + int(panel_h * 0.8), btn_w, btn_h, (100, 116, 139), (148, 163, 184), lambda: set_state('MAIN'))

def draw_history_menu():
    panel_w, panel_h = int(SCREEN_WIDTH * 0.6), int(SCREEN_HEIGHT * 0.5)
    panel_x, panel_y = (SCREEN_WIDTH // 2) - (panel_w // 2), (SCREEN_HEIGHT // 2) - (panel_h // 2) + 40
    s = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    s.fill((30, 41, 59, 220))
    screen.blit(s, (panel_x, panel_y))
    pygame.draw.rect(screen, (100, 116, 139), (panel_x, panel_y, panel_w, panel_h), 2, border_radius=4)
    title_surf = font_title.render("LICH SU TRAN CHIEN", True, COLOR_TEXT)
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, panel_y - int(SCREEN_HEIGHT * 0.12)))
    for i, records in enumerate(history_data):
        rec_surf = font_sub.render(records, True, COLOR_TEXT)
        screen.blit(rec_surf, (panel_x + 30, panel_y + 80 + i * 45))
    btn_w, btn_h = int(panel_w * 0.4), int(SCREEN_HEIGHT * 0.07)
    draw_button("QUAY LAI", SCREEN_WIDTH//2 - btn_w//2, panel_y + panel_h - btn_h - 30, btn_w, btn_h, (100, 116, 139), (148, 163, 184), lambda: set_state('MAIN'))

def draw_grid(board, offset_x, offset_y, hide_ships):
    if CUSTOM_ASSETS["water"]:
        screen.blit(CUSTOM_ASSETS["water"], (offset_x, offset_y))
    else:
        grid_bg = pygame.Surface((GRID_SIZE_PX, GRID_SIZE_PX), pygame.SRCALPHA)
        grid_bg.fill((15, 23, 42, 180)) 
        screen.blit(grid_bg, (offset_x, offset_y))

    for x in range(10):
        for y in range(10):
            rect = (offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

    pygame.draw.rect(screen, (255, 255, 255), (offset_x - 4, offset_y - 4, GRID_SIZE_PX + 8, GRID_SIZE_PX + 8), 3, border_radius=4)

    if not hide_ships and board is not None:
        for ship in board.ships:
            start_x, start_y = ship.positions[0]
            px = offset_x + start_x * CELL_SIZE
            py = offset_y + start_y * CELL_SIZE
            
            is_horizontal = True
            if ship.size_name != "2x2" and len(ship.positions) > 1:
                is_horizontal = (ship.positions[0][1] == ship.positions[1][1])

            img_to_draw = SHIP_IMAGES[ship.size_name].copy()
            if ship.size_name != "2x2" and not is_horizontal:
                img_to_draw = pygame.transform.rotate(img_to_draw, -90)
                
            screen.blit(img_to_draw, (px, py))

    for x in range(10):
        for y in range(10):
            rect = (offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            center = (rect[0] + CELL_SIZE//2, rect[1] + CELL_SIZE//2)
            if board is not None:
                if (x, y) in board.hits_coords:
                    r_max = CELL_SIZE // 2 - 2
                    pygame.draw.circle(screen, COLOR_HOLE_BORDER, center, r_max)
                    pygame.draw.circle(screen, COLOR_HOLE_FIRE, center, int(r_max * 0.7))
                    pygame.draw.circle(screen, COLOR_HOLE_CORE, center, int(r_max * 0.4))
                elif (x, y) in board.miss_coords:
                    pygame.draw.circle(screen, COLOR_MISS, center, CELL_SIZE//2 - int(CELL_SIZE*0.3))

def draw_placement_state():
    title_surf = font_title.render("DAT TAU CUA BAN", True, (34, 197, 94))
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, int(SCREEN_HEIGHT * 0.04)))
    
    info_x = GRID_OFFSET_X_HUMAN + GRID_SIZE_PX + int(SCREEN_WIDTH * 0.06)
    current_size = placement_sizes[placement_index]
    size_str = "Khối vuông 2x2" if current_size == "2x2" else f"{current_size} ô liền"
    guide_txt1 = font_menu.render(f"Loai tau: {size_str}", True, COLOR_TEXT)
    guide_txt2 = font_sub.render("Nhan [SPACE] de XOAY huong tau", True, (234, 179, 8))
    guide_txt3 = font_menu.render(f"Huong: {'NGANG' if placement_horizontal else 'DOC'}", True, COLOR_TEXT)
    screen.blit(guide_txt1, (info_x, GRID_OFFSET_Y + 50))
    if current_size != "2x2":
        screen.blit(guide_txt2, (info_x, GRID_OFFSET_Y + 110))
        screen.blit(guide_txt3, (info_x, GRID_OFFSET_Y + 160))
    
    av_x = GRID_OFFSET_X_HUMAN - 160
    av_y = GRID_OFFSET_Y
    pygame.draw.rect(screen, (30, 41, 59), (av_x, av_y, 132, 192), border_radius=8)
    pygame.draw.rect(screen, (34, 197, 94), (av_x, av_y, 132, 192), 2, border_radius=8)
    if CUSTOM_ASSETS["human_avatar"]:
        screen.blit(CUSTOM_ASSETS["human_avatar"], (av_x + 6, av_y + 6))
    
    draw_grid(board_human, GRID_OFFSET_X_HUMAN, GRID_OFFSET_Y, hide_ships=False)
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if GRID_OFFSET_X_HUMAN <= mouse_x < GRID_OFFSET_X_HUMAN + GRID_SIZE_PX and \
       GRID_OFFSET_Y <= mouse_y < GRID_OFFSET_Y + GRID_SIZE_PX:
        gx = (mouse_x - GRID_OFFSET_X_HUMAN) // CELL_SIZE
        gy = (mouse_y - GRID_OFFSET_Y) // CELL_SIZE
        size = placement_sizes[placement_index]
        temp_positions = []
        is_valid = True
        
        if size == "2x2":
            if gx + 1 < 10 and gy + 1 < 10: temp_positions = [(gx, gy), (gx + 1, gy), (gx, gy + 1), (gx + 1, gy+1)]
            else: is_valid = False
        else:
            if placement_horizontal:
                if gx + size <= 10: temp_positions = [(gx + i, gy) for i in range(size)]
                else: is_valid = False
            else:
                if gy + size <= 10: temp_positions = [(gx, gy + i) for i in range(size)]
                else: is_valid = False
            
        if is_valid:
            for ship in board_human.ships:
                if any(p in ship.positions for p in temp_positions):
                    is_valid = False
                    break
                    
        if is_valid:
            px = GRID_OFFSET_X_HUMAN + gx * CELL_SIZE
            py = GRID_OFFSET_Y + gy * CELL_SIZE
            preview_img = SHIP_IMAGES[size].copy()
            if size != "2x2" and not placement_horizontal:
                preview_img = pygame.transform.rotate(preview_img, -90)
            preview_img.set_alpha(160)
            screen.blit(preview_img, (px, py))
        else:
            for (tx, ty) in temp_positions:
                r_px = GRID_OFFSET_X_HUMAN + tx * CELL_SIZE + 2
                r_py = GRID_OFFSET_Y + ty * CELL_SIZE + 2
                s = pygame.Surface((CELL_SIZE-4, CELL_SIZE-4))
                s.set_alpha(120)
                s.fill((239, 68, 68))
                screen.blit(s, (r_px, r_py))

    btn_w, btn_h = int(SCREEN_WIDTH * 0.2), int(SCREEN_HEIGHT * 0.07)
    draw_button("QUAY LAI MENU", SCREEN_WIDTH//2 - btn_w//2, SCREEN_HEIGHT - btn_h - 40, btn_w, btn_h, (100, 116, 139), (148, 163, 184), lambda: set_state('MAIN'))

def draw_playing_state():
    title_surf = font_title.render(f"BATTLESHIP - DO KHO: {game_settings['difficulty'].upper()}", True, (34, 197, 94))
    screen.blit(title_surf, (SCREEN_WIDTH//2 - title_surf.get_width()//2, int(SCREEN_HEIGHT * 0.04)))
    
    txt_human = font_menu.render("BAN DO CUA BAN", True, COLOR_TEXT)
    screen.blit(txt_human, (GRID_OFFSET_X_HUMAN + (GRID_SIZE_PX//2) - txt_human.get_width()//2, GRID_OFFSET_Y - 50))
    txt_ai = font_menu.render("BAN DO CUA AI", True, (239, 68, 68))
    screen.blit(txt_ai, (GRID_OFFSET_X_AI + (GRID_SIZE_PX//2) - txt_ai.get_width()//2, GRID_OFFSET_Y - 50))

    h_av_x = GRID_OFFSET_X_HUMAN - 160
    pygame.draw.rect(screen, (30, 41, 59), (h_av_x, GRID_OFFSET_Y, 132, 192), border_radius=8)
    pygame.draw.rect(screen, (34, 197, 94), (h_av_x, GRID_OFFSET_Y, 132, 192), 2, border_radius=8)
    if CUSTOM_ASSETS["human_avatar"]:
        screen.blit(CUSTOM_ASSETS["human_avatar"], (h_av_x + 6, GRID_OFFSET_Y + 6))

    ai_av_x = GRID_OFFSET_X_AI + GRID_SIZE_PX + 28
    pygame.draw.rect(screen, (30, 41, 59), (ai_av_x, GRID_OFFSET_Y, 132, 192), border_radius=8)
    pygame.draw.rect(screen, (239, 68, 68), (ai_av_x, GRID_OFFSET_Y, 132, 192), 2, border_radius=8)
    if CUSTOM_ASSETS["ai_avatar"]:
        screen.blit(CUSTOM_ASSETS["ai_avatar"], (ai_av_x + 6, GRID_OFFSET_Y + 6))

    draw_grid(board_human, GRID_OFFSET_X_HUMAN, GRID_OFFSET_Y, hide_ships=False)
    draw_grid(board_ai, GRID_OFFSET_X_AI, GRID_OFFSET_Y, hide_ships=True)

    explosion_manager.draw(screen)

    if game_over:
        msg_surf = font_title.render(winner_text, True, (234, 179, 8))
        screen.blit(msg_surf, (SCREEN_WIDTH//2 - msg_surf.get_width()//2, SCREEN_HEIGHT - int(SCREEN_HEIGHT * 0.22)))
    else:
        turn_txt = "LUOT CUA BAN" if current_turn == "HUMAN" else "LUOT CUA AI..."
        turn_color = (34, 197, 94) if current_turn == "HUMAN" else (203, 213, 225)
        turn_surf = font_menu.render(turn_txt, True, turn_color)
        screen.blit(turn_surf, (SCREEN_WIDTH//2 - turn_surf.get_width()//2, SCREEN_HEIGHT - int(SCREEN_HEIGHT * 0.22)))

    btn_w, btn_h = int(SCREEN_WIDTH * 0.15), int(SCREEN_HEIGHT * 0.07)
    draw_button("THOAT", SCREEN_WIDTH//2 - btn_w//2, SCREEN_HEIGHT - btn_h - 40, btn_w, btn_h, (185, 28, 28), (220, 38, 38), lambda: set_state('MAIN'))

running = True
