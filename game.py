import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Spirit Hunter")

# Background
background = pygame.image.load("assets/backgrounds/back2 town.png").convert()

#scaling background
background_height= screen.get_height()

scale= HEIGHT/background.get_height()

new_width= int(background.get_width()*scale)

background=pygame.transform.scale(background,(new_width,HEIGHT))
# -------------------------
# CHARACTER IDLE ANIMATION
# -------------------------
idle_frames = []

for i in range(0, 10):
    image = pygame.image.load(
        f"assets/Character/idle/0{i}.png"
    ).convert_alpha()

    # Resize character
    image = pygame.transform.scale(image, (100, 100))

    idle_frames.append(image)

#current animation frame
current_frame= 0

#animation speed
animation_speed= 150 #miliseconds
last_update = pygame.time.get_ticks()

# -------------------------
# PLAYER
# -------------------------
player = pygame.Rect(100, 400, 100, 100)

speed = 3



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
    # IDLE ANIMATION
    # -------------------------
    now = pygame.time.get_ticks()

    if now - last_update > animation_speed:

        current_frame += 1

        if current_frame >= len(idle_frames):
            current_frame = 0

        last_update = now

    # -------------------------
    # DRAW BACKGROUND
    # -------------------------
    screen.blit(background, (-camera_x, 0))

    
     # -------------------------
    # DRAW CHARACTER
    # -------------------------
    player_screen_x = player.x - camera_x

    screen.blit(
        idle_frames[current_frame],
        (player_screen_x, player.y)
    )

    pygame.display.flip()

pygame.quit()
