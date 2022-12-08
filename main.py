import pygame
from random import randint

width = 400
height = 300
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('RogueLike')

screen.fill((255, 255, 255))

clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 150)
        self.speed = 5

    def update(self):

        self.rect.clamp_ip(screen.get_rect())
        keys = pygame.key.get_pressed()
        movements = {
            pygame.K_LEFT: (-self.speed, 0),
            pygame.K_RIGHT: (self.speed, 0),
            pygame.K_UP: (0, -self.speed),
            pygame.K_DOWN: (0, self.speed),
        }

        for key, (dx, dy) in movements.items():
            if keys[key]:
                self.rect.x += dx
                self.rect.y += dy


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 200)

    def get_random_position(self):
        x = randint(0, width)
        y = randint(0, height)
        self.rect.center = (x, y)


SPAWN_RATE = 1
last_spawn_time = 0
sec = 1000

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
point_counter: int = 0
coins = []

running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    all_sprites.update()
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > SPAWN_RATE * sec:
        coin = Coin()
        coin.get_random_position()
        all_sprites.add(coin)
        last_spawn_time = current_time
        coins.append(coin)

    for coin in coins:
        if player.rect.colliderect(coin.rect):
            coins.remove(coin)
            all_sprites.remove(coin)
            point_counter += 1

    font = pygame.font.Font(None, 36)
    text = font.render(f"Punkty: {point_counter}", True, (0, 0, 0))

    screen.fill((255, 255, 255))
    screen.blit(text, (10, 10))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)
