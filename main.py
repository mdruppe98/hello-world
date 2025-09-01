import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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

# Create sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
invaders = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for row in range(5):
    for col in range(10):
        invader = Invader(50 + col * 50, 50 + row * 30)
        all_sprites.add(invader)
        invaders.add(invader)

# Game state
game_over = False
win = False

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

        # Update
        all_sprites.update()

        # Check for bullet-invader collisions
        pygame.sprite.groupcollide(invaders, bullets, True, True)

        # Check for win condition
        if not invaders:
            win = True
            game_over = True

        # Check for loss condition
        if pygame.sprite.spritecollide(player, invaders, False):
            game_over = True

        for invader in invaders:
            if invader.rect.bottom >= player.rect.top:
                game_over = True
                break

        # Draw / render
        screen.fill(BLACK)
        all_sprites.draw(screen)

    else: # Game is over
        screen.fill(BLACK) # Clear screen
        if win:
            draw_text(screen, "You Win!", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        else:
            draw_text(screen, "Game Over", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)

    # *after* drawing everything, flip the display
    pygame.display.flip()

    if game_over:
        pygame.time.wait(3000)
        running = False


pygame.quit()
sys.exit()
