from random import randint
import pygame

pygame.init()

height = 750
width = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('FlappyAI')
bottom = pygame.image.load('background.png').convert_alpha()
background = pygame.image.load('back.jpg').convert()
background_rect = background.get_rect()
clock = pygame.time.Clock()
gravity = 0
score = 0


class Bird(pygame.sprite.Sprite):
    def __init__(self, bird_width, bird_height, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bird.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (bird_width, bird_height))
        self.bird_width = bird_width
        self.bird_height = bird_height
        self.x = x
        self.y = y
        self.terminal_velocity = 5
        self.rect1 = self.image.get_rect()
        self.center = self.rect1.center
        self.velocity = 0
        self.ang = 0
        self.dead = False

    def render(self):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, sprite):
        if self.rect1.colliderect(sprite) and not self.dead:
            self.dead = True

    def rect(self):
        self.rect1 = self.image.get_rect(x=self.x, y=self.y, width=self.bird_width, height=self.bird_height)

    def jump(self):
        global gravity
        gravity = 0
        self.velocity = -10

    def drop(self):
        self.velocity += gravity
        self.y += self.velocity
        if self.velocity > self.terminal_velocity:
            self.velocity = self.terminal_velocity


def text_objects(text, font):
    text_surface = font.render(text, True, (255, 255, 255))
    return text_surface


def score_display(x_pos, y_pos):
    large_text = pygame.font.Font('font.TTF', 50)
    text = text_objects(str(score), large_text)
    screen.blit(text, (x_pos, y_pos))


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image1 = pygame.image.load('pipe.png').convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, (28 * 2, 600 * 2))
        self.image2 = pygame.image.load('pipe1.png').convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, (28 * 2, 600 * 2))
        self.rect1 = self.image1.get_rect()
        self.rect2 = self.image2.get_rect()

    def render(self):
        screen.blit(self.image1, (self.x_pos, self.y_pos - (600 * 2 + 150)))
        screen.blit(self.image2, (self.x_pos, self.y_pos))

    def rect(self):
        self.rect1 = self.image1.get_rect(x=self.x_pos, y=self.y_pos - 150 - 600, width=(26 * 2) + 6, height=600)
        self.rect2 = self.image2.get_rect(x=self.x_pos, y=self.y_pos, width=(26 * 2) + 7, height=height)

    def move(self):
        self.x_pos -= 5


def restart():
    global gravity, score
    gravity = 0
    bird.velocity = 1
    bird.y = 0
    bird.x = 5
    bird.ang = 0
    bird.fitness_score = 0
    bird.dead = False
    pipe.x_pos = width - 20
    pipe.y_pos = randint(200, 450)
    pipe.x_change = 3
    score = 0
    global pipes
    pipes = [Pipe(width, randint(200, 450))]
    game_loop()

pipes = []
pipe = Pipe(width, randint(200, 450))
pipes.append(pipe)
bird = Bird(40, 30, 5, 0)

def game_loop():
    global score
    while True:
        global gravity
        if gravity < bird.terminal_velocity:
            gravity += 0.1
        if pipes[-1].x_pos == width/2:
            new_pipe = Pipe(width, randint(200, 450))
            pipes.append(new_pipe)
        screen.blit(background, (0, 0))
        if bird.y >= height - 115 and not bird.dead:
            bird.dead = True
        if bird.dead:
            restart()
        if not bird.dead:
            bird.render()
            bird.rect()
            bird.drop()
            for p in pipes:
                p.render()
                p.rect()
            bird.check_collision(pipes[0].rect1)
            bird.check_collision(pipes[0].rect2)
        if pipes[0].x_pos < -26:
            pipes[0].x_pos = width
            pipes[0].y_pos = randint(200, 450)
            pipes.pop(0)
            score += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()
        for p in pipes:
            p.render()
            p.rect()
            p.move()
        screen.blit(bottom, (0, height-109))
        score_display(width / 2, 0)
        clock.tick(60)
        pygame.display.flip()


game_loop()
