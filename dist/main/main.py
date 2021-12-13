# import packages
import pygame
import sys
import random
import pickle

# initialize pygame package
pygame.init()

# game state class
class GAME:
    # initialize game state
    def __init__(self): 
        self.game_running = True
    
    # main game loop
    def game_loop(self):
        pygame.display.set_caption("Worm on a String")

        pygame.time.set_timer(WIN_UPDATE, 150)

        game_logic.background_music()

        # draw elements
        while game_state.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == WIN_UPDATE:
                    game_logic.update()

                    # movement
                    userInput = pygame.key.get_pressed()

                    if userInput[pygame.K_a]:
                        if game_logic.worm.direction.x != 1:
                            game_logic.worm.direction = pygame.math.Vector2(-1, 0)
                    if userInput[pygame.K_d]:
                        if game_logic.worm.direction.x != -1:
                            game_logic.worm.direction = pygame.math.Vector2(1, 0)
                    if userInput[pygame.K_w]:
                        if game_logic.worm.direction.y != 1:
                            game_logic.worm.direction = pygame.math.Vector2(0, -1)
                    if userInput[pygame.K_s]:
                        if game_logic.worm.direction.y != -1:
                            game_logic.worm.direction = pygame.math.Vector2(0, 1)
            
            win.fill(pygame.Color('green'))
            game_logic.draw_elements()

            pygame.display.update()
            fps.tick(60)

    # start game
    def initiate(self):
        self.game_running = True
        game_logic.start_menu()

