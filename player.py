import pygame, os
from setting import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, enemies_group):
        super().__init__()
        base_path = os.path.dirname(__file__)

        self.position = position
        self.images = {
            "south" : pygame.image.load(os.path.join(base_path, "images/player_south.png")).convert_alpha(),
            "north" : pygame.image.load(os.path.join(base_path, "images/player_north.png")).convert_alpha(),
            "east" : pygame.image.load(os.path.join(base_path, "images/player_east.png")).convert_alpha()
        } # 동서남북 바라보는 이미지
        self.image = self.images["south"]
        self.rect = self.image.get_rect(center=position)

        self.health = 10 # 체력
        self.attack_stat = 2 # 공격력
        self.attack_speed = 2 # 공격속도 (기본 : 초당 2번 공격)
        self.speed = 3 # 이동속도
        self.move_direction = pygame.math.Vector2() # 플레이어 이동 방향
        self.watch_direction = "south" # 플레이어가 바라보는 방향 (기본값 : 남쪽)
        self.shots = pygame.sprite.Group() # 플레이어가 공격한 공격 클래스들의 그룹
        self.invincible = False # 무적 상태 여부
        self.invincible_start_time = 0 # 무적 상태 시작 시각
        self.invincible_duration = 2 # 무적 상태 지속 시간 (2초)
        self.blink_interval = 0.1 # 깜박임 간격 (0.1초)
        self.last_attack_time = 0 # 마지막 공격 시각 기록
        self.enemies_group = enemies_group # 적 스프라이트들의 집합

        self.key_count = 0 # 열쇠 개수
        self.coin_count = 0 # 동전 개수
        self.bomb_count = 0 # 폭탄 개수

    def update_move_direction(self): # 플레이어 이동 방향 업데이트
        keys = pygame.key.get_pressed() # 키보드 입력 받기

        # 수평 방향
        if keys[pygame.K_LEFT]:
            self.move_direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.move_direction.x = 1
        else:
            self.move_direction.x = 0

        # 수직 방향
        if keys[pygame.K_UP]:
            self.move_direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.move_direction.y = 1
        else:
            self.move_direction.y = 0

    def update_watch_direction(self): # 플레이어가 바라보는 방향 업데이트 (이미지도 바뀐다.)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery

        if abs(dx) > abs(dy):
            if dx > 0:
                self.image = self.images["east"]
                self.watch_direction = "east"
            else:
                self.image = pygame.transform.flip(self.images["east"], True, False)
                self.watch_direction = "west"
        else:
            if dy > 0:
                self.image = self.images["south"]
                self.watch_direction = "south"
            else:
                self.image = self.images["north"]
                self.watch_direction = "north"

    def move(self, speed): # 플레이어 이동
        if self.move_direction.magnitude() != 0: # 방향 벡터 단위화
            self.move_direction = self.move_direction.normalize()

        self.rect.x += self.move_direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.move_direction.y * speed
        self.collision('vertical')
    
        # 플레이어 이동 제한
        if self.rect.left < MINIMUM_MOVEMENT_X:
            self.rect.left = MINIMUM_MOVEMENT_X
        elif self.rect.right > MAXIMUM_MOVEMENT_X:
            self.rect.right = MAXIMUM_MOVEMENT_X

        if self.rect.top < MINIMUM_MOVEMENT_Y:
            self.rect.top = MINIMUM_MOVEMENT_Y
        elif self.rect.bottom > MAXIMUM_MOVEMENT_Y:
            self.rect.bottom = MAXIMUM_MOVEMENT_Y

    def collision(self, direction): # 플레이어 충돌 로직
        # 적들과 충돌 했을 때의 로직

        if direction == 'horizontal':
            for enemy in self.enemies_group: 
                if enemy.rect.colliderect(self.rect):
                    # 오른쪽으로 이동 중 충돌 : 적의 왼쪽 부분에 충돌했음
                    if self.move_direction.x > 0: # moving right
                        self.rect.right = enemy.rect.left

                    # 왼쪽으로 이동 중 충돌 : 적의 오른쪽 부분에 충돌했음
                    if self.move_direction.x < 0: # moving left
                        self.rect.left = enemy.rect.right

                    self.take_damaged(enemy.attack_stat)

        if direction == 'vertical':
            for enemy in self.enemies_group:
                if enemy.rect.colliderect(self.rect):
                    # 아랫쪽으로 이동 중 충돌 : 적의 위쪽 부분에 충돌했음
                    if self.move_direction.y > 0: # moving down
                        self.rect.bottom = enemy.rect.top

                    # 위쪽으로 이동 중 충돌 : 적의 아랫쪽 부분에 충돌했음
                    if self.move_direction.y < 0: # moving left
                        self.rect.top = enemy.rect.bottom

                    self.take_damaged(enemy.attack_stat)    

    def update(self):
        self.update_move_direction()
        self.update_watch_direction()
        self.move(self.speed)
        self.check_isvincible(self.invincible_duration)

    def draw(self, screen):
        if not self.invincible: # 무적 상태가 아닐 경우
            screen.blit(self.image, self.rect)
        else: # 무적 상태일 경우 
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.invincible_start_time
            if int(elapsed_time / (self.blink_interval * 1000)) % 2 == 0: # 이 조건에 만족할 때만 그린다. (깜박임 효과)
                screen.blit(self.image, self.rect)

    def take_damaged(self, damage): # 플레이어가 적과 충돌 시 데미지를 입음.
        if not self.invincible: # 무적 상태가 아니면 공격을 받는다.
            self.health -= damage
            print(f"{damage}만큼의 공격을 입음. 현재체력 : {self.health}, 무적 상태 시작")
            self.invincible = True # 무적 상태로 전환
            self.invincible_start_time = pygame.time.get_ticks()

    def check_isvincible(self, duration_time): # 무적 상태 체크
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if (current_time - self.invincible_start_time) >= (duration_time * 1000):
                self.invincible = False
                print("무적 상태 끝")