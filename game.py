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

    # Prioritize .ogg and .wav first, then .mp3
    candidates = []
    for ext in supported_formats:
        for file in os.listdir(audio_folder):
            lower = file.lower()
            if lower.startswith("spirit_fight") and lower.endswith(ext):
                candidates.append(os.path.join(audio_folder, file))

    if not candidates:
        print(
            "Audio file not found in assets/audio/. "
            "Convert spirit_fight to .ogg, .wav, or .mp3 and place it there."
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
            print(
                f"Could not decode '{music_path}': {e}\n"
                "Convert the audio properly to .ogg or .mp3 (renaming alone will not work)."
            )


init_music()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.RESIZABLE
)

pygame.display.set_caption("Spirit Hunter")


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
# BLOCK ANIMATIONS
# ==================================================

block_left = pygame.image.load(
    "assets/Character/block_left/00.png"
).convert_alpha()
block_left = pygame.transform.scale(block_left, (170, 170))

block_right = pygame.image.load(
    "assets/Character/block_right/00.png"
).convert_alpha()
block_right = pygame.transform.scale(block_right, (170, 170))

blocking = False
block_direction = None


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


# ==================================================
# PLAYER
# ==================================================

player = pygame.Rect(100, 0, 170, 170)
speed = 3
facing = "right"


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

            # SPACE = JUMP
            if event.key == pygame.K_SPACE:
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

            # J = DODGE WITH DIRECTION (can cancel an attack)
            if event.key == pygame.K_j:
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
            if event.key == pygame.K_u or event.unicode.lower() == "u":
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
                        last_attack_update = now
                        punch_end_time = 0

                    # First U: start punch_1
                    elif not attacking:
                        attacking = True
                        attack_step = 1
                        combo_queued = False
                        attack_frame = 0
                        last_attack_update = now

                    # Second U during punch_1: queue punch_2 (leg)
                    elif attack_step == 1:
                        combo_queued = True

    # ==================================================
    # WINDOW SIZE
    # ==================================================

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # ==================================================
    # PLAYER INPUT
    # ==================================================

    keys = pygame.key.get_pressed()
    running_direction = None
    blocking = False
    block_direction = None

    # ==================================================
    # BLOCK INPUT
    # ==================================================

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

    # ==================================================
    # DODGE MOVEMENT
    # ==================================================

    if dodging:
        if dodge_direction == "left":
            player.x -= dodge_speed
        elif dodge_direction == "right":
            player.x += dodge_speed

        dodge_distance += dodge_speed

        if dodge_distance >= max_dodge_distance:
            dodging = False
            dodge_direction = None

    # ==================================================
    # ATTACK FORWARD MOVEMENT
    # ==================================================

    elif attacking:
        step_speed = punch_move_speed if attack_step == 1 else leg_move_speed
        if facing == "left":
            player.x -= step_speed
        elif facing == "right":
            player.x += step_speed

    # ==================================================
    # NORMAL MOVEMENT
    # ==================================================

    elif not blocking:
        # Q = RUN LEFT
        if keys[pygame.K_q]:
            player.x -= speed
            running_direction = "left"
            facing = "left"

        # D = RUN RIGHT
        elif keys[pygame.K_d]:
            player.x += speed
            running_direction = "right"
            facing = "right"

    # ==================================================
    # LEVEL BOUNDARIES
    # ==================================================

    max_player_x = max(0, background_width - player.width)
    if player.x < 0:
        player.x = 0
    elif player.x > max_player_x:
        player.x = max_player_x

    # ==================================================
    # GRAVITY & GROUND COLLISION
    # ==================================================

    velocity_y += gravity
    player.y += velocity_y

    GROUND_Y = int(screen_height * 0.73)

    if player.bottom >= GROUND_Y:
        player.bottom = GROUND_Y
        velocity_y = 0
        on_ground = True
        jumping = False
    else:
        on_ground = False

    # ==================================================
    # CAMERA
    # ==================================================

    camera_x = player.x - 250

    if camera_x < 0:
        camera_x = 0

    max_camera = max(0, background_width - screen_width)

    if camera_x > max_camera:
        camera_x = max_camera

    # ==================================================
    # ANIMATIONS
    # ==================================================

    now = pygame.time.get_ticks()

    # ATTACK COMBO ANIMATION
    if attacking:
        if now - last_attack_update >= attack_animation_speed:
            attack_frame += 1
            last_attack_update = now

            # Punch 1 finished -> chain into Leg 2 if U was pressed again
            if attack_step == 1 and attack_frame >= len(punch_right_frames):
                if combo_queued:
                    if keys[pygame.K_q]:
                        facing = "left"
                    elif keys[pygame.K_d]:
                        facing = "right"

                    attack_step = 2
                    attack_frame = 0
                    combo_queued = False
                else:
                    attacking = False
                    attack_step = 0
                    attack_frame = 0
                    punch_end_time = now

            # Leg 2 finished -> end combo
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
    )

    if is_idle:
        # PHASE 1: FRAMES 00-04
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

        # PHASE 2: FRAMES 05-09
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
    # DRAW CHARACTER
    # ==================================================

    player_screen_x = player.x - camera_x

    if dodging:
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
    # UPDATE SCREEN
    # ==================================================

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()