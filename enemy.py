import pygame, os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)
        self.position = position
        # self.health = None # (임시)
        # self.attack_stat = None # (임시)
        # self.speed = None # (임시)
        #self.drop_things = drop_things

    # def move(self): # 적의 움직임 (적 타입에 따라 달라짐)
    #     pass

    # def take_damaged(self, damage): # 적이 데미지를 입음
    #     self.health -= damage
    #     if self.health <= 0:
    #         self.select_drop_things()
    #         self.kill()

    # def select_drop_things(self): # 적이 죽을 시 드롭템을 결정
    #     drop_chance = random.random()

    #     print(drop_chance)

    #     if drop_chance <= 0.4:
    #         return
    #     elif 0.4 < drop_chance <= 0.6:
    #         drop_things_type = "key"
    #     elif 0.6 < drop_chance <= 0.8:
    #         drop_things_type = "bomb"
    #     elif 0.8 < drop_chance <= 1:
    #         drop_things_type = "coin"

    #     drop_things_image = self.drop_things[drop_things_type]
    #     dropthing = DropThing(drop_things_image, self.rect.center, drop_things_type)
    #     dropthings.add(dropthing)

    def draw(self, screen, image, rect):
        screen.blit(image, rect)

# 적 - 근접 미니언
class WarriorMinion(Enemy):
    def __init__(self, position, group):
        super().__init__(position, group)
        base_path = os.path.dirname(__file__)
        image_path = os.path.join(base_path, "images/enemy_warrior.png")

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.health = 6
        self.attack_stat = 1
        self.speed = 1

    def update(self):
        pass

# 적 - 원거리 미니언
class MagicianMinion(Enemy):
    def __init__(self, position, group):
        super().__init__(position, group)
        base_path = os.path.dirname(__file__)
        image_path = os.path.join(base_path, "images/enemy_magician.png")
        
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        #self.original_image = image # 원래 이미지는 동쪽을 바라보고 있다.
        self.health = 4
        self.attack_stat = 1
        self.attack_speed = 0.5 # 2초당 1회 공격
        self.speed = 2
        #self.direction = "east"
        #self.dx = 1
        #self.shots = pygame.sprite.Group() # 원거리 미니언의 공격들의 그룹
        #self.last_attack_time = 0 # 마지막 공격 시각 기록

    def update(self):
        pass

    # def update(self):
    #     self.update_direction() # 이동 방향 처리
    #     self.move() # 적의 움직임 처리
    #     self.attack() # 공격 로직
    #     self.shots.update()

    # def update_direction(self):
    #     if self.direction == "east":
    #         self.image = self.original_image
    #     elif self.direction == "west":
    #         self.image = pygame.transform.flip(self.original_image, True, False)

    # def move(self): # 원거리 미니언 움직임 : 수평 이동(동, 서)
    #     if self.direction == "east":
    #         self.rect.x += self.speed * self.dx
    #     elif self.direction == "west":
    #         self.rect.x -= self.speed * self.dx

    #     if self.rect.left < 0:
    #         self.direction = "east"
    #     if self.rect.right > screen_width:
    #         self.direction = "west"

    #     self.position = (self.rect.x, self.rect.y)

    # def check_can_attack(self): # 공격 가능 확인 함수
    #     current_time = pygame.time.get_ticks()
    #     if (current_time - self.last_attack_time) >= (1000 / self.attack_speed):
    #         self.last_attack_time = current_time
    #         return True
    #     return False

    # def attack(self):
    #     if self.check_can_attack():
    #         shot = MagicianMinionShot(magicminion_shot_image, self.rect.center, self.direction)
    #         self.shots.add(shot)
    #         print("공격!")

    # def draw(self, screen):
    #     screen.blit(self.image, self.rect)
    #     self.shots.draw(screen)