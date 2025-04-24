# scalar-match_.py - Orbital clock visualization of scalar match, the Moon’s periods, and the universal trick
__author__ = 'Forest Mars'
__version__ = '1.0.0' 
__all__ = []

import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cosmic Clock: 6585.3, the Universal Trick")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SILVER = (192, 192, 192)
GOLD = (255, 215, 0)
GLOW = (255, 100, 100)
BLUE = (100, 100, 255)

# Clock parameters
center = (width // 2, height // 2)
radius = 250
font = pygame.font.SysFont("arial", 14)
small_font = pygame.font.SysFont("arial", 12)

# Astronomical constants (in days)
SAROS_CYCLE = 6585.321
SOLAR_YEAR = 365.2422
LONG_TERM_CYCLE = 6585.3 * SOLAR_YEAR

# Animation scaling: 1 second = 100 years
TIME_SCALE = 100 * SOLAR_YEAR / 1000

# Fourier inset
inset_x, inset_y = 600, 50
inset_w, inset_h = 150, 100
frequencies = [1/29.53059, 1/27.21222, 1/27.55455, 1/6585.321]
max_time = 7000
samples = 1000

# Main loop
running = True
time_days = 0
trail_saros = []
trail_year = []
glow_alpha = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            pygame.image.save(screen, "cosmic_clock.png")

    time_days += TIME_SCALE * clock.get_time()

    saros_angle = (time_days / SAROS_CYCLE * 2 * math.pi) % (2 * math.pi)
    year_angle = (time_days / SOLAR_YEAR * 2 * math.pi) % (2 * math.pi)

    screen.fill(BLACK)

    pygame.draw.circle(screen, WHITE, center, radius, 2)
    pygame.draw.line(screen, WHITE, (center[0], center[1] - radius),
                     (center[0], center[1] - radius + 20), 3)

    saros_end = (center[0] + radius * math.sin(saros_angle),
                 center[1] - radius * math.cos(saros_angle))
    pygame.draw.line(screen, SILVER, center, saros_end, 6)
    trail_saros.append(saros_end)
    if len(trail_saros) > 50:
        trail_saros.pop(0)
    for i, pos in enumerate(trail_saros):
        alpha = i / len(trail_saros) * 255
        surf = pygame.Surface((5, 5))
        surf.set_alpha(alpha)
        pygame.draw.circle(surf, SILVER, (2, 2), 2)
        screen.blit(surf, (int(pos[0]) - 2, int(pos[1]) - 2))

    year_end = (center[0] + radius * 0.8 * math.sin(year_angle),
                center[1] - radius * 0.8 * math.cos(year_angle))
    pygame.draw.line(screen, GOLD, center, year_end, 3)
    trail_year.append(year_end)
    if len(trail_year) > 100:
        trail_year.pop(0)
    for i, pos in enumerate(trail_year):
        alpha = i / len(trail_year) * 255
        surf = pygame.Surface((3, 3))
        surf.set_alpha(alpha)
        pygame.draw.circle(surf, GOLD, (1, 1), 1)
        screen.blit(surf, (int(pos[0]) - 1, int(pos[1]) - 1))

    if abs(time_days - LONG_TERM_CYCLE) < SOLAR_YEAR:
        glow_alpha = 128 + 128 * math.sin(pygame.time.get_ticks() / 200)
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*GLOW, int(glow_alpha)), center, radius + 10, 5)
        screen.blit(surf, (0, 0))

    pygame.draw.rect(screen, WHITE, (inset_x, inset_y, inset_w, inset_h), 1)
    t = np.linspace(0, max_time, samples)
    signal = sum(np.cos(2 * np.pi * f * t) for f in frequencies)
    signal = (signal / max(abs(signal))) * (inset_h / 2 - 10) + inset_h / 2
    points = [(inset_x + i * inset_w / samples, inset_y + signal[i]) for i in range(samples)]
    if len(points) > 1:
        pygame.draw.lines(screen, BLUE, False, points, 1)

    time_years = time_days / SOLAR_YEAR
    text = font.render(f"Time: {time_years:.1f} years", True, WHITE)
    screen.blit(text, (10, 10))
    caption = font.render("6585.3 days (Saros) = 6585.3 years (solar-lunar),", True, WHITE)
    screen.blit(caption, (10, height - 180))
    caption2 = font.render("because 365 counts cycles and converts days to", True, WHITE)
    screen.blit(caption2, (10, height - 150))
    caption3 = font.render("years, a trick every star-planet-moon trio knows", True, WHITE)
    screen.blit(caption3, (10, height - 120))
    caption4 = font.render("if its eclipse cycle beats the year, half us, half math", True, WHITE)
    screen.blit(caption4, (10, height - 90))
    caption5 = small_font.render("*Saros sings early: 6585.3 days, not 22,000, thanks", True, WHITE)
    screen.blit(caption5, (10, height - 60))
    caption6 = small_font.render("to the Moon’s synodic, draconic, anomalistic hum", True, WHITE)
    screen.blit(caption6, (10, height - 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()