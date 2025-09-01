import pygame
import sys
import os
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
STAR_COUNT = 200

# Asset paths
ASSETS_DIR = "Assets"

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load assets
def load_assets():
    assets = {}
    asset_files = {
        "player": "player.png",
        "alien_red": "red.png",
        "alien_green": "green.png",
        "alien_yellow": "yellow.png",
        "mystery_ship": "extra.png",
    }
    for key, filename in asset_files.items():
        try:
            path = os.path.join(ASSETS_DIR, filename)
            assets[key] = pygame.image.load(path).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load asset: {filename}")
            raise SystemExit(e)
    return assets

assets = load_assets()

# Stars
stars = []
for _ in range(STAR_COUNT):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    size = random.randint(1, 2)
    stars.append({'x': x, 'y': y, 'size': size, 'brightness': random.randint(50, 200)})

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = assets['player']
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        # Only shoot if there are no lasers on screen
        if not lasers:
            laser = Laser(self.rect.centerx, self.rect.top)
            all_sprites.add(laser)
            lasers.add(laser)

# Laser class
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill((255, 255, 0)) # Yellow
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y, points):
        super().__init__()
        self.image = assets[f'alien_{color}']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.points = points

class AlienBomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill((255, 0, 0)) # Red
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Bunker(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        bunker_width = 72
        bunker_height = 54
        self.image = pygame.Surface((bunker_width, bunker_height))
        self.image.set_colorkey((0,0,0))

        block_size = 6
        for row in range(bunker_height // block_size):
            for col in range(bunker_width // block_size):
                rect = pygame.Rect(col * block_size, row * block_size, block_size, block_size)
                pygame.draw.rect(self.image, (0, 255, 0), rect)

        pygame.draw.rect(self.image, (0,0,0), (bunker_width/2 - 18, 30, 36, 24))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def damage(self, point):
        radius = 10
        pygame.draw.circle(self.image, (0,0,0), point, radius)
        self.mask = pygame.mask.from_surface(self.image)

class MysteryShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = assets['mystery_ship']
        self.rect = self.image.get_rect()
        self.rect.y = 20

        if random.choice([True, False]):
            self.rect.x = -self.rect.width
            self.speedx = 3
        else:
            self.rect.x = SCREEN_WIDTH
            self.speedx = -3

        self.points = random.randint(50, 300)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.kill()

# Main game loop
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def create_armada():
    alien_rows = [
        {'color': 'red', 'points': 30},
        {'color': 'yellow', 'points': 20},
        {'color': 'yellow', 'points': 20},
        {'color': 'green', 'points': 10},
        {'color': 'green', 'points': 10}
    ]
    for row_index, row_data in enumerate(alien_rows):
        for col_index in range(11):
            x = 60 + col_index * 60
            y = 50 + row_index * 40
            alien = Alien(row_data['color'], x, y, row_data['points'])
            aliens.add(alien)
            all_sprites.add(alien)

def handle_events(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_SPACE:
                player.shoot()
    return True

def check_collisions(game_state, player):
    # Laser-alien collisions
    hits = pygame.sprite.groupcollide(lasers, aliens, True, True)
    for alien_list in hits.values():
        for alien in alien_list:
            game_state['score'] += alien.points
            game_state['alien_move_interval'] *= 0.98
            if game_state['alien_move_interval'] < 100:
                game_state['alien_move_interval'] = 100

    # Laser-bunker collisions
    for laser in lasers:
        hits = pygame.sprite.spritecollide(laser, bunkers, False, pygame.sprite.collide_mask)
        if hits:
            laser.kill()
            for bunker in hits:
                rel_x = laser.rect.centerx - bunker.rect.x
                rel_y = laser.rect.centery - bunker.rect.y
                bunker.damage((rel_x, rel_y))

    # Laser-mystery ship collisions
    hits = pygame.sprite.groupcollide(lasers, mystery_ship, True, True)
    for ship_list in hits.values():
        for ship in ship_list:
            game_state['score'] += ship.points

    # Bomb-player collisions
    if pygame.sprite.spritecollide(player, bombs, True, pygame.sprite.collide_mask):
        game_state['lives'] -= 1
        if game_state['lives'] <= 0:
            return False

    # Bomb-bunker collisions
    for bomb in bombs:
        hits = pygame.sprite.spritecollide(bomb, bunkers, False, pygame.sprite.collide_mask)
        if hits:
            bomb.kill()
            for bunker in hits:
                rel_x = bomb.rect.centerx - bunker.rect.x
                rel_y = bomb.rect.centery - bunker.rect.y
                bunker.damage((rel_x, rel_y))

    # Alien-player collision
    if pygame.sprite.spritecollide(player, aliens, False, pygame.sprite.collide_mask):
        return False

    # Alien-bunker collision
    for alien in aliens:
        collided_bunkers = pygame.sprite.spritecollide(alien, bunkers, False, pygame.sprite.collide_mask)
        for bunker in collided_bunkers:
            bunker.damage((alien.rect.centerx - bunker.rect.x, alien.rect.centery - bunker.rect.y))

    return True

def update_game_state(game_state):
    all_sprites.update()

    # Alien movement
    now = pygame.time.get_ticks()
    if now - game_state['alien_move_timer'] > game_state['alien_move_interval']:
        game_state['alien_move_timer'] = now
        change_direction = False
        for alien in aliens:
            alien.rect.x += 10 * game_state['alien_move_direction']
            if alien.rect.right > SCREEN_WIDTH or alien.rect.left < 0:
                change_direction = True
        if change_direction:
            game_state['alien_move_direction'] *= -1
            for alien in aliens:
                alien.rect.y += 20

    # Alien shooting
    if now - game_state['alien_shoot_timer'] > game_state['alien_shoot_interval']:
        game_state['alien_shoot_timer'] = now
        if aliens:
            random_alien = random.choice(aliens.sprites())
            bomb = AlienBomb(random_alien.rect.centerx, random_alien.rect.bottom)
            all_sprites.add(bomb)
            bombs.add(bomb)

    # Mystery ship spawning
    if not mystery_ship and now - game_state['mystery_ship_spawn_timer'] > game_state['mystery_ship_spawn_interval']:
        game_state['mystery_ship_spawn_timer'] = now
        new_ship = MysteryShip()
        mystery_ship.add(new_ship)
        all_sprites.add(new_ship)

    # Level complete
    if not aliens:
        draw_text(screen, "Level Complete!", 50, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)
        pygame.display.flip()
        pygame.time.wait(2000)
        create_armada()
        game_state['alien_move_interval'] *= 0.95 # Make the new wave faster

    # Aliens reach bottom
    for alien in aliens:
        if alien.rect.bottom >= SCREEN_HEIGHT:
            return False

    return True

def draw_screen(game_state):
    screen.fill(BLACK)
    for star in stars:
        star['brightness'] += random.randint(-10, 10)
        if star['brightness'] < 50: star['brightness'] = 50
        if star['brightness'] > 200: star['brightness'] = 200
        color = (star['brightness'], star['brightness'], star['brightness'])
        pygame.draw.circle(screen, color, (star['x'], star['y']), star['size'])
    all_sprites.draw(screen)
    draw_text(screen, f"Score: {game_state['score']}", 24, SCREEN_WIDTH / 2, 10)
    draw_text(screen, f"Lives: {game_state['lives']}", 24, 60, 10)
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()

    global all_sprites, lasers, aliens, bombs, bunkers, mystery_ship
    all_sprites = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    bunkers = pygame.sprite.Group()
    mystery_ship = pygame.sprite.GroupSingle()
    player = Player()
    all_sprites.add(player)

    create_armada()

    bunker_width = 72
    for i in range(4):
        bunker_x = (SCREEN_WIDTH / 5) * (i + 1) - (bunker_width / 2)
        bunker_y = SCREEN_HEIGHT - 150
        bunker = Bunker(bunker_x, bunker_y)
        bunkers.add(bunker)
        all_sprites.add(bunker)

    game_state = {
        'score': 0,
        'lives': 100,
        'alien_move_direction': 1,
        'alien_move_timer': 0,
        'alien_move_interval': 1000,
        'alien_shoot_timer': 0,
        'alien_shoot_interval': 2000,
        'mystery_ship_spawn_timer': 0,
        'mystery_ship_spawn_interval': 15000,
    }

    running = True
    while running:
        running = handle_events(player)
        if not running: break

        running = update_game_state(game_state)
        if not running: break

        running = check_collisions(game_state, player)
        if not running: break

        draw_screen(game_state)

        clock.tick(60)

    screen.fill(BLACK)
    draw_text(screen, "Game Over", 74, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)
    pygame.display.flip()
    pygame.time.wait(3000)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
