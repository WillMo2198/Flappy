from random import randint
import pygame
from bird import Bird
from pipe import Pipe

pygame.init()

clock = pygame.time.Clock()

window_height = 750
window_width = 500
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Flappy')

bottom = pygame.image.load('assets/surfaces/bottom.png').convert()
background = pygame.image.load('assets/surfaces/background.jpg').convert()

pipes = [Pipe(window_width, randint(200, 450))]
bird = Bird(5, window_height/2 - 140)


def text_objects(text, font):
    text_surface = font.render(text, True, (255, 255, 255))
    return text_surface


def score_display(x_pos, y_pos, score):
    large_text = pygame.font.Font('assets/fonts/8bit.TTF', 50)
    text = text_objects(str(score), large_text)
    screen.blit(text, (x_pos, y_pos))


def restart():
    bird.velocity = 1
    bird.x = 5
    bird.y = window_height/2 - 140
    bird.angle = 0
    global pipes
    pipes = [Pipe(window_width, randint(200, 450))]
    pipes[0].x_pos = window_width - 20
    pipes[0].y_pos = randint(200, 450)
    main()


def play(sound):
    effect = pygame.mixer.Sound('assets/sounds/{0}.wav'.format(sound))
    pygame.mixer.Sound.play(effect)
    pygame.mixer.music.stop()


def main():
    score = 0
    while True:
        screen.blit(background, (0, 0))
        bird.drop()
        bird.rect()
        for p in pipes:
            p.render()
            p.rect()
            p.move()
        bird.render()
        if bird.y >= window_height - 140 or bird.y <= 0:
            play('thud')
            score = 0
            restart()
        elif bird.check_collision(pipes[0].rect1) or bird.check_collision(pipes[0].rect2):
            play('slap')
            score = 0
            restart()
        if pipes[0].x_pos <= -26:
            play('score')
            pipes[0].x_pos = window_width
            pipes[0].y_pos = randint(200, 450)
            pipes.pop(0)
            score += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                play('whoosh')
                bird.jump()
        if pipes[-1].x_pos == window_width/2:
            pipes.append(Pipe(window_width, randint(200, 450)))
        screen.blit(bottom, (0, window_height-109))
        score_display(window_width / 2, 0, score)
        clock.tick(60)
        pygame.display.flip()


main()
