import pygame as pg
import sys, time
from bird import Bird
from pipe import Pipe

pg.init()

class Game:
    def __init__(self):
        # Setting window config
        self.width = 600
        self.height = 768
        self.scale_factor = 1.5
        self.win = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.move_speed = 250
        self.bird = Bird(self.scale_factor)

        self.is_enter_pressed = False
        self.pipes = []
        self.pipe_generate_counter = 71
        self.setUpBgAndGround()
        self.game_over = False  # Flag for game over state
        self.score = 0  # Current score
        self.high_score = 0  # High score

        self.gameLoop()

    def gameLoop(self):
        last_time = time.time()
        while True:
            # Calculate delta time
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.is_enter_pressed = True
                        self.bird.update_on = True
                    if event.key == pg.K_SPACE and self.is_enter_pressed and not self.game_over:
                        self.bird.flap(dt)
                    if event.key == pg.K_r and self.game_over:  # Restart game on 'R' key
                        self.resetGame()

            if not self.game_over:
                self.updateEverything(dt)
                self.checkCollisions()
            self.drawEverything()

            pg.display.update()
            self.clock.tick(60)

    def checkCollisions(self):
        if len(self.pipes):
            if self.bird.rect.bottom > 568:
                self.bird.update_on = False
                self.is_enter_pressed = False
                self.game_over = True  # End the game when hitting the ground
            if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
                self.bird.rect.colliderect(self.pipes[0].rect_up)):
                self.game_over = True  # End the game on pipe collision
            else:
                # Update score when passing a pipe
                if self.pipes[0].rect_up.right < self.bird.rect.left:
                    self.score += 1
                    self.pipes.pop(0)  # Remove the passed pipe
                    if self.score > self.high_score:
                        self.high_score = self.score  # Update high score

    def updateEverything(self, dt):
        if self.is_enter_pressed:
            # Moving the ground
            self.ground1_rect.x -= int(self.move_speed * dt)
            self.ground2_rect.x -= int(self.move_speed * dt)

            if self.ground1_rect.right < 0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right < 0:
                self.ground2_rect.x = self.ground1_rect.right

            # Generating pipes
            if self.pipe_generate_counter > 70:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_generate_counter = 0

            self.pipe_generate_counter += 1

            # Moving the pipes
            for pipe in self.pipes:
                pipe.update(dt)

            # Removing pipes if out of screen
            if len(self.pipes) != 0:
                if self.pipes[0].rect_up.right < 0:
                    self.pipes.pop(0)

        # Moving the bird
        self.bird.update(dt)

    def drawEverything(self):
        self.win.blit(self.bg_img, (0, -300))
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)

        # Draw the current score (top-left)
        self.drawScore()

        if self.game_over:
            self.drawGameOverScreen()

    def drawScore(self):
        font = pg.font.SysFont("Arial", 30)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.win.blit(score_text, (10, 10))  # Top-left corner

        high_score_text = font.render(f"High Score: {self.high_score}", True, (0, 0, 255))
        self.win.blit(high_score_text, (self.width - 180, 10))  # Top-right corner

    def drawGameOverScreen(self):
        # Draw the "Game Over" text
        font = pg.font.SysFont("Arial", 50)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.win.blit(game_over_text, text_rect)

        # Draw the restart instruction
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        restart_text_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.win.blit(restart_text, restart_text_rect)

    def setUpBgAndGround(self):
        # Loading images for bg and ground
        self.bg_img = pg.transform.scale_by(pg.image.load("assets/bg.png").convert(), self.scale_factor)
        self.ground1_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor)
        self.ground2_img = pg.transform.scale_by(pg.image.load("assets/ground.png").convert(), self.scale_factor)

        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = 568
        self.ground2_rect.y = 568

    def resetGame(self):
        # Resetting game variables
        self.is_enter_pressed = False
        self.game_over = False
        self.score = 0  # Reset score
        self.bird = Bird(self.scale_factor)
        self.pipes.clear()
        self.pipe_generate_counter = 71
        self.setUpBgAndGround()

game = Game()

