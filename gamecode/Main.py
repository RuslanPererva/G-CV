import math

import pygame,random,time,sys
from os import path
import openpyxl

#Directories I may use:
img_dir = path.join(path.dirname(__file__), 'img')
aud_dir = path.join(path.dirname(__file__), 'audio')

#constants
WIDTH = 800
HEIGHT = 800
FPS = 60


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

enviromental_sprites = pygame.sprite.Group()

def draw_text(font, text, x, y):
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x,y)
    screen.blit(text_surface,text_rect)
def draw_cursor (font,x,y,x2,y2):
    draw_text(font, "*", x,y)
    draw_text(font, "*", x2, y2)

class cursor():
    def __init__(self,font):
        self.font = font
        self.x = 250
        self.x2= 550
        self.y = 500
        self.y2 = self.y
        self.text = "*"
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x, self.y)
        screen.blit(text_surface, text_rect)

        text2_surface = font.render(self.text, True, WHITE)
        text2_rect = text2_surface.get_rect()
        text2_rect.center = (self.x, self.y)
        screen.blit(text2_surface, text2_rect)
    def move (self, x, x2, y):
        self.x = x
#Player for now:
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
        self.rect.center = (400, 700)

    def update(self):
        if self.type == "VG":
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
        self.counter += 1
        self.rect.y += 2
        if self.index == len(self.images) - 1:
            self.index = -1
        if self.counter >= speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]


class gelgoog(pygame.sprite.Sprite):
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
        print (self.index)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.counter = 0
        self.start = 0
    def update(self):
        timer = 300
        if self.energy != 4:
            if self.start < timer:
                self.start +=1
            if self.start == timer:
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
        print (self.index)
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
        # For simplicity, let's assume we have 4 control points: start, two middle, and end
        # Here, start is the current position (cx, cy), and end is the target position (tx, ty)
        # Two middle control points are calculated based on the difference between start and end
        # You can adjust the control points to change the curve shape
        control1 = (cx + (tx - cx) / 3, cy - (ty - cy) / 3)
        control2 = (cx + 2 * (tx - cx) / 3, cy - 2 * (ty - cy) / 3)

        points = []
        steps = 100  # Adjust this for smoother or coarser curves
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
    def __init__(self, cx, cy, target):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(f"img/Char/roc.png")
        self.original_image = img
        self.rect = self.original_image.get_rect()
        self.rect.x = cx
        self.rect.y = cy
        self.speed = 3
        self.damage = 15
        self.target = target
        self.curve_points = self.calculate_bezier_curve(cx, cy, target.rect.x, target.rect.y)
        self.curve_index = 0
        self.rotation = 0  # Initial rotation

    def update(self):
        if self.curve_index < len(self.curve_points):
            curve_point = self.curve_points[self.curve_index]
            self.rect.x = curve_point[0]
            self.rect.y = curve_point[1]
            self.curve_index += 1
            # Calculate rotation angle towards end point of the Bezier curve
            if self.curve_index < len(self.curve_points):
                next_curve_point = self.curve_points[self.curve_index]
                dx = next_curve_point[0] - curve_point[0]
                dy = next_curve_point[1] - curve_point[1]
                self.rotation = math.degrees(math.atan2(dy, dx)) - 90  # Adjust for initial sprite orientation
                self.rotate_image()

            if self.rect.colliderect(self.target.rect):
                self.target.health -= self.damage  # Apply damage to the target
                self.explode()  # Create an explosion
                self.kill()  # Destroy the missile
        else:
            self.explode()
            self.kill()

    def explode(self):
        # Create an explosion at the missile's position
        Explosion = explosion(self.rect.centerx, self.rect.centery)
        enviromental_sprites.add(Explosion)

    def calculate_bezier_curve(self, cx, cy, tx, ty):
        # Bezier curve calculation
        # For simplicity, let's assume we have 4 control points: start, two middle, and end
        # Here, start is the current position (cx, cy), and end is the target position (tx, ty)
        # Two middle control points are calculated based on the difference between start and end
        # You can adjust the control points to change the curve shape
        control1 = (cx + (tx - cx) / 3, cy - (ty - cy) / 3)
        control2 = (cx + 2 * (tx - cx) / 3, cy - 2 * (ty - cy) / 3)

        points = []
        steps = 100  # Adjust this for smoother or coarser curves
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
    def __init__(self, x, y, target):
        super().__init__()
        self.burst_delay = 10
        self.burst_count = 0
        self.counter = 0
        self.mgs = []
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
        self.health = 100  # Adjust health as per your requirement
        self.abilities = {
            "Shoulder Shield": {"cooldown": random.randint (500,600), "cooldown_timer": 600},
            "ASR-78 MS Anti-Ship Rifle": {"cooldown": random.randint (0,800), "cooldown_timer": 800},
            "Type A2 MS Bazooka": {"cooldown": random.randint (0,700), "cooldown_timer": 700},
            "Machine Gun": {"cooldown": random.randint (0,100), "cooldown_timer": 100},
        }
    def update(self):

        speed = 20
        self.counter += 1
        print ("cannon",self.cannonShoot)
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
        # Fire three rounds with a delay between each shot
        current_time = pygame.time.get_ticks()  # Get the current time
        time_since_last_shot = current_time - self.last_shot_time

        if time_since_last_shot > 500:  # Adjust delay time between shots as needed
            for _ in range(3):
                round = MissileShot(self.rect.x, self.rect.y, target)
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
        snake_bullet = SnakeBullet(self.rect.centerx - 50, self.rect.centery-10)
        self.bullets_group.add(snake_bullet)
        snake_bullet = SnakeBullet(self.rect.centerx - 50, self.rect.centery-20)
        self.bullets_group.add(snake_bullet)


class SnakeBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(f"img/02.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 2  # Horizontal speed
        self.speed_y = 3  # Vertical speed
        self.amplitude = 20  # Oscillation amplitude
        self.angle = 0  # Initial angle for oscillation
        self.dir = 1
        self.moveCount =50
        self.curMove = 0

    def update(self):
        # Oscillate back and forth on the x-axis
        self.rect.y +=5
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
        now = pygame.time.get_ticks()

        if now - self.last_shot >= self.shoot_delay:
            self.last_shot = now
            self.shoot()
            self.curshot +=1

    def shoot(self):
        start_x, start_y = self.rect.center
        spacing = 5
        velocities = [-2, -1, 0, 1, 2]

        for velocity in velocities:
            bullet = Bullet(start_x, start_y, velocity, spacing)
            self.bullets_group.add(bullet)
            bullet = Bullet(start_x, start_y+25, velocity, spacing)
            self.bullets_group.add(bullet)
            bullet = Bullet(start_x, start_y+45, velocity, spacing)
            self.bullets_group.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, spacing):
        super().__init__()
        self.image = pygame.Surface((10, 10))  # Placeholder image
        self.image.fill((255, 255, 0))  # Yellow color for visibility
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity_x = velocity_x  # Adjust spacing along the x-axis
        self.velocity_y = spacing  # Constant velocity along the y-axis

    def update(self):
        # Move the bullet
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Check if the bullet is out of bounds
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()  # Remove the bullet if it's out of bounds
class sqaudren():
    def __init__(self, type, lane, group):
        match lane:
            case -3:
                self.spawnx=100
            case -2:
                self.spawnx =200
            case -1:
                self.spawnx = 300
            case 0:
                self.spawnx = 300
            case 1:
                self.spawnx = 500
            case 2:
                self.spawnx = 600
            case 3:
                self.spawnx = 700

        self.type = type
        self.group = group
        match type:
            case "Zaku":
                temp1 = Zaku(self.spawnx, 0)
                temp2 = Zaku(self.spawnx-50, -30)
                temp3 = Zaku(self.spawnx+50, -30)
                temp4 = Zaku(self.spawnx, -60)
                self.group.add(temp1)
                self.group.add(temp2)
                self.group.add(temp3)
                self.group.add(temp4)



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

def create_account(username, password):
    wb = openpyxl.load_workbook('PlayerLogin.xlsx')
    ws = wb.active
    ws.append([username, password])
    wb.save('PlayerLogin.xlsx')
    print("Account created successfully.")

def check_credentials(username, password):
    wb = openpyxl.load_workbook('PlayerLogin.xlsx')
    ws = wb.active
    for row in ws.iter_rows(values_only=True):
        print (row[0], row[1])
        if row[0] == username and row[1] == password:
            return True
    return False

