import pygame
import math
import sys
import random


black = (  0,   0,   0)
white = (255, 255, 255)
red   = (255,   0,   0)
green = (0,   255,   0)

SCREEN = pygame.display.set_mode([800, 600])

class Enemy(pygame.sprite.Sprite):
    def __init__(self, size, xPos, yPos, speed, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([size,size])
        self.image.fill(green)
        self.size = size
        self.rect = self.image.get_rect(topleft=(xPos, yPos))
        self.speed = speed
        self.direction = direction
                
    def update(self):
		if self.direction == 0:
			self.rect.x += self.speed
			if self.rect.x > 800:
				self.kill()
                
		elif self.direction == 1:
			self.rect.y += self.speed
			if self.rect.y > 600:
				self.kill()
                
		elif self.direction == 2:
			self.rect.x -= self.speed
			if self.rect.x < 0 - self.size:
				self.kill()
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([15, 15])
        self.image.fill(red)
        self.rect = self.image.get_rect(topleft=(390, 500))
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
  

class Text(object):
	def __init__(self, size, message, color, xpos, ypos, textFont=None):
		self.font = pygame.font.Font(textFont, size)
		self.surface = self.font.render(message, True, color)
		self.rect = self.surface.get_rect(topleft=(xpos, ypos))

	def draw(self, surface):
		surface.blit(self.surface, self.rect)
        
class Dodger(object):
    def __init__(self):
        pygame.init()
        self.screen = SCREEN
        
        pygame.mouse.set_visible(False)
        self.reset()
        
    def reset(self):
        self.clock = pygame.time.Clock()
        self.enemies = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.players.add(self.player)
        self.all_sprites.add(self.player)
        self.enemySpawnTimer = pygame.time.get_ticks()
        self.score = 0
        self.scoreText = Text(30, "Score:", white, 0, 0)
        self.actualScoreText = Text(30, str(self.score), white, 50, 0)
        self.scoreText.draw(self.screen)
        self.actualScoreText.draw(self.screen)
        self.gameOver = False
        
    def spawn_enemies(self):
        if (pygame.time.get_ticks() - self.enemySpawnTimer) >= 100:
            enemySize = random.randint(20, 70)
            enemyDirection = random.randint(0, 2)

            if enemyDirection == 0:
                print 1
                xPos = -enemySize
                yPos = random.randint(0, 600 - enemySize)
            elif enemyDirection == 1:
                print 2
                xPos = random.randint(0,  800 - enemySize)
                yPos = 0
            elif enemyDirection == 2:
                print 3
                xPos = 800
                yPos = random.randint(0, 600 - enemySize)
				
            enemySpeed = random.randint(5, 8)
			
            
            #print enemySize, " ", xPos
            
            newEnemy = Enemy(enemySize, xPos, yPos,enemySpeed, enemyDirection)
            self.enemies.add(newEnemy)
            self.all_sprites.add(newEnemy)
            
            self.enemySpawnTimer = pygame.time.get_ticks()
    def update_score(self):
        self.scoreText.draw(self.screen)
        self.actualScoreText = Text(30, str(self.score), white, 70, 0)
        self.actualScoreText.draw(self.screen)
        self.score += 1
        
    def check_collisions(self):
        if pygame.sprite.groupcollide(self.enemies, self.players, False, False):
            self.gameOver = True
    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if self.gameOver == True:
                if event.type == pygame.KEYUP:
                    self.reset()
                 
    def main(self):
        while True:
            if not self.gameOver:
                self.screen.fill(black)
                
                self.update_score()
                self.all_sprites.update()
                self.spawn_enemies()
                
                self.check_collisions()
                
                self.all_sprites.draw(self.screen)
                self.check_input()
            if self.gameOver:
                self.gameOverText = Text(50, "Game Over", white, 290, 289)
                self.gameOverText.draw(self.screen)
                self.check_input()
            
            pygame.display.update()
            self.clock.tick(60)
            
if __name__ == '__main__':
    dodger = Dodger()
    dodger.main()