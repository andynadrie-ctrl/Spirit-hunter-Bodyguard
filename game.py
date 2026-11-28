import os
import pygame

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()

# ==================================================
# BACKGROUND MUSIC
# ==================================================

MUSIC_VOLUME = 0.5
music_muted = False


def init_music():
    audio_folder = os.path.join("assets", "audio")
    supported_formats = (".ogg", ".wav", ".mp3")

    if not os.path.isdir(audio_folder):
        print("Folder 'assets/audio' not found.")
        return

    candidates = []
    for ext in supported_formats:
        for file in os.listdir(audio_folder):
            lower = file.lower()
            if lower.startswith("spirit_fight") and lower.endswith(ext):
                candidates.append(os.path.join(audio_folder, file))

    if not candidates:
        print(
            "Audio file not found in assets/audio/. "
            "Place spirit_fight.wav, .ogg, or .mp3 inside assets/audio/."
        )
        return

    for music_path in candidates:
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            pygame.mixer.music.play(-1)
            print("Now playing:", music_path)
            return
        except pygame.error as e:
            print(f"Could not decode '{music_path}': {e}")


init_music()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.RESIZABLE
)

pygame.display.set_caption("Spirit Hunter")


# ==================================================
# HELPER FOR CASE-INSENSITIVE CHARACTER SPRITES
# ==================================================

def load_character_sprite(folder_name, filename="00.png", size=(170, 170)):
    char_dir = os.path.join("assets", "Character")
    target = folder_name.lower()
    matched_folder = folder_name

    if os.path.isdir(char_dir):
        for entry in os.listdir(char_dir):
            if entry.lower() == target and os.path.isdir(os.path.join(char_dir, entry)):
                matched_folder = entry
                break

    full_path = os.path.join(char_dir, matched_folder, filename)
    image = pygame.image.load(full_path).convert_alpha()
    return pygame.transform.scale(image, size)


# ==================================================
# BACKGROUND
# ==================================================

original_background = pygame.image.load(
    "assets/backgrounds/back4 town.png"
).convert()

ZOOM = 1.5


def scale_background(screen_height):
    scale = (screen_height * ZOOM) / original_background.get_height()
    bg_width = int(original_background.get_width() * scale)
    bg_height = int(original_background.get_height() * scale)
    bg_surface = pygame.transform.scale(original_background, (bg_width, bg_height))
    return bg_surface, bg_width, bg_height


background, background_width, background_height = scale_background(HEIGHT)


# ==================================================
# CHARACTER IDLE ANIMATION
# ==================================================

idle_frames = []

for i in range(10):
    image = pygame.image.load(
        f"assets/Character/idle/{i:02d}.png"
    ).convert_alpha()
    image = pygame.transform.scale(image, (170, 170))
    idle_frames.append(image)

current_frame = 0
animation_speed = 150
last_update = pygame.time.get_ticks()

idle_intro_start = pygame.time.get_ticks()
IDLE_INTRO_TIME = 10000

idle_intro = True
idle_later = False


# ==================================================
# CHARACTER JUMP ANIMATION
# ==================================================

jump_frames = []

for i in range(8):
    image = pygame.image.load(
        f"assets/Character/jump/{i:02d}.png"
    ).convert_alpha()
    image = pygame.transform.scale(image, (170, 170))
    jump_frames.append(image)

jump_frame = 0
jump_animation_speed = 80
last_jump_update = pygame.time.get_ticks()

jumping = False


# ==================================================
# RUNNING ANIMATIONS
# ==================================================

running_left_frames = []
for i in range(8):
    image = pygame.image.load(
        f"assets/Character/running_left/{i:02d}.png"
    ).convert_alpha()
    image = pygame.transform.scale(image, (170, 170))
    running_left_frames.append(image)

running_right_frames = []
for i in range(8):
    image = pygame.image.load(
        f"assets/Character/running_right/{i:02d}.png"
    ).convert_alpha()
    image = pygame.transform.scale(image, (170, 170))
    running_right_frames.append(image)

