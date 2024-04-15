import math

import pygame,random,time,sys
from os import path
import openpyxl



img_dir = path.join(path.dirname(__file__), 'img')
aud_dir = path.join(path.dirname(__file__), 'audio')


WIDTH = 800
HEIGHT = 800
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
#Colors I may use:
WHITE = (255, 255, 255)
ALMOST_WHITE = (250, 220, 255)
GRAY1 = (205, 205, 205)
GRAY2 = (155, 155, 155)
GRAY3 = (105, 105, 105)
GRAY3A = (55, 55, 55)
GRAY4 = (40, 40, 40)
GRAY5 = (20, 20, 20)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 20, 147)
CYAN = (50, 50, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self, img,type):
        super().__init__()
        self.index = 0
        self.counter = 0
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (400, 700)
        self.color = BLACK
        self.speed = 5
        self.dir = "N"
        self.health = 300
        self.type = type
        self.images = []
        self.sizes = []
        if self.type == "VG":
            for x in range(1, 5):
                img = pygame.image.load(f"img/V-gundam/VG ({x}).png")
                img.set_colorkey(BLACK)
                self.sizes.append(img.get_size())
                self.images.append(img)
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
        else:
            for x in range(1, 5):
                img = pygame.image.load(f"img/RX ({x}).png")
                img.set_colorkey(BLACK)
                self.sizes.append(img.get_size())
                self.images.append(img)
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()

        self.rect.center = (400, 700)

    def update(self):
            speed = 20
            self.counter += 1
            if self.index == len(self.images) - 1:
                self.index = -1
            if self.counter >= speed and self.index < len(self.images) - 1:
                self.counter = 0
                self.index += 1
                self.image = self.images[self.index]


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def shoot (self, bgroup):
        spawnx = self.rect.x + 45
        b = PlayerBullet(spawnx, self.rect.y)
        bgroup.add(b)

class Fin(pygame.sprite.Sprite):
    def __init__(self, cx, cy, Player):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(f"img/V-gundam/fin.png")
        self.index = 0
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.counter = 0
        self.damage = 50
        self.lifeTimer = 15000
        self.starttimer = pygame.time.get_ticks()
        self.follow = Player

    def shoot(self, bList):
        temp = FinShot(self.rect.x, self.rect.y)
        bList.add(temp)

class Zaku(pygame.sprite.Sprite):
    def __init__(self, cx, cy):
        super().__init__()
        self.images = []
        self.sizes = []
        for x in range (1,5):
            img = pygame.image.load(f"img/ZakuI{x}.png")
            img.set_colorkey(BLACK)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.speed = 2
        self.health = 100
        self.score = 10
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.counter = 0

    def update(self):
        speed = 20
        if self.health <=0:
            self.kill()
        self.counter += 1
        self.rect.y += 2
        if self.index == len(self.images) - 1:
            self.index = -1
        if self.counter >= speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]


class Gelgoog(pygame.sprite.Sprite):
    def __init__(self, x, y,target):
        super().__init__()
        self.image = pygame.image.load(f"img/Gelgoog-shield.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.health = 100
        self.score = 25
        self.shield = 3
        self.stun = False
        self.target = target
        self.fired = False
        self.firedTimer = 60
        self.cooldown = 0
    def follow (self):
        if self.target.rect.x <self.rect.x:
            self.rect.x -= self.speed
        if self.target.rect.x >self.rect.x:
            self.rect.x += self.speed
    def update(self):
        if self.health <=0:
            self.kill()
        if self.cooldown >0:
            self.cooldown -=1
        if self.shield ==0:
            self.stun = True
        if (not self.stun):
            self.rect.y+= self.speed
            self.follow()
            if self.rect.x == self.target.rect.x and self.cooldown != self.firedTimer:
                self.fired = True
                self.cooldown = self.firedTimer
        elif (self.stun):
            self.image = pygame.image.load(f"img/Gelgoog-stunned.png")



class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, cx, cy):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(f"img/beam.png")
        self.index = 0
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.counter = 0

    def update(self):
        speed = 4
        if self.rect.y < 0:
            self.kill()
        else:
            self.rect.y -=speed


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, cx, cy):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(f"img/enemybeam.png")
        self.index = 0
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.damage = 5
        self.counter = 0

    def update(self):
        speed = 4
        if self.rect.y > 800:
            self.kill()
        else:
            self.rect.y += speed

