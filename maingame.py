import os
import pygame

# 캐릭터 클래스
class Character(pygame.sprite.Sprite):
    def __init__(self, image, position, name):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.name = name
        self.position = position
        self.health = 1 # 임시
        self.attack = 1 # 임시
        self.speed = 1 # 임시

    def show_spec(self): # 임시 : 스텟 정보 표시
        print(f"이름 : {self.name}")
        print(f"체력 : {self.health}")
        print(f"공격력 : {self.attack}")
        print(f"이동 속도 : {self.speed}")

    # 화면에 캐릭터를 그리는 함수
    def draw(self, screen):
        screen.blit(self.image, self.position)

# 플레이어 클래스
class Player(Character):
    def __init__(self, image, position, name):
        super().__init__(image, position, name)
        self.health = 10
        self.attack = 2
        self.speed = 5

    def move(self, dx, dy, screen_width, screen_height):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # 경계선 처리
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

        # 위치 업데이트
        self.position = (self.rect.x, self.rect.y)

    def show_position(self):
        print(self.position)

    def show_rect(self):
        print(f"x : {self.rect.x}, y : {self.rect.y}")

# 적 클래스
class Enemy(Character):
    def __init__(self, image, position, name):
        super().__init__(image, position, name)
        self.health = 6
        self.attack = 1
        self.speed = 1

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
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "images/background.png")).convert_alpha()

# 플레이어 캐릭터 불러오기
player_image = pygame.image.load(os.path.join(current_path, "images/player.png")).convert_alpha() # 플레이어 캐릭터 이미지 불러오기
player = Player(player_image, (screen_width / 2, screen_height / 2), "플레이어")

# 적 캐릭터 불러오기
enemy_image = pygame.image.load(os.path.join(current_path, "images/enemy.png")).convert_alpha() # 적 캐릭터 이미지 불러오기
enemy = Enemy(enemy_image, (100, 100), "적")

# 플레이어 이동 방향
dx = 0
dy = 0

# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(60) # FPS 설정 (1초당 60번 동작)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 창을 닫으면 게임 종료
            running = False

        if event.type == pygame.KEYDOWN: # 방향키를 눌렀을 시
            if event.key == pygame.K_LEFT: 
                dx = -1
            if event.key == pygame.K_RIGHT:
                dx = 1
            if event.key == pygame.K_UP:
                dy = -1
            if event.key == pygame.K_DOWN:
                dy = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and dx == -1: 
                dx = 0
            if event.key == pygame.K_RIGHT and dx == 1:
                dx = 0
            if event.key == pygame.K_UP and dy == -1:
                dy = 0
            if event.key == pygame.K_DOWN and dy == 1:
                dy = 0
    
    player.move(dx, dy, screen_width, screen_height)
  
    screen.blit(background, (0, 0)) # 배경화면
    player.draw(screen) # 플레이어 그리기
    enemy.draw(screen) # 적 그리기
    pygame.display.update() # 게임화면 다시 그리기

# pygame 종료
pygame.quit()