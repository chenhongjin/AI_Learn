import pygame
import random
import time
import sys
from pygame.locals import *

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# 方向定义
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # 蛇初始位置在屏幕中央
        self.direction = RIGHT  # 初始方向向右
        self.length = 1  # 初始长度
        self.score = 0  # 初始分数
        self.color = GREEN  # 蛇的颜色
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_head = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)
        
        # 检查是否撞到自己
        if new_head in self.positions[1:]:
            return False  # 游戏结束
        
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
            
        return True  # 游戏继续
    
    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.length = 1
        self.score = 0
    
    def render(self, surface):
        for p in self.positions:
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)  # 边框

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), (random.randint(0, GRID_HEIGHT - 1)))
    
    def render(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)  # 边框

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('贪吃蛇游戏')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 20)
        self.snake = Snake()
        self.food = Food()
        self.game_over = False
        self.paused = False
        self.control_type = 'keyboard'  # 默认键盘控制
        self.difficulty = 'normal'  # 默认难度
        self.sound_enabled = True  # 默认开启音效
        
    def check_collision(self):
        # 检查是否吃到食物
        if self.snake.get_head_position() == self.food.position:
            self.snake.length += 1
            self.snake.score += 10
            self.food.randomize_position()
            # 确保食物不会出现在蛇身上
            while self.food.position in self.snake.positions:
                self.food.randomize_position()
            if self.sound_enabled:
                # 这里可以添加吃食物的音效
                pass
    
    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y))
    
    def show_score(self):
        score_text = self.font.render(f'分数: {self.snake.score}', True, BLACK)
        self.screen.blit(score_text, (5, 5))
        
    def show_game_over(self):
        game_over_text = self.font.render('游戏结束! 按R键重新开始', True, RED)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        
    def show_pause(self):
        pause_text = self.font.render('游戏暂停! 按P键继续', True, BLUE)
        self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_r and self.game_over:
                    self.reset_game()
                elif event.key == K_p:
                    self.paused = not self.paused
                elif not self.game_over and not self.paused:
                    if self.control_type == 'keyboard':
                        if event.key == K_UP and self.snake.direction != DOWN:
                            self.snake.direction = UP
                        elif event.key == K_DOWN and self.snake.direction != UP:
                            self.snake.direction = DOWN
                        elif event.key == K_LEFT and self.snake.direction != RIGHT:
                            self.snake.direction = LEFT
                        elif event.key == K_RIGHT and self.snake.direction != LEFT:
                            self.snake.direction = RIGHT
            elif event.type == MOUSEBUTTONDOWN and self.control_type == 'swipe':
                # 这里可以添加滑动控制的逻辑
                pass
    
    def reset_game(self):
        self.snake.reset()
        self.food.randomize_position()
        self.game_over = False
        self.paused = False
    
    def run(self):
        while True:
            self.handle_events()
            
            if not self.game_over and not self.paused:
                if not self.snake.update():
                    self.game_over = True
                self.check_collision()
            
            # 绘制游戏界面
            self.screen.fill(WHITE)
            self.draw_grid()
            self.snake.render(self.screen)
            self.food.render(self.screen)
            self.show_score()
            
            if self.game_over:
                self.show_game_over()
            elif self.paused:
                self.show_pause()
            
            pygame.display.update()
            self.clock.tick(FPS)

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
