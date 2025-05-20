import pygame
import sys
import argparse

# コマンドライン引数の解析
parser = argparse.ArgumentParser()
parser.add_argument("--speed", type=int, default=5, help="Ball speed (default: 5)")
args = parser.parse_args()

# ゲーム初期化
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("ブロック崩し")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# クラス定義
class Ball:
    def __init__(self, speed=5):
        self.radius = 10
        self.x = 400
        self.y = 500
        self.speed = speed
        self.dx = self.speed
        self.dy = -self.speed

    def move(self):
        self.x += self.dx
        self.y += self.dy

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = 350
        self.y = 550

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= 10
        if direction == "right" and self.x < 700:
            self.x += 10

class Brick:
    def __init__(self, x, y):
        self.width = 75
        self.height = 20
        self.x = x
        self.y = y

class StartScreen:
    def __init__(self):
        self.width = 200
        self.height = 50
        self.x = 300
        self.y = 250

    def draw(self, screen, font):
        pygame.draw.rect(screen, (0, 200, 0), (self.x, self.y, self.width, self.height))
        start_text = font.render("Start Game", True, (0, 0, 0))
        screen.blit(start_text, (self.x + 20, self.y + 10))

# ゲームループ
ball = Ball(speed=args.speed)  # コマンドライン引数で速度を指定可能
paddle = Paddle()
bricks = [Brick(x, y) for x in range(50, 750, 80) for y in range(50, 200, 30)]
score = 0
game_over = False
start_screen = StartScreen()
game_state = "start"  # "start", "playing", "game_over"

def reset_game():
    global ball, paddle, bricks, score, game_over
    ball = Ball(speed=args.speed)  # コマンドライン引数で速度を指定可能
    paddle = Paddle()
    bricks = [Brick(x, y) for x in range(50, 750, 80) for y in range(50, 200, 30)]
    score = 0
    game_over = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # リセットボタン処理
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 350 <= mouse_x <= 450 and 350 <= mouse_y <= 400 and game_over:
                reset_game()
            # ゲーム開始ボタン処理
            if game_state == "start" and start_screen.x <= mouse_x <= start_screen.x + start_screen.width and start_screen.y <= mouse_y <= start_screen.y + start_screen.height:
                game_state = "playing"
        # スペースキーでゲーム開始
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_state == "start":
            game_state = "playing"

    if game_state == "start":
        # ゲーム開始画面描画
        start_screen.draw(screen, font)
    elif game_state == "playing":
        if not game_over:
            # ゲームロジック
            ball.move()
            
            # パドル操作
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move("left")
            if keys[pygame.K_RIGHT]:
                paddle.move("right")

            # ボールとパドルの衝突判定
            if (ball.x > paddle.x and ball.x < paddle.x + paddle.width and
                ball.y - ball.radius < paddle.y + paddle.height and
                ball.y + ball.radius > paddle.y):
                ball.dy = -ball.dy  # ボールの方向を反転

            # ボールとブロックの衝突判定
            for brick in bricks[:]:
                if (ball.x > brick.x and ball.x < brick.x + brick.width and
                    ball.y - ball.radius < brick.y + brick.height and
                    ball.y + ball.radius > brick.y):
                    bricks.remove(brick)
                    score += 10
                    # 跳ね返り処理を修正
                    ball.dy *= -1

            # 画面端との衝突判定
            if ball.x - ball.radius < 0 or ball.x + ball.radius > 800:
                ball.dx *= -1
            if ball.y - ball.radius < 0:
                ball.dy *= -1
            # ゲームオーバー判定（ボールが画面下に落ちた場合）
            if ball.y + ball.radius > 600:
                game_over = True
            # ゲームクリア判定（すべてのブロックを破壊した場合）
            if not game_over and len(bricks) == 0:
                game_over = True

        # 描画
        screen.fill((0, 0, 0))
        
        # ボール描画
        pygame.draw.circle(screen, (255, 255, 255), (int(ball.x), int(ball.y)), ball.radius)
        
        # パドル描画
        pygame.draw.rect(screen, (255, 255, 255), (paddle.x, paddle.y, paddle.width, paddle.height))
        
        # ブロック描画
        for brick in bricks:
            pygame.draw.rect(screen, (255, 0, 0), (brick.x, brick.y, brick.width, brick.height))

        # スコア表示
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # リセットボタン描画（ゲームオーバー時のみ）
        if game_over:
            if len(bricks) == 0:
                game_over_text = font.render("Congratulations!", True, (0, 255, 0))
            else:
                game_over_text = font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (300, 300))
            
            # リセット/ゲーム開始ボタン描画
            pygame.draw.rect(screen, (0, 200, 0), (350, 350, 100, 50))
            if len(bricks) == 0:
                reset_text = font.render("Start Game", True, (0, 0, 0))
            else:
                reset_text = font.render("Restart", True, (0, 0, 0))
            screen.blit(reset_text, (360, 360))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
