import pygame
from setting import MAXIMUM_X, MAXIMUM_Y, MINIMUM_X, MINIMUM_Y

# 공격 클래스
class Shot(pygame.sprite.Sprite):
    def __init__(self, image, position, speed ,direction):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.direction = direction
        self.speed = speed

    def move(self, direction):
        if direction == "north":
            self.rect.y -= self.speed
        elif direction == "south":
            self.rect.y += self.speed
        elif direction == "east":
            self.rect.x += self.speed
        elif direction == "west":
            self.rect.x -= self.speed

        if ((self.rect.left < MINIMUM_X) or (self.rect.right > MAXIMUM_X) or 
            (self.rect.top < MINIMUM_Y) or (self.rect.bottom > MAXIMUM_Y)):
            self.kill()

    def update(self):
        self.move(self.direction)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 플레이어 공격 클래스
class PlayerShot(Shot):
    def __init__(self, image, position, speed, direction):
        super().__init__(image, position, speed, direction)

# 원거리 미니언 공격 클래스
class MagicianMinionShot(Shot):
    def __init__(self, image, position, speed, direction):
        super().__init__(image, position, speed, direction)