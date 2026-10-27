import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Spirit Hunter")

# Background
background = pygame.image.load("assets/backgrounds/back2 town.png").convert()

# Player
player = pygame.Rect(100, 510, 50, 50)
speed = 2

# Camera
camera_x = 0

running = True

while running:

    # -------------------------
    # EVENTS
    # -------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -------------------------
    # PLAYER MOVEMENT
    # -------------------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        player.x += speed

    if keys[pygame.K_LEFT]:
        player.x -= speed

    # -------------------------
    # CAMERA
    # -------------------------
    camera_x = player.x - 200

    if camera_x < 0:
        camera_x = 0

    if camera_x > background.get_width() - WIDTH:
        camera_x = background.get_width() - WIDTH

    # -------------------------
    # DRAW BACKGROUND
    # -------------------------
    screen.blit(background, (-camera_x, 0))

    # -------------------------
    # DRAW PLAYER
    # -------------------------
    player_screen_x = player.x - camera_x

    pygame.draw.rect(
        screen,
        (255, 0, 0),
        (player_screen_x, player.y, player.width, player.height)
    )

    pygame.display.flip()

pygame.quit()