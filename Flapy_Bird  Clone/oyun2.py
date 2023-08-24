import pygame
import sys
import random

# Pygame başlatılıyor
pygame.init()

# Ekran boyutları
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ekran oluşturuluyor
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Emülatörü")

# Top boyutları
BALL_SIZE = 40
ball_x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
ball_y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
ball_speed = 3

# Yerçekimi ve zıplama
GRAVITY = 0.7
JUMP = -10

# Boru boyutları
PIPE_WIDTH = 80
PIPE_GAP = 200
pipe_x = SCREEN_WIDTH
pipe_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)

clock = pygame.time.Clock()

# Ana döngü
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_y += JUMP

    ball_y += GRAVITY

    # Topun ekran sınırlarına çarpma kontrolü
    if ball_y <= 0:
        ball_y = 0
    if ball_y >= SCREEN_HEIGHT - BALL_SIZE:
        ball_y = SCREEN_HEIGHT - BALL_SIZE

    pipe_x -= ball_speed

    # Borunun ekran dışına çıkması durumunda yeni boru oluşturma
    if pipe_x <= -PIPE_WIDTH:
        pipe_x = SCREEN_WIDTH
        pipe_height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)

    # Çarpışma kontrolü
    if (ball_x + BALL_SIZE > pipe_x and ball_x < pipe_x + PIPE_WIDTH and
            (ball_y < pipe_height or ball_y + BALL_SIZE > pipe_height + PIPE_GAP)):
        pygame.quit()
        sys.exit()

    screen.fill(BLACK)  # Arka planı siyah yap
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))  # Topu çiz
    pygame.draw.rect(screen, WHITE, (pipe_x, 0, PIPE_WIDTH, pipe_height))  # Üst boruyu çiz
    pygame.draw.rect(screen, WHITE, (pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT))  # Alt boruyu çiz

    pygame.display.update()
    clock.tick(60)