class explosion(pygame.sprite.Sprite):
    def __init__(self,cx,cy):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.sizes=[]
        for x in range (1,4):
            img = pygame.image.load(f"img/Explosion{x}.png")
            img.set_colorkey(BLACK)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.counter = 0
    def update(self):
        speed = 4
        self.counter+=1
        if self.counter >= speed and self.index < len(self.images) -1:
            self.counter=0
            self.index+=1
            self.image=self.images[self.index]
        if self.index >= len(self.images) -1 and self.counter >= speed:
            self.kill()
class grenexplosion(pygame.sprite.Sprite):
    def __init__(self,cx,cy):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.sizes=[]
        for x in range (1,7):
            img = pygame.image.load(f"img/grenexpl ({x}).png")
            img.set_colorkey(BLACK)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.counter = 0
    def update(self):
        speed = 4
        self.counter+=1
        if self.counter >= speed and self.index < len(self.images) -1:
            self.counter=0
            self.index+=1
            self.image=self.images[self.index]
        if self.index >= len(self.images) -1 and self.counter >= speed:
            self.kill()
class stars(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"img/Starfield 8 - 1024x1024.png")
        self.image.set_alpha(50)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 2
        self.frame = 0

    def update(self):

        if (self.frame != self.counter):
            self.frame+=1
        else:
            self.frame = 0
            if (self.rect.y < 1024):
                self.rect.y += 1
            elif (self.rect.y >= 1024):
                self.rect.y = -1024

class grenadeBar(pygame.sprite.Sprite):
    def __init__(self,cx,cy):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.sizes=[]
        self.energy = 0
        for x in range (1,5):
            img = pygame.image.load(f"img/grenadebar ({x}).png")
            img.set_colorkey(WHITE)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
    def update(self):
        if self.energy == 0:
            self.index = 3
        if self.energy == 1:
            self.index = 0
        if self.energy == 2:
            self.index = 1
        if self.energy == 3:
            self.index = 2
        if self.energy >3:
            self.energy = 3
        self.image = self.images[self.index]

class energyBar(pygame.sprite.Sprite):
    def __init__(self,cx,cy):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.sizes=[]
        self.energy = 0
        for x in range (1,6):
            img = pygame.image.load(f"img/energyBar{x}.png")
            img.set_colorkey(WHITE)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.counter = 0
        self.start = 0
        self.timer = 300
    def update(self):
        if self.energy >4:
            self.energy = 4
        if self.energy != 4:
            if self.start < self.timer:
                self.start +=1
            if self.start == self.timer:
                self.energy+=1
                self.start = 0
        self.image = self.images[self.energy]


class healthBar(pygame.sprite.Sprite):
    def __init__(self,cx,cy):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.sizes=[]
        self.health=300
        for x in range (1,6):
            img = pygame.image.load(f"img/healthBar ({x}).png")
            img.set_colorkey(WHITE)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.count = 0
    def update(self):
        if self.health ==300:
            self.count = 4
        if 200<= self.health < 300:
            self.count = 3
        if 100<= self.health < 200:
            self.count = 2
        if 0< self.health < 100:
            self.count = 1
        elif self.health <= 0:
            self.count = 0
        self.image = self.images[self.count]

class Swordswing(pygame.sprite.Sprite):
    def __init__(self,cx,cy):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.sizes=[]
        for x in range (1,4):
            img = pygame.image.load(f"img/Swordswing{x}.png")
            img.set_colorkey(BLACK)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.counter = 0
    def update(self):
        speed = 4
        self.counter+=1
        self.rect.y-=5
        if self.counter >= speed and self.index < len(self.images) -1:
            self.counter=0
            self.index+=1
            self.image=self.images[self.index]

