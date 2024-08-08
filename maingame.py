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

# 플레이어 캐릭터 불러오기
player = pygame.image.load("images/player.png").convert_alpha() # 플레이어 캐릭터 이미지 불러오기
player_size = player.get_rect().size # 이미지 크기 구하기
player_width = player_size[0] # 플레이어 가로 크기
player_height = player_size[1] # 플레이어 세로 크기
# 화면 중앙에 플레이어 위치
player_x_pos = (screen_width / 2) - (player_width / 2)
player_y_pos = (screen_height / 2) - (player_height / 2)

# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 창을 닫으면 게임 종료
            running = False

    screen.blit(player, (player_x_pos, player_y_pos))
    pygame.display.update() # 게임화면 다시 그리기

# pygame 종료
pygame.quit()