# Import and initialize the pygame library
import pygame
import time
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_s,
    K_w,
    KEYDOWN,
)

pygame.init()

# Set up the drawing screen/display
screen_width = 800
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])

# set the pygame window name
pygame.display.set_caption('Super Awesome Pong')
center = (screen_width // 2, screen_height // 2)

# colors
blue, green, white, black = ((0, 0, 225), (0, 255, 0), (255, 255, 255), (0, 0, 0))
def random_color():
    color = (random.randint(5, 250), random.randint(5, 250), random.randint(5, 250))
    return color

# Scoreboard
player_a_score, player_b_score = (0, 0)
font = pygame.font.Font('freesansbold.ttf', 22)
text = font.render(f"Player A: {player_a_score} | Player B: {player_b_score}", True, white)
scoreboard = text.get_rect()
scoreboard.center = (screen_width // 2, 20)
winning_score = 7

# Win proclamation
winning_player = "nobody"
win_font = pygame.font.Font('freesansbold.ttf', 62)

# ball parameters
ball_r = 20
ball_x, ball_y = center
ball_x_velocity, ball_y_velocity = (1, 1)
ball_color = random_color()
ball_reset, collision = (False, False)
speed_up = 1

#paddle parameters
paddle_a_width, paddle_a_height = (18, 85)
paddle_a_x, paddle_a_y  = (20, screen_height // 2 - paddle_a_height // 2)
paddle_b_width, paddle_b_height = (18, 85)
paddle_b_x, paddle_b_y = (screen_width - paddle_b_width - 20, screen_height // 2 - paddle_b_height // 2)
paddle_move_speed = 1 * speed_up
paddle_a_moving, paddle_b_moving = (0, 0)

# inputs
def get_inputs(paddle_a_moving, paddle_b_moving, paddle_move_speed):
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_s:
                paddle_a_moving += paddle_move_speed
            elif event.key == K_w:
                paddle_a_moving -= paddle_move_speed
            if event.key == K_UP:
                paddle_b_moving -= paddle_move_speed
            elif event.key == K_DOWN:
                paddle_b_moving += paddle_move_speed
        if event.type == pygame.KEYUP:
            if event.key == K_s:
                paddle_a_moving = 0
            elif event.key == K_w:
                paddle_a_moving = 0
            if event.key == K_UP:
                paddle_b_moving = 0
            elif event.key == K_DOWN:
                paddle_b_moving = 0
        elif event.type == pygame.QUIT:
            pygame.quit()
            quit()
    return paddle_a_moving, paddle_b_moving

game_start_time = time.time()
game_over_time = time.time()

while True:
    screen.fill(black)

    # draw game objects
    paddle_a = pygame.draw.rect(screen, green, pygame.Rect(paddle_a_x, paddle_a_y, paddle_a_width, paddle_a_height))
    paddle_b = pygame.draw.rect(screen, green, pygame.Rect(paddle_b_x, paddle_b_y, paddle_b_width, paddle_b_height))
    ball = pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_r)

    # Print live scoreboard
    screen.blit(text, scoreboard)
    text = font.render(f"Player A: {player_a_score} | Player B: {player_b_score}| Speed: {round(speed_up, 1)}", True, white)

    # check for paddle movements
    paddle_a_moving, paddle_b_moving = get_inputs(paddle_a_moving, paddle_b_moving, paddle_move_speed)
    
    # ball moves
    if time.time() > game_over_time + 2:
        ball_y += ball_y_velocity * speed_up
        ball_x += ball_x_velocity * speed_up

    # random ball color
    if collision:
        ball_color = random_color()
        collision = False

    # paddles move
    paddle_a_y += paddle_a_moving
    paddle_b_y += paddle_b_moving
    
    # ball reset
    if ball_x <= -10 or ball_x >= 810:
        if ball_x <= -10:
            player_b_score += 1
        else:
            player_a_score += 1
        ball_x, ball_y = center
        ball_reset = True
        #ball is served to loser
        ball_x_velocity = -ball_x_velocity

    # top and bottom borders
    if ball_y >= (screen_height - ball_r) or ball_y <= ball_r:
        ball_y_velocity = - ball_y_velocity
        collision = True

    # Paddle limit
    if paddle_a_y <= 0:
        paddle_a_y = 0
    if paddle_a_y + paddle_a_height >= screen_height:
        paddle_a_y = screen_height - paddle_a_height
    if paddle_b_y <= 0:
        paddle_b_y = 0
    if paddle_b_y + paddle_b_height >= screen_height :
        paddle_b_y = screen_height - paddle_b_height
    
    # ball and paddle_a collisions
    if paddle_a_x <= (ball_x - ball_r) <= (paddle_a_x + paddle_a_width) and (paddle_a_y + paddle_a_height + ball_r) >= ball_y >= (paddle_a_y - ball_r):
        ball_x_velocity = -ball_x_velocity
        ball_x += 3
        collision = True

    # ball and paddle_b collisions
    if (paddle_b_x + paddle_b_width) >= (ball_x + ball_r) >= paddle_b_x and (paddle_b_y + paddle_b_height + ball_r) >= ball_y >= (paddle_b_y - ball_r):
        ball_x_velocity = -ball_x_velocity
        ball_x -= 3
        collision = True

    # Speed up ball as game progresses
    if time.time() > game_start_time + 10:
        game_start_time = time.time()
        speed_up += .1
    
    # ball reset if scored
    if ball_reset:
        ball_reset = False
        game_over_time = time.time()
        if speed_up > 1.2:
            speed_up -= .2
        else:
            speed_up = 1

    # end game if player wins
    if player_a_score == winning_score or player_b_score == winning_score:
        if player_a_score == winning_score:
            winning_player = "PLAYER A"
        else:
            winning_player = "PLAYER B"
        text = win_font.render(f"{winning_player} WINS!!", True, ball_color)
        ball_x, ball_y = (400, 75)
        scoreboard = text.get_rect()
        scoreboard.center = center
        if time.time() > game_over_time + 2:
            pygame.quit()
            quit()

    pygame.display.flip()
    time.sleep(.003)