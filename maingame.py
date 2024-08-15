import os, time, math, random
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
        self.health = 10 # 체력
        self.attack_stat = 2 # 공격력
        self.attack_speed = 2 # 공격속도 (기본 : 초당 2번 공격)
        self.speed = 3
        self.images = images
        self.direction = "south" # 플레이어가 바라보는 방향 (이 방향으로 공격이 나갈 것임)
        self.shots = pygame.sprite.Group() # 플레이어가 공격한 공격 클래스들의 그룹
        self.invincible = False # 무적 상태 여부
        self.invincible_start_time = 0 # 무적 상태 시작 시각
        self.invincible_duration = 2 # 무적 상태 지속 시간 (2초)
        self.blink_interval = 0.1 # 깜박임 간격 (0.1초)
        self.last_attack_time = 0 # 마지막 공격 시각 기록

        self.key_count = 0 # 열쇠 개수
        self.coin_count = 0 # 동전 개수
        self.bomb_count = 0 # 폭탄 개수

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

    def update_direction(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery

        if abs(dx) > abs(dy):
            if dx > 0:
                self.image = self.images["east"]
                self.direction = "east"
            else:
                self.image = pygame.transform.flip(self.images["east"], True, False)
                self.direction = "west"
        else:
            if dy > 0:
                self.image = self.images["south"]
                self.direction = "south"
            else:
                self.image = self.images["north"]
                self.direction = "north"

    def draw(self, screen):
        if not self.invincible: # 무적 상태가 아닐 경우
            super().draw(screen) # 그냥 플레이어를 그린다.
        else: # 무적 상태일 경우 
            current_time = time.time()
            elapsed_time = current_time - self.invincible_start_time
            if int(elapsed_time / self.blink_interval) % 2 == 0: # 이 조건에 만족할 때만 그린다. (깜박임 효과)
                super().draw(screen)

    def check_can_attack(self): # 공격 가능 확인 함수
        current_time = time.time()
        if (current_time - self.last_attack_time) >= (1 / self.attack_speed):
            self.last_attack_time = current_time
            return True
        return False

    def attack(self):
        if self.check_can_attack():
            shot = Shot(shot_image, self.rect.center, self.direction)
            self.shots.add(shot)

    def shot_move(self):
        self.shots.update()

    def shot_draw(self, screen):
        self.shots.draw(screen)

    def take_damaged(self, damage):
        if not self.invincible: # 무적 상태가 아니면 공격을 받는다.
            self.health -= damage
            print(f"{damage}만큼의 공격을 입음. 현재체력 : {self.health}")
            self.invincible = True # 무적 상태로 전환
            self.invincible_start_time = time.time()

    def check_isvincible(self, duration_time):
        if self.invincible:
            current_time = time.time()
            if current_time - self.invincible_start_time > duration_time:
                self.invincible = False

# 적 클래스
class Enemy(Character):
    def __init__(self, image, position, drop_things):
        super().__init__(image, position)
        self.health = None # (임시)
        self.attack_stat = None # (임시)
        self.speed = None # (임시)
        self.drop_things = drop_things

    def move(self): # 적의 움직임 (적 타입에 따라 달라짐)
        pass

    def take_damaged(self, damage): # 적이 데미지를 입음
        self.health -= damage
        if self.health <= 0:
            self.select_drop_things()
            self.kill()

    def select_drop_things(self): # 적이 죽을 시 드롭템을 결정
        drop_chance = random.random()

        print(drop_chance)

        if drop_chance <= 0.4:
            return
        elif 0.4 < drop_chance <= 0.6:
            drop_things_type = "key"
        elif 0.6 < drop_chance <= 0.8:
            drop_things_type = "bomb"
        elif 0.8 < drop_chance <= 1:
            drop_things_type = "coin"

        drop_things_image = self.drop_things[drop_things_type]
        dropthing = DropThing(drop_things_image, self.rect.center, drop_things_type)
        dropthings.add(dropthing)

# 적 - 근접 미니언
class WarriorMinion(Enemy):
    def __init__(self, image, position, drop_things):
        super().__init__(image, position, drop_things)
        self.health = 6
        self.attack_stat = 1
        self.speed = 1

# 적 - 원거리 미니언
class MagicianMinion(Enemy):
    def __init__(self, image, position, drop_things):
        super().__init__(image, position, drop_things)
        self.health = 4
        self.attack_stat = 1
        self.speed = 2

# 공격 클래스
class Shot(pygame.sprite.Sprite):
    def __init__(self, image, position, direction):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.position = position
        self.speed = 5
        self.direction = direction # 이동 방향 (플레이어가 바라보는 방향에 따라 결정된다.)

    def update(self):
        # 이동
        if self.direction == "north":
            self.rect.y -= self.speed
        elif self.direction == "south":
            self.rect.y += self.speed
        elif self.direction == "east":
            self.rect.x += self.speed
        elif self.direction == "west":
            self.rect.x -= self.speed

        # 화면 밖을 벗어나면 제거
        if (self.rect.right < 0 or self.rect.left > screen_width or
            self.rect.bottom < 0 or self.rect.top > screen_height):
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# 아이템 클래스
class Item(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.original_position  = pygame.Vector2(position) # 원래 위치
        self.position = pygame.Vector2(position) # 현재 위치

        self.move_amplitude = 10 # 움직임의 크기
        self.move_speed = 0.3 # 속도
        self.move_start_time = pygame.time.get_ticks()

    def update(self):
        # 위 아래로 천천히 움직이게 만드는 로직 
        elapsed_time = (pygame.time.get_ticks() - self.move_start_time)
        elapsed_time = elapsed_time * 0.01 # 시간의 흐름을 느리게 해서 천천히 움직이도록 한다.
        offset = self.move_amplitude * math.sin(self.move_speed * elapsed_time)
        self.position.y = self.original_position.y + offset
        self.rect.center = self.position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 드롭 아이템 클래스
class DropThing(pygame.sprite.Sprite):
    def __init__(self, image, position, type):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.type = type
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

def check_collision(player, enemies, dropthings):
    # 적들과 충돌한 shot 확인
    for shot in player.shots:
        # 충돌한 적은 확인
        collided_enemies = pygame.sprite.spritecollide(shot, enemies, False)
        if collided_enemies:
            shot.kill() # 충돌한 shot도 제거
            for enemy in collided_enemies: 
                enemy.take_damaged(player.attack_stat) # shot과 충돌한 적이 데미지를 입음

    # 플레이어와 적과의 충돌 확인
    collided_enemy = pygame.sprite.spritecollideany(player, enemies)
    if collided_enemy:
        player.take_damaged(collided_enemy.attack_stat) # 플레이어가 데미지를 입음

    # 플레이어가 드롭템을 먹는 로직
    collided_dropthings = pygame.sprite.spritecollide(player, dropthings, True)
    if collided_dropthings:
        for dropthing in collided_dropthings:
            if dropthing.type == "key":
                player.key_count += 1
            if dropthing.type == "bomb":
                player.bomb_count += 1
            if dropthing.type == "coin":
                player.coin_count += 1

        # print(f"동전 개수 : {player.coin_count}")
        # print(f"열쇠 개수 : {player.key_count}")
        # print(f"폭탄 개수 : {player.bomb_count}")

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

# 드롭템 불러오기
dropthings_images = {
    "key" : pygame.image.load(os.path.join(current_path, "images/key.png")).convert_alpha(), # 열쇠 이미지
    "bomb" : pygame.image.load(os.path.join(current_path, "images/bomb.png")).convert_alpha(), # 폭탄 이미지
    "coin" : pygame.image.load(os.path.join(current_path, "images/coin.png")).convert_alpha(), # 동전 이미지
}

# (임시) 드롭템 객체 생성
key = DropThing(dropthings_images["key"], (900, 100), "key")
bomb = DropThing(dropthings_images["bomb"], (900, 150), "bomb")
coin = DropThing(dropthings_images["coin"], (900, 200), "coin")

# (임시) 드롭템 그룹 생성
dropthings = pygame.sprite.Group()
dropthings.add(key, bomb, coin)

# 플레이어 캐릭터 이미지 불러오기
player_images = {
    "south" : pygame.image.load(os.path.join(current_path, "images/player_south.png")).convert_alpha(),
    "north" : pygame.image.load(os.path.join(current_path, "images/player_north.png")).convert_alpha(),
    "east" : pygame.image.load(os.path.join(current_path, "images/player_east.png")).convert_alpha()
}

# 플레이어 캐릭터 불러오기
player = Player(player_images["south"], (screen_width / 2, screen_height / 2), player_images)

# 적 캐릭터 이미지 불러오기
enemy_images = {
    "minion_warrior" : pygame.image.load(os.path.join(current_path, "images/enemy_warrior.png")).convert_alpha(),
    "minion_magician" : pygame.image.load(os.path.join(current_path, "images/enemy_magician.png")).convert_alpha(),
}
enemy_warrior1 = WarriorMinion(enemy_images["minion_warrior"], (150, 150), dropthings_images)
enemy_warrior2 = WarriorMinion(enemy_images["minion_warrior"], (150, 200), dropthings_images)
enemy_magician1 = MagicianMinion(enemy_images["minion_magician"], (300, 150), dropthings_images)
enemy_magician2 = MagicianMinion(enemy_images["minion_magician"], (300, 200), dropthings_images)

# (임시) 적 캐릭터 그룹 생성
enemies = pygame.sprite.Group()
enemies.add(enemy_warrior1, enemy_warrior2, enemy_magician1, enemy_magician2)

# (임시) 아이템 불러오기
item_images = {
    "sword" : pygame.image.load(os.path.join(current_path, "images/item_bfsword.png")).convert_alpha(),
    "bow" : pygame.image.load(os.path.join(current_path, "images/item_bow.png")).convert_alpha(),
    "belt" : pygame.image.load(os.path.join(current_path, "images/item_belt.png")).convert_alpha()
}
item_sword = Item(item_images["sword"], (300, 450))
item_belt = Item(item_images["belt"], (300, 500))
item_bow = Item(item_images["bow"], (300, 550))

# (임시) 아이템 그룹 생성
items = pygame.sprite.Group()
items.add(item_sword, item_belt, item_bow)

# 공격 이미지 불러오기
shot_image = pygame.image.load(os.path.join(current_path, "images/attack.png")).convert_alpha() # 공격 모션 이미지 불러오기

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

        if event.type == pygame.MOUSEBUTTONDOWN:
            player.attack() # 플레이어 공격
    
    player.move(dx, dy, screen_width, screen_height) # 플레이어 이동
    player.update_direction(mouse_pos) # 플레이어가 바라보는 방향 업데이트
    player.shot_move() # 플레이어 공격 이동
    check_collision(player, enemies, dropthings) # 충돌 체크
    player.check_isvincible(player.invincible_duration) # 무적 상태 체크

    items.update() # 아이템 움직임 업데이트

    screen.blit(background, (0, 0)) # 배경화면
    player.shot_draw(screen) # 플레이어 공격 그리기
    player.draw(screen) # 플레이어 그리기
    enemies.draw(screen) # 적 그리기
    items.draw(screen) # 아이템 그리기
    dropthings.draw(screen) # 드롭템 그리기

    pygame.display.update() # 게임화면 다시 그리기

# pygame 종료
pygame.quit()