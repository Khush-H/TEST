import pygame
import random
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 400
HEIGHT = 600
GRAVITY = 0.25
BIRD_FLAP = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_WIDTH = 50
FPS = 60

# Colors
WHITE = (0, 0, 0)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)

# Bird properties
bird_x = 100
bird_y = HEIGHT // 2
bird_velocity = 0
bird_radius = 20

# Pipe properties
pipes = []
pipe_frequency = 90  # Frames between new pipes
score = 0
frame_count = 0

# Font for score
font = pygame.font.SysFont("arial", 30)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

def draw_bird():
    pygame.draw.circle(screen, YELLOW, (int(bird_x), int(bird_y)), bird_radius)

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe['x'], 0, PIPE_WIDTH, pipe['top']))
        pygame.draw.rect(screen, GREEN, (pipe['x'], pipe['bottom'], PIPE_WIDTH, HEIGHT))

def update_pipes():
    global score
    for pipe in pipes:
        pipe['x'] -= PIPE_SPEED
    pipes[:] = [pipe for pipe in pipes if pipe['x'] > -PIPE_WIDTH]
    for pipe in pipes:
        if pipe['x'] + PIPE_WIDTH < bird_x and not pipe.get('scored', False):
            score += 1
            pipe['scored'] = True

def create_pipe():
    gap_y = random.randint(150, HEIGHT - 150)
    return {'x': WIDTH, 'top': gap_y - PIPE_GAP // 2, 'bottom': gap_y + PIPE_GAP // 2, 'scored': False}

def check_collision():
    for pipe in pipes:
        if bird_x + bird_radius > pipe['x'] and bird_x - bird_radius < pipe['x'] + PIPE_WIDTH:
            if bird_y - bird_radius < pipe['top'] or bird_y + bird_radius > pipe['bottom']:
                return True
    if bird_y - bird_radius < 0 or bird_y + bird_radius > HEIGHT:
        return True
    return False

def setup():
    global bird_y, bird_velocity, pipes, score, frame_count
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes.clear()
    score = 0
    frame_count = 0
    pipes.append(create_pipe())

async def main():
    global bird_y, bird_velocity, frame_count
    setup()
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = BIRD_FLAP
        
        # Update bird
        bird_velocity += GRAVITY
        bird_y += bird_velocity
        
        # Update pipes
        frame_count += 1
        if frame_count % pipe_frequency == 0:
            pipes.append(create_pipe())
        update_pipes()
        
        # Check collision
        if check_collision():
            setup()  # Reset game
        
        # Draw
        screen.fill(WHITE)
        draw_pipes()
        draw_bird()
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        
        await asyncio.sleep(1.0 / FPS)
        clock.tick(FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())