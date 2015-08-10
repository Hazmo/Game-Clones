import pygame
import sys
import math
SCREEN = pygame.display.set_mode([800, 600])

IMG_NAMES = ["ship", "square", "bullet"]
IMAGES 	= {name: pygame.image.load("images/{}.png".format(name)).convert_alpha()
				for name in IMG_NAMES}

black = (  0,   0,   0)
white = (255, 255, 255)
red   = (255,   0,   0)
green = (0,   255,   0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["square"]
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(400, 600))
        self.rotationAngle = 0
        self.rotateSpeed = 3
        self.speed = 0.1
        
        self.velX = 0
        self.velY = 0
        
        self.x = 400
        self.y = 600
        
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rotationAngle += self.rotateSpeed
            self.image = pygame.transform.rotate(self.original_image, self.rotationAngle)
            self.rect = self.image.get_rect(center=(self.rect.center))
        if keys[pygame.K_RIGHT]:
            self.rotationAngle -= self.rotateSpeed
            self.image = pygame.transform.rotate(self.original_image, self.rotationAngle)
            self.rect = self.image.get_rect(center=(self.rect.center))
        if keys[pygame.K_UP]:
            self.rotationAngleRadians = math.radians(self.rotationAngle)
            self.velX += math.sin(self.rotationAngleRadians) * self.speed
            self.velY += math.cos(self.rotationAngleRadians) * self.speed
            
        self.velX *= 0.98
        self.velY *= 0.98
        
        self.x -= self.velX
        self.y -= self.velY
        
        if self.x > 800:
            self.x = 0 - self.rect.width
        elif self.x < 0 - self.rect.width:
            self.x = 800
              
        if self.y > 600:
            self.y = 0 - self.rect.height
        elif self.y < 0 - self.rect.height:
            self.y = 600
        
        if self.rotationAngle > 360:
            self.rotationAngle = 0
        elif self.rotationAngle < 0:
            self.rotationAngle = 360
            
            
        self.rect.centerx = self.x
        self.rect.centery = self.y
        
        asteroid.screen.blit(self.image, self.rect)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, rotationAngle):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["bullet"]
        self.image = pygame.transform.rotate(self.image, rotationAngle)
        self.rect = self.image.get_rect(center=(xPos, yPos))
        self.rotationAngleRadians = math.radians(rotationAngle)
        self.speed = 6
    def update(self, *args):
        self.rect.x -= math.sin(self.rotationAngleRadians) * speed
        self.rect.y -= math.coz(self.rotationAngleRadians) * speed
        

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    continue
        
        
    def main(self):
        while True:
            if not self.gameOver:
            
            
                self.check_input()
                self.screen.fill(black)
                
                self.all_sprites.update(self.keys)
                
                self.all_sprites.draw(self.screen)
                
                
                
            pygame.display.update()
            self.clock.tick(60)
if __name__ == "__main__":
    asteroid = Asteroid()
    asteroid.main()