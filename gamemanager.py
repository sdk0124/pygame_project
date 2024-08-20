import pygame, os
from setting import *
from player import Player
from enemy import *

class GameManager():
    def __init__(self):
        self.surface = pygame.display.get_surface()
        base_path = os.path.dirname(__file__)
        self.background_image_path = os.path.join(base_path, "images/background.png")
        
        self.visible_sprites = pygame.sprite.Group() # 화면에 그려지는 모든 스프라이트들의 집합 (플레이어는 제외)
        self.enemy_sprites = pygame.sprite.Group() # 적 스프라이트들의 집합 (플레이어 충돌 로직에 사용)

        self.create_map()

    def create_map(self):
        # image, sprite setup
        self.background = pygame.image.load(self.background_image_path).convert_alpha()
        self.player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), self.enemy_sprites) # 플레이어는 화면 가운데에서 시작
        
        # 임시로 적들 추가
        WarriorMinion((150, 150), [self.visible_sprites, self.enemy_sprites])
        WarriorMinion((150, 200), [self.visible_sprites, self.enemy_sprites])
        MagicianMinion((300, 150), [self.visible_sprites, self.enemy_sprites])
        MagicianMinion((300, 200), [self.visible_sprites, self.enemy_sprites])
        
    def run(self):
        self.surface.blit(self.background, (0, 0))
        self.visible_sprites.draw(self.surface)
        self.player.update()
        self.player.draw(self.surface)
        self.visible_sprites.update()