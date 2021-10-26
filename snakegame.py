"""The video used for writing this code initially is https://www.youtube.com/watch?v=QFvqStqPCRU&t"""

import pygame, sys, random
from pygame.math import Vector2


#Creating the snake by writing a class
class SNAKE:
    def __init__(self):
        
        self.body = [Vector2(5,7), Vector2(4,7), Vector2(3,7)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up =  pygame.image.load('Graphics/headup.png').convert_alpha()
        self.head_down =  pygame.image.load('Graphics/headdown.png').convert_alpha()
        self.head_left =  pygame.image.load('Graphics/headleft.png').convert_alpha()
        self.head_right =  pygame.image.load('Graphics/headright.png').convert_alpha()

        self.tail_up =  pygame.image.load('Graphics/tailup.png').convert_alpha()
        self.tail_down =  pygame.image.load('Graphics/taildown.png').convert_alpha()
        self.tail_left =  pygame.image.load('Graphics/tailleft.png').convert_alpha()
        self.tail_right =  pygame.image.load('Graphics/tailright.png').convert_alpha()

        self.body_vertical =  pygame.image.load('Graphics/bodyvertical.png').convert_alpha()
        self.body_horizontal =  pygame.image.load('Graphics/bodyhorizontal.png').convert_alpha()

        self.body_tr =  pygame.image.load('Graphics/tr.png').convert_alpha()
        self.body_tl =  pygame.image.load('Graphics/tl.png').convert_alpha()
        self.body_br =  pygame.image.load('Graphics/br.png').convert_alpha()
        self.body_bl =  pygame.image.load('Graphics/bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
        

    def draw_snake(self):

        self.update_head_graphics()
        self.update_tail_graphics()
        
        for index, block in enumerate(self.body):
            x_pos = int((block.x * cell_size)+side_border)
            y_pos = int((block.y * cell_size)+top_border)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)

            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)

            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)

                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)

                else:
                    if previous_block.x == -1 and  next_block.y == -1 or previous_block.y == -1 and next_block.x ==-1:
                        screen.blit(self.body_tl, block_rect)
                    if previous_block.x == -1 and  next_block.y == 1 or previous_block.y == 1 and next_block.x ==-1:
                        screen.blit(self.body_bl, block_rect)
                    if previous_block.x == 1 and  next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    if previous_block.x == 1 and  next_block.y == 1 or previous_block.y == 1 and next_block.x ==1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-1] - self.body[-2]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down


    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,7), Vector2(4,7), Vector2(3,7)]
        self.direction = Vector2(0,0)

#Creating the fruit by writing a class
class FRUIT:
    
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int((self.pos.x * cell_size)+side_border), int((self.pos.y * cell_size)+top_border), cell_size, cell_size)
        screen.blit(orange, fruit_rect)
        #pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

#Class if which the main logic of our game will be written like eating the fruit, etc.
class MAIN:
    
    def __init__(self, hs):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.hs = hs

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):

        #to check if the snake is moving out of the block
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        #to check if the snake is colliding with it self
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        
        self.snake.reset()

    def draw_grass(self):
        grass_color = (159, 236, 238)
        for row in range(cell_number):
            if row%2==0:
                for col in range(cell_number):
                    if col%2 == 0:
                        grass_rect = pygame.Rect((col*cell_size)+side_border, (row*cell_size)+top_border, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col%2 != 0:
                        grass_rect = pygame.Rect((col*cell_size)+side_border, (row*cell_size)+top_border, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        if int(score_text)>self.hs:
            self.hs = int(score_text)
        hs_t = str(self.hs)
        
        score_surface = game_font.render(score_text, True, (255, 255, 255))
        hs_s = game_font.render(hs_t, True, (255, 255, 255))
        score_x = 80
        score_y = 40
        hs_x = 160
        hs_y = 40
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        hs_rect = score_surface.get_rect(center = (hs_x, hs_y))
        orange_rect = orange.get_rect(midright = (score_rect.left, score_rect.centery))
        trophy_rect = trophy.get_rect(midright = (hs_rect.left, hs_rect.centery))

        r_s = key_font.render('-Enter R to RESET', True, (171, 236, 238))
        r_x = 550
        r_y = 40
        r_rect = r_s.get_rect(center = (r_x, r_y))
        
        screen.blit(score_surface, score_rect)
        screen.blit(orange, orange_rect)
        screen.blit(hs_s, hs_rect)
        screen.blit(trophy, trophy_rect)
        screen.blit(r_s, r_rect)

                      
pygame.mixer.pre_init(44100, -16, 2, 512)       
pygame.init()
cell_size = 40
cell_number = 15
top_border = 4 * 30
side_border = 1 * 30
bottom_border = 1 * 30
screen_vsize = (cell_number*cell_size) + top_border + bottom_border
screen_hsize = (cell_number*cell_size) + (2 * side_border)
screen = pygame.display.set_mode((screen_hsize, screen_vsize))
clock = pygame.time.Clock()
orange = pygame.image.load('Graphics/orange.png').convert_alpha()
trophy = pygame.image.load('Graphics/trophy.png').convert_alpha()
game_font = pygame.font.Font('Fonts/PoetsenOne-Regular.ttf', 28)
key_font = pygame.font.Font('Fonts/PoetsenOne-Regular.ttf', 22)



t1 = pygame.Surface((screen_hsize,top_border))
t2 = pygame.Surface((side_border,screen_vsize))
t3 = pygame.Surface((screen_hsize,bottom_border))
ss = pygame.Surface((screen_hsize, int(3 * 30)))


t1.fill(())
t2.fill((0, 210, 210))
t3.fill((0, 210, 210))
ss.fill((0, 185 , 185))
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

hs = 0
main_game = MAIN(hs)

#At the start of our game will we check for every possible event
while True:
    for event in pygame.event.get():
        
        #we will check if the user chose quit (x at top right corner) to close the window.
        if event.type == pygame.QUIT:
            #if that is the case we will close the screen
            pygame.quit()
            sys.exit()

        #Updating the screen based on the timer
        if event.type == SCREEN_UPDATE:
            main_game.update()

        #Looking for user inputs to move the snake (keys like up, down, right, left)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            
            if event.key == pygame.K_r:
                main_game.snake.reset()

        
    screen.fill((171, 236, 238))
    screen.blit(t1,(0,0))
    screen.blit(t2,(0,0))
    screen.blit(t2,(screen_hsize-side_border,0))
    screen.blit(t3,(0,screen_vsize-bottom_border))
    screen.blit(ss,(0,0))
    main_game.draw_elements()
    pygame.disp0, lay.update()

    clock.tick(60)

