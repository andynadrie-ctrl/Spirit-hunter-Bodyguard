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


# How zoomed the world should be
ZOOM = 1.5


# ==================================================
# CHARACTER IDLE ANIMATION
# ==================================================

idle_frames = []

for i in range(0, 10):

    image = pygame.image.load(
        f"assets/Character/idle/0{i}.png"
    ).convert_alpha()

    # Bigger character
    image = pygame.transform.scale(
        image,
        (150, 150)
    )

    idle_frames.append(image)


# Current animation frame
current_frame = 0

# Animation speed
animation_speed = 150
last_update = pygame.time.get_ticks()


# ==================================================
# PLAYER
# ==================================================

player = pygame.Rect(
    100,
    0,
    150,
    150
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


    # ==================================================
    # GET CURRENT WINDOW SIZE
    # ==================================================

    screen_width = screen.get_width()
    screen_height = screen.get_height()


    # ==================================================
    # SCALE BACKGROUND
    # ==================================================

    # Make the background tall enough to fill
    # the current window.

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
        (
            background_width,
            background_height
        )
    )


    # ==================================================
    # PLAYER MOVEMENT
    # ==================================================

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:

        player.x += speed

    if keys[pygame.K_LEFT]:

        player.x -= speed


    # ==================================================
    # JUMP
    # ==================================================

    if keys[pygame.K_SPACE] and on_ground:

        velocity_y = jump_strength

        on_ground = False


    # ==================================================
    # GRAVITY
    # ==================================================

    velocity_y += gravity

    player.y += velocity_y


    # ==================================================
    # GROUND COLLISION
    # ==================================================

    # The road is approximately here.
    # Adjust this number if necessary.

    GROUND_Y = int(screen_height * 0.73)

    if player.bottom >= GROUND_Y:

        player.bottom = GROUND_Y

        velocity_y = 0

        on_ground = True

    else:

        on_ground = False


    # ==================================================
    # CAMERA
    # ==================================================

    # Character stays around this position
    # while the world moves.

    camera_x = player.x - 250


    if camera_x < 0:

        camera_x = 0


    # Don't scroll beyond the background

    max_camera = background_width - screen_width

    if max_camera < 0:

        max_camera = 0

    if camera_x > max_camera:

        camera_x = max_camera


    # ==================================================
    # IDLE ANIMATION
    # ==================================================

    now = pygame.time.get_ticks()

    if now - last_update > animation_speed:

        current_frame += 1

        if current_frame >= len(idle_frames):

            current_frame = 0

        last_update = now


    # ==================================================
    # DRAW BACKGROUND
    # ==================================================

    # Align the bottom of the background with
    # the bottom of the window.
    #
    # This prevents the black bar.

    background_y = screen_height - background_height

    screen.blit(
        background,
        (-camera_x, background_y)
    )


    # ==================================================
    # DRAW CHARACTER
    # ==================================================

    player_screen_x = player.x - camera_x

    screen.blit(
        idle_frames[current_frame],
        (
            player_screen_x,
            player.y
        )
    )


    # ==================================================
    # UPDATE SCREEN
    # ==================================================

    pygame.display.flip()


pygame.quit()