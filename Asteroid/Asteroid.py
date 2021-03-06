import pygame
import sys
import math
import random
SCREEN = pygame.display.set_mode([800, 600])

IMG_NAMES = ["ship", "bullet", "asteroid"]
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
        self.image = IMAGES["ship"]
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(400, 300))
        self.mask = pygame.mask.from_surface(self.image)
        self.rotationAngle = 0
        self.rotateSpeed = 3
        self.speed = 0.1
        
        self.velX = 0
        self.velY = 0
        
        self.x = 400
        self.y = 300
        
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
        
        self.mask = pygame.mask.from_surface(self.image)
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, rotationAngle):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["bullet"]
        self.image = pygame.transform.rotate(self.image, rotationAngle)
        self.mask = pygame.mask.from_surface(self.image)
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
    def __init__(self, size, posX, posY, directionAngle, speed, rotationSpeed, generation):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = IMAGES["asteroid"]
        self.size = size
        self.original_image = pygame.transform.scale(self.original_image, (size, size))
        self.image = self.original_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(posX, posY))
        self.speed = speed
        self.rotationSpeed = rotationSpeed
        self.directionAngleRadians = math.radians(directionAngle)
        self.generation = generation
        self.rotation = 0
        #represents the middle of the asteroid
        self.x = posX + size
        self.y = posY + size
    def update(self, *args):
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=(self.rect.center))
        self.rotation += self.rotationSpeed
        self.x -= math.sin(self.directionAngleRadians) * self.speed
        self.y -= math.cos(self.directionAngleRadians) * self.speed
        
        
        if self.x > 830 + self.rect.width:
            self.x = 0 - self.rect.width
        elif self.x < -30 - self.rect.width:
            self.x = 800 + self.rect.width
              
        if self.y > 630 + self.rect.height:
            self.y = 0 - self.rect.height
        elif self.y < -30 - self.rect.height:
            self.y = 600 + self.rect.height
            
        self.rect.centerx = self.x
        self.rect.centery = self.y
            
        self.mask = pygame.mask.from_surface(self.image)
        
        
class Text(object):
	def __init__(self, size, message, color, xpos, ypos, textFont=None):
		self.font = pygame.font.Font(textFont, size)
		self.surface = self.font.render(message, True, color)
		self.rect = self.surface.get_rect(topleft=(xpos, ypos))

	def draw(self, surface):
		surface.blit(self.surface, self.rect)
        
        

class AsteroidGame:
    def __init__(self):
        pygame.init()
        self.screen = SCREEN
        
        self.highScore = 0
        
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
        self.score = 0
        self.scoreText = Text(23, "Score:", white, 0, 0)
        self.scoreText.draw(self.screen)
        self.highScoreText = Text(23, "High Score:", white, 650, 0)  
        self.actualHighScoreText = Text(23, str(self.highScore), white, 740, 1)
        
        self.asteroidSpawnTimer = pygame.time.get_ticks()
        self.bulletTime = pygame.time.get_ticks()
        
        
        
    def check_input(self):
        self.keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.gameOver:
                    self.reset()
                else:
                    if event.key == pygame.K_SPACE:
                        if (pygame.time.get_ticks() - self.bulletTime) >= 300:
                            bullet = Bullet(self.player.x, self.player.y, self.player.rotationAngle)
                            self.bullets.add(bullet)
                            self.all_sprites.add(bullet)
                            self.bulletTime = pygame.time.get_ticks()
                    
    def check_collisions(self):
    
        bullet_asteroid_collision = pygame.sprite.groupcollide(self.bullets, self.asteroids, True, False, pygame.sprite.collide_mask)
        #bullet hitting asteroid
        if bullet_asteroid_collision:
            shot_asteroid = bullet_asteroid_collision.itervalues().next()[0]
            shot_asteroid.kill()
            self.update_score(shot_asteroid)
            if shot_asteroid.generation < 2:
            
                newSize = int(shot_asteroid.size * (0.7 ** shot_asteroid.generation))
                newDirectionAngle1 = random.randint(0, 360)
                newDirectionAngle2 = (newDirectionAngle1 + 180) % 360
                newSpeed = shot_asteroid.speed
                newGeneration = shot_asteroid.generation + 1
                
                newAsteroid1 = Asteroid(newSize,shot_asteroid.x, shot_asteroid.y, newDirectionAngle1, newSpeed, shot_asteroid.rotationSpeed, newGeneration)
                newAsteroid2 = Asteroid(newSize, shot_asteroid.x, shot_asteroid.y, newDirectionAngle2, newSpeed, shot_asteroid.rotationSpeed, newGeneration)
            
                newAsteroid1.add(self.asteroids, self.all_sprites)
                newAsteroid2.add(self.asteroids, self.all_sprites)
                   
        #player hitting asteroid
        player_asteroid_collision = pygame.sprite.spritecollideany(self.player, self.asteroids, pygame.sprite.collide_mask)
        if player_asteroid_collision is not None:
            self.gameOver = True
    def draw_text(self):
        self.scoreText.draw(self.screen)
        self.highScoreText.draw(self.screen)
        self.actualHighScoreText.draw(self.screen)
        self.actualScoreText = Text(23, str(self.score), white, 52, 1)
        self.actualScoreText.draw(self.screen)
        
        
    def update_score(self, asteroid):
        generation = asteroid.generation
        self.score += 10 * generation
        
    def spawn_asteroids(self):
        if(pygame.time.get_ticks() - self.asteroidSpawnTimer) >= 1000 and len(self.asteroids) < 5:
            size = random.randint(35, 60)
            
            randomAngles = [random.randint(51, 140), random.randint(141, 230), random.randint(231, 320), random.choice([random.randint(321, 360), random.randint(0, 50)])]
            directionAngle = random.choice(randomAngles)
            
                
            #right    
            if directionAngle >= 231 and directionAngle <= 320:
                xPos = 0 - size
                yPos = random.randint(200, 400)
            #down
            elif directionAngle >= 141 and directionAngle <= 230:
                xPos = random.randint(300, 500)
                yPos = 0 - size
            #left
            elif directionAngle >= 51 and directionAngle <= 140:
                xPos = 800 + size
                yPos = random.randint(200, 400)
            #up
            elif directionAngle >= 321 and directionAngle <= 360 or directionAngle >= 0 and directionAngle <= 50:
                xPos = random.randint(200, 500)
                yPos = 600 + size
            
                    
            speed = random.randint(2, 4)
            rotationSpeed = random.randint(1, 4)
            
            
            asteroid = Asteroid(size, xPos, yPos, directionAngle, speed, rotationSpeed, 1)
            self.asteroids.add(asteroid)
            self.all_sprites.add(asteroid)
               
            self.asteroidSpawnTimer = pygame.time.get_ticks()
            
            
    def main(self):
        while True:
            if not self.gameOver:
            
            
                self.check_input()
                self.screen.fill(black)
                
                self.spawn_asteroids()
                self.check_collisions()
                self.all_sprites.update(self.keys)
                
                self.all_sprites.draw(self.screen)
                self.draw_text()
            if self.gameOver:
                if self.score > self.highScore:
                    self.highScore = self.score
                self.gameOverText = Text(50, "Game Over", white, 290, 289)
                self.gameOverText.draw(self.screen)
                self.check_input()
                
               
            pygame.display.update()
            self.clock.tick(60)
if __name__ == "__main__":
    asteroid = AsteroidGame()
    asteroid.main()