import pygame, os
import numpy as np
pygame.font.init()

WIDTH, HEIGHT = 800, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')

FPS = 60

BACKGROUND_MENU = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background_menu.png')),(WIDTH, HEIGHT))
BACKGROUND_GAME = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background_game.png')), (WIDTH, HEIGHT))

CURSOR = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background_game.png')),(20, 20))
FOOD = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'food.png')),(20, 20))

PLAYER_HEAD = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'player_head.png')),(20, 20))
PLAYER_BODY = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'player_body.png')),(20, 20))

class Cursor:
    def __init__(self, x, y):
        self.cursor_img = CURSOR
        self.x = x
        self.y = y

    def draw(self, window):
        window.blit(self.cursor_img, (self.x, self.y))
        
class Food:
    def __init__(self, x, y):
        self.img = FOOD
        self.x = x
        self.y = y
        #self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y)) 

class Player:

    def __init__(self, x, y, vel):
        self.head_img = PLAYER_HEAD
        self.body_img = PLAYER_BODY
        self.x = [x, x - 20, x - 40]
        self.y = [y, y, y]
        self.vel = vel
        self.head_mask = pygame.mask.from_surface(self.head_img)
        self.body_mask = pygame.mask.from_surface(self.body_img)
        self.cooldown_counter = 1
    
    def cooldown(self, movement_speed):
        if self.cooldown_counter >= movement_speed:
            self.cooldown_counter = 0
        elif self.cooldown_counter >= 0:
            self.cooldown_counter += 1

    def movement(self):
        if self.cooldown_counter == 0:
            if self.x[0] > self.x[1]:
                self.x[-1] = self.x[0] + self.vel
                self.y[-1] = self.y[0]
                self.x.insert(0, self.x.pop())
                self.y.insert(0, self.y.pop())
            elif self.x[0] < self.x[1]:
                self.x[-1] = self.x[0] - self.vel
                self.y[-1] = self.y[0]
                self.x.insert(0, self.x.pop())
                self.y.insert(0, self.y.pop())
            elif self.y[0] > self.y[1]:
                self.x[-1] = self.x[0]
                self.y[-1] = self.y[0] + self.vel
                self.x.insert(0, self.x.pop())
                self.y.insert(0, self.y.pop())
            elif self.y[0] < self.y[1]:
                self.x[-1] = self.x[0]
                self.y[-1] = self.y[0] - self.vel
                self.x.insert(0, self.x.pop())
                self.y.insert(0, self.y.pop())


    def draw(self, window):
        window.blit(self.head_img, (self.x[0], self.y[0])) 
        for i in range(1, len(self.x)):
            window.blit(self.body_img, (self.x[i], self.y[i]))

    def collide(self):
        for i in range(1, len(self.x)):
            if self.x[0] == self.x[i] and self.y[0] == self.y[i]:
                quit()

def main(spd):
    run = True
    score = 0
    main_font = pygame.font.SysFont('arial', 50)
    clock = pygame.time.Clock()
    food_x, food_y = 0, 0

    movement_speed = 30 / (spd+1)

    stage_matrix = np.zeros((45,40))

    #This part of the code exclude section at the top where score is located
    for i in range(0, 40):
        for j in range(0, 6):
            stage_matrix[j, i] = 3

    player = Player(600, 500, 20)
    food = Food(int(food_x), int(food_y))


    def player_location():
        for i in range(0, len(player.x)):
            stage_matrix[int(player.x[i]/20), int(player.y[i]/20)] = 1
        

    def food_location(matrix):
        matrix = matrix.flatten()

        empty_space = np.array(np.where(matrix == 0))
        empty_space = empty_space.flatten()

        food_space = np.random.choice(empty_space)

        matrix[food_space] = 2
        matrix = np.reshape(matrix, (40, 45))

        global food_y, food_x
        food_y, food_x = np.array(np.where(matrix == 2))


    def redraw_window():
        WIN.blit(BACKGROUND_GAME, (0,0))

        score_label = main_font.render(f'Score: {score}', 1, (255,255,255))
       
        WIN.blit(score_label, (10,10))

        player_location()
        food_location(stage_matrix)

        player.cooldown(movement_speed)
        player.movement()
        player.collide()
        player.draw(WIN)

        food.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.x[-1] = player.x[0]
                    player.y[-1] = player.y[0] - player.vel
                    player.x.insert(0, player.x.pop())
                    player.y.insert(0, player.y.pop())
                    player.cooldown_counter = 0
                if event.key == pygame.K_DOWN:
                    player.x[-1] = player.x[0]
                    player.y[-1] = player.y[0] + player.vel
                    player.x.insert(0, player.x.pop())
                    player.y.insert(0, player.y.pop())
                    player.cooldown_counter = 0
                if event.key == pygame.K_LEFT:
                    player.x[-1] = player.x[0] - player.vel
                    player.y[-1] = player.y[0]
                    player.x.insert(0, player.x.pop())
                    player.y.insert(0, player.y.pop())
                    player.cooldown_counter = 0
                if event.key == pygame.K_RIGHT:
                    player.x[-1] = player.x[0] + player.vel
                    player.y[-1] = player.y[0]
                    player.x.insert(0, player.x.pop())
                    player.y.insert(0, player.y.pop())
                    player.cooldown_counter = 0


def main_menu():
    title_font = pygame.font.SysFont('arial', 75)
    menu_font = pygame.font.SysFont('arial', 40)
    menu_y = [250, 500, 750]
    cursor_location = 0
    cursor_x = 300
    cursor_y = menu_y[cursor_location]
    speed_options = ['Low', 'Medium', "High"]
    speed = 0

    def redraw_window():
        WIN.blit(BACKGROUND_MENU, (0,0))
        
        title_label = title_font.render('SNAKE', 1, (255,255,255))
        start_label = menu_font.render('Start', 1, (255,255,255))
        speed_label = menu_font.render(f'Speed', 1, (255,255,255))
        speed_value_label = menu_font.render(f'{speed_options[speed]}', 1, (255, 255, 255))
        quit_label = menu_font.render('Quit', 1, (255,255,255))

        WIN.blit(title_label, ((WIDTH - title_label.get_width())/2, 20))
        WIN.blit(start_label, ((WIDTH - start_label.get_width())/2, menu_y[0]))
        WIN.blit(speed_label, ((WIDTH - speed_label.get_width())/2, menu_y[1]))
        WIN.blit(speed_value_label, ((WIDTH - speed_label.get_width())/2 + WIDTH/4, menu_y[1]))
        WIN.blit(quit_label, ((WIDTH - quit_label.get_width())/2, menu_y[-1]))

        cursor.draw(WIN)

        pygame.display.update()

    run = True
    while run:
        cursor_y = menu_y[cursor_location]
        cursor = Cursor(cursor_x, cursor_y)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and cursor_y != menu_y[-1]:
                    cursor_location += 1
                if event.key == pygame.K_UP and cursor_y != menu_y[0]:
                    cursor_location -= 1                
                if event.key == pygame.K_SPACE and cursor_y == menu_y[0]:
                    main(speed)
                if event.key == pygame.K_RIGHT and cursor_y == menu_y[1] and speed < 2:
                    speed += 1
                if event.key == pygame.K_LEFT and cursor_y == menu_y[1] and speed > 0:
                    speed -= 1
                if event.key == pygame.K_SPACE and cursor_y == menu_y[-1]:
                    run = False

    pygame.quit()    

main_menu()