pygame.init()
pygame.font.init()
my_font = pygame.font.Font('img/Vermin Vibes 1989.ttf', 30)
menu_font = pygame.font.Font('img/Vermin Vibes 1989.ttf', 50)
hud_font = pygame.font.Font('img/Vermin Vibes 1989.ttf', 20)
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('MSG:COSMIC_VANGUARD')

logo = pygame.sprite.Sprite()
logo.image = pygame.image.load("img/Logo.png").convert_alpha()
logo.rect = logo.image.get_rect()
logo.rect.center = [400,250]
pxl = pygame.sprite.Sprite()
pxl.image = pygame.image.load("img/Gundampxl.png").convert_alpha()
pxl.rect = pxl.image.get_rect()
pxl.rect.center = (520, 400)

Zpxl = pygame.sprite.Sprite()
Zpxl.image = pygame.image.load("img/zakuArt.png").convert_alpha()
Zpxl.rect = Zpxl.image.get_rect()
Zpxl.rect.center = (150, 350)

RXPXL = pygame.sprite.Sprite()
RXPXL.image = pygame.image.load("img/RXPXL.png").convert_alpha()
RXPXL.rect = RXPXL.image.get_rect()
RXPXL.rect.center = (200, 350)

VGPXL = pygame.sprite.Sprite()
VGPXL.image = pygame.image.load("img/VGPXL.png").convert_alpha()
VGPXL.rect = VGPXL.image.get_rect()
VGPXL.rect.center = (600, 350)

starsG = pygame.sprite.Group()
starSprite1 = stars(400,400)
starSprite2 = stars(400, -624)
starsG.add(starSprite1)
starsG.add(starSprite2)
clock = pygame.time.Clock()
bullets = pygame.sprite.Group()
PlayerBullets = pygame.sprite.Group()
enemies=pygame.sprite.Group()
enemyGelgoogs = pygame.sprite.Group()
enemyBullets = pygame.sprite.Group()
swordslash = pygame.sprite.Group()
healthBarBox=pygame.Rect(0,0,300,20)
Player_img = pygame.image.load(path.join(img_dir,'Gundam-b.png')).convert()
Player_img.set_colorkey(BLACK)
bkg_img = pygame.image.load(path.join(img_dir, 'SpaceP.png')).convert()
dth_img = pygame.image.load(path.join(img_dir, 'dthscr.png')).convert()
HUD_img = pygame.image.load(path.join(img_dir, 'NewHUD.png')).convert()
HUD_img.set_colorkey(WHITE)
HUD_img.set_alpha(50)
HUD = Background(HUD_img)
crack = pygame.image.load(path.join(img_dir, 'screen break.png')).convert_alpha()
crack.set_alpha(50)
crackbkg = Background(crack)
background = Background(bkg_img)
Player1 = Player(Player_img,"VG")
explosions = pygame.sprite.Group()
pygame.mixer.init()
boss = pygame.sprite.Group()
shoot_sfx = pygame.mixer.Sound("audio/beam-rifle-shot.mp3")
sword_sfx = pygame.mixer.Sound("audio/sword-schwing-40520.mp3")
death_sfx = pygame.mixer.Sound("audio/gundam-deathSFX.mp3")
swordE = energyBar(25, 700)
healthB = healthBar(25, 750)
SE = pygame.sprite.Group()
SE.add(swordE)
SE.add(healthB)
thruster = Thrust(Player1.rect.x+15, Player1.rect.y+25)
thr = pygame.sprite.Group()

