import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Bros.")

# Constants
GRAVITY = 0.8

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        # For now, we'll use the whole spritesheet. We can crop it later.
        # Let's take a small part of the spritesheet for the player
        self.image = self.image.subsurface(pygame.Rect(0, 0, 32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.vx = 0
        self.vy = 0
        self.on_ground = False

    def update(self):
        # Apply gravity
        self.vy += GRAVITY
        # Limit fall speed
        if self.vy > 15:
            self.vy = 15

        self.rect.x += self.vx
        self.rect.y += self.vy

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 255, 0)) # Green
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0)) # Red
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 2
        self.vy = 0

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

# Level map
level = [
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "P                                      P",
    "P                                      P",
    "P                                      P",
    "P          PPPPPPP                     P",
    "P                                      P",
    "P                                      P",
    "P    PPPP                              P",
    "P          E                           P",
    "P         PPPPPP                       P",
    "P                                      P",
    "P         PPPP                         P",
    "P                                      P",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
]

# Create sprite groups
player = Player()
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Parse the level map
for i, row in enumerate(level):
    for j, col in enumerate(row):
        if col == "P":
            platform = Platform(j * 32, i * 32, 32, 32)
            platforms.add(platform)
            all_sprites.add(platform)
        elif col == "E":
            enemy = Enemy(j * 32, i * 32)
            enemies.add(enemy)
            all_sprites.add(enemy)

all_sprites.add(player)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.vx = -5
            if event.key == pygame.K_RIGHT:
                player.vx = 5
            if event.key == pygame.K_SPACE and player.on_ground:
                player.vy = -15
                player.on_ground = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.vx < 0:
                player.vx = 0
            if event.key == pygame.K_RIGHT and player.vx > 0:
                player.vx = 0

    # Update
    all_sprites.update()

    # Enemy-platform collision
    for enemy in enemies:
        enemy.vy += GRAVITY
        enemy_hits = pygame.sprite.spritecollide(enemy, platforms, False)
        if enemy_hits:
            enemy.rect.bottom = enemy_hits[0].rect.top
            enemy.vy = 0

            # Check if enemy is at the edge of a platform
            # To do this, we check for a platform just in front of the enemy
            probe_x = enemy.rect.x + enemy.vx * 32
            probe_y = enemy.rect.y + 32

            platform_ahead = False
            for p in platforms:
                if p.rect.collidepoint(probe_x, probe_y):
                    platform_ahead = True
                    break

            if not platform_ahead:
                enemy.vx *= -1


    # Player-enemy collision
    enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
    if enemy_hits:
        # Check if player is on top of the enemy
        if player.vy > 0 and player.rect.bottom < enemy_hits[0].rect.centery:
            enemy_hits[0].kill()
        else:
            print("Game Over")
            running = False

    # Check for collisions between player and platforms
    hits = pygame.sprite.spritecollide(player, platforms, False)
    if player.vy > 0 and hits:
        # Find the highest platform the player is colliding with
        highest_platform = min(hits, key=lambda p: p.rect.top)
        player.rect.bottom = highest_platform.rect.top
        player.vy = 0
        player.on_ground = True

    # Camera
    camera_x = player.rect.x - SCREEN_WIDTH / 2
    camera_y = player.rect.y - SCREEN_HEIGHT / 2

    # Draw
    screen.fill((147, 217, 255)) # Light blue background
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)


# Quit Pygame
pygame.quit()
