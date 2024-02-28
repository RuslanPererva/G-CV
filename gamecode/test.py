import pygame
import random


class CharNovaZakuII(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 50, 50)
        self.firerate = 0
        self.burst_count = 0
        self.burst_delay = 10  # Adjust as needed
        self.burst_timer = 0
        self.bullets = pygame.sprite.Group()

    def update(self):
        # Update the firing rate
        if self.firerate > 0:
            self.firerate -= 1

        # Update the burst timer
        if self.burst_timer > 0:
            self.burst_timer -= 1

        # Check if it's time to start a burst
        if self.firerate == 0 and self.burst_timer == 0:
            self.start_burst()

        # Update bullets
        self.bullets.update()

    def start_burst(self):
        # Set burst parameters
        self.burst_count = 3  # Number of bullets per burst
        self.burst_timer = 60  # Duration of burst in frames (adjust as needed)

    def activate_machine_gun(self):
        # Fire bullets during burst
        if self.burst_count > 0:
            bullet = Bullet(self.rect.x + random.randint(0, 50), self.rect.y + random.randint(0, 50))
            self.bullets.add(bullet)
            self.burst_count -= 1

        # Reset firing rate after burst delay
        if self.burst_count == 0:
            self.firerate = self.burst_delay


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 255))  # White color for bullet
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5  # Adjust bullet speed as needed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 800:  # Screen width, adjust as needed
            self.kill()  # Remove the bullet when it goes off-screen


# Example usage:
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player = CharNovaZakuII(100, 300)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()