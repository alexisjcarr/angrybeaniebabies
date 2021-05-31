import pygame
import os


pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Angry Beanie Babies")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

OPENER = pygame.mixer.Sound('assets/opener.mp3')
BULLET_HIT_SOUND = pygame.mixer.Sound('assets/hit.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('assets/bullet.mp3')
WINNER = pygame.mixer.Sound('assets/winner.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
BEAR_WIDTH, BEAR_HEIGHT = 55, 40

LEFT_BEAR_HIT = pygame.USEREVENT + 1
RIGHT_BEAR_HIT = pygame.USEREVENT + 2

LEFT_BEAR = pygame.image.load(
    os.path.join('Assets', 'Teddy_32x32_sand_heart_stand_R.png'))

RIGHT_BEAR = pygame.image.load(
    os.path.join('Assets', 'Teddy_32x32_sand_heart_stand_L.png'))

BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'background.jpeg')), (WIDTH, HEIGHT))


class Game:
    def _draw_window(
        self, right_bear, left_bear, right_bear_bullets,
        left_bear_bullets, right_bear_health, left_bear_health
    ):
        WIN.blit(BACKGROUND, (0, 0))
        pygame.draw.rect(WIN, BLACK, BORDER)

        right_bear_health_text = HEALTH_FONT.render(
            "Health: " + str(right_bear_health), 1, WHITE)
        left_bear_health_text = HEALTH_FONT.render(
            "Health: " + str(left_bear_health), 1, WHITE)
        WIN.blit(right_bear_health_text, (WIDTH - right_bear_health_text.get_width() - 10, 10))
        WIN.blit(left_bear_health_text, (10, 10))

        WIN.blit(LEFT_BEAR, (left_bear.x, left_bear.y))
        WIN.blit(RIGHT_BEAR, (right_bear.x, right_bear.y))

        for bullet in right_bear_bullets:
            pygame.draw.rect(WIN, RED, bullet)

        for bullet in left_bear_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)

        pygame.display.update()

    def _left_bear_handle_movement(self, keys_pressed, left_bear_bear):
        if keys_pressed[pygame.K_a] and left_bear_bear.x - VEL > 0:  # LEFT
            left_bear_bear.x -= VEL
        if keys_pressed[pygame.K_d] and left_bear_bear.x + VEL + left_bear_bear.width < BORDER.x:  # RIGHT
            left_bear_bear.x += VEL
        if keys_pressed[pygame.K_w] and left_bear_bear.y - VEL > 0:  # UP
            left_bear_bear.y -= VEL
        if keys_pressed[pygame.K_s] and left_bear_bear.y + VEL + left_bear_bear.height < HEIGHT - 15:  # DOWN
            left_bear_bear.y += VEL

    def _right_bear_handle_movement(self, keys_pressed, right_bear_bear):
        if keys_pressed[pygame.K_LEFT] and right_bear_bear.x - VEL > BORDER.x + BORDER.width:  # LEFT
            right_bear_bear.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and right_bear_bear.x + VEL + right_bear_bear.width < WIDTH:  # RIGHT
            right_bear_bear.x += VEL
        if keys_pressed[pygame.K_UP] and right_bear_bear.y - VEL > 0:  # UP
            right_bear_bear.y -= VEL
        if keys_pressed[pygame.K_DOWN] and right_bear_bear.y + VEL + right_bear_bear.height < HEIGHT - 15:  # DOWN
            right_bear_bear.y += VEL

    def _handle_bullets(self, left_bear_bullets, right_bear_bullets, left_bear, right_bear):
        for bullet in left_bear_bullets:
            bullet.x += BULLET_VEL
            if right_bear.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RIGHT_BEAR_HIT))
                left_bear_bullets.remove(bullet)
            elif bullet.x > WIDTH:
                left_bear_bullets.remove(bullet)

        for bullet in right_bear_bullets:
            bullet.x -= BULLET_VEL
            if left_bear.colliderect(bullet):
                pygame.event.post(pygame.event.Event(LEFT_BEAR_HIT))
                right_bear_bullets.remove(bullet)
            elif bullet.x < 0:
                right_bear_bullets.remove(bullet)

    def _draw_winner(self, text):
        WINNER.play()
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                            2, HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(10000)

    def main(self):
        OPENER.play()
        right_bear = pygame.Rect(700, 300, BEAR_WIDTH, BEAR_HEIGHT)
        left_bear = pygame.Rect(100, 300, BEAR_WIDTH, BEAR_HEIGHT)

        right_bear_bullets = []
        left_bear_bullets = []

        right_bear_health = 10
        left_bear_health = 10

        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(left_bear_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(
                            left_bear.x + left_bear.width, left_bear.y + left_bear.height//2 - 2, 10, 5)
                        left_bear_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

                    if event.key == pygame.K_RCTRL and len(right_bear_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(
                            right_bear.x, right_bear.y + right_bear.height//2 - 2, 10, 5)
                        right_bear_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

                if event.type == RIGHT_BEAR_HIT:
                    right_bear_health -= 1
                    BULLET_HIT_SOUND.play()

                if event.type == LEFT_BEAR_HIT:
                    left_bear_health -= 1
                    BULLET_HIT_SOUND.play()

            winner_text = ""
            if right_bear_health <= 0:
                winner_text = "The Bear on the Left Wins!"

            if left_bear_health <= 0:
                winner_text = "The Bear on the Right Wins!"

            if winner_text != "":
                self._draw_winner(winner_text)
                break

            keys_pressed = pygame.key.get_pressed()
            self._left_bear_handle_movement(keys_pressed, left_bear)
            self._right_bear_handle_movement(keys_pressed, right_bear)

            self._handle_bullets(left_bear_bullets, right_bear_bullets, left_bear, right_bear)

            self._draw_window(right_bear, left_bear, right_bear_bullets, left_bear_bullets,
                              right_bear_health, left_bear_health)

        self.main()


if __name__ == "__main__":
    game = Game()
    game.main()
