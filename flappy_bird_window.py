import pygame
import random
import os

pygame.init()

WIDTH, HEIGHT = 500, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy bird")

WHITE = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

FONT = pygame.font.SysFont("comicsansms", 30)

bird_x = 100
bird_radius = 20
gravity = 0.5
jump_strength = -10
floor_y = HEIGHT - bird_radius

pipe_speed = 5
initial_pipe_gap = 200
min_pipe_gap = 130
initial_pipe_spacing = 300
min_pipe_spacing = 180

pipe_top = pygame.image.load("pipe-down.png").convert_alpha()
pipe_bottom = pygame.image.load("pipe-up.png").convert_alpha()
pipe_width = pipe_top.get_width()

background = pygame.image.load("background.png")
bg_width = background.get_width()

bird_up = pygame.image.load("wings_up.png")
bird_down = pygame.image.load("wings_down.png")

BEST_SCORE_FILE = "best_score.txt"

def load_best_score():
    if os.path.exists(BEST_SCORE_FILE):
        with open(BEST_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    return 0

def save_best_score(score):
    best_score = load_best_score()
    if score > best_score:
        with open(BEST_SCORE_FILE, "w") as file:
            file.write(str(score))

def draw_text(text, y):
    """Function to display text on screen"""
    text_surface = FONT.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
    SCREEN.blit(text_surface, text_rect)

def calculate_pipe_gap(score):
    return max(initial_pipe_gap - (score * 2), min_pipe_gap)

def calculate_pipe_spacing(score):
    return max(initial_pipe_spacing - (score * 5), min_pipe_spacing)


def game():
    """Main game function"""
    bird_y = HEIGHT // 2
    velocity = 0
    score = 0
    best_score = load_best_score()

    pipes = []
    pipe_spacing = initial_pipe_spacing

    for i in range(3):
        pipe_x = WIDTH + i * pipe_spacing
        pipe_height = random.randint(150, 400)
        pipes.append([pipe_x, pipe_height])

    bg_x = 0
    flap_frame = 0

    running = True
    while running:
        SCREEN.fill(WHITE)

        bg_x -= 2
        if bg_x <= -bg_width:
            bg_x = 0

        SCREEN.blit(background, (bg_x, 0))
        SCREEN.blit(background, (bg_x + bg_width, 0))

        if bg_x + bg_width < WIDTH:
            SCREEN.blit(background, (bg_x + 2 * bg_width, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    velocity = jump_strength
                    flap_frame = 1

        if flap_frame == 1:
            SCREEN.blit(bird_up, (bird_x - bird_radius, int(bird_y) - bird_radius))
        else:
            SCREEN.blit(bird_down, (bird_x - bird_radius, int(bird_y) - bird_radius))

        flap_frame = 1 if flap_frame == 0 else 0

        velocity += gravity
        bird_y += velocity

        if bird_y >= floor_y:
            bird_y = floor_y
            velocity = 0
            running = False

        if bird_y <= bird_radius:
            bird_y = bird_radius
            velocity = 0

        for pipe in pipes:
            pipe[0] -= pipe_speed

            pipe_x, pipe_height = pipe
            pipe_gap = calculate_pipe_gap(score)

            SCREEN.blit(pipe_top, (pipe_x, pipe_height - pipe_top.get_height()))
            SCREEN.blit(pipe_bottom, (pipe_x, pipe_height + pipe_gap))

            # Check collision
            if bird_x + bird_radius > pipe_x and bird_x - bird_radius < pipe_x + pipe_width:
                if bird_y - bird_radius < pipe_height or bird_y + bird_radius > pipe_height + pipe_gap:
                    running = False

            # Remove pipes that go off-screen and add new ones
        if pipes[0][0] + pipe_width < 0:
            pipes.pop(0)  # Remove old pipe
            score += 1  # Increase score
            pipe_spacing = calculate_pipe_spacing(score)  # Adjust spacing dynamically

            # Add a new pipe at the right
            new_pipe_x = pipes[-1][0] + pipe_spacing
            new_pipe_height = random.randint(150, 400)
            pipes.append([new_pipe_x, new_pipe_height])

            # Display score
        draw_text(f"Score: {score}", 10)
        draw_text(f"Best score: {best_score}", 50)

        pygame.display.update()
        pygame.time.delay(30)

    save_best_score(score)
    game_over_screen(score)

def game_over_screen(score):
    best_score = load_best_score()
    """Displays Game Over Screen and waits for user to restart"""
    SCREEN.fill(WHITE)
    draw_text("Game over!", HEIGHT // 3)
    draw_text(f"Your score: {score}", HEIGHT // 2)
    draw_text(f"Best score: {best_score}", HEIGHT // 2 + 50)
    draw_text("Press SPACE to Restart", HEIGHT // 1.5)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game()

game()
