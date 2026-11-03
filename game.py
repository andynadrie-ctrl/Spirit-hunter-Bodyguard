
import pygame

pygame.init()

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


# ==================================================
# CHARACTER IDLE ANIMATION
# ==================================================

idle_frames = []

for i in range(0, 10):

    image = pygame.image.load(
        f"assets/Character/idle/{i:02d}.png"
    ).convert_alpha()

    image = pygame.transform.scale(image, (170, 170))

    idle_frames.append(image)


current_frame = 0
animation_speed = 150
last_update = pygame.time.get_ticks()


# ==================================================
# IDLE ANIMATION TIMING
# ==================================================

idle_intro_start = pygame.time.get_ticks()

IDLE_INTRO_TIME = 10000

idle_intro = True
idle_later = False


# ==================================================
# CHARACTER JUMP ANIMATION
# ==================================================

jump_frames = []

for i in range(0, 8):

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
# RUNNING LEFT ANIMATION
# ==================================================

running_left_frames = []

for i in range(0, 8):

    image = pygame.image.load(
        f"assets/Character/running_left/{i:02d}.png"
    ).convert_alpha()

    image = pygame.transform.scale(image, (170, 170))

    running_left_frames.append(image)


# ==================================================
# RUNNING RIGHT ANIMATION
# ==================================================

running_right_frames = []

for i in range(0, 8):

    image = pygame.image.load(
        f"assets/Character/running_right/{i:02d}.png"
    ).convert_alpha()

    image = pygame.transform.scale(image, (170, 170))

    running_right_frames.append(image)


# Running animation settings

run_frame = 0

run_animation_speed = 100

last_run_update = pygame.time.get_ticks()

running_direction = None


# ==================================================
# PLAYER
# ==================================================

player = pygame.Rect(
    100,
    0,
    170,
    170
)

speed = 3


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

while running:

    # ==================================================
    # EVENTS
    # ==================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # SPACE = JUMP

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                if on_ground and not jumping:

                    velocity_y = jump_strength

                    on_ground = False

                    jumping = True

                    jump_frame = 0

                    last_jump_update = pygame.time.get_ticks()


    # ==================================================
    # GET CURRENT WINDOW SIZE
    # ==================================================

    screen_width = screen.get_width()
    screen_height = screen.get_height()


    # ==================================================
    # SCALE BACKGROUND
    # ==================================================

    scale = (
        screen_height * ZOOM
        / original_background.get_height()
    )

    background_width = int(
        original_background.get_width() * scale
    )

    background_height = int(
        original_background.get_height() * scale
    )

    background = pygame.transform.scale(
        original_background,
        (background_width, background_height)
    )


    # ==================================================
    # PLAYER MOVEMENT
    # ==================================================

    keys = pygame.key.get_pressed()

    running_direction = None

    # Q = RUN LEFT

    if keys[pygame.K_q]:

        player.x -= speed

        running_direction = "left"

    # D = RUN RIGHT

    elif keys[pygame.K_d]:

        player.x += speed

        running_direction = "right"


    # ==================================================
    # GRAVITY
    # ==================================================

    velocity_y += gravity

    player.y += velocity_y


    # ==================================================
    # GROUND COLLISION
    # ==================================================

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

    max_camera = background_width - screen_width

    if max_camera < 0:

        max_camera = 0

    if camera_x > max_camera:

        camera_x = max_camera


    # ==================================================
    # JUMP ANIMATION
    # ==================================================

    if jumping:

        now = pygame.time.get_ticks()

        if now - last_jump_update >= jump_animation_speed:

            jump_frame += 1

            last_jump_update = now

            if jump_frame >= len(jump_frames):

                jump_frame = len(jump_frames) - 1


    # ==================================================
    # RUNNING ANIMATION
    # ==================================================

    if running_direction is not None and not jumping:

        now = pygame.time.get_ticks()

        if now - last_run_update >= run_animation_speed:

            run_frame += 1

            if run_frame >= 8:

                run_frame = 0

            last_run_update = now


    # ==================================================
    # IDLE ANIMATION
    # ==================================================

    if not jumping and running_direction is None:

        now = pygame.time.get_ticks()

        # PHASE 1: FRAMES 00-04

        if idle_intro:

            if now - idle_intro_start >= IDLE_INTRO_TIME:

                idle_intro = False

                idle_later = True

                current_frame = 5

                last_update = now

            else:

                if now - last_update >= animation_speed:

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


    # ==================================================
    # DRAW BACKGROUND
    # ==================================================

    background_y = screen_height - background_height

    screen.blit(
        background,
        (-camera_x, background_y)
    )


    # ==================================================
    # DRAW CHARACTER
    # ==================================================

    player_screen_x = player.x - camera_x

    # JUMP HAS HIGHEST PRIORITY

    if jumping:

        screen.blit(
            jump_frames[jump_frame],
            (player_screen_x, player.y)
        )


    # RUN LEFT

    elif running_direction == "left":

        screen.blit(
            running_left_frames[run_frame],
            (player_screen_x, player.y)
        )


    # RUN RIGHT

    elif running_direction == "right":

        screen.blit(
            running_right_frames[run_frame],
            (player_screen_x, player.y)
        )


    # IDLE

    else:

        screen.blit(
            idle_frames[current_frame],
            (player_screen_x, player.y)
        )


    # ==================================================
    # UPDATE SCREEN
    # ==================================================

    pygame.display.flip()


pygame.quit()
