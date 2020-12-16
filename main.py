import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos+288, 450))


def create_pipe():
    randompos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(350, randompos))
    top_pipe = pipe_surface.get_rect(midbottom=(350, randompos-150))
    return top_pipe, bottom_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 1
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if oiseau_rect.colliderect(pipe):
            sound_hit.play()
            return False

    if oiseau_rect.top <= 0 or oiseau_rect.bottom >= 450:
        sound_hit.play()
        return False

    return True


def rotate_oiseau(oiseau):
    new_oiseau = pygame.transform.rotozoom(oiseau, -oiseau_mouvement*3, 1)
    return new_oiseau


def oiseau_animation():
    new_oiseau_surface = oiseau_frames[oiseau_index]
    new_oiseau_rect = oiseau_surface.get_rect(center=(50, oiseau_rect.centery))
    return new_oiseau_surface, new_oiseau_rect


def score_display(run):
    if run == False:
        score_surface = font.render("Score: " + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
        high_score_surface = font.render("Highest Score: " + str(int(high_score)), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 432))
        screen.blit(high_score_surface, high_score_rect)
    else:
        score_surface = font.render("Score: " + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)


pygame.init()
pygame.mixer.pre_init(frequency=441000, size=16, channels=1, buffer=256 )
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()

# Game variables
gravity = 0.25
oiseau_mouvement = 0
game_on = True
game_over_surface = pygame.image.load("sprites/message.png").convert_alpha()
font = pygame.font.SysFont('04B_19.TTF', 40)
score = 0
high_score = 0

# background
surface = pygame.image.load('sprites/background-day.png').convert()
# surface = pygame.transform.scale2x(surface)

# FLOOR
floor_surface = pygame.image.load('sprites/base.png').convert()
floor_x_pos = 0

# OISEAU
bottom_oiseau_surface = pygame.image.load("sprites/bluebird-downflap.png").convert_alpha()
mid_oiseau_surface = pygame.image.load("sprites/bluebird-midflap.png").convert_alpha()
top_oiseau_surface = pygame.image.load("sprites/bluebird-upflap.png").convert_alpha()
oiseau_frames = [bottom_oiseau_surface, mid_oiseau_surface, top_oiseau_surface]
oiseau_index = 0
oiseau_surface = oiseau_frames[oiseau_index]
oiseau_rect = oiseau_surface.get_rect(center=(50, 256))

FRAMESTIME = pygame.USEREVENT + 1
pygame.time.set_timer(FRAMESTIME, 200)

# PIPE
pipe_surface = pygame.image.load("sprites/pipe-green.png").convert()
pipe_list = []
SPAWNTIME = pygame.USEREVENT
pygame.time.set_timer(SPAWNTIME, 1200)
pipe_height = [200, 300, 400]

# SOUNDS
sound_flap = pygame.mixer.Sound("audio/wing.wav")
sound_hit = pygame.mixer.Sound("audio/hit.wav")
sound_score = pygame.mixer.Sound("audio/point.wav")
score_sound_counter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_on:
                oiseau_mouvement = -6
                sound_flap.play()
            if event.key == pygame.K_SPACE and game_on != True:
                game_on = True
                pipe_list.clear()
                oiseau_rect.center = (50, 256)
                oiseau_mouvement = 0
                score = 0
        if event.type == SPAWNTIME:
            pipe_list.extend(create_pipe())
        if event.type == FRAMESTIME:
            if oiseau_index < 2:
                oiseau_index += 1
            else:
                oiseau_index = 0
            oiseau_surface, oiseau_rect = oiseau_animation()

    screen.blit(surface, (0, 0))

    if game_on:
        # oiseau
        oiseau_mouvement += gravity
        oiseau_rotate = rotate_oiseau(oiseau_surface)
        oiseau_rect.centery += oiseau_mouvement
        screen.blit(oiseau_rotate, oiseau_rect)

        game_on = check_collision(pipe_list)

        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_sound_counter += 1
        if score_sound_counter == 100:
            sound_score.play()
            score_sound_counter = 0
    else:
        if high_score < score:
            high_score = score

        game_over_rect = game_over_surface.get_rect(center=(144, 256))
        screen.blit(game_over_surface, game_over_rect)

    score_display(game_on)

    # floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)