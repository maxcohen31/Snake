### SNAKE GAME MADE USING PYGAME LIBRARY ###
# Inspired by: cyysu
# Modified by: maxcohen31 (Emanuele) 


import pygame
import sys
import time
from copy import deepcopy
import random
from math import sqrt
from pygame import mixer


class Apple:
    def __init__(self):
        self.fruit_x = random.randint(10, 590) # X coordinate
        self.fruit_y = random.randint(10, 590) # Y coordinate
    
    def position(self):
        return [self.fruit_x, self.fruit_y]  # Return a list of coordinates
    
    def draw_apple(self):
        # Initialize the points and return them
        self.fruit_x = random.randint(10, 590)
        self.fruit_y = random.randint(10, 590)
        return self.position() 
    
class Snake:
    def __init__(self):
        self.body = [[15, 15], [14, 15], [13, 15]] # Snake body
        self.sound = pygame.mixer.init()
        self.bite = pygame.mixer.Sound('Bite.wav')
        
    def snake_position(self):
        return self.body # Return the position of the snake   
    
    def movement(self, direction):
        pos = len(self.body) - 1 # Start position

        while pos > 0:
            self.body[pos] = deepcopy(self.body[pos-1])
            pos -= 1
        
        # Up movement
        if direction == 'UP': 
            self.body[pos][1] -= 10
            if self.body[pos][1] < 0:
                self.body[pos][1] = 600
                
        # Right movement        
        if direction == 'RIGHT':
            self.body[pos][0] += 10
            if self.body[pos][0] > 600:
                self.body[pos][0] = 0
                
        # Left movement
        if direction == 'LEFT':
            self.body[pos][0] -= 10
            if self.body[pos][0] < 0:
                self.body[pos][0] = 600 
        
        # Down movement
        if  direction == 'DOWN':
            self.body[pos][1] += 10
            if self.body[pos][1] > 600:
                self.body[pos][1] = 0                      
    
    # Method to draw the snake body             
    def draw_snake(self): 
        snake_points = []
        for point in self.body:
            snake_points.append(pygame.draw.circle(screen, (0, 255, 0), point, 5, 0))

    # Method that allows the snake to eat the apple  
    def eating_apple(self, apple_pos):
        self.body.append(apple_pos)   
        
    # Setting game boundaries    
    def boundaries(self):
        if self.body[0][1] == 600:
            score.game_over()
        if self.body[0][0] == 0:
            score.game_over()  
        if self.body[0][1] == 0:
            score.game_over()
        if self.body[0][0] == 600:
            score.game_over()
    
    # Check if the snake collide with the apple
    # to do that i used the formula to calculate
    # the distance between two points         
    def check_collision_and_new_body(self):
        pos_apple_x = apple.position()[0]
        pos_apple_y = apple.position()[1]
        collision = sqrt(pow(self.body[0][0] - pos_apple_x, 2) + (pow(self.body[0][1] - pos_apple_y, 2)))
        if collision < 15:
            apple.draw_apple() # Spawning another apple
            self.body.append(apple.position()) # Add a new part
            self.bite.play() 

    # Snake eats itself then game over
    def snake_collision(self):
        for part in self.body[1:]:
            if self.body[0][0] == part[0] and self.body[0][1] == part[1]:
                score.game_over()


class Score:
    def __init__(self):
        pygame.font.init()
        
    def game_over(self):
        screen.fill((255,255,255))
        selected_font = pygame.font.SysFont("times new roman", 80)
        wasted = selected_font.render("WASTED!", True, (255, 0, 0))
        wasted_rect = wasted.get_rect()
        wasted_rect.centerx = screen.get_rect().centerx
        wasted_rect.centery = screen.get_rect().centery - 10
        screen.blit(wasted, wasted_rect) 
        pygame.display.flip()
        time.sleep(2)
        sys.exit()
     
    def show_score(self):
        initial_score = len(snake.body) - 3
        score_font = pygame.font.SysFont("bold", 20)
        score_surface = score_font.render(f"Score: {initial_score}", True, (255, 255, 255))
        score_rect = screen.get_rect()
        screen.blit(score_surface, score_rect)
        pygame.display.flip()
        
# Objects               
apple = Apple()
snake = Snake()
score = Score()

# Settings
pygame.init()
pygame.display.set_caption('Snake')
icon = pygame.image.load('snake.png')
get_icon = pygame.display.set_icon(icon)
clock = pygame.time.Clock() 
screen  = pygame.display.set_mode((600,600), 0, 32)  
mixer.music.load("Main_theme.wav")
mixer.music.play(-1)

# Movement triggers
moving_up = False
moving_right = True
moving_down = False
moving_left = False
start = True
snake.movement('RIGHT')     
game = True

# Main 
while game:  
    screen.fill((0,0,0))   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit() 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                moving_up = True
                moving_right = False
                moving_down = False
                moving_left = False
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                moving_up = False 
                moving_right = False
                moving_down = True
                moving_left = False
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                moving_up = False 
                moving_right = False
                moving_down = False
                moving_left = True     
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                moving_up = False 
                moving_right = True
                moving_down = False
                moving_left = False  
                
    moving_time = clock.tick(25) # Movement time
    if moving_up:               
        snake.movement('UP')    # Snake goes up
    if moving_right:
        snake.movement('RIGHT') # Snake goes right
    if moving_down:
        snake.movement('DOWN') # Snake goes down
    if moving_left:
        snake.movement('LEFT') # Snake goes left
                               
    apple_pos = apple.position()
    fruit_display = pygame.draw.circle(screen, (255, 0, 0), apple_pos, 10) # Draw the apple  
    snake.draw_snake() # Draw the snake
    snake.boundaries() # Set boundaries
    snake.check_collision_and_new_body() # Collision
    snake.snake_collision() # Snake collision
    score.show_score() # Show score
    pygame.display.update()
