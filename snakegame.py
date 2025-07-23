import pygame,sys,random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.score = 0

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
            self.score += 1

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        global game_state, final_score
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            final_score = self.score
            if qualifies_top3(final_score):
                game_state = ENTER_NAME
            else:
                game_state = GAME_OVER
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                final_score = self.score
                if qualifies_top3(final_score):
                    game_state = ENTER_NAME
                else:
                    game_state = GAME_OVER

    def reset(self):
        self.snake.reset()
        self.fruit.randomize()
        self.score = 0

    def draw_grass(self):
        grass_color = (167,209,61)
        for row in range(cell_number):
            if row % 2 == 0: 
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)            

    def draw_score(self):
        score_text = str(self.score)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect,2)

# Button helpers
def draw_button(rect, text):
    pygame.draw.rect(screen, (100, 200, 100), rect)
    pygame.draw.rect(screen, (56,74,12), rect, 3)
    lines = text.split('\n')
    total_height = sum(game_font.size(line)[1] for line in lines)
    y_offset = rect.centery - total_height // 2
    for line in lines:
        text_surf = game_font.render(line, True, (56,74,12))
        text_rect = text_surf.get_rect(center=(rect.centerx, y_offset + text_surf.get_height() // 2))
        screen.blit(text_surf, text_rect)
        y_offset += text_surf.get_height()

# Function to check if the score qualifies for top 3
def qualifies_top3(score):
    if len(top_scores) < 3:
        return True
    return score > min(s for _, s in top_scores)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
TOP_SCORES = 3 
ENTER_NAME = 4
username = ""
game_state = MENU
final_score = 0
top_scores = []  # List to store top 3 (username, score) tuples

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_state == PLAYING:
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0,-1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1,0)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0,1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1,0)
        elif game_state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if start_button.collidepoint(mx, my):
                    main_game.reset()
                    game_state = PLAYING
                elif top3_button.collidepoint(mx, my):
                    game_state = TOP_SCORES
        elif game_state == GAME_OVER:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if restart_button.collidepoint(mx, my):
                    main_game.reset()
                    game_state = PLAYING
                elif back_menu_button.collidepoint(mx, my):
                    game_state = MENU
        elif game_state == TOP_SCORES:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back_menu_button.collidepoint(mx, my):
                    game_state = MENU
                elif restart_button.collidepoint(mx, my):
                    main_game.reset()
                    game_state = PLAYING
        elif game_state == ENTER_NAME:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username:
                        top_scores.append((username, final_score))
                        top_scores.sort(key=lambda x: x[1], reverse=True)
                        top_scores[:] = top_scores[:3]
                        game_state = TOP_SCORES
                        username = ""  # Clear username after submission
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    # Only allow reasonable characters
                    if len(username) < 12 and event.unicode.isprintable() and event.unicode != '\r' and event.unicode != '\n':
                        username += event.unicode

    screen.fill((175,215,70))
    if game_state == PLAYING:
        main_game.draw_elements()
    elif game_state == MENU:
        # Draw main menu
        title_surf = game_font.render("Snake Game", True, (56,74,12))
        title_rect = title_surf.get_rect(center=(cell_size*cell_number//2, cell_size*cell_number//2 - 120))
        screen.blit(title_surf, title_rect)
        start_button = pygame.Rect(cell_size*cell_number//2 - 150, cell_size*cell_number//2 - 40, 300, 70)
        top3_button = pygame.Rect(cell_size*cell_number//2 - 150, cell_size*cell_number//2 + 50, 300, 70)
        draw_button(start_button, "Play")
        draw_button(top3_button, "Leaderboard")
    elif game_state == GAME_OVER:
        # Draw game over screen, but do not add to top_scores here
        over_surf = game_font.render("Game Over!", True, (200,30,30))
        over_rect = over_surf.get_rect(center=(cell_size*cell_number//2, cell_size*cell_number//2 - 120))
        screen.blit(over_surf, over_rect)
        score_surf = game_font.render(f"Final Score: {final_score}", True, (56,74,12))
        score_rect = score_surf.get_rect(center=(cell_size*cell_number//2, cell_size*cell_number//2 - 60))
        screen.blit(score_surf, score_rect)
        restart_button = pygame.Rect(cell_size*cell_number//2 - 150, cell_size*cell_number//2 + 10, 300, 70)
        back_menu_button = pygame.Rect(cell_size*cell_number//2 - 150, cell_size*cell_number//2 + 100, 300, 70)
        draw_button(restart_button, "Play Again")
        draw_button(back_menu_button, "Main Menu")
    elif game_state == TOP_SCORES:
        # Draw top 3 scores screen
        title_surf = game_font.render("Top 3 Scores", True, (56,74,12))
        title_rect = title_surf.get_rect(center=(cell_size*cell_number//2, cell_size*cell_number//2 - 120))
        screen.blit(title_surf, title_rect)
        for i, (name, score) in enumerate(top_scores):
            score_surf = game_font.render(f"{i+1}. {name}: {score}", True, (56,74,12))
            score_rect = score_surf.get_rect(center=(cell_size*cell_number//2, cell_size*cell_number//2 - 30 + i*40))
            screen.blit(score_surf, score_rect)
        back_menu_button = pygame.Rect(cell_size*cell_number//2 - 150, cell_size*cell_number//2 + 100, 300, 70)
        restart_button = pygame.Rect(cell_size*cell_number//2 - 150, cell_size*cell_number//2 + 190, 300, 70)
        draw_button(back_menu_button, "Main Menu")
        draw_button(restart_button, "Play Again")
    elif game_state == ENTER_NAME:
        # Draw username input screen
        prompt = "Enter your name: "
        input_surf = game_font.render(prompt + username, True, (56,74,12))
        input_rect = input_surf.get_rect(center=(cell_size*cell_number//2, cell_size*cell_number//2 - 40))
        screen.blit(input_surf, input_rect)
        info_surf = game_font.render("Press Enter to confirm", True, (56,74,12))
        info_rect = info_surf.get_rect(center=(cell_size*cell_number//2, cell_size*cell_number//2 + 10))
        screen.blit(info_surf, info_rect)

    pygame.display.update()
    clock.tick(60)