# 365-scalar.py - Orbital clock showing 365’s dual role as scaling factor and conversion unit. 
#      Independent cycles converging numerically, not via transformation.
#      Earth’s rhythms as the non-arbitrary root, with a probabilistic glow for resonance.
__author__ = 'Forest Mars'
__version__ = '1.0.0' 
__all__ = []

import pygame
import math

# Initialize Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cosmic Clock: 6585.3 Harmonic Trick")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SILVER = (192, 192, 192)  # Lunar Saros
GOLD = (255, 215, 0)      # Earth-solar year
GLOW = (255, 100, 100)    # Alignment highlight

# Clock parameters
center = (width // 2, height // 2)
radius = 250
font = pygame.font.SysFont("arial", 18)

# Astronomical constants (in days)
SAROS_CYCLE = 6585.321  # Saros cycle (lunar rhythm)
SOLAR_YEAR = 365.2422   # Tropical year (Earth-solar rhythm)
LONG_TERM_CYCLE = 6585.3 * SOLAR_YEAR  # Solar-lunar cycle (days)

# Animation scaling: 1 second = 100 years
TIME_SCALE = 100 * SOLAR_YEAR / 1000  # Days per millisecond

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

    # Update time
    time_days += TIME_SCALE * clock.get_time()

    # Calculate hand angles (radians, clockwise from 12 o'clock)
    saros_angle = (time_days / SAROS_CYCLE * 2 * math.pi) % (2 * math.pi)
    year_angle = (time_days / SOLAR_YEAR * 2 * math.pi) % (2 * math.pi)

    # Clear screen
    screen.fill(BLACK)

    # Draw clock face
    pygame.draw.circle(screen, WHITE, center, radius, 2)
    pygame.draw.line(screen, WHITE, (center[0], center[1] - radius),
                     (center[0], center[1] - radius + 20), 3)

    # Draw Saros hand (lunar, 6585.321 days)
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

    # Draw year hand (Earth-solar, 365.2422 days)
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

    # Pulsating glow for alignment
    if abs(time_days - LONG_TERM_CYCLE) < SOLAR_YEAR:
        glow_alpha = 128 + 128 * math.sin(pygame.time.get_ticks() / 200)
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*GLOW, int(glow_alpha)), center, radius + 10, 5)
        screen.blit(surf, (0, 0))

    # Draw text
    time_years = time_days / SOLAR_YEAR
    text = font.render(f"Time: {time_years:.1f} years", True, WHITE)
    screen.blit(text, (10, 10))
    caption = font.render("6585.3 days (Saros) = 6585.3 years (solar-lunar)", True, WHITE)
    screen.blit(caption, (10, height - 120))
    caption2 = font.render("Why? 365 Saros cycles ≈ 365 days/year", True, WHITE)
    screen.blit(caption2, (10, height - 90))
    caption3 = font.render("Harmonic trick: 365 scales and converts", True, WHITE)
    screen.blit(caption3, (10, height - 60))
    caption4 = font.render("Rooted in Earth's rhythms", True, WHITE)
    screen.blit(caption4, (10, height - 30))

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()