
# dual-clock_.py - Constrasts Earth’s scalar match with the counterfactual’s failure, using two clocks and Fourier insets.
__author__ = 'Forest Mars'
__version__ = '1.0.0' 
__all__ = []

import pygame
import math
import numpy as np

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cosmic Clocks: The Approximation’s Triumph and Fall")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SILVER = (192, 192, 192)
GOLD = (255, 215, 0)
GLOW = (255, 100, 100)
BLUE = (100, 100, 255)

center1 = (200, 300)
center2 = (600, 300)
radius = 150
font = pygame.font.SysFont("arial", 12)
small_font = pygame.font.SysFont("arial", 10)

SAROS_CYCLE = 6585.321
SOLAR_YEAR = 365.2422
LONG_TERM_CYCLE1 = 6585.3 * SOLAR_YEAR
ECLIPSE_CYCLE = 5000
COUNTER_YEAR = 510
LONG_TERM_CYCLE2 = 500 * COUNTER_YEAR

TIME_SCALE = 100 * SOLAR_YEAR / 1000

inset_x1, inset_y1 = 50, 50
inset_x2, inset_y2 = 600, 50
inset_w, inset_h = 100, 80
earth_freqs = [1/29.53059, 1/27.21222, 1/27.55455, 1/6585.321]
counter_freqs = [1/50.0, 1/48.0, 1/49.0, 1/5000]
max_time = 7000
samples = 1000

