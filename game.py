
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
# RUNNING LEFT ANIMATION
# ==================================================

running_left_frames = []

for i in range(8):

    image = pygame.image.load(
        f"assets/Character/running_left/{i:02d}.png"
    ).convert_alpha()

    image = pygame.transform.scale(image, (170, 170))

    running_left_frames.append(image)


# ==================================================
# RUNNING RIGHT ANIMATION
# ==================================================

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
# DODGE LEFT ANIMATION
# ==================================================

dodge_left_frames = []

for i in range(7):

    image = pygame.image.load(
        f"assets/Character/dodge_left/{i:02d}.png"
    ).convert_alpha()

    image = pygame.transform.scale(image, (170, 170))

    dodge_left_frames.append(image)


# ==================================================
# DODGE RIGHT ANIMATION
# ==================================================

dodge_right_frames = []

for i in range(7):

    image = pygame.image.load(
        f"assets/Character/dodge_right/{i:02d}.png"
    ).convert_alpha()

    image = pygame.transform.scale(image, (170, 170))

    dodge_right_frames.append(image)


# Dodge settings

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

block_left = pygame.transform.scale(
    block_left, (170, 170)
)


block_right = pygame.image.load(
    "assets/Character/block_right/00.png"
).convert_alpha()

block_right = pygame.transform.scale(
    block_right, (170, 170)
)


# Block settings

blocking = False

block_direction = None


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

clock = pygame.time.Clock()

while running:

    # ==================================================
    # EVENTS
    # ==================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


        if event.type == pygame.KEYDOWN:

            # SPACE = JUMP

            if event.key == pygame.K_SPACE:

                keys = pygame.key.get_pressed()

                if (
                    on_ground
                    and not jumping
                    and not dodging
                    and not keys[pygame.K_s]
                ):

                    velocity_y = jump_strength

                    on_ground = False

                    jumping = True

                    jump_frame = 0

                    last_jump_update = pygame.time.get_ticks()


            # J = DODGE WITH DIRECTION

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


                    elif keys[pygame.K_d]:

                        dodging = True

                        dodge_direction = "right"


                    if dodging:

                        dodge_frame = 0

                        dodge_distance = 0

                        last_dodge_update = now

                        last_dodge_time = now


    # ==================================================
    # WINDOW SIZE
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
    # PLAYER INPUT
    # ==================================================

    keys = pygame.key.get_pressed()

    running_direction = None

    blocking = False

    block_direction = None


    # ==================================================
    # BLOCK INPUT
    # ==================================================

    if not dodging and not jumping and on_ground and keys[pygame.K_s]:

        if keys[pygame.K_q]:

            blocking = True

            block_direction = "left"


        elif keys[pygame.K_d]:

            blocking = True

            block_direction = "right"


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
    # NORMAL MOVEMENT
    # ==================================================

    elif not blocking:

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

    if (
        running_direction is not None
        and not jumping
        and not dodging
        and not blocking
    ):

        now = pygame.time.get_ticks()

        if now - last_run_update >= run_animation_speed:

            run_frame += 1

            if run_frame >= 8:

                run_frame = 0

            last_run_update = now


    # ==================================================
    # DODGE ANIMATION
    # ==================================================

    if dodging:

        now = pygame.time.get_ticks()

        if now - last_dodge_update >= dodge_animation_speed:

            dodge_frame += 1

            last_dodge_update = now

            if dodge_frame >= 7:

                dodge_frame = 6


    # ==================================================
    # IDLE ANIMATION
    # ==================================================

    if (
        not jumping
        and running_direction is None
        and not dodging
        and not blocking
    ):

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


    # DODGE

    if dodging:

        if dodge_direction == "left":

            screen.blit(
                dodge_left_frames[dodge_frame],
                (player_screen_x, player.y)
            )

        elif dodge_direction == "right":

            screen.blit(
                dodge_right_frames[dodge_frame],
                (player_screen_x, player.y)
            )


    # BLOCK

    elif blocking:

        if block_direction == "left":

            screen.blit(
                block_left,
                (player_screen_x, player.y)
            )

        elif block_direction == "right":

            screen.blit(
                block_right,
                (player_screen_x, player.y)
            )


    # JUMP

    elif jumping:

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

    clock.tick(60)


pygame.quit()
