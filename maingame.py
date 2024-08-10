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

# FPS
clock = pygame.time.Clock()

# 배경화면 설정
background = pygame.image.load("images/background.png").convert_alpha()

# 플레이어 캐릭터 불러오기
player = pygame.image.load("images/player.png").convert_alpha() # 플레이어 캐릭터 이미지 불러오기
player_size = player.get_rect().size # 이미지 크기 구하기
player_width = player_size[0] # 플레이어 가로 크기
player_height = player_size[1] # 플레이어 세로 크기

# 화면 중앙에 플레이어 위치
player_x_pos = (screen_width / 2) - (player_width / 2)
player_y_pos = (screen_height / 2) - (player_height / 2)

# 적 캐릭터 불러오기
enemy = pygame.image.load("images/enemy.png").convert_alpha() # 적 캐릭터 이미지 불러오기
enemy_size = enemy.get_rect().size # 이미지 크기 구하기
enemy_width = enemy_size[0] # 적 가로 크기
enemy_height = enemy_size[1] # 적 세로 크기

# 임의의 위치에 적 위치
enemy_x_pos = (screen_width / 2) - (enemy_width / 2)
enemy_y_pos = screen_height - enemy_height

# 플레이어가 이동할 좌표
to_x = 0
to_y = 0

# 플레이어 이동 속도
player_speed = 0.2

# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(60) # FPS 설정 (1초당 60번 동작)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 창을 닫으면 게임 종료
            running = False

        if event.type == pygame.KEYDOWN: # 방향키를 눌렀을 시
            if event.key == pygame.K_LEFT: 
                to_x -= player_speed
            if event.key == pygame.K_RIGHT:
                to_x += player_speed
            if event.key == pygame.K_UP:
                to_y -= player_speed
            if event.key == pygame.K_DOWN:
                to_y += player_speed

        if event.type == pygame.KEYUP: # 방향키에서 뗐을 시
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
            
    # 플레이어 좌표 계산
    player_x_pos += to_x * dt
    player_y_pos += to_y * dt

    # 가로 좌표 경계 계산
    if player_x_pos < 0:
        player_x_pos = 0
    elif player_x_pos > screen_width - player_width:
        player_x_pos = screen_width - player_width
    
    # 세로 좌표 경계 계산
    if player_y_pos < 0:
        player_y_pos = 0
    elif player_y_pos > screen_height - player_height:
        player_y_pos = screen_height - player_height
    
    screen.blit(background, (0, 0)) # 배경화면
    screen.blit(player, (player_x_pos, player_y_pos)) # 플레이어 그리기
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos)) # 적 그리기
    pygame.display.update() # 게임화면 다시 그리기

# pygame 종료
pygame.quit()