running = True
time_days = 0
trail_saros = []
trail_year1 = []
trail_eclipse = []
trail_year2 = []
glow_alpha1 = 0
glow_alpha2 = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            pygame.image.save(screen, "cosmic_clocks.png")

    time_days += TIME_SCALE * clock.get_time()

    saros_angle = (time_days / SAROS_CYCLE * 2 * math.pi) % (2 * math.pi)
    year1_angle = (time_days / SOLAR_YEAR * 2 * math.pi) % (2 * math.pi)
    eclipse_angle = (time_days / ECLIPSE_CYCLE * 2 * math.pi) % (2 * math.pi)
    year2_angle = (time_days / COUNTER_YEAR * 2 * math.pi) % (2 * math.pi)

    screen.fill(BLACK)

    pygame.draw.circle(screen, WHITE, center1, radius, 2)
    pygame.draw.line(screen, WHITE, (center1[0], center1[1] - radius),
                     (center1[0], center1[1] - radius + 15), 3)
    saros_end = (center1[0] + radius * math.sin(saros_angle),
                 center1[1] - radius * math.cos(saros_angle))
    pygame.draw.line(screen, SILVER, center1, saros_end, 5)
    trail_saros.append(saros_end)
    if len(trail_saros) > 50:
        trail_saros.pop(0)
    for i, pos in enumerate(trail_saros):
        alpha = i / len(trail_saros) * 255
        surf = pygame.Surface((4, 4))
        surf.set_alpha(alpha)
        pygame.draw.circle(surf, SILVER, (2, 2), 2)
        screen.blit(surf, (int(pos[0]) - 2, int(pos[1]) - 2))

    year1_end = (center1[0] + radius * 0.8 * math.sin(year1_angle),
                 center1[1] - radius * 0.8 * math.cos(year1_angle))
    pygame.draw.line(screen, GOLD, center1, year1_end, 3)
    trail_year1.append(year1_end)
    if len(trail_year1) > 100:
        trail_year1.pop(0)
    for i, pos in enumerate(trail_year1):
        alpha = i / len(trail_year1) * 255
        surf = pygame.Surface((3, 3))
        surf.set_alpha(alpha)
        pygame.draw.circle(surf, GOLD, (1, 1), 1)
        screen.blit(surf, (int(pos[0]) - 1, int(pos[1]) - 1))

    if abs(time_days - LONG_TERM_CYCLE1) < SOLAR_YEAR:
        glow_alpha1 = 128 + 128 * math.sin(pygame.time.get_ticks() / 200)
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*GLOW, int(glow_alpha1)), center1, radius + 10, 5)
        screen.blit(surf, (0, 0))

    pygame.draw.circle(screen, WHITE, center2, radius, 2)
    pygame.draw.line(screen, WHITE, (center2[0], center2[1] - radius),
                     (center2[0], center2[1] - radius + 15), 3)
    eclipse_end = (center2[0] + radius * math.sin(eclipse_angle),
                   center2[1] - radius * math.cos(eclipse_angle))
    pygame.draw.line(screen, SILVER, center2, eclipse_end, 5)
    trail_eclipse.append(eclipse_end)
    if len(trail_eclipse) > 50:
        trail_eclipse.pop(0)
    for i, pos in enumerate(trail_eclipse):
        alpha = i / len(trail_eclipse) * 255
        surf = pygame.Surface((4, 4))
        surf.set_alpha(alpha)
        pygame.draw.circle(surf, SILVER, (2, 2), 2)
        screen.blit(surf, (int(pos[0]) - 2, int(pos[1]) - 2))

    year2_end = (center2[0] + radius * 0.8 * math.sin(year2_angle),
                 center2[1] - radius * 0.8 * math.cos(year2_angle))
    pygame.draw.line(screen, GOLD, center2, year2_end, 3)
    trail_year2.append(year2_end)
    if len(trail_year2) > 100:
        trail_year2.pop(0)
    for i, pos in enumerate(trail_year2):
        alpha = i / len(trail_year2) * 255
        surf = pygame.Surface((3, 3))
        surf.set_alpha(alpha)
        pygame.draw.circle(surf, GOLD, (1, 1), 1)
        screen.blit(surf, (int(pos[0]) - 1, int(pos[1]) - 1))

    if abs(time_days - LONG_TERM_CYCLE2) < COUNTER_YEAR:
        glow_alpha2 = 128 + 128 * math.sin(pygame.time.get_ticks() / 200)
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*GLOW, int(glow_alpha2)), center2, radius + 10, 5)
        screen.blit(surf, (0, 0))

    pygame.draw.rect(screen, WHITE, (inset_x1, inset_y1, inset_w, inset_h), 1)
    t = np.linspace(0, max_time, samples)
    signal1 = sum(np.cos(2 * np.pi * f * t) for f in earth_freqs)
    signal1 = (signal1 / max(abs(signal1))) * (inset_h / 2 - 10) + inset_h / 2
    points1 = [(inset_x1 + i * inset_w / samples, inset_y1 + signal1[i]) for i in range(samples)]
    pygame.draw.lines(screen, BLUE, False, points1, 1)

    pygame.draw.rect(screen, WHITE, (inset_x2, inset_y2, inset_w, inset_h), 1)
    signal2 = sum(np.cos(2 * np.pi * f * t) for f in counter_freqs)
    signal2 = (signal2 / max(abs(signal2))) * (inset_h / 2 - 10) + inset_h / 2
    points2 = [(inset_x2 + i * inset_w / samples, inset_y2 + signal2[i]) for i in range(samples)]
    pygame.draw.lines(screen, BLUE, False, points2, 1)

    time_years = time_days / SOLAR_YEAR
    text = font.render(f"Time: {time_years:.1f} Earth years", True, WHITE)
    screen.blit(text, (10, 10))
    caption = font.render("Earth: 365 ≈ 365.2422 yields 6585.3 match.", True, WHITE)
    screen.blit(caption, (10, height - 180))
    caption2 = font.render("Counterfactual: 51 ≠ 510 breaks scalar at 500.", True, WHITE)
    screen.blit(caption2, (10, height - 150))
    caption3 = font.render("A single rotation reveals the fluke.", True, WHITE)
    screen.blit(caption3, (10, height - 120))
    caption4 = font.render("Mathematics shrugs, unimpressed.", True, WHITE)
    screen.blit(caption4, (10, height - 90))
    caption5 = small_font.render("Note: Earth’s luck is not a law.", True, WHITE)
    screen.blit(caption5, (10, height - 60))
    caption6 = small_font.render("The cosmos carries on regardless.", True, WHITE)
    screen.blit(caption6, (10, height - 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()