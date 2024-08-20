import pygame, os
pygame.init()

current_path = os.path.dirname(__file__)

# 배경화면 이미지
background_image = pygame.image.load(os.path.join(current_path, "images/background.png")).convert_alpha()