class CresentShot(pygame.sprite.Sprite):
    def __init__(self, cx, cy, target):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.sizes = []
        for x in range(1, 5):
            img = pygame.image.load(f"img/cresent{x}.png")
            img.set_colorkey(BLACK)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.speed = 1
        self.counter = 0
        self.damage = 10
        self.target = target
        self.curve_points = self.calculate_bezier_curve(cx, cy, target.rect.x, target.rect.y)
        self.curve_index = 0

    def update(self):
        speed = 20
        self.counter += 1
        if self.index == len(self.images) - 1:
            self.index = -1
        if self.counter >= speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.curve_index < len(self.curve_points):
            curve_point = self.curve_points[self.curve_index]
            self.rect.x = curve_point[0]
            self.rect.y = curve_point[1]
            self.curve_index += 1
        else:
            self.kill()

    def calculate_bezier_curve(self, cx, cy, tx, ty):
        # Bezier curve calculation
        control1 = (cx + (tx - cx) / 3, cy - (ty - cy) / 3)
        control2 = (cx + 2 * (tx - cx) / 3, cy - 2 * (ty - cy) / 3)

        points = []
        steps = 100  # Adjust this for smoother or coarser curves. Warning: more steps may lag game while calculating
        for t in range(steps):
            x = ((1 - t / steps) ** 3) * cx + 3 * ((1 - t / steps) ** 2) * (t / steps) * control1[0] + 3 * (
                        (1 - t / steps)) * ((t / steps) ** 2) * control2[0] + ((t / steps) ** 3) * tx
            y = ((1 - t / steps) ** 3) * cy + 3 * ((1 - t / steps) ** 2) * (t / steps) * control1[1] + 3 * (
                        (1 - t / steps)) * ((t / steps) ** 2) * control2[1] + ((t / steps) ** 3) * ty
            points.append((x, y))
        return points



class FinShot(pygame.sprite.Sprite):
    def __init__(self,cx,cy):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.sizes=[]
        for x in range (1,5):
            img = pygame.image.load(f"img/V-gundam/fin-shot ({x}).png")
            img.set_colorkey(BLACK)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.speed = 1
        self.counter = 0
        self.target = None
    def update(self):
        speed = 20
        self.counter+=1
        self.rect.y-=5
        if self.index == len(self.images) -1:
            self.index=-1
        if self.counter >= speed and self.index < len(self.images) -1:
            self.counter=0
            self.index+=1
            self.image=self.images[self.index]
        if self.target != None:
            if self.target.rect.x < self.rect.x:
                self.rect.x -= self.speed
            if self.target.rect.x > self.rect.x:
                self.rect.x += self.speed
        if self.rect.y<0:
            self.kill()

class MachineShot(pygame.sprite.Sprite):
    def __init__(self,cx,cy):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.sizes=[]
        for x in range (1,5):
            img = pygame.image.load(f"img/Char/Char_beam ({x}).png")
            img.set_colorkey(BLACK)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.speed = 1
        self.counter = 0
        self.damage = 2

    def update(self):
        speed = 20
        self.counter+=1
        self.rect.y+=5
        if self.index == len(self.images) -1:
            self.index=-1
        if self.counter >= speed and self.index < len(self.images) -1:
            self.counter=0
            self.index+=1
            self.image=self.images[self.index]
        if self.rect.y>800:
            self.kill()

class CannonShot(pygame.sprite.Sprite):
    def __init__(self,cx,cy):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.sizes=[]
        for x in range (1,5):
            img = pygame.image.load(f"img/Char/CharBigShot ({x}).png")
            img.set_colorkey(BLACK)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.speed = 1
        self.counter = 0
        self.damage = 30

    def update(self):
        speed = 20
        self.counter+=1
        self.rect.y+=10
        if self.index == len(self.images) -1:
            self.index=-1
        if self.counter >= speed and self.index < len(self.images) -1:
            self.counter=0
            self.index+=1
            self.image=self.images[self.index]
        if self.rect.y>800:
            self.kill()

