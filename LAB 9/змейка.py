import pygame
import random
import time

pygame.init() 
CLOCK = pygame.time.Clock()
FPS = 8  
WINDOW_WIDTH, WINDOW_HEIGHT = 480, 440  
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT+80)) 
WHITE = (255, 255, 255)   
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

BLOCK_SIZE = 20

font = pygame.font.SysFont('Verdana', 63, bold=True)
font_small = pygame.font.SysFont('Verdana', 18) 

SCORE = 0   
LEVEL = 0   

pygame.display.set_caption('Zmeika')  

POSITIONS_OF_THE_WALL = ('top', 'left', 'bottom', 'right')  


def check_food_collision() -> bool:  
    global food, walls, snake

    for wa in walls:
        for p in wa.construction:
            if food.collide(p):
                return True

    for tail_of_snake in snake.body:
        if food.collide(tail_of_snake):
            return True

    return False


def generate_random_color() -> tuple:   
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def own_round(value, base=BLOCK_SIZE):   
    return base * round(value / BLOCK_SIZE)


def draw_grid():  
    for i in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for j in range(0, WINDOW_HEIGHT+20, BLOCK_SIZE):
            pygame.draw.rect(SCREEN, pygame.Color('grey'), (i, j, BLOCK_SIZE, BLOCK_SIZE), 1)


class Particle:  
    def __init__(self, _x=0, _y=0, color=(0, 0, 0)):
        super().__init__()
        self.x = _x
        self.y = _y
        self.image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))  
        self.image.fill(color)

    def draw(self):
        SCREEN.blit(self.image, self.get_coordinates())

    def get_coordinates(self) -> tuple: 
        return self.x, self.y


class Wall:
    def __init__(self, _position='top', _length=6, _color=(0, 0, 0)):
        self.construction = [] 
        self.position = _position  
        self.length = _length  
        self.color = _color
        self.construct() 

    def construct(self):
        if self.position == 'top' or self.position == 'bottom': 
            x = own_round(random.randint(WINDOW_WIDTH//4, 3*WINDOW_WIDTH//4))
            y = 0 if self.position == 'top' else WINDOW_HEIGHT 
            for i in range(self.length):
                self.construction.append(Particle(_x=x+i*BLOCK_SIZE, _y=y, color=self.color))
        if self.position == 'right' or self.position == 'left':  
            y = own_round(random.randint(WINDOW_HEIGHT//4, 3*WINDOW_HEIGHT//4))
            x = 0 if self.position == 'left' else WINDOW_WIDTH-BLOCK_SIZE 
            for i in range(self.length):
                self.construction.append(Particle(_x=x, _y=y+i*BLOCK_SIZE, color=self.color))

    def draw(self): 
        for particle in self.construction:
            particle.draw()


class Food:
    def __init__(self):
        self.particle = Particle(color=generate_random_color())
        self.weight = random.randint(1, 5)  # Generate random weight for food
        self.set_random_position()
        self.color = GREEN
        self.start_time = time.time()# Remember the time when food began to exist

    def set_random_position(self):  
        self.particle.x = own_round(random.randint(BLOCK_SIZE, WINDOW_WIDTH-BLOCK_SIZE))
        self.particle.y = own_round(random.randint(BLOCK_SIZE, WINDOW_HEIGHT-BLOCK_SIZE))

    def draw(self):
        self.particle.draw() 

    def collide(self, particle) -> bool:
        return self.particle.x == particle.x and self.particle.y == particle.y


class Snake:
    def __init__(self, *args, **kwargs):
        self.body = [Particle(BLOCK_SIZE, BLOCK_SIZE, generate_random_color())]
        self.tail_color = generate_random_color() 
        self.add_tail()
        self.add_tail()
        self.block = BLOCK_SIZE
        self.dx = self.block
        self.dy = 0

    def head(self): 
        return self.body[0]

    def move(self): 
        for i in range(len(self.body)-1, 0, -1):
            self.body[i].x = self.body[i-1].x 
            self.body[i].y = self.body[i-1].y

        self.head().x += self.dx  
        self.head().y += self.dy

        if self.head().x > WINDOW_WIDTH:   
            self.head().x = 0
        if self.head().x < 0:
            self.head().x = WINDOW_WIDTH
        if self.head().y > WINDOW_HEIGHT:
            self.head().y = 0
        if self.head().y < 0:
            self.head().y = WINDOW_HEIGHT

    def draw(self):
        for i, particle in enumerate(self.body):
            particle.draw()

    def add_tail(self):
        self.body.append(Particle(color=self.tail_color))

    def head_collide(self, particle) -> bool:
        return self.head().x == particle.x and self.head().y == particle.y


level_increased = False 
game_over = False
snake = Snake() 
food = Food()
walls = []
color_of_wall = generate_random_color() 


def over_the_game(): 
    global game_over
    SCREEN.fill((69, 172, 116))
    SCREEN.blit(font.render('GAME OVER', True, WHITE), (30, 170))
    SCREEN.blit(font_small.render(f'Score: {SCORE}', True, WHITE), (32, 250))
    SCREEN.blit(font_small.render(f'Level: {LEVEL}', True, WHITE), (32, 275))
    pygame.display.update()
    time.sleep(6)
    game_over = True


for pos in POSITIONS_OF_THE_WALL: 
    w = Wall(_position=pos, _length=random.randint(5, 7), _color=color_of_wall)
    w.construct()
    walls.append(w)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP] and snake.dx != 0: 
                snake.dy = -1 * snake.block
                snake.dx = 0
            if pressed[pygame.K_DOWN] and snake.dx != 0:
                snake.dy = snake.block
                snake.dx = 0
            if pressed[pygame.K_LEFT] and snake.dy != 0:
                snake.dy = 0
                snake.dx = -1 * snake.block
            if pressed[pygame.K_RIGHT] and snake.dy != 0:
                snake.dy = 0
                snake.dx = snake.block

    SCREEN.fill(WHITE)
    snake.move()
    snake.draw()
    draw_grid()
    food.draw()
    for w in walls:
        w.draw()

   # Check if food disappears after a certain time
    if time.time() - food.start_time > 5: # if more than 5 seconds have passed
        food.set_random_position()
        food.start_time = time.time()  # reset the food spawn timer

    SCREEN.blit(font_small.render(f'Score: {SCORE}', True, BLUE), (11, WINDOW_HEIGHT+30))
    SCREEN.blit(font_small.render(f'Level: {LEVEL}', True, BLUE), (11, WINDOW_HEIGHT+53))

    if snake.head_collide(food.particle):
        SCORE += food.weight  # Add points depending on the weight of the food
        snake.add_tail()
        food.set_random_position()

    if check_food_collision():
        food.set_random_position()

    for tail in snake.body[1:]:
        if snake.head_collide(tail):
            over_the_game()

    for w in walls:
        for part in w.construction:
            if snake.head_collide(part):
                over_the_game()

    if SCORE % 7 == 0 and SCORE != 0: 
        if not level_increased:
            level_increased = True
            LEVEL += 1
            FPS += 2
    elif SCORE % 7 == 1:
        level_increased = False

    pygame.display.update()
    CLOCK.tick(FPS)

pygame.quit()