def charSel():
    running = True
    selected = 1
    while running:
        keys = pygame.key.get_pressed()
        #screen.fill(BLACK)
        screen.blit(bkg_img, (0, 0))
        background.draw(screen)
        screen.blit(VGPXL.image, VGPXL.rect)
        screen.blit(RXPXL.image, RXPXL.rect)
        pygame.draw.rect(screen, BLUE, VGPXL.rect, 3)
        pygame.draw.rect(screen, BLUE, RXPXL.rect, 3)
        if selected ==1:
            pygame.draw.rect(screen, GREEN, RXPXL.rect, 5)
        if selected ==2:
            pygame.draw.rect(screen, GREEN, VGPXL.rect, 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if keys[pygame.K_RIGHT]:
                if (selected == 1):
                    selected =2
                    pygame.display.update()
                elif (selected == 2):
                    selected =1
                    pygame.display.update()
            if keys[pygame.K_LEFT]:
                if (selected == 1):
                    selected =2
                    pygame.display.update()
                elif (selected == 2):
                    selected =1
                    pygame.display.update()
            if keys[pygame.K_SPACE]:
                if (selected == 1):
                    Player1 = Player(Player_img,"RX")
                    menu(Player1)
                if (selected == 2):
                    Player1 = Player(Player_img,"VG")
                    menu(Player1)

        draw_text(menu_font, 'RX-78-2 Gundam', 200, 600)
        draw_text(menu_font, 'RX-93 v Gundam', 600, 600)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    exit()


def menu (P1):
    running = True
    selected = 1
    Player1 = P1
    #pygame.mixer.music.load("audio/caraaa.mp3")
    #pygame.mixer.music.play(100)
    while running:
        keys = pygame.key.get_pressed()
        screen.fill(BLACK)
        screen.blit(bkg_img, (0,0))
        background.draw(screen)
        screen.blit(pxl.image, pxl.rect)
        screen.blit(Zpxl.image, Zpxl.rect)
        screen.blit(logo.image, logo.rect)

        print (selected)
        if (selected == 1):
            draw_cursor(menu_font, 250, 500, 550, 500)
        if (selected == 2):
            draw_cursor(menu_font, 325, 550, 475, 550)
        if (selected == 3):
            draw_cursor(menu_font, 270, 600, 525, 600)
        if (selected == 4):
            draw_cursor(menu_font, 200, 650, 590, 650)
        if (selected == 5):
            draw_cursor(menu_font, 335, 700, 460, 700)
        draw_text(menu_font, 'Start Game', 400, 500)
        draw_text(menu_font, 'Login', 400, 550)
        draw_text(menu_font, 'Controls', 400, 600)
        draw_text(menu_font, 'Gundam Select', 400, 650)
        draw_text(menu_font, 'Quit', 400, 700)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if keys[pygame.K_DOWN]:
                if (selected == 1):
                    selected =2
                    pygame.display.update()
                elif (selected == 2):
                    selected =3
                    pygame.display.update()
                elif (selected == 3):
                    selected =4
                    pygame.display.update()
                elif (selected == 4):
                    selected =5
                    pygame.display.update()
                elif (selected == 5):
                    selected =1
                    pygame.display.update()
            if keys[pygame.K_UP]:
                if (selected == 1):
                    selected =5
                    pygame.display.update()
                elif (selected == 2):
                    selected =1
                    pygame.display.update()
                elif (selected == 3):
                    selected =2
                    pygame.display.update()
                elif (selected == 4):
                    selected =3
                    pygame.display.update()
                elif (selected == 5):
                    selected =4
                    pygame.display.update()
            if keys[pygame.K_SPACE]:
                if (selected == 1):
                    game(P1)
                if (selected == 2):
                    login()
                if (selected == 3):
                    pass
                if (selected ==4):
                    charSel()
                if (selected ==5):
                    running = False
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    exit()
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.callback = callback
        self.hovered = False

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                self.callback()

class TextInputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # Return the text if Enter is pressed.
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    # Remove one character from the text.
                    self.text = self.text[:-1]
                else:
                    # Add the pressed character to the text.
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)
        return None  # Return None if no text is submitted

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
def login():
    def submit_credentials(username, password):
        if username.strip() and password.strip(): # Check if both fields are not empty
            if check_credentials(username_box.text, password_box.text) == False:
                create_account(username, password)  # Call the create_account function when both fields are not empty
                # Clear the input boxes after submitting
                username_box.text = ''
                password_box.text = ''
            elif check_credentials(username_box.text, password_box.text) == True:
                print ("account exists")
        else:
            draw_text(menu_font, "Must fill out both Username and Password", 500, 200)
    username_box = TextInputBox(300, 200, 140, 32)
    password_box = TextInputBox(300, 300, 140, 32)

    # Define button coordinates and dimensions
    button_x = 300
    button_y = 400
    button_width = 140
    button_height = 50

    # Create the button
    button = Button(button_x, button_y, button_width, button_height, "Submit", (0, 255, 0), (0, 200, 0),
                    lambda: submit_credentials(username_box.text, password_box.text))

    input_boxes = [username_box, password_box]

    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_text(menu_font, "Account Management", 400, 100)
        draw_text(menu_font, "Username:", 200, 200)
        draw_text(menu_font, "Password:", 200, 300)

        for box in input_boxes:
            box.update()
            box.draw(screen)

        button.draw(screen)  # Draw the button

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if check_credentials(username_box,password_box) == False:
                        submit_credentials(username_box.text, password_box.text)
                    elif check_credentials(username_box,password_box) == True:
                        running = False
            for box in input_boxes:
                box.handle_event(event)
            button.handle_event(event)  # Handle events for the button


