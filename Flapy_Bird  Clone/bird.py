import pygame
import sys
import random

pygame.init()

# Ekran boyutları
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Kuş boyutları
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
BIRD_X = 100
BIRD_IMG = pygame.image.load("bird.png")  # Kuş resmi yükleniyor
BIRD_IMG = pygame.transform.scale(BIRD_IMG, (BIRD_WIDTH, BIRD_HEIGHT))  # Kuş resmi boyutlandırılıyor

# Yerçekimi
GRAVITY = 0.5
JUMP = -8

# Boru boyutları
PIPE_WIDTH = 50
MIN_PIPE_GAP = BIRD_HEIGHT * 2
MAX_PIPE_GAP = BIRD_HEIGHT * 3
PIPE_VELOCITY = -5

# Boru görüntüleri
UP_PIPE_IMG = pygame.image.load("ust.png")
DOWN_PIPE_IMG = pygame.image.load("alt.png")
UP_PIPE_IMG = pygame.transform.scale(UP_PIPE_IMG, (PIPE_WIDTH, SCREEN_HEIGHT // 2))  # Boru yüksekliği boyunca ölçeklenir
DOWN_PIPE_IMG = pygame.transform.scale(DOWN_PIPE_IMG, (PIPE_WIDTH, SCREEN_HEIGHT // 2))

# Arka plan görüntüsü
BACKGROUND_IMG = pygame.image.load("arka.png")
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Font
FONT = pygame.font.Font(None, 36)
SCORE = 0

# Oyun başlangıç
def game_start():
    global SCORE
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")

    bird = pygame.Rect(BIRD_X, SCREEN_HEIGHT // 2, BIRD_WIDTH, BIRD_HEIGHT)
    pipes = []

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.y += JUMP

        # Yerçekimi etkisi
        bird.y += GRAVITY

        screen.blit(BACKGROUND_IMG, (0, 0))  # Arka planı çiz

        # Kuş resmini çiz
        screen.blit(BIRD_IMG, (bird.x, bird.y))

        # Boruları hareket ettirme ve yeni boru oluşturma
        for pipe in pipes:
            pipe[0].x += PIPE_VELOCITY
            pipe[1].x += PIPE_VELOCITY
            screen.blit(UP_PIPE_IMG, pipe[0])
            screen.blit(DOWN_PIPE_IMG, pipe[1])

        if len(pipes) == 0 or pipes[-1][0].x <= SCREEN_WIDTH - 200:
            create_pipe(pipes)

        # Boru geçişi kontrolü ve sayaç güncellemesi
        if pipes and pipes[0][0].x + PIPE_WIDTH < bird.x:
            pipes.pop(0)
            SCORE += 1

        # Boru çarpışma kontrolü
        for pipe in pipes:
            if bird.colliderect(pipe[0]) or bird.colliderect(pipe[1]):
                game_over()

        # Sayaç metnini ekrana yazdırma
        score_text = FONT.render(f"Score: {SCORE}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()  # Ekranı güncelleme
        clock.tick(30)

# Yeni bir boru oluştur
def create_pipe(pipes):
    gap_y = random.randint(BIRD_HEIGHT * 2, SCREEN_HEIGHT - MIN_PIPE_GAP - BIRD_HEIGHT * 2)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, gap_y - BIRD_HEIGHT)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, gap_y + MIN_PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT // 2 - (gap_y + MIN_PIPE_GAP))
    pipes.append((top_pipe, bottom_pipe))

# Oyun bitti ekranı
def game_over():
    global SCORE
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    restart_text = font.render("Press R to Restart", True, BLACK)
    restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    SCORE = 0  # Skoru sıfırla
                    game_start()

        screen.fill(WHITE)
        screen.blit(text, text_rect)
        screen.blit(restart_text, restart_text_rect)

        pygame.display.update()

# Oyunu başlat
game_start()
