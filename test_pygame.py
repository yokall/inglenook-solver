import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("WSL2 Pygame Test")

# Test audio init
try:
    pygame.mixer.init()
    print("Audio OK:", pygame.mixer.get_init())
except pygame.error as e:
    print("Audio failed (non-fatal for now):", e)

print("Display driver:", pygame.display.get_driver())
print("Pygame version:", pygame.version.ver)

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    screen.fill((30, 30, 60))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()