# class for player character
class WORM:
    
    # initialize worm 
    def __init__(self):
        # worm body
        self.body = [pygame.math.Vector2(5, 10), pygame.math.Vector2(4,10), pygame.math.Vector2(3,10)]
        self.direction = pygame.math.Vector2(1, 0)
        self.worm_part = False

        # worm head animation
        self.head_up = pygame.image.load('dist\main\Graphics\Worm_Head_Up.png').convert_alpha()
        self.head_down = pygame.image.load('dist\main\Graphics\Worm_Head_Down.png').convert_alpha()
        self.head_right = pygame.image.load('dist\main\Graphics\Worm_Head_Right_.png').convert_alpha()
        self.head_left = pygame.image.load('dist\main\Graphics\Worm_Head_Left.png').convert_alpha()

        # worm tail animation
        self.tail_up = pygame.image.load('dist\main\Graphics\Worm_Tail_Up.png').convert_alpha()
        self.tail_down = pygame.image.load('dist\main\Graphics\Worm_Tail_Down.png').convert_alpha()
        self.tail_right = pygame.image.load('dist\main\Graphics\Worm_Tail_Right.png').convert_alpha()
        self.tail_left = pygame.image.load('dist\main\Graphics\Worm_Tail_Left.png').convert_alpha()

        # worm body animation
        self.body_vertical = pygame.image.load('dist\main\Graphics\Worm_Body_Vertical_.png').convert_alpha()
        self.body_horizontal = pygame.image.load('dist\main\Graphics\Worm_Body_Horizontal.png').convert_alpha()

        # worm turn animation
        self.body_tr = pygame.image.load('dist\main\Graphics\Worm_Turn_Lower_Right.png').convert_alpha()
        self.body_tl = pygame.image.load('dist\main\Graphics\Worm_Turn_Lower_Left.png').convert_alpha()
        self.body_br = pygame.image.load('dist\main\Graphics\Worm_Turn_Upper_Right.png').convert_alpha()
        self.body_bl = pygame.image.load('dist\main\Graphics\Worm_Turn_Upper_Left.png').convert_alpha()

        # worm sound effects
        self.slurp = pygame.mixer.Sound('dist\main\SFX\impactsplat08.wav')

    # drawing worm on screen
    def draw_worm(self):
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size) 
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            # showing animations
            if index == 0 and self.direction == pygame.math.Vector2(1, 0):
                win.blit(self.head_right, block_rect)
            elif index == 0 and self.direction == pygame.math.Vector2(-1, 0):
                win.blit(self.head_left, block_rect)
            elif index == 0 and self.direction == pygame.math.Vector2(0, -1):
                win.blit(self.head_up, block_rect)
            elif index == 0 and self.direction == pygame.math.Vector2(0, 1):
                win.blit(self.head_down, block_rect)
            elif index == len(self.body) - 1 and self.direction == pygame.math.Vector2(1, 0):
                win.blit(self.tail_right, block_rect)
            elif index == len(self.body) - 1 and self.direction == pygame.math.Vector2(-1, 0):
                win.blit(self.tail_left, block_rect)
            elif index == len(self.body) - 1 and self.direction == pygame.math.Vector2(0, -1):
                win.blit(self.tail_up, block_rect)
            elif index == len(self.body) - 1 and self.direction == pygame.math.Vector2(0, 1):
                win.blit(self.tail_down, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    win.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    win.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        win.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        win.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        win.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        win.blit(self.body_br,block_rect)
    
    # initializing movement
    def movement(self):
        if self.worm_part == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.worm_part = False
        else: 
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    # adding block when eating apple
    def add_block(self):
        self.worm_part = True

    # slurp sound effect
    def slurp_apple(self):
        self.slurp.play()

# apple class
class APPLE:
    def __init__(self):
        self.randomize()

    # drawing apple on screen
    def draw_apple(self):
        apple_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        win.blit(apple, apple_rect)
    
    # random placement of apple on screen
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = pygame.math.Vector2(self.x, self.y)

# game logic class
class LOGIC:
    # initializing parts of game
    def __init__(self):
        self.worm = WORM()
        self.apple = APPLE()
        self.bgm = pygame.mixer.music.load('dist/main/SFX/bgm_action_4.wav')
        self.button1 = pygame.draw.rect(win, 'red', (winX - 325, winY - 200, 150, 75))
        self.button2 = pygame.draw.rect(win, 'red', (winX - 325, winY - 200, 150, 75))

    # start menu
    def start_menu(self):
        menu = True
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
            win.fill('green')

            title_text = "Worm on a String"
            title_surface = title_font.render(title_text, True, 'white')  
            title_rect = title_surface.get_rect(center = ((winX / 2), (winY - 400)))  
            win.blit(title_surface, title_rect) 

            # create start button
            button1_surface = pygame.Surface((150, 75))
            pygame.Surface.fill(button1_surface, "red")
            button1 = self.button1
            win.blit(button1_surface, button1)  

            button1_text = "START"
            button1_surface = game_font.render(button1_text, True, 'white')  
            button1_rect = button1_surface.get_rect(center = ((winX - 250), (winY - 165)))  
            win.blit(button1_surface, button1_rect) 
            
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            # provide functionality to button
            if self.button1.collidepoint(mouse):
                if click[0] == 1:
                    print("click")
                    game_state.game_loop() 

            pygame.display.update()
            fps.tick(15)

    # update game screen when playing
    def update(self):
        self.worm.movement()
        self.monch()
        self.failure()
    
    # draw game elements on screen
    def draw_elements(self):
        self.worm.draw_worm()
        self.apple.draw_apple() 
        self.score()
    
    # worm eating apple mechanism
    def monch(self):
        if self.apple.pos == self.worm.body[0]:
            print('om nom')
            self.apple.randomize()
            self.worm.add_block()
            self.worm.slurp_apple()

    # keeping score
    def score(self):
        # show score on screen
        score_text = "Score:" + str(len(self.worm.body) - 3)
        score_surface = game_font.render(score_text, True, 'white')
        score_x = int(cell_size * cell_number - 80)
        score_y = int(cell_size * cell_number - 20)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        win.blit(score_surface, score_rect)

    # defining what failure means
    def failure(self):
        # initialize pickling of scores
        file_name = 'scores'
        # score dict
        d = {"High Score ": str(len(self.worm.body) - 3)}
        final_score = open(file_name, "wb")
        # lose conditions
        if not 0 <= self.worm.body[0].x <= cell_number - 1:
            self.game_over()
            pickle.dump(d, final_score)
            final_score.close()
        if not 0 <= self.worm.body[0].y <= cell_number - 1:
            self.game_over()
            pickle.dump(d, final_score)
            final_score.close()
        for block in self.worm.body[1:]:
            if block == self.worm.body[0]:
                self.game_over()
                pickle.dump(d, final_score)
                final_score.close()

    # game over screen
    def game_over(self):
        while game_state.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            game_state.game_running = False
            while game_state.game_running == False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                win.fill('black')
                title_text = "GAME OVER"
                title_surface = title_font.render(title_text, True, 'red')  
                title_rect = title_surface.get_rect(center = ((winX / 2), (winY - 400)))  
                win.blit(title_surface, title_rect)      
                
                # quit button
                button2_surface = pygame.Surface((150, 75))
                pygame.Surface.fill(button2_surface, "red")
                button2 = self.button2
                win.blit(button2_surface, button2)  
                
                button2_text = "QUIT"
                button2_surface = game_font.render(button2_text, True, 'white')  
                button2_rect = button2_surface.get_rect(center = ((winX - 250), (winY - 165)))  
                win.blit(button2_surface, button2_rect) 

                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()

                # button function
                if self.button2.collidepoint(mouse):
                    if click[0] == 1:
                        print("click")
                        pygame.quit()
                        sys.exit()

                pygame.display.update()
                fps.tick(15)

    # win condition
    def win_condition(self):
        # score if player wins
        file_name = 'scores'
        d = {"High Score ": str(len(self.worm.body) - 3)}
        final_score = open(file_name, "wb")
        # if length of worm body is 4 less than screen size, player wins
        if len(self.worm.body) != int((cell_size * cell_number) - 4):
            pickle.dump(d, final_score)
            pygame.quit()
            final_score.close()
            sys.exit()
    
    # background music
    def background_music(self):
        # playing on a loop (-1)
        pygame.mixer.music.play(-1)

# setting size of blocks
cell_size = 25
cell_number = 20

# width and height of screen
winX = cell_number * cell_size
winY = cell_number * cell_size

# screen
win = pygame.display.set_mode((winX, winY))

# frames per second
fps = pygame.time.Clock()

# apple image
apple = pygame.image.load('dist/main/Graphics/Apple_Worm_On_A_String.png').convert_alpha()

# fonts
title_font = pygame.font.Font('dist/main/Font/04B_30__.TTF', 35)
game_font = pygame.font.Font('dist/main/Font/04B_30__.TTF', 25)

# logic and game state
WIN_UPDATE = pygame.USEREVENT
game_logic = LOGIC()
game_state = GAME()

# starting game
if __name__ == '__main__':
    game_state.initiate()

