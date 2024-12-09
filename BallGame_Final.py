import pygame
from time import sleep

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

RADIUS = 20
center = (WIDTH // 2, HEIGHT // 2)

positions = {
    "1": (WIDTH // 15, 14 * HEIGHT // 15), #左下
    "2": (WIDTH // 2, 14 * HEIGHT // 15),
    "3": (14 * WIDTH // 15, 14 * HEIGHT // 15), #右下
    "4": (WIDTH // 15, HEIGHT // 2),
    "5": (WIDTH // 2, HEIGHT // 2),
    "6": (14 * WIDTH // 15, HEIGHT // 2),
    "7": (WIDTH // 15, HEIGHT // 15), #左上
    "8": (WIDTH // 2, HEIGHT // 15),
    "9": (14 * WIDTH // 15, HEIGHT // 15), #右上
}

command_sequences = {
    "a": ["9", "3", "5", "9", "1", "3", "6", "9", "4", "7"],
    "b": ["2", "5", "1", "6", "6", "7", "9", "1", "6", "9"],
    "c": ["3", "4", "7", "8", "5", "3", "7", "4", "4", "6"],
    "d": ["6", "4", "7", "6", "1", "3", "5", "9", "1", "2"],
    "e": ["8", "5", "4", "9", "1", "4", "1", "6", "8", "2"],
    "f": ["7", "3", "2", "1", "4", "9", "1", "3", "2", "8"],
    "g": ["2", "7", "4", "2", "2", "7", "8", "9", "6", "9"],
    "h": ["6", "6", "3", "9", "5", "7", "6", "9", "2", "4"],
    "i": ["8", "6", "2", "1", "3", "9", "4", "7", "4", "6"],
    "j": ["3", "8", "5", "3", "2", "6", "2", "3", "2", "9"],
    "k": ["5", "8", "3", "6", "9", "7", "4", "6", "6", "4"],
    "l": ["9", "2", "5", "1", "1", "5", "1", "2", "3", "7"],
    "m": ["6", "5", "9", "6", "4", "1", "5", "9", "4", "8"],
    "n": ["7", "8", "1", "5", "8", "2", "6", "9", "3", "2"], 
    "o": ["1", "2", "3", "4", "5", "6", "7", "8", "4", "9"],
}

selected_sequence = None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            key = event.unicode.lower()
            if key in command_sequences:
                selected_sequence = command_sequences[key]
                running = False

for command in selected_sequence:
    screen.fill(WHITE)
    pygame.draw.circle(screen, GREEN, center, RADIUS)
    pygame.display.flip()
    sleep(3)

    if command in positions:
        screen.fill(WHITE)
        pygame.draw.circle(screen, RED, positions[command], RADIUS)
        pygame.display.flip()
        sleep(2)

screen.fill(WHITE)
pygame.draw.circle(screen, GREEN, center, RADIUS)
pygame.display.flip()
sleep(3)

pygame.quit()
