import pygame

pygame.init()


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.height = 40
        self.width = 30
        self.image = pygame.image.load('assets/surfaces/bird.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.height, self.width))
        self.rot_image = self.image
        self.x = x
        self.y = y
        self.rect1 = self.image.get_rect()
        self.center = self.rect1.center
        self.velocity = 0
        self.angle = 0
        self.terminal_velocity = 10
        self.dead = False

    def render(self):
        from main import screen
        screen.blit(self.rot_image, (self.x, self.y))

    def check_collision(self, sprite):
        if self.rect1.colliderect(sprite) and not self.dead:
            return True

    def rect(self):
        self.rect1 = self.image.get_rect(x=self.x, y=self.y, width=self.width, height=self.height)

    def rotate(self, angle):
        self.rot_image = pygame.transform.rotate(self.image, angle)
        self.rot_image.get_rect().center = self.center
        return self.rot_image

    def jump(self):
        self.velocity = - self.terminal_velocity - 5
        self.rotate(self.angle)

    def drop(self):
        self.velocity += 1
        self.y += self.velocity
        if self.velocity > self.terminal_velocity:
            self.velocity = self.terminal_velocity
        if self.velocity > 0:
            self.angle -= self.velocity
        elif self.velocity < 0:
            self.angle = 30
        if self.angle < -90:
            self.angle = -90
        self.rotate(self.angle)