run_frame = 0
run_animation_speed = 100
last_run_update = pygame.time.get_ticks()

running_direction = None


# ==================================================
# DODGE ANIMATIONS
# ==================================================

dodge_left_frames = []
for i in range(7):
    image = pygame.image.load(
        f"assets/Character/dodge_left/{i:02d}.png"
    ).convert_alpha()
    image = pygame.transform.scale(image, (170, 170))
    dodge_left_frames.append(image)

dodge_right_frames = []
for i in range(7):
    image = pygame.image.load(
        f"assets/Character/dodge_right/{i:02d}.png"
    ).convert_alpha()
    image = pygame.transform.scale(image, (170, 170))
    dodge_right_frames.append(image)

dodge_frame = 0
dodge_animation_speed = 50
last_dodge_update = pygame.time.get_ticks()

dodging = False
dodge_direction = None
dodge_speed = 12
dodge_distance = 0
max_dodge_distance = 120

DODGE_COOLDOWN = 700
last_dodge_time = 0


# ==================================================
# BLOCK & HIT ANIMATIONS
# ==================================================

block_left = load_character_sprite("block_left", "00.png")
block_right = load_character_sprite("block_right", "00.png")

blocking = False
block_direction = None

hit_left = load_character_sprite("hit_left", "00.png")
hit_right = load_character_sprite("hit_right", "00.png")

player_hit = False
player_hit_start = 0
PLAYER_HIT_DURATION = 250


# ==================================================
# COMBO ATTACK ANIMATIONS (PUNCH 1 -> LEG 2)
# ==================================================

punch_left_frames = []
for i in range(5):
    image = pygame.image.load(
        f"assets/Character/punch_1/Punch_left/{i:02d}.png"
    ).convert_alpha()
    image = pygame.transform.scale(image, (170, 170))
    punch_left_frames.append(image)

punch_right_frames = []
for i in range(5):
    image = pygame.image.load(
        f"assets/Character/punch_1/punch_right/{i:02d}.png"
    ).convert_alpha()
    image = pygame.transform.scale(image, (170, 170))
    punch_right_frames.append(image)

leg_left_frames = []
for i in range(4):
    image = pygame.image.load(
        f"assets/Character/punch_2/leg_left/{i:02d}.png"
    ).convert_alpha()
    image = pygame.transform.scale(image, (170, 170))
    leg_left_frames.append(image)

leg_right_frames = []
for i in range(4):
    image = pygame.image.load(
        f"assets/Character/punch_2/leg_right/{i:02d}.png"
    ).convert_alpha()
    image = pygame.transform.scale(image, (170, 170))
    leg_right_frames.append(image)

attacking = False
attack_step = 0          # 1 = punch_1, 2 = punch_2 (leg)
combo_queued = False     # True when U is pressed again during punch_1
attack_frame = 0
attack_animation_speed = 90
last_attack_update = pygame.time.get_ticks()

COMBO_GRACE_TIME = 400
punch_end_time = 0

punch_move_speed = 2     # Forward step speed during punch
leg_move_speed = 3       # Forward step speed during leg kick
player_has_dealt_damage = False


# ==================================================
# ENEMY_1 SPRITE LOADER & SETUP
# ==================================================

def find_enemy_base_dir():
    candidates = [
        os.path.join("assets", "enemy_1"),
        os.path.join("assets", "Character", "enemy_1"),
        "enemy_1",
    ]
    for path in candidates:
        if os.path.isdir(path):
            return path
    return candidates[0]


ENEMY_BASE_DIR = find_enemy_base_dir()


def normalize_name(name):
    return name.lower().replace(" ", "").replace("_", "")


