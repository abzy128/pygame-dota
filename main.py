# pylint: skip-file
import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Abzy's techies demolitionist game")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 74)
score = 0
speed = 60

GAME_OVER_EVENT = pygame.USEREVENT + 1
game_over = False
game_over_fx_played = False

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/spirit_breaker.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH // 2, HEIGHT)
        # Add smooth movement variables
        self.target_x = self.rect.x
        self.target_y = self.rect.y
        self.vel_x = 0
        self.vel_y = 0
        self.acceleration = 0.3
        self.friction = 0.8
                                        
    def update(self):
        # Mouse movement with inertia
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.target_x = mouse_x - self.rect.width // 2
        self.target_y = mouse_y - self.rect.height // 2

        # Calculate velocity with acceleration towards target
        self.vel_x += (self.target_x - self.rect.x) * self.acceleration
        self.vel_y += (self.target_y - self.rect.y) * self.acceleration
        
        # Apply friction
        self.vel_x *= self.friction
        self.vel_y *= self.friction

        # Update position
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Boundary checks
        if self.rect.x <= 0:
            self.rect.x = 0
            self.vel_x = 0
        if self.rect.x >= WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
            self.vel_x = 0
        if self.rect.y >= HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
            self.vel_y = 0
        if self.rect.y <= HEIGHT // 6 * 5:
            self.rect.y = HEIGHT // 6 * 5
            self.vel_y = 0

class Player2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/primal_beast.png')
        self.image = pygame.transform.scale(self.image, (75 * 1.5, 75))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH // 4, HEIGHT)
    
    def update(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_s]:
            self.rect.y += 5
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5

        # Boundary checks
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x >= WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.y >= HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
        if self.rect.y <= HEIGHT // 6 * 5:
            self.rect.y = HEIGHT // 6 * 5

class Enemy(pygame.sprite.Sprite):
    speed_modifier = 1
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/techies_mine.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed_modifier = random.randint(80, 120) / 100

    def update(self):
        global score
        global speed
        self.rect.y += (speed // 10) * self.speed_modifier

class Line(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.image = pygame.Surface((WIDTH, 2))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.y = y

def reset_game():
    global score, speed, game_over, game_over_fx_played
    score = 0
    speed = 60
    game_over = False
    game_over_fx_played = False
    player.rect.midbottom = (WIDTH // 2, HEIGHT)
    player2.rect.midbottom = (WIDTH // 4, HEIGHT)
    
    for enemy in enemies:
        enemy.rect.y = random.randint(-200, -40)
        enemy.rect.x = random.randint(0, WIDTH - enemy.rect.width)

# Initialize both players
player = Player(WIDTH // 2, HEIGHT - 100)
player2 = Player2(WIDTH // 4, HEIGHT - 100)
player_sprites = pygame.sprite.Group()
player_sprites.add(player)
player_sprites.add(player2)

enemies = pygame.sprite.Group()
for _ in range(10):
    enemy = Enemy(random.randint(0, WIDTH - 40), random.randint(-100, -40))
    enemies.add(enemy)

running = True
lines = pygame.sprite.Group()
lines.add(Line(HEIGHT / 6 * 1))
lines.add(Line(HEIGHT / 6 * 2))
lines.add(Line(HEIGHT / 6 * 3))
lines.add(Line(HEIGHT / 6 * 4))
lines.add(Line(HEIGHT / 6 * 5))

def all_enemies_out_of_screen(enemies):
    for enemy in enemies:
        if enemy.rect.y <= HEIGHT:
            return False
    return True

def line_out_of_screen(line):
    return line.rect.y > HEIGHT

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == GAME_OVER_EVENT:
            game_over = True
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()
    if not game_over:
        player.update()  # Mouse-controlled player
        player2.update(keys)  # Keyboard-controlled player
        enemies.update()
        lines.update()

    screen.fill((255, 255, 255))

    if pygame.sprite.spritecollideany(player, enemies) or pygame.sprite.spritecollideany(player2, enemies):
        pygame.event.post(pygame.event.Event(GAME_OVER_EVENT))
        score_text = font.render(f"Game Over! Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (WIDTH // 2 - 200, HEIGHT // 2))
        pygame.display.flip()
        if not game_over_fx_played:
            explosion_frames = [pygame.image.load(f'assets/fx/explosion/explosion-{i}.png') for i in range(0, 25)]
            explosion_sound = pygame.mixer.Sound('assets/sfx/Land_Mines_explosion.mp3')
            explosion_sound.play()
            for frame in explosion_frames:
                screen.blit(frame, (player.rect.x, player.rect.y))
                pygame.display.flip()
                pygame.time.delay(100)
            game_over_fx_played = True

    if not game_over:
        if all_enemies_out_of_screen(enemies):
            for enemy in enemies:
                enemy.rect.y = random.randint(-200, -40)
                enemy.rect.x = random.randint(0, WIDTH - enemy.rect.width)
            score += 1
            if score % 10 == 0:
                speed += 10
                new_enemy = Enemy(random.randint(0, WIDTH - 40), random.randint(-100, -40))
                enemies.add(new_enemy)
                print("Enemy count: ", len(enemies))

        player_sprites.draw(screen)
        enemies.draw(screen)
        lines.draw(screen)

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
