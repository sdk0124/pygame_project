import pygame

# 초기화
pygame.init()

# 화면 크기 설정
screen_width = 960
screen_height = 640
screen_size = (screen_width, screen_height)
screen = pygame.display.set_mode(screen_size)

# 화면 타이틀 설정
pygame.display.set_caption("Pygame")

# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 창을 닫으면 게임 종료
            running = False

# pygame 종료
pygame.quit()