def load_enemy_sequence(folder_hint, count, size=(170, 170), allow_empty=False):
    frames = []
    target_norm = normalize_name(folder_hint)
    matched_dir = None

    if os.path.isdir(ENEMY_BASE_DIR):
        for entry in os.listdir(ENEMY_BASE_DIR):
            full_entry = os.path.join(ENEMY_BASE_DIR, entry)
            if os.path.isdir(full_entry) and normalize_name(entry) == target_norm:
                matched_dir = full_entry
                break

    if matched_dir:
        # 1. Check standard 00.png .. 05.png inside matched subfolder
        for i in range(count):
            img_path = os.path.join(matched_dir, f"{i:02d}.png")
            if os.path.isfile(img_path):
                img = pygame.image.load(img_path).convert_alpha()
                frames.append(pygame.transform.scale(img, size))

        # 2. If files inside matched subfolder have prefixes (e.g. death_00.png), sort all PNGs
        if not frames:
            png_files = sorted(
                f for f in os.listdir(matched_dir) if f.lower().endswith(".png")
            )
            for fname in png_files[:count]:
                img = pygame.image.load(os.path.join(matched_dir, fname)).convert_alpha()
                frames.append(pygame.transform.scale(img, size))

    elif os.path.isdir(ENEMY_BASE_DIR):
        # 3. Check files directly inside enemy_1/ (e.g. death_00.png, death _00.png)
        matching_files = sorted(
            f
            for f in os.listdir(ENEMY_BASE_DIR)
            if f.lower().endswith(".png")
            and normalize_name(os.path.splitext(f)[0]).startswith(target_norm)
        )
        for fname in matching_files[:count]:
            img = pygame.image.load(os.path.join(ENEMY_BASE_DIR, fname)).convert_alpha()
            frames.append(pygame.transform.scale(img, size))

    if not frames:
        if allow_empty:
            return None
        contents = os.listdir(ENEMY_BASE_DIR) if os.path.isdir(ENEMY_BASE_DIR) else "Folder missing"
        print(f"Warning: Could not find sprites for enemy_1/{folder_hint}. Found: {contents}")
        transparent = pygame.Surface(size, pygame.SRCALPHA)
        frames = [transparent]

    return frames


enemy_idle_left = load_enemy_sequence("idle_left", 6)
enemy_idle_right = load_enemy_sequence("idle_right", 6)
enemy_attack_left = load_enemy_sequence("attack_left", 5)
enemy_attack_right = load_enemy_sequence("attack_right", 5)
enemy_hit_left = load_enemy_sequence("hit_left", 2)
enemy_hit_right = load_enemy_sequence("hit_right", 2)

# Support either death_left/death_right folders or a single death folder/sequence
enemy_death_left = load_enemy_sequence("death_left", 6, allow_empty=True)
enemy_death_right = load_enemy_sequence("death_right", 6, allow_empty=True)

if enemy_death_left is None or enemy_death_right is None:
    shared_death = load_enemy_sequence("death", 6)
    enemy_death_left = enemy_death_left or shared_death
    enemy_death_right = enemy_death_right or shared_death


# ==================================================
# PLAYER
# ==================================================

player = pygame.Rect(100, 0, 170, 170)
speed = 3
facing = "right"

PLAYER_MAX_HP = 100
player_hp = PLAYER_MAX_HP


# ==================================================
# ENEMY_1 STATE & AI SETTINGS
# ==================================================

enemy = pygame.Rect(650, 0, 170, 170)
enemy_facing = "left"
enemy_speed = 2

ENEMY_MAX_HP = 100
enemy_hp = ENEMY_MAX_HP
enemy_visible = True

ENEMY_VISION_RANGE = 420      # Distance at which enemy spots and chases player
ENEMY_ATTACK_RANGE = 95       # Distance at which enemy swings
ENEMY_ATTACK_COOLDOWN = 1400  # Ms between enemy attacks
ENEMY_DAMAGE = 12

ENEMY_DEATH_ANIM_SPEED = 220  # Slow, clear death animation (ms per frame)
ENEMY_DEATH_LINGER = 350      # Brief pause on final frame before disappearing

