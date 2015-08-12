import pygame
import sys
import math
import random
SCREEN = pygame.display.set_mode([800, 600])

IMG_NAMES = ["ship", "square", "bullet"]
IMAGES 	= {name: pygame.image.load("images/{}.png".format(name)).convert_alpha()
				for name in IMG_NAMES}

black = (  0,   0,   0)
white = (255, 255, 255)
red   = (255,   0,   0)
green = (0,   255,   0)
grey  = (128, 128, 128)

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
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, rotationAngle):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["bullet"]
        self.image = pygame.transform.rotate(self.image, rotationAngle)
        self.rect = self.image.get_rect(center=(xPos, yPos))
        self.rotationAngleRadians = math.radians(rotationAngle)
        self.speed = 9
        self.aliveTimer = pygame.time.get_ticks()
        
    def update(self, *args):
        if (pygame.time.get_ticks() - self.aliveTimer) >= 1800:
            self.kill()
        self.rect.x -= math.sin(self.rotationAngleRadians) * self.speed
        self.rect.y -= math.cos(self.rotationAngleRadians) * self.speed
        
        if self.rect.x > 800:
            self.rect.x = 0 - self.rect.width
        elif self.rect.x < 0 - self.rect.width:
            self.rect.x = 800
              
        if self.rect.y > 600:
            self.rect.y = 0 - self.rect.height
        elif self.rect.y < 0 - self.rect.height:
            self.rect.y = 600
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, size, posX, posY, directionAngle, speed, rotationSpeed):
        pygame.sprite.Sprite.__init__(self)
        #TODO make it spawn on outskirts of map
        self.original_image = pygame.Surface([size, size])
        self.image = self.original_image
        self.image.fill(grey)
        self.rect = self.image.get_rect(topleft=(posX, posY))
        self.speed = speed
        self.rotationSpeed = rotationSpeed
        self.directionAngleRadians = math.radians(directionAngle)
        self.rotation = 0
        #TODO
        #set random rotation, set random speed and direction, make update keep it spinning.
    def update(self, *args):
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=(self.rect.center))
        self.rotation += self.rotationSpeed
        self.rect.x -= math.sin(self.directionAngleRadians) * self.speed
        self.rect.y -= math.cos(self.directionAngleRadians) * self.speed
        
        

class AsteroidGame:
    def __init__(self):
        self.screen = SCREEN
        
        self.reset()
        
    def reset(self):
        self.clock = pygame.time.Clock()
        self.gameOver = False
        self.asteroids = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.keys = pygame.key.get_pressed()
        
        self.player = Player()
        self.players.add(self.player)
        self.all_sprites.add(self.player)
        
        self.asteroidSpawnTimer = pygame.time.get_ticks()
        
    def check_input(self):
        self.keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(self.player.x, self.player.y, self.player.rotationAngle)
                    self.bullets.add(bullet)
                    self.all_sprites.add(bullet)
    
    def spawn_asteroids(self):
        if(pygame.time.get_ticks() - self.asteroidSpawnTimer) >= 3:
            size = random.randint(5, 20)
            directionAngle = random.randint(0, 359)
            
            excludedAngles = [0, 90, 180, 270]
            
            if directionAngle in excludedAngles:
                directionAngle += random.randint(20, 70)
            
            
            #moving up-right
            if directionAngle >= 0 and directionAngle < 90:
                xPos = random.choice([800 + size, random.randint(100 + size, 700)])
                if xPos < 800:
                    yPos = 0 - size
                else:
                    yPos = random.randint(100 + size, 500)
            #down-right       
            elif directionAngle >= 90 and directionAngle < 180:
                xPos = random.choice([800 + size, random.randint(100 + size, 700)])
                if xPos < 800:
                    yPos = 600 + size
                else:
                    yPos = random.randint(100 + size, 500)
                    
            #down-left
            elif directionAngle >= 180 and directionAngle < 270:
                xPos = random.choice([0 - size, random.randint(100 + size, 700)])
                if xPos > 0:
                    yPos = 600 + size
                else:
                    yPos = random.randint(100 + size, 500)
            #up-left
            elif directionAngle >= 270 and directionAngle < 360:
                xPos = random.choice([0 - size, random.randint(100 + size, 700)])
                if xPos > 0:
                    yPos = 0 - size
                else:
                    yPos = random.randint(100 + size, 500)
                    
            speed = random.randint(2, 6)
            rotationSpeed = random.randint(1, 4)
            
            print directionAngle
            
            asteroid = Asteroid(size, xPos, yPos, directionAngle, speed, rotationSpeed)
            self.asteroids.add(asteroid)
            self.all_sprites.add(asteroid)
                
                
                
        
    def main(self):
        while True:
            if not self.gameOver:
            
            
                self.check_input()
                self.screen.fill(black)
                
                self.spawn_asteroids()
                self.all_sprites.update(self.keys)
                
                self.all_sprites.draw(self.screen)
                
               
            pygame.display.update()
            self.clock.tick(60)
if __name__ == "__main__":
    asteroid = AsteroidGame()
    asteroid.main()