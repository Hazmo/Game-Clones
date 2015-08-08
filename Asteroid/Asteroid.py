import pygame
import sys

SCREEN = pygame.display.set_mode([800, 600])

black = (  0,   0,   0)
white = (255, 255, 255)
red   = (255,   0,   0)
green = (0,   255,   0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([15, 10])
        self.original_image = self.image
        self.image.fill(white)
        self.rect = self.image.get_rect(topleft=(395, 295))
        self.rotationAngle = 0
        
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            print "yes"
            self.rotationAngle += 1
        if keys[pygame.K_RIGHT]:
            self.rotationAngle -= 1
            
        self.image = pygame.transform.rotate(self.original_image, self.rotationAngle)
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

class Asteroid:
    def __init__(self):
        self.screen = SCREEN
        
        self.reset()
        
    def reset(self):
        self.clock = pygame.time.Clock()
        self.gameOver = False
        self.enemies = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.keys = pygame.key.get_pressed()
        
        self.player = Player()
        self.players.add(self.player)
        self.all_sprites.add(self.player)
        
    def check_input(self):
        self.keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        
    def main(self):
        while True:
            if not self.gameOver:
                self.screen.fill(black)
                
                self.all_sprites.update(self.keys)
                self.all_sprites.draw(self.screen)
                
                self.check_input()
                
            pygame.display.update()
            self.clock.tick(60)
if __name__ == "__main__":
    asteroid = Asteroid()
    asteroid.main()