class MissileShot(pygame.sprite.Sprite):
    def __init__(self, cx, cy, target, envg):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(f"img/Char/roc.png")
        self.original_image = img
        self.rect = self.original_image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.envg = envg
        self.speed = 3
        self.damage = 15
        self.target = target
        self.curve_points = self.calculate_bezier_curve(cx, cy, target.rect.x, target.rect.y)
        self.curve_index = 0
        self.rotation = 0

    def update(self):
        if self.curve_index < len(self.curve_points):
            curve_point = self.curve_points[self.curve_index]
            self.rect.x = curve_point[0]
            self.rect.y = curve_point[1]
            self.curve_index += 1

            if self.curve_index < len(self.curve_points):
                next_curve_point = self.curve_points[self.curve_index]
                dx = next_curve_point[0] - curve_point[0]
                dy = next_curve_point[1] - curve_point[1]
                self.rotation = math.degrees(math.atan2(dy, dx)) - 90
                self.rotate_image()

            if self.rect.colliderect(self.target.rect):
                self.target.health -= self.damage
                self.explode(self.envg)
                self.kill()
        else:
            self.explode(self.envg)
            self.kill()

    def explode(self, enviromental_sprites):

        Explosion = explosion(self.rect.centerx - 10, self.rect.centery - 10)
        enviromental_sprites.add(Explosion)

    def calculate_bezier_curve(self, cx, cy, tx, ty):

        control1 = (cx + (tx - cx) / 3, cy - (ty - cy) / 3)
        control2 = (cx + 2 * (tx - cx) / 3, cy - 2 * (ty - cy) / 3)

        points = []
        steps = 100
        for t in range(steps):
            x = ((1 - t / steps) ** 3) * cx + 3 * ((1 - t / steps) ** 2) * (t / steps) * control1[0] + 3 * (
                    (1 - t / steps)) * ((t / steps) ** 2) * control2[0] + ((t / steps) ** 3) * tx
            y = ((1 - t / steps) ** 3) * cy + 3 * ((1 - t / steps) ** 2) * (t / steps) * control1[1] + 3 * (
                    (1 - t / steps)) * ((t / steps) ** 2) * control2[1] + ((t / steps) ** 3) * ty
            points.append((x, y))
        return points

    def rotate_image(self):
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
class CharNovaZakuII(pygame.sprite.Sprite):
    def __init__(self, x, y, target,envg):
        super().__init__()
        self.burst_delay = 10
        self.burst_count = 0
        self.counter = 0
        self.mgs = []
        self.envg = envg
        self.rockets = []
        self.cannons = []
        self.target = target
        self.abilgroup = pygame.sprite.Group()
        self.shieldActive = False
        for x in range(1, 5):
            mg = pygame.image.load(f"img/Char/charMG ({x}).png")
            mg.set_colorkey(BLACK)
            self.mgs.append(mg)
            rocket = pygame.image.load(f"img/Char/charRocket ({x}).png")
            rocket.set_colorkey(BLACK)
            self.rockets.append(rocket)
            canon = pygame.image.load(f"img/Char/CharCannon ({x}).png")
            canon.set_colorkey(BLACK)
            self.cannons.append(canon)
        self.index = 0
        self.curMode = self.mgs
        self.image = self.curMode[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.stepsneeded = 350
        self.stepstaken = 0
        self.move = 2
        self.last_shot_time = 0
        self.cannonFire = False
        self.shottimer = 0
        self.firerate = 50
        self.cannonShoot = 300
        self.health = 500
        self.abilities = {
            "Shoulder Shield": {"cooldown": random.randint (500,600), "cooldown_timer": 600},
            "ASR-78 MS Anti-Ship Rifle": {"cooldown": random.randint (0,800), "cooldown_timer": 800},
            "Type A2 MS Bazooka": {"cooldown": random.randint (0,700), "cooldown_timer": 700},
            "Machine Gun": {"cooldown": random.randint (0,100), "cooldown_timer": 100},
        }
    def update(self):

        speed = 20
        self.counter += 1
        if self.cannonFire:
            if self.abilgroup.has(Charge):
                pass
            else:
                if self.cannonShoot > 0:
                    self.cannonShoot-=1
                else:
                    self.fireASR()
                    self.chargup.kill()
                    self.cannonFire = False
                    self.cannonShoot =300


        if self.stepstaken == self.stepsneeded:
            self.move *= -1
            self.stepstaken = 0

        else:
            self.stepstaken+=1

        if self.index == len(self.curMode) -1:
            self.index=-1
        if self.counter >= speed and self.index < len(self.curMode) -1:
            self.counter=0
            self.index+=1
            self.image=self.curMode[self.index]


        self.rect.x += self.move
        if self.shieldActive:
            self.shield.rect.x += self.move
            if self.shield.health ==0:
                self.shield.kill()
                self.shieldActive = False
        if self.cannonFire:
            self.chargup.rect.x = self.rect.x

        for ability in self.abilities:
            if self.shieldActive or self.cannonFire:
                break
            if self.abilities[ability]["cooldown"] >0:
                self.abilities[ability]["cooldown"] -=1
            if self.abilities[ability]["cooldown"] == 0:
                self.activate_ability(ability)
                self.abilities[ability]["cooldown"] = random.randint (0,self.abilities[ability]["cooldown_timer"])
        self.abilgroup.update()

    def activate_ability(self, ability_name):
        if ability_name == "Shoulder Shield":
            self.activate_shoulder_shield()
        elif ability_name == "ASR-78 MS Anti-Ship Rifle":
            self.activate_anti_ship_rifle()
        elif ability_name == "Type A2 MS Bazooka":
            self.activate_bazooka(self.target)
        elif ability_name == "Machine Gun":
            self.activate_machine_gun()

    class CharsShield(pygame.sprite.Sprite):
        def __init__(self, cx, cy):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(f"img/Char/Shield.png")
            self.rect = self.image.get_rect()
            self.rect.x = cx
            self.rect.y = cy
            self.health = 3
    def activate_shoulder_shield(self):
        if self.shieldActive == False:
            self.shield = self.CharsShield(self.rect.x-5, self.rect.y+50)
            self.shieldActive = True
            self.abilgroup.add(self.shield)



    def activate_machine_gun(self):
        round = MachineShot(self.rect.x, self.rect.y)
        self.abilgroup.add(round)

    def activate_bazooka(self, target):

        current_time = pygame.time.get_ticks()
        time_since_last_shot = current_time - self.last_shot_time

        if time_since_last_shot > 500:
            for _ in range(3):
                round = MissileShot(self.rect.x, self.rect.y, target, self.envg)
                self.abilgroup.add(round)
                self.last_shot_time = current_time

    def fireASR(self):
        round = CannonShot(self.rect.x, self.rect.y)
        self.abilgroup.add(round)
        self.cannonFire=False
    def activate_anti_ship_rifle(self):
        if self.cannonFire == False:

            self.chargup = Charge(self.rect.x, self.rect.y +15)
            self.abilgroup.add(self.chargup)
            self.cannonFire = True
            self.curMode = self.cannons
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, elist, envg):
        super().__init__()
        self.image = pygame.image.load(f"img/grenade.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 5
        self.startY = y
        self.envg = envg
        self.explosion_radius = 200
        self.damage = 200
        self.enemylist = elist

    def update(self):
        self.rect.y -= self.velocity
        if self.startY - self.rect.y > 300 or self.rect.y <= 100:
            self.explode(self.envg)

    def explode(self, envg):
        exp = grenexplosion(self.rect.centerx-100, self.rect.centery-100)
        envg.add(exp)
        for enemy in self.enemylist:
            distancex = self.rect.x - enemy.rect.x
            if distancex <0:
                distancex=distancex* -1
            distancey = self.rect.y - enemy.rect.y
            if distancey < 0:
                distancey = distancex * -1
            if distancex <= self.explosion_radius and distancey <= self.explosion_radius:
                enemy.health -= self.damage
        self.kill()


class Zeong (pygame.sprite.Sprite):
    def __init__(self, target):
        super().__init__()

        self.chest_active = False
        self.image = pygame.image.load("img/zeong.png")
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = -200
        self.health = 1500
        self.target = target
        self.fist_active = False
        self.fistrecharge = 15000
        self.chestcharge = 17000
        self.last_update = pygame.time.get_ticks()
        self.abilgroup = pygame.sprite.Group()
        self.abilities = {
            "flying fist": {"cooldown": random.randint(100, 300), "cooldown_timer": 300},
            "Chest cannon": {"cooldown": random.randint(100, 800), "cooldown_timer": 800},
            "laser fingers": {"cooldown": random.randint(100, 700), "cooldown_timer": 700},
        }
    def update(self):
        current_time = pygame.time.get_ticks()
        print (self.fist_active)
        if current_time - self.last_update > self.fistrecharge and self.fist_active:
            self.fist_active = False
        if current_time - self.last_update > self.chestcharge and self.chest_active:
            self.chest_active = False

        if self.rect.y < 0:
             self.rect.y += 1
        else:
             for ability in self.abilities:
                 if self.abilities[ability]["cooldown"] > 0:
                     self.abilities[ability]["cooldown"] -= 1
                 if self.abilities[ability]["cooldown"] == 0:
                     self.activate_ability(ability)
                     self.abilities[ability]["cooldown"] = random.randint(0, self.abilities[ability]["cooldown_timer"])

    def activate_ability(self, ability_name):
        if ability_name == "flying fist":
            self.activate_fists(self.target)
        elif ability_name == "Chest cannon"and self.chest_active == False and self.fist_active == False:
           self.activate_chest()
        elif ability_name == "laser fingers" and self.fist_active == False and self.chest_active == False:
            self.activate_fingers()
    def activate_fists (self, target):
        tempfist = FlyingFist(random.randint(5,795), -20, target)
        self.abilgroup.add(tempfist)



    def activate_fingers(self):
        self.fist_active = True
        self.last_update = pygame.time.get_ticks()
        SpawnX= {60, 110, 160, 210, 260, 740, 690, 640, 590, 540}
        for xs in SpawnX:
            temp = laserFingers(xs, self.target)
            self.abilgroup.add(temp)

    def activate_chest(self):
        self.chest_active = True
        self.last_update = pygame.time.get_ticks()
        temp = chestLaser(385, self.target)
        self.abilgroup.add(temp)

class chestLaser(pygame.sprite.Sprite):
    def __init__(self, x,  target):
        super().__init__()
        self.image = pygame.image.load("img/chestlaser.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, -800)
        self.target = target
        self.time_to_fly = 3000
        self.time_to_live = 8000
        self.needs_to_shoot = True
        self.last_update = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.time_to_fly and self.needs_to_shoot:
            self.rect.y = 100
            self.last_update = pygame.time.get_ticks()
            self.needs_to_shoot = False
        else:
            self.draw_path(screen, self.rect.x)
        if self.rect.colliderect(self.target.rect):
            self.target.health -= .1
        if current_time - self.last_update > self.time_to_live:
            print("Laser time to live exceeded")
            self.kill()

    def draw_path(self, screen,x):

        rect_width = abs(100)
        rect_height = abs(800)
        blit_x = self.rect.centerx - 50
        blit_y = self.rect.centery
        surface = pygame.Surface((abs(rect_width), abs(rect_height)), pygame.SRCALPHA)
        pygame.draw.rect(surface, (255, 0, 0, 100), (0, 0, abs(rect_width), abs(rect_height)), 2)
        screen.blit(surface, (blit_x, 0))

class laserFingers(pygame.sprite.Sprite):
    def __init__(self, x,  target):
        super().__init__()

        self.image = pygame.image.load("img/LaserFist.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, -800)
        self.target = target
        self.time_to_fly = 3000
        self.time_to_live = 8000
        self.needs_to_shoot = True
        self.last_update = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.time_to_fly and self.needs_to_shoot:
            self.rect.y = 0
            self.last_update = pygame.time.get_ticks()
            self.needs_to_shoot = False
        else:
            self.draw_path(screen, self.rect.x)
        if self.rect.colliderect(self.target.rect):
            self.target.health -= .1
        if current_time - self.last_update > self.time_to_live:
            print("Laser time to live exceeded")
            self.kill()

    def draw_path(self, screen,x):

        rect_width = abs(25)
        rect_height = abs(800)
        blit_x = self.rect.centerx
        blit_y = self.rect.centery
        surface = pygame.Surface((abs(rect_width), abs(rect_height)), pygame.SRCALPHA)
        pygame.draw.rect(surface, (255, 0, 0, 100), (0, 0, abs(rect_width), abs(rect_height)), 2)
        screen.blit(surface, (blit_x, 0))
class FlyingFist(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()

        if x >= 400:
            self.original_image = pygame.image.load("img/fistL.png")
        else:
            self.original_image = pygame.image.load("img/fistR.png")
        self.rect = self.original_image.get_rect()
        self.rect.center = (x, y)
        self.target = target
        self.angle = self.calculate_angle()
        self.speed = 15
        self.canHit = True
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.time_to_fly = 2000
        self.last_update = pygame.time.get_ticks()
        self.initial_rotation = 180
        if self.rect.x > 400:
            self.initial_rotation = -180
        self.image = pygame.transform.rotate(self.original_image, self.angle)

        self.end_point = self.calculate_end_point()

    def calculate_end_point(self):

        end_x = self.rect.centerx + math.cos(self.angle) * self.speed * (self.time_to_fly / 1000)
        end_y = self.rect.centery + math.sin(self.angle) * self.speed * (self.time_to_fly / 1000)
        return end_x, end_y

    def calculate_angle(self):

        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        return math.atan2(dy, dx)
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.time_to_fly:
            self.rect.x += self.dx
            self.rect.y += self.dy
            self.rotate_image()
        else:
            self.draw_path(screen)
        if self.rect.colliderect(self.target.rect) and self.canHit:
            self.target.health -= 10
            self.canHit = False
        if self.rect.y > 800:
            self.kill()

    def rotate_image(self):

        angle = math.degrees(math.atan2(-self.dy, self.dx)) + self.initial_rotation +135
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw_path(self, screen):

        rect_width = abs(25)
        rect_height = abs(self.end_point[1] - self.rect.centery) * 100


        dx = self.end_point[0] - self.rect.centerx
        dy = self.end_point[1] - self.rect.centery
        trajectory_angle = math.atan2(dx, dy)
        if self.rect.x >= 400:
            if trajectory_angle > 0:
                trajectory_angle += math.pi
            else:
                trajectory_angle -= math.pi

        surface = pygame.Surface((abs(rect_width), abs(rect_height)), pygame.SRCALPHA)
        pygame.draw.rect(surface, (255, 0, 0, 100), (0, 0, abs(rect_width), abs(rect_height)), 2)
        rotated_surface = pygame.transform.rotate(surface, math.degrees(trajectory_angle))

        blit_x = min(self.rect.centerx, self.end_point[0])
        blit_y = min(self.rect.centery, self.end_point[1])

        screen.blit(rotated_surface, (blit_x, blit_y))

    def rotate_image(self):

        rotation_angle = math.atan2(self.dy, self.dx)

        self.image = pygame.transform.rotate(self.original_image, math.degrees(rotation_angle) + self.initial_rotation)
        self.rect = self.image.get_rect(center=self.rect.center)






class Gouf(pygame.sprite.Sprite):
    def __init__(self, x, y, bullets_group):
        super().__init__()
        self.images = []
        self.sizes = []
        for yx in range(1, 5):
            img = pygame.image.load(f"img/Gouf ({yx}).png")
            img.set_colorkey(BLACK)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.health = 200
        self.score = 30
        self.counter = 0
        self.shield = 3
        self.dir = 1
        self.bullets_group = bullets_group
        self.fired_timer = 1500
        self.last_shot_time = pygame.time.get_ticks()

    def update(self):
        speed = 20
        self.counter+=1
        if self.health <=0:
            self.kill()
        if self.index == len(self.images) - 1:
            self.index = -1
        if self.counter >= speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.rect.y < 300:
            self.rect.y += self.speed
        else:
            if self.rect.x > 700:
                self.dir = -1
            if self.rect.x < 100:
                self.dir = 1
            self.rect.x += self.speed * self.dir
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.fired_timer:
            self.shoot_snake_bullet()
            self.last_shot_time = current_time

    def shoot_snake_bullet(self):
        snake_bullet = SnakeBullet(self.rect.centerx-50, self.rect.centery)
        self.bullets_group.add(snake_bullet)
        snake_bullet = SnakeBullet(self.rect.centerx - 50, self.rect.centery-20)
        self.bullets_group.add(snake_bullet)
        snake_bullet = SnakeBullet(self.rect.centerx - 50, self.rect.centery-40)
        self.bullets_group.add(snake_bullet)


class SnakeBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(f"img/02.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.damage = 15
        self.rect.y = y
        self.speed_x = 5
        self.speed_y = 1
        self.amplitude = 20
        self.angle = 0
        self.dir = 1
        self.moveCount =100
        self.curMove = 0

    def update(self):

        self.rect.y +=2
        if self.curMove < self.moveCount:
            self.rect.x += 2*self.dir
            self.curMove +=1
        else:
            self.curMove = 0
            self.dir *=-1

class Acguy(pygame.sprite.Sprite):
    def __init__(self, x, y, bullets_group):
        super().__init__()
        self.image = pygame.image.load(f"img/acguy.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.bullets_group = bullets_group
        self.shoot_delay = 2000
        self.shotammount = 3
        self.curshot = 0
        self.health = 200
        self.score = 20
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += 1
        if self.health <=0:
            self.kill()
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_delay:
            self.last_shot = now
            self.shoot()
            self.curshot +=1

    def shoot(self):
        start_x, start_y = self.rect.center
        spacing = 3
        velocities = [-2, -1, 0, 1, 2]


        for velocity in velocities:
            bullet = spread(start_x, start_y, velocity, spacing)
            self.bullets_group.add(bullet)
            bullet = spread(start_x, start_y+25, velocity, spacing)
            self.bullets_group.add(bullet)
            bullet = spread(start_x, start_y+45, velocity, spacing)
            self.bullets_group.add(bullet)

class spread(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, spacing):
        super().__init__()
        self.counter = 0
        self.images = []
        self.sizes = []
        for tx in range(1, 5):
            img = pygame.image.load(f"img/spread ({tx}).png")
            img.set_colorkey(BLACK)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.damage = 2
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity_x = velocity_x
        self.velocity_y = spacing

    def update(self):
        speed = 20
        self.counter += 1
        if self.index == len(self.images) - 1:
            self.index = -1
        if self.counter >= speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y


        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()


class Orb(pygame.sprite.Sprite):
    def __init__(self, cx, cy, type):
        super().__init__()
        self.counter = 0
        self.type = type
        self.images = []
        self.sizes = []
        if type == "heal":
            for x in range(1, 6):
                img = pygame.image.load(f"img/healorb ({x}).png")
                img.set_colorkey(BLACK)
                self.sizes.append(img.get_size())
                self.images.append(img)
        if type == "energy":
            for x in range(1, 6):
                img = pygame.image.load(f"img/energyorb ({x}).png")
                img.set_colorkey(BLACK)
                self.sizes.append(img.get_size())
                self.images.append(img)
        if type == "grenade":
            for x in range(1, 6):
                img = pygame.image.load(f"img/grenadeDrop ({x}).png")
                img.set_colorkey(BLACK)
                self.sizes.append(img.get_size())
                self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(cx, cy))
        self.velocity_y = 2
        self.health_value = 20
        self.energy_value = 1
    def update(self):
        speed = 20
        self.rect.y += self.velocity_y
        self.counter += 1
        if self.index == len(self.images) - 1:
            self.index = -1
        if self.counter >= speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

class Charge(pygame.sprite.Sprite):
    def __init__(self, cx, cy):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.sizes = []
        for x in range(1, 5):
            img = pygame.image.load(f"img/Char/chargup ({x}).png")
            img.set_colorkey(BLACK)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.counter = 0
        self.totalCount = 0

    def update(self):
        speed = 20
        self.counter += 1
        if self.index == len(self.images) - 1:
            self.index = -1
        if self.counter >= speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.totalCount +=1
            self.index += 1
            self.image = self.images[self.index]

    def fire(self):
        if self.totalCount == 10:
            return True

class Thrust(pygame.sprite.Sprite):
    def __init__(self, cx, cy):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.sizes = []
        for x in range(1, 5):
            img = pygame.image.load(f"img/thrust{x}.png")
            img.set_colorkey(BLACK)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.counter = 0

    def update(self):
        speed = 20
        self.counter += 1
        if self.index == len(self.images) - 1:
            self.index = -1
        if self.counter >= speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
class dashlight (pygame.sprite.Sprite):
    def __init__(self, cx, cy):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.sizes = []
        for x in range(1, 5):
            img = pygame.image.load(f"img/icon ({x}).png")
            img.set_colorkey(BLACK)
            self.sizes.append(img.get_size())
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.status = "off"
        self.counter = 0

    def update(self):
        if self.status != "off":
            speed = 20
            self.counter += 1
            if self.index == len(self.images) - 1:
                self.index = -1
            if self.counter >= speed and self.index < len(self.images) - 1:
                self.counter = 0
                self.index += 1
                self.image = self.images[self.index]
class Background ():
    def __init__(self,img):
        self.color = BLACK
        self.x=400
        self.y=400
        self.rect = pygame.Rect(self.x, self.y, 500, 500)
        self.sprite=img.get_rect()
        self.sprite.center = self.x, self.y
    def draw (self, screen):
        pygame.draw.rect(screen, self.color, self.sprite, 1)