# States: "idle", "chase", "attack", "hit", "death"
enemy_state = "idle"
enemy_frame = 0
enemy_last_anim_update = pygame.time.get_ticks()
enemy_last_attack_time = 0
enemy_has_dealt_damage = False
enemy_death_finished_time = None


# ==================================================
# GRAVITY
# ==================================================

velocity_y = 0
gravity = 1
jump_strength = -18
on_ground = False


# ==================================================
# CAMERA
# ==================================================

camera_x = 0


# ==================================================
# HELPER FUNCTIONS (COMBAT & HEALTH BARS)
# ==================================================

def reset_fight():
    global player_hp, player_hit, enemy_hp, enemy_visible, enemy_state, enemy_frame
    global enemy_death_finished_time, attacking, attack_step, combo_queued
    global dodging, jumping, velocity_y

    player.x = 100
    player.y = 0
    player_hp = PLAYER_MAX_HP
    player_hit = False
    velocity_y = 0
    jumping = False
    dodging = False
    attacking = False
    attack_step = 0
    combo_queued = False

    enemy.x = 650
    enemy.y = 0
    enemy_hp = ENEMY_MAX_HP
    enemy_visible = True
    enemy_state = "idle"
    enemy_frame = 0
    enemy_death_finished_time = None


def draw_health_bars(surface, p_hp, p_max_hp, e_rect, e_hp, e_max_hp, e_vis, cam_x):
    # 1. Big Player Health Bar (Top-Left HUD: Green -> Yellow -> Red)
    bar_x = 25
    bar_y = 25
    bar_width = 260
    bar_height = 24

    hp_ratio = max(0.0, min(1.0, p_hp / p_max_hp))
    fill_width = int(bar_width * hp_ratio)

    if hp_ratio > 0.5:
        bar_color = (46, 204, 113)    # Green
    elif hp_ratio > 0.25:
        bar_color = (241, 196, 15)    # Yellow
    else:
        bar_color = (231, 76, 60)     # Red

    pygame.draw.rect(surface, (25, 25, 30), (bar_x - 3, bar_y - 3, bar_width + 6, bar_height + 6), border_radius=6)
    pygame.draw.rect(surface, (60, 60, 70), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
    if fill_width > 0:
        pygame.draw.rect(surface, bar_color, (bar_x, bar_y, fill_width, bar_height), border_radius=4)
    pygame.draw.rect(surface, (230, 230, 235), (bar_x - 3, bar_y - 3, bar_width + 6, bar_height + 6), width=2, border_radius=6)

    # 2. Mini Red Health Bar directly above the Enemy (follows constantly while alive)
    if e_vis and e_hp > 0:
        mini_w = 72
        mini_h = 8
        mini_x = (e_rect.x - cam_x) + (e_rect.width // 2) - (mini_w // 2)
        mini_y = e_rect.y - 12

        e_ratio = max(0.0, min(1.0, e_hp / e_max_hp))
        e_fill_w = int(mini_w * e_ratio)

        pygame.draw.rect(surface, (20, 20, 20), (mini_x - 2, mini_y - 2, mini_w + 4, mini_h + 4), border_radius=3)
        pygame.draw.rect(surface, (70, 25, 25), (mini_x, mini_y, mini_w, mini_h), border_radius=2)
        if e_fill_w > 0:
            pygame.draw.rect(surface, (225, 45, 45), (mini_x, mini_y, e_fill_w, mini_h), border_radius=2)


# ==================================================
# GAME LOOP
# ==================================================

running = True
clock = pygame.time.Clock()

while running:

    # ==================================================
    # EVENTS
    # ==================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            background, background_width, background_height = scale_background(
                event.h
            )

        if event.type == pygame.KEYDOWN:

            # M = MUTE / UNMUTE MUSIC
            if event.key == pygame.K_m:
                music_muted = not music_muted
                pygame.mixer.music.set_volume(0.0 if music_muted else MUSIC_VOLUME)

            # R = RESET / RESPAWN FIGHT
            if event.key == pygame.K_r:
                reset_fight()

            # SPACE = JUMP
            if event.key == pygame.K_SPACE and player_hp > 0 and not player_hit:
                keys = pygame.key.get_pressed()

                if (
                    on_ground
                    and not jumping
                    and not dodging
                    and not attacking
                    and not keys[pygame.K_s]
                ):
                    velocity_y = jump_strength
                    on_ground = False
                    jumping = True
                    jump_frame = 0
                    last_jump_update = pygame.time.get_ticks()

            # J = DODGE WITH DIRECTION
            if event.key == pygame.K_j and player_hp > 0 and not player_hit:
                keys = pygame.key.get_pressed()
                now = pygame.time.get_ticks()

                if (
                    not dodging
                    and on_ground
                    and not jumping
                    and not keys[pygame.K_s]
                    and now - last_dodge_time >= DODGE_COOLDOWN
                ):
                    if keys[pygame.K_q]:
                        dodging = True
                        dodge_direction = "left"
                        facing = "left"
                    elif keys[pygame.K_d]:
                        dodging = True
                        dodge_direction = "right"
                        facing = "right"

                    if dodging:
                        attacking = False
                        attack_step = 0
                        combo_queued = False
                        punch_end_time = 0
                        dodge_frame = 0
                        dodge_distance = 0
                        last_dodge_update = now
                        last_dodge_time = now

            # U = COMBO ATTACK (U -> PUNCH, U+U -> LEG)
            if (event.key == pygame.K_u or event.unicode.lower() == "u") and player_hp > 0 and not player_hit:
                keys = pygame.key.get_pressed()
                now = pygame.time.get_ticks()

                if (
                    on_ground
                    and not jumping
                    and not dodging
                    and not keys[pygame.K_s]
                ):
                    if keys[pygame.K_q]:
                        facing = "left"
                    elif keys[pygame.K_d]:
                        facing = "right"

                    # Trigger leg immediately if U is pressed right after punch_1
                    if not attacking and (now - punch_end_time <= COMBO_GRACE_TIME):
                        attacking = True
                        attack_step = 2
                        combo_queued = False
                        attack_frame = 0
                        player_has_dealt_damage = False
                        last_attack_update = now
                        punch_end_time = 0

                    # First U: start punch_1
                    elif not attacking:
                        attacking = True
                        attack_step = 1
                        combo_queued = False
                        attack_frame = 0
                        player_has_dealt_damage = False
                        last_attack_update = now

                    # Second U during punch_1: queue punch_2 (leg)
                    elif attack_step == 1:
                        combo_queued = True

    # ==================================================
    # WINDOW SIZE & GROUND LEVEL
    # ==================================================

    screen_width = screen.get_width()
    screen_height = screen.get_height()
    GROUND_Y = int(screen_height * 0.73)
    now = pygame.time.get_ticks()

    # ==================================================
    # UPDATE PLAYER HIT TIMER
    # ==================================================

    if player_hit and (now - player_hit_start >= PLAYER_HIT_DURATION):
        player_hit = False

    # ==================================================
    # PLAYER INPUT & MOVEMENT
    # ==================================================

    keys = pygame.key.get_pressed()
    running_direction = None
    blocking = False
    block_direction = None

    if player_hp > 0 and not player_hit:
        # BLOCK INPUT
        if (
            not dodging
            and not jumping
            and not attacking
            and on_ground
            and keys[pygame.K_s]
        ):
            blocking = True
            if keys[pygame.K_q]:
                facing = "left"
            elif keys[pygame.K_d]:
                facing = "right"
            block_direction = facing

        # DODGE MOVEMENT
        if dodging:
            if dodge_direction == "left":
                player.x -= dodge_speed
            elif dodge_direction == "right":
                player.x += dodge_speed

            dodge_distance += dodge_speed

            if dodge_distance >= max_dodge_distance:
                dodging = False
                dodge_direction = None

        # ATTACK FORWARD MOVEMENT
        elif attacking:
            step_speed = punch_move_speed if attack_step == 1 else leg_move_speed
            if facing == "left":
                player.x -= step_speed
            elif facing == "right":
                player.x += step_speed

        # NORMAL MOVEMENT
        elif not blocking:
            if keys[pygame.K_q]:
                player.x -= speed
                running_direction = "left"
                facing = "left"
            elif keys[pygame.K_d]:
                player.x += speed
                running_direction = "right"
                facing = "right"

    # ==================================================
    # PLAYER LEVEL BOUNDARIES & GRAVITY
    # ==================================================

    max_player_x = max(0, background_width - player.width)
    player.x = max(0, min(player.x, max_player_x))

    velocity_y += gravity
    player.y += velocity_y

    if player.bottom >= GROUND_Y:
        player.bottom = GROUND_Y
        velocity_y = 0
        on_ground = True
        jumping = False
    else:
        on_ground = False

    # ==================================================
    # ENEMY_1 AI, COMBAT & ANIMATION
    # ==================================================

    if enemy_visible:
        enemy.bottom = GROUND_Y

        dx = player.centerx - enemy.centerx
        distance_to_player = abs(dx)

        if enemy_state == "death":
            active_death_frames = (
                enemy_death_left if enemy_facing == "left" else enemy_death_right
            )
            if enemy_frame < len(active_death_frames) - 1:
                if now - enemy_last_anim_update >= ENEMY_DEATH_ANIM_SPEED:
                    enemy_frame += 1
                    enemy_last_anim_update = now
                    if enemy_frame == len(active_death_frames) - 1:
                        enemy_death_finished_time = now
            else:
                if enemy_death_finished_time is None:
                    enemy_death_finished_time = now
                elif now - enemy_death_finished_time >= ENEMY_DEATH_LINGER:
                    enemy_visible = False

        elif enemy_state == "hit":
            if now - enemy_last_anim_update >= 120:
                enemy_frame += 1
                enemy_last_anim_update = now
                if enemy_frame >= len(enemy_hit_right):
                    enemy_state = "idle"
                    enemy_frame = 0

        elif enemy_state == "attack":
            if now - enemy_last_anim_update >= 110:
                enemy_frame += 1
                enemy_last_anim_update = now

                # Deal damage on active strike frame (frame 2)
                if enemy_frame == 2 and not enemy_has_dealt_damage and player_hp > 0:
                    enemy_has_dealt_damage = True
                    in_front = (enemy_facing == "right" and dx >= -20) or (
                        enemy_facing == "left" and dx <= 20
                    )
                    if in_front and distance_to_player <= ENEMY_ATTACK_RANGE + 20:
                        if not dodging:
                            if blocking and facing != enemy_facing:
                                player_hp = max(0, player_hp - 2)
                            else:
                                player_hp = max(0, player_hp - ENEMY_DAMAGE)
                                player_hit = True
                                player_hit_start = now
                                attacking = False
                                attack_step = 0
                                combo_queued = False

                                if enemy_facing == "right":
                                    player.x = min(max_player_x, player.x + 15)
                                else:
                                    player.x = max(0, player.x - 15)

                if enemy_frame >= len(enemy_attack_right):
                    enemy_state = "idle"
                    enemy_frame = 0
                    enemy_last_attack_time = now

        else:
            # AI Decision: See player -> Chase or Attack
            if player_hp > 0 and distance_to_player <= ENEMY_VISION_RANGE:
                enemy_facing = "right" if dx >= 0 else "left"

                if distance_to_player <= ENEMY_ATTACK_RANGE:
                    enemy_state = "idle"
                    if now - enemy_last_attack_time >= ENEMY_ATTACK_COOLDOWN:
                        enemy_state = "attack"
                        enemy_frame = 0
                        enemy_has_dealt_damage = False
                        enemy_last_anim_update = now
                else:
                    enemy_state = "chase"
                    if enemy_facing == "right":
                        enemy.x += enemy_speed
                    else:
                        enemy.x -= enemy_speed
            else:
                enemy_state = "idle"

            anim_delay = 95 if enemy_state == "chase" else 140
            if now - enemy_last_anim_update >= anim_delay:
                enemy_frame = (enemy_frame + 1) % len(enemy_idle_right)
                enemy_last_anim_update = now

        # Clamp enemy inside level boundaries
        max_enemy_x = max(0, background_width - enemy.width)
        enemy.x = max(0, min(enemy.x, max_enemy_x))

    # ==================================================
    # PLAYER ATTACK HIT DETECTION ON ENEMY_1
    # ==================================================

    if (
        enemy_visible
        and attacking
        and attack_frame == 2
        and not player_has_dealt_damage
        and enemy_hp > 0
        and enemy_state != "death"
    ):
        attack_reach = 120 if attack_step == 1 else 140
        target_in_front = (facing == "right" and enemy.centerx >= player.centerx - 20) or (
            facing == "left" and enemy.centerx <= player.centerx + 20
        )

        if target_in_front and abs(enemy.centerx - player.centerx) <= attack_reach:
            player_has_dealt_damage = True
            damage = 15 if attack_step == 1 else 25
            enemy_hp = max(0, enemy_hp - damage)

            knockback = 12 if attack_step == 1 else 24
            max_enemy_x = max(0, background_width - enemy.width)
            if facing == "right":
                enemy.x = min(max_enemy_x, enemy.x + knockback)
            else:
                enemy.x = max(0, enemy.x - knockback)

            if enemy_hp <= 0:
                enemy_state = "death"
                enemy_frame = 0
                enemy_death_finished_time = None
                enemy_last_anim_update = now
            else:
                enemy_state = "hit"
                enemy_facing = "left" if facing == "right" else "right"
                enemy_frame = 0
                enemy_last_anim_update = now

    # ==================================================
    # CAMERA
    # ==================================================

    camera_x = player.x - 250
    camera_x = max(0, min(camera_x, max(0, background_width - screen_width)))

    # ==================================================
    # PLAYER ANIMATIONS
    # ==================================================

    # ATTACK COMBO ANIMATION
    if attacking:
        if now - last_attack_update >= attack_animation_speed:
            attack_frame += 1
            last_attack_update = now

            if attack_step == 1 and attack_frame >= len(punch_right_frames):
                if combo_queued:
                    if keys[pygame.K_q]:
                        facing = "left"
                    elif keys[pygame.K_d]:
                        facing = "right"

                    attack_step = 2
                    attack_frame = 0
                    combo_queued = False
                    player_has_dealt_damage = False
                else:
                    attacking = False
                    attack_step = 0
                    attack_frame = 0
                    punch_end_time = now

            elif attack_step == 2 and attack_frame >= len(leg_right_frames):
                attacking = False
                attack_step = 0
                attack_frame = 0
                combo_queued = False
                punch_end_time = 0

    # JUMP ANIMATION
    if jumping:
        if now - last_jump_update >= jump_animation_speed:
            jump_frame += 1
            last_jump_update = now
            if jump_frame >= len(jump_frames):
                jump_frame = len(jump_frames) - 1

    # RUNNING ANIMATION
    if (
        running_direction is not None
        and not jumping
        and not dodging
        and not blocking
        and not attacking
        and not player_hit
    ):
        if now - last_run_update >= run_animation_speed:
            run_frame = (run_frame + 1) % len(running_right_frames)
            last_run_update = now

    # DODGE ANIMATION
    if dodging:
        if now - last_dodge_update >= dodge_animation_speed:
            dodge_frame += 1
            last_dodge_update = now
            if dodge_frame >= len(dodge_right_frames):
                dodge_frame = len(dodge_right_frames) - 1

    # IDLE ANIMATION
    is_idle = (
        not jumping
        and running_direction is None
        and not dodging
        and not blocking
        and not attacking
        and not player_hit
    )

    if is_idle:
        if idle_intro:
            if now - idle_intro_start >= IDLE_INTRO_TIME:
                idle_intro = False
                idle_later = True
                current_frame = 5
                last_update = now
            elif now - last_update >= animation_speed:
                current_frame += 1
                if current_frame > 4:
                    current_frame = 0
                last_update = now
        elif idle_later:
            if now - last_update >= animation_speed:
                current_frame += 1
                if current_frame >= 10:
                    current_frame = 0
                    idle_intro = True
                    idle_later = False
                    idle_intro_start = now
                last_update = now
    else:
        idle_intro = True
        idle_later = False
        idle_intro_start = now
        current_frame = 0
        last_update = now

    # ==================================================
    # DRAW BACKGROUND
    # ==================================================

    background_y = screen_height - background_height
    screen.blit(background, (-camera_x, background_y))

    # ==================================================
    # DRAW ENEMY_1 (ONLY WHILE VISIBLE)
    # ==================================================

    if enemy_visible:
        enemy_screen_x = enemy.x - camera_x

        if enemy_state == "death":
            e_frames = enemy_death_left if enemy_facing == "left" else enemy_death_right
        elif enemy_state == "hit":
            e_frames = enemy_hit_left if enemy_facing == "left" else enemy_hit_right
        elif enemy_state == "attack":
            e_frames = enemy_attack_left if enemy_facing == "left" else enemy_attack_right
        else:
            e_frames = enemy_idle_left if enemy_facing == "left" else enemy_idle_right

        safe_e_frame = min(enemy_frame, len(e_frames) - 1)
        screen.blit(e_frames[safe_e_frame], (enemy_screen_x, enemy.y))

    # ==================================================
    # DRAW PLAYER
    # ==================================================

    player_screen_x = player.x - camera_x

    if player_hit:
        hit_sprite = hit_left if facing == "left" else hit_right
        screen.blit(hit_sprite, (player_screen_x, player.y))

    elif dodging:
        if dodge_direction == "left":
            screen.blit(dodge_left_frames[dodge_frame], (player_screen_x, player.y))
        elif dodge_direction == "right":
            screen.blit(dodge_right_frames[dodge_frame], (player_screen_x, player.y))

    elif attacking:
        if attack_step == 1:
            frames = punch_left_frames if facing == "left" else punch_right_frames
            screen.blit(frames[attack_frame], (player_screen_x, player.y))
        elif attack_step == 2:
            frames = leg_left_frames if facing == "left" else leg_right_frames
            screen.blit(frames[attack_frame], (player_screen_x, player.y))

    elif blocking:
        if block_direction == "left":
            screen.blit(block_left, (player_screen_x, player.y))
        elif block_direction == "right":
            screen.blit(block_right, (player_screen_x, player.y))

    elif jumping:
        screen.blit(jump_frames[jump_frame], (player_screen_x, player.y))

    elif running_direction == "left":
        screen.blit(running_left_frames[run_frame], (player_screen_x, player.y))

    elif running_direction == "right":
        screen.blit(running_right_frames[run_frame], (player_screen_x, player.y))

    else:
        screen.blit(idle_frames[current_frame], (player_screen_x, player.y))

    # ==================================================
    # DRAW HEALTH BARS
    # ==================================================

    draw_health_bars(
        screen,
        player_hp,
        PLAYER_MAX_HP,
        enemy,
        enemy_hp,
        ENEMY_MAX_HP,
        enemy_visible,
        camera_x,
    )

    # ==================================================
    # UPDATE SCREEN
    # ==================================================

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()