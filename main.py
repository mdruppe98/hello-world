import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Window Title
pygame.display.set_caption("Space Invaders")

def draw_text(surf, text, size, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 25])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        # Fire a bullet only if there isn't one already on the screen
        if not bullets:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([5, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([5, 10])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Invader(pygame.sprite.Sprite):
    speed = 2

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([40, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += Invader.speed

class Blocker(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class MysteryShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([45, 20])
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect.width
        self.rect.y = 40
        self.speedx = 3

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

def create_new_wave(level):
    # Set initial speed for the new wave
    Invader.speed = 1.5 + (level * 0.5)
    # Create new invaders
    for row in range(5):
        for col in range(10):
            invader = Invader(50 + col * 50, 50 + row * 30)
            all_sprites.add(invader)
            invaders.add(invader)

# Create sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bombs = pygame.sprite.Group()
invaders = pygame.sprite.Group()
bunkers = pygame.sprite.Group()
mystery_ship_group = pygame.sprite.GroupSingle()
player = Player()
all_sprites.add(player)

# Create Bunkers
bunker_y = 480
block_size = 10
for i in range(4):
    bunker_x = (SCREEN_WIDTH / 4 * i) + 75
    for row in range(4):
        for col in range(6):
            blocker = Blocker(bunker_x + col * block_size, bunker_y + row * block_size, block_size)
            bunkers.add(blocker)
            all_sprites.add(blocker)

# Create stars
stars = []
for _ in range(100):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    stars.append((x, y))

# Game state
game_over = False
player_lives = 3
level = 1
mystery_ship_spawn_time = pygame.time.get_ticks() + random.randint(10000, 20000)

# Create initial wave
create_new_wave(level)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # keep loop running at the right speed
    clock.tick(60)

    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over and event.key == pygame.K_SPACE:
                player.shoot()

    if not game_over:
        # Spawn Mystery Ship
        now = pygame.time.get_ticks()
        if not mystery_ship_group and now > mystery_ship_spawn_time:
            mystery_ship = MysteryShip()
            all_sprites.add(mystery_ship)
            mystery_ship_group.add(mystery_ship)
            mystery_ship_spawn_time = now + random.randint(10000, 20000)

        # Game logic
        # Check if any invader is about to hit the side
        change_direction = False
        for invader in invaders:
            if (invader.rect.right + Invader.speed > SCREEN_WIDTH and Invader.speed > 0) or \
               (invader.rect.left + Invader.speed < 0 and Invader.speed < 0):
                change_direction = True
                break

        if change_direction:
            Invader.speed *= -1
            for invader in invaders:
                invader.rect.y += 10

        # Invaders shoot
        for invader in invaders:
            if random.random() < 0.001:
                bomb = Bomb(invader.rect.centerx, invader.rect.bottom)
                all_sprites.add(bomb)
                bombs.add(bomb)

        # Update
        all_sprites.update()

        # Check for collisions
        hits = pygame.sprite.groupcollide(invaders, bullets, True, True)
        if hits:
            # Increase speed for each invader hit
            for _ in hits:
                if Invader.speed > 0:
                    Invader.speed += 0.05
                else:
                    Invader.speed -= 0.05

        if pygame.sprite.groupcollide(bullets, mystery_ship_group, True, True):
            print("Mystery Ship destroyed! +100 points")

        pygame.sprite.groupcollide(bullets, bunkers, True, True)
        pygame.sprite.groupcollide(bombs, bunkers, True, True)

        # Check for player collision (with invaders or bombs)
        invader_hit_list = pygame.sprite.spritecollide(player, invaders, True)
        bomb_hit_list = pygame.sprite.spritecollide(player, bombs, True)
        if invader_hit_list or bomb_hit_list:
            player_lives -= 1
            if player_lives <= 0:
                game_over = True
            else:
                player.rect.centerx = SCREEN_WIDTH // 2
                player.rect.bottom = SCREEN_HEIGHT - 10
                pygame.time.wait(1000) # Brief pause on death

        # Check for invaders reaching the bottom
        for invader in invaders:
            if invader.rect.bottom >= SCREEN_HEIGHT:
                game_over = True
                break

        # Check for level clear
        if not invaders:
            level += 1
            draw_text(screen, f"Level {level}", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
            pygame.display.flip()
            pygame.time.wait(2000)
            create_new_wave(level)

        # Draw / render
        screen.fill(BLACK)
        # Draw stars
        for star in stars:
            pygame.draw.circle(screen, WHITE, star, 1)
        all_sprites.draw(screen)
        draw_text(screen, f"Lives: {player_lives}", 22, 60, 10)
        draw_text(screen, f"Level: {level}", 22, SCREEN_WIDTH - 60, 10)

    else: # Game is over
        screen.fill(BLACK) # Clear screen
        # Draw stars
        for star in stars:
            pygame.draw.circle(screen, WHITE, star, 1)

        draw_text(screen, "Game Over", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)

    # *after* drawing everything, flip the display
    pygame.display.flip()

    if game_over:
        pygame.time.wait(3000)
        running = False


pygame.quit()
sys.exit()
