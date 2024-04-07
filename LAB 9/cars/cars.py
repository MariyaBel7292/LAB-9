import random
import time
import pygame

clock = pygame.time.Clock()
fps = 60  

RED = (255, 0, 0) 
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
SPEED = 6  
SCORE = 0  
coins_collected = 0  # Counter of collected coins
N = 5  # Number of coins to increase enemy speed

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 393, 600  
pygame.init() 
screen = pygame.display.set_mode(WINDOW_SIZE)

font = pygame.font.SysFont('Verdana', 63)  
font_small = pygame.font.SysFont('Verdana', 18) 
game_over_text_label = font.render('Game over!', True, WHITE)  
background = pygame.image.load('street.png')  
pygame.mixer.init()  
pygame.mixer.music.set_volume(0.45)  
pygame.mixer.music.load('Lab8_racer_background.wav')  
pygame.mixer.music.play(loops=10 ** 9)  

pygame.display.set_caption('CARs')  

game_over = False

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('coin.png')
        self.rect = self.image.get_rect()
        self.set_random_position()
        self.weight = random.randint(1, 5) # Generate random weight for a coin

    def move(self):
        self.rect.move_ip(0, 3)
        if self.rect.top > WINDOW_HEIGHT:
            self.set_random_position()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def set_random_position(self):
        self.rect.center = (random.randint(65, WINDOW_WIDTH - 65), 0)
        self.rect.bottom = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('red cat.png')
        self.rect = self.image.get_rect()
        self.set_random_position()

    def move(self):
        global SPEED, SCORE
        self.rect.move_ip(0, SPEED)

        if self.rect.top > WINDOW_HEIGHT:
            SCORE += 1
            self.set_random_position()

    def set_random_position(self):
        self.rect.center = (random.randint(64, WINDOW_WIDTH - 64), 0)
        self.rect.bottom = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('blue.png')
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 43:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < WINDOW_WIDTH - 43:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(coin)

enemies = pygame.sprite.Group()
enemies.add(enemy)

coins = pygame.sprite.Group()
coins.add(coin)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 4000)

def generate_new_coin():
    global coin
    coin = Coin()
    coins.add(coin)
    all_sprites.add(coin)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == INC_SPEED:
            SPEED += 0.5

    screen.blit(background, (0, 0))

    screen.blit(
        font_small.render(f'Score: {SCORE}', True, BLUE), (293, 10)
    )

    screen.blit(
        font_small.render(f'Coins: {coins_collected}', True, BLUE), (293, 30)
    )

    for sprite in all_sprites:
        sprite.move()
        sprite.draw(screen)

    if pygame.sprite.spritecollideany(player, coins):
        coin.kill()
        coins_collected += 1
        SCORE += 1
        generate_new_coin()

        # Check if the player has reached the required number of coins to increase the enemy's speed
        if coins_collected >= N:
            SPEED += 1  # Increase the speed of the enemy

    if pygame.sprite.spritecollideany(player, enemies):
        pygame.mixer.music.stop()
        pygame.mixer.Sound('Lab8_racer_crash.wav').play()
        time.sleep(1)

        screen.fill((69, 172, 116))
        screen.blit(game_over_text_label, (12, 190))
        screen.blit(font_small.render(f'Your score: {SCORE}', True, WHITE), (15, 270))
        screen.blit(font_small.render(f'Captured coins: {coins_collected}', True, WHITE),
                    (15, 290))

        pygame.display.update()

        for sprite in all_sprites:
            sprite.kill()

        time.sleep(7)

        game_over = True

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
