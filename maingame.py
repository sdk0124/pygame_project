import os
import pygame

# 캐릭터 클래스
class Character(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.position = position

    # 화면에 캐릭터를 그리는 함수
    def draw(self, screen):
        screen.blit(self.image, self.position)

# 플레이어 클래스
class Player(Character):
    def __init__(self, image, position, images):
        super().__init__(image, position)
        self.health = 10
        self.attack_stat = 2
        self.speed = 3
        self.images = images

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
        print(f"x : {self.rect.centerx}, y : {self.rect.centery}")

    def update_direction(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery

        if abs(dx) > abs(dy):
            if dx > 0:
                self.image = self.images["east"]
            else:
                self.image = pygame.transform.flip(self.images["east"], True, False)
        else:
            if dy > 0:
                self.image = self.images["south"]
            else:
                self.image = self.images["north"]

    def attack(self):
        pass

# 적 클래스
class Enemy(Character):
    def __init__(self, image, position):
        super().__init__(image, position)
        self.health = 6
        self.attack = 1
        self.speed = 1

class Shot(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.position = position

    def draw(self, screen):
        screen.blit(self.image, self.position)
    
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

# 플레이어 캐릭터 이미지 불러오기
player_images = {
    "south" : pygame.image.load(os.path.join(current_path, "images/player_south.png")).convert_alpha(),
    "north" : pygame.image.load(os.path.join(current_path, "images/player_north.png")).convert_alpha(),
    "east" : pygame.image.load(os.path.join(current_path, "images/player_east.png")).convert_alpha()
}

# 플레이어 캐릭터 불러오기
player = Player(player_images["south"], (screen_width / 2, screen_height / 2), player_images)

# 적 캐릭터 불러오기
enemy_image = pygame.image.load(os.path.join(current_path, "images/enemy.png")).convert_alpha() # 적 캐릭터 이미지 불러오기
enemy = Enemy(enemy_image, (100, 100))

# (임시) 공격 모션 불러오기
shot_image = pygame.image.load(os.path.join(current_path, "images/attack.png")).convert_alpha() # 공격 모션 이미지 불러오기
shot = Shot(shot_image, (200, 200))

# 플레이어 이동 방향
dx = 0
dy = 0
mouse_pos = (0, 0)

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

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
    
    player.move(dx, dy, screen_width, screen_height) # 플레이어 이동
    player.update_direction(mouse_pos) # 플레이어가 바라보는 방향

    screen.blit(background, (0, 0)) # 배경화면
    player.draw(screen) # 플레이어 그리기
    enemy.draw(screen) # 적 그리기
    shot.draw(screen) # 공격 그리기
    pygame.display.update() # 게임화면 다시 그리기

# pygame 종료
pygame.quit()