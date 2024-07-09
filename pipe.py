import pygame

pygame.init()

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image1 = pygame.image.load('assets/surfaces/pipe_top.png').convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, (28 * 2, 600 * 2))
        self.image2 = pygame.image.load('assets/surfaces/pipe_bottom.png').convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, (28 * 2, 600 * 2))
        self.rect1 = self.image1.get_rect()
        self.rect2 = self.image2.get_rect()

    def render(self):
        from main import screen
        screen.blit(self.image1, (self.x_pos, self.y_pos - (600 * 2 + 150)))
        screen.blit(self.image2, (self.x_pos, self.y_pos))

    def rect(self):
        self.rect1 = self.image1.get_rect(x=self.x_pos, y=self.y_pos - 150 - 600, width=(26 * 2) + 6, height=600)
        self.rect2 = self.image2.get_rect(x=self.x_pos, y=self.y_pos, width=(26 * 2) + 7, height=600)

    def move(self):
        self.x_pos -= 5