Char = CharNovaZakuII( 50, 50, Player1)
# boss.add(Char)
bossSpawn = False
def death_screen():
    running = True
    selected = 1
    space_pressed = False
    while running:

        screen.blit(dth_img, (-100, 0))
        draw_text(menu_font, 'press esc to go back to menu', 400, 750)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not space_pressed:
                    running = False
                    menu(Player1)
                    running = False
                    space_pressed = True
        pygame.display.flip()
        clock.tick(60)


    pygame.quit()
    exit()
def game(P1=Player1):
    Player1 = P1
    PlayerBullets = pygame.sprite.Group()
    score = 0
    done = False
    Char = CharNovaZakuII(50, 50,Player1)
    bossSpawn = False
    DASH_COOLDOWN = 5000
    last_dash_time = pygame.time.get_ticks()
    while not done:
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if current_time - last_dash_time >= DASH_COOLDOWN:
            dash_active = True
            draw_text(menu_font, "DASH ACTIVE", 700, 400)
        else:
            dash_active = False
        text_surface = my_font.render(str(score), False, WHITE)
        scoreRect=text_surface.get_rect()
        scoreRect.center=(600,15)
        if keys[pygame.K_w] and Player1.rect.y>0:  # w
            if dash_active and keys[pygame.K_LSHIFT]:
                Player1.rect.y -= 100
                last_dash_time = pygame.time.get_ticks()
            else:
                Player1.rect.y -= 5
        if keys[pygame.K_s] and Player1.rect.y<725:  # w
            if dash_active and keys[pygame.K_LSHIFT]:
                Player1.rect.y += 100
                last_dash_time = pygame.time.get_ticks()
            else:
                Player1.rect.y += 5
        if keys[pygame.K_a] and Player1.rect.x>5:  # w
            if dash_active and keys[pygame.K_LSHIFT]:
                Player1.rect.x -= 100
                last_dash_time = pygame.time.get_ticks()
            else:
                Player1.rect.x -= 5
        if keys[pygame.K_d] and Player1.rect.x<735:  # w
            if dash_active and keys[pygame.K_LSHIFT]:
                Player1.rect.x += 100
                last_dash_time = pygame.time.get_ticks()
            else:
                Player1.rect.x += 5
        if keys[pygame.K_e] and len(swordslash) == 0: #and swordE.energy == 4:
            if (Player1.type == "VG"):
                temp1 = Fin (Player1.rect.x - 25, Player1.rect.y, Player1)
                temp2 = Fin(Player1.rect.x + 35, Player1.rect.y,Player1)
                swordslash.add (temp1)
                swordslash.add (temp2)
            else:
                ss = Swordswing(Player1.rect.x-20, Player1.rect.y - 10)
                swordslash.add(ss)
            swordE.energy = 0
        if keys[pygame.K_1]:
            if len(enemies)<1:
                e = sqaudren("Zaku", 2, enemies)
        if keys[pygame.K_2]:
            if len(enemies) < 1:
                g = Gouf(random.randint(50, 600), -50, enemyBullets)
                enemies.add(g)
        if keys[pygame.K_3]:
            if len(boss) <1:
                Char = CharNovaZakuII(50, 50, Player1)
                boss.add(Char)
                bossSpawn = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == 32:
                    if len(PlayerBullets) < 5:  # spacebar
                        shoot_sfx.play()
                        Player1.shoot(PlayerBullets)
                    if swordslash.__len__()>1 and Player1.type=="VG" and len(PlayerBullets)< 10:
                        temp1.shoot(PlayerBullets)
                        temp2.shoot(PlayerBullets)
        for b in PlayerBullets:
            for e in enemies:
                if pygame.sprite.collide_rect(b,e):
                    if isinstance(e, gelgoog) and e.stun:
                        e.health -= 100
                        if (e.health <= 0):
                            death_sfx.play()
                            tempx = e.rect.x
                            ex = explosion(tempx, e.rect.y)
                            e.kill()
                            explosions.add(ex)
                            score += e.score
                        b.kill()
                        break
                    elif isinstance(e,gelgoog) and e.stun == False:
                        b.kill()
                        e.shield-=1
                    else:
                        e.health -=100
                        b.kill()
                        if (e.health <= 0):
                            #death_sfx.play()
                            tempx = e.rect.x
                            ex = explosion(tempx, e.rect.y)
                            e.kill()
                            explosions.add(ex)
                            score += e.score
                        break
        for s in swordslash:
            for b in enemyBullets:
                if pygame.sprite.collide_rect(b,s):
                    b.kill()
            for e in enemies:
                if pygame.sprite.collide_rect(s, e):
                    #death_sfx.play()
                    tempx = e.rect.x
                    ex = explosion(tempx, e.rect.y)
                    e.kill()
                    explosions.add(ex)
                    score += 10
        screen.fill(BLACK)
        screen.blit(bkg_img, background.sprite)
        background.draw(screen)
        explosions.draw(screen)
        explosions.update()
        bullets.draw(screen)
        bullets.update()
        PlayerBullets.draw(screen)
        PlayerBullets.update()
        swordslash.draw(screen)
        swordslash.update()
        enemyBullets.draw(screen)
        enemyBullets.update()
        enviromental_sprites.draw(screen)
        enviromental_sprites.update()
        SE.draw(screen)
        SE.update()

        if swordslash.__len__()>1:
            temp1.rect.y = Player1.rect.y
            temp2.rect.y = Player1.rect.y
            print (pygame.time.get_ticks()-temp1.starttimer)
            if temp1.rect.x != Player1.rect.x - 45:
                temp1.rect.x = Player1.rect.x - 45
            if temp2.rect.x != Player1.rect.x + 50:
                temp2.rect.x = Player1.rect.x + 50
            if pygame.time.get_ticks() - temp1.starttimer > 4999:
                temp1.kill()
            if pygame.time.get_ticks() - temp2.starttimer > 4999:
                temp2.kill()
        starsG.draw(screen)
        starsG.update()
        for b in PlayerBullets:
            b.update()
            if Char.shieldActive and pygame.sprite.collide_rect(Char.shield, b):
                b.kill()
                Char.shield.health -=1
                if Char.shield.health ==0:
                    Char.shield.kill()
            elif not Char.shieldActive and pygame.sprite.collide_rect(Char, b):
                Char.health -= 5
                b.kill()
        for s in swordslash:
            if s.rect.y < 0:
                s.kill()
        for b in enemyBullets:
            b.update()
            if pygame.sprite.collide_rect(b,Player1):
                Player1.health-=5
                b.kill()
        for e in enemies:
            if (random.randint(1,100)<2):
                spawnx = e.rect.x+15
                if isinstance(e, gelgoog):
                    b = CresentShot(spawnx, e.rect.y, Player1)
                    enemyBullets.add(b)
                if isinstance(e, Gouf):
                    pass
                else:
                    b = EnemyBullet(spawnx, e.rect.y+25)
                    enemyBullets.add(b)
        if bossSpawn:
            for a in Char.abilgroup:
                if pygame.sprite.collide_rect(a, Player1):
                    Player1.health -= a.damage
                    a.kill()
        enemies.draw(screen)
        healthB.health = Player1.health
        health_percent = Player1.health * 100 // 300
        enemies.update()
        tempRect = Player_img.get_rect()
        tempRect.center = 200, 200
        Player1.draw(screen)
        Player1.update()
        thr.update()
        boss.update()
        boss.draw(screen)
        if Char.health <= 0:
            Char.abilgroup.empty()
            Char.kill()
        Char.abilgroup.draw(screen)
        thr.draw(screen)
        screen.blit(HUD_img, HUD.sprite)
        HUD.draw(screen)
        screen.blit(text_surface, scoreRect)
        if (health_percent < 30):
            screen.blit(crack, crackbkg.sprite)
        if health_percent <= 0:
            Player1.kill()
            enemies.empty()
            bullets.empty()
            boss.empty()
            menu(Player1)
        draw_text(hud_font, 'Ability', 55, 700)
        draw_text(hud_font, 'AP:'+health_percent.__str__()+"%", 75, 750)
        if boss.__len__()>0:
            draw_text(hud_font, 'Chars AP:' + Char.health.__str__(), 75, 100)
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)
        print (screen.get_rect())
    pygame.quit()
    exit()
print (Player1.type)
death_screen()
