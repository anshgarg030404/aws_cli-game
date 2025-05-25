#!/usr/bin/env python3
"""
2D Platformer Game
A complete platformer game built with Pygame featuring player movement,
enemies, platforms, coins, and multiple game states.
"""
import os
import sys
import random
import pygame
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()  # For sound effects and music

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Platformer Adventure"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SKYBLUE = (135, 206, 235)
BROWN = (139, 69, 19)

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.8
PLAYER_JUMP = -16

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
WIN = 3

# Asset directories
game_dir = os.path.dirname(__file__)
img_dir = os.path.join(game_dir, 'assets', 'images')
sound_dir = os.path.join(game_dir, 'assets', 'sounds')

# Create directories if they don't exist
os.makedirs(os.path.join(game_dir, 'assets', 'images'), exist_ok=True)
os.makedirs(os.path.join(game_dir, 'assets', 'sounds'), exist_ok=True)

# Set up assets
font_name = pygame.font.match_font('arial')

class Player(pygame.sprite.Sprite):
    """
    Player class representing the main character controlled by the user.
    Handles movement, jumping, and collision detection.
    """
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((30, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.pos = pygame.math.Vector2(100, SCREEN_HEIGHT - 200)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.facing_right = True
        self.jumping = False
        self.on_ground = False
        self.lives = 3
        
        # Animation frames would go here in a more complete implementation
        # self.walking_frames_r = []
        # self.walking_frames_l = []
        # self.current_frame = 0
        # self.last_update = 0

    def jump(self):
        """Make the player jump if standing on a platform"""
        # Only jump if standing on a platform
        self.rect.y += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = PLAYER_JUMP
            # Play jump sound
            self.game.jump_sound.play()

    def update(self):
        """Update player position and state"""
        self.acc = pygame.math.Vector2(0, PLAYER_GRAVITY)
        
        # Check for keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
            self.facing_right = True
            
        # Apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        
        # Equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        
        # Wrap around the screen (optional)
        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
            
        # Update rect position
        self.rect.midbottom = self.pos
        
        # Check if player fell off the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.game.player_die()

    def animate(self):
        """
        Handle player animations
        This is a placeholder for animation logic
        """
        pass

class Platform(pygame.sprite.Sprite):
    """
    Platform class for surfaces the player can stand on
    """
    def __init__(self, x, y, width, height, is_moving=False, move_range=0, move_speed=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_moving = is_moving
        self.move_range = move_range
        self.move_speed = move_speed
        self.start_pos = x
        self.direction = 1  # 1 for right, -1 for left

    def update(self):
        """Update platform position if it's a moving platform"""
        if self.is_moving:
            self.rect.x += self.move_speed * self.direction
            if abs(self.rect.x - self.start_pos) > self.move_range:
                self.direction *= -1  # Reverse direction

class Enemy(pygame.sprite.Sprite):
    """
    Enemy class for obstacles that can harm the player
    """
    def __init__(self, x, y, patrol_range=100, speed=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.patrol_range = patrol_range
        self.speed = speed
        self.start_pos = x
        self.direction = 1  # 1 for right, -1 for left

    def update(self):
        """Update enemy position based on patrol pattern"""
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.start_pos) > self.patrol_range:
            self.direction *= -1  # Reverse direction

class Coin(pygame.sprite.Sprite):
    """
    Coin class for collectible items that increase score
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    """
    Main game class that manages game state, sprites, and the game loop
    """
    def __init__(self):
        """Initialize game window, clock, and sprites"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = MENU
        self.score = 0
        self.level = 1
        
        # Create dummy sounds to avoid errors
        self.jump_sound = pygame.mixer.Sound(buffer=bytearray([0] * 44100))
        self.coin_sound = pygame.mixer.Sound(buffer=bytearray([0] * 44100))
        self.death_sound = pygame.mixer.Sound(buffer=bytearray([0] * 44100))
        
        # No background music for now to avoid errors
        # pygame.mixer.music.load(os.path.join(sound_dir, 'background.wav'))
        # pygame.mixer.music.set_volume(0.5)

    def create_placeholder_sounds(self):
        """Create placeholder sound files if they don't exist"""
        # This function is no longer needed as we're using in-memory sounds
        pass

    def new_game(self):
        """Set up for a new game"""
        self.score = 0
        self.game_state = PLAYING
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        
        # Create player
        self.player = Player(self)
        self.all_sprites.add(self.player)
        
        # Create platforms
        self.create_level(self.level)
        
        # Start background music (commented out to avoid errors)
        # pygame.mixer.music.play(loops=-1)

    def create_level(self, level):
        """Create platforms, enemies, and coins for the current level"""
        # Ground platform
        ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
        self.all_sprites.add(ground)
        self.platforms.add(ground)
        
        # Add platforms based on level
        if level == 1:
            platform_list = [
                (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),  # Ground
                (100, 400, 150, 20),
                (300, 300, 100, 20),
                (500, 200, 150, 20),
                (250, 120, 100, 20),
                (650, 350, 100, 20, True, 100, 1)  # Moving platform
            ]
            
            enemy_list = [
                (300, 280, 80),
                (500, 180, 100)
            ]
            
            coin_list = [
                (130, 370),
                (330, 270),
                (530, 170),
                (280, 90),
                (680, 320)
            ]
        else:
            # More complex levels could be defined here
            platform_list = [
                (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),  # Ground
                (100, 450, 100, 20),
                (300, 350, 100, 20),
                (500, 250, 100, 20),
                (200, 150, 100, 20),
                (400, 100, 100, 20),
                (600, 150, 100, 20),
                (100, 250, 100, 20, True, 150, 2)  # Moving platform
            ]
            
            enemy_list = [
                (300, 330, 80),
                (500, 230, 80),
                (200, 130, 80),
                (600, 130, 80)
            ]
            
            coin_list = [
                (130, 420),
                (330, 320),
                (530, 220),
                (230, 120),
                (430, 70),
                (630, 120),
                (130, 220)
            ]
        
        # Create platforms
        for plat in platform_list:
            if len(plat) > 5:  # Moving platform
                p = Platform(plat[0], plat[1], plat[2], plat[3], plat[4], plat[5], plat[6])
            else:  # Static platform
                p = Platform(plat[0], plat[1], plat[2], plat[3])
            self.all_sprites.add(p)
            self.platforms.add(p)
        
        # Create enemies
        for e in enemy_list:
            enemy = Enemy(e[0], e[1], e[2])
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
        
        # Create coins
        for c in coin_list:
            coin = Coin(c[0], c[1])
            self.all_sprites.add(coin)
            self.coins.add(coin)

    def run(self):
        """Game loop"""
        while self.running:
            self.clock.tick(FPS)
            self.events()
            
            if self.game_state == PLAYING:
                self.update()
            
            self.draw()

    def events(self):
        """Process game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                if self.game_state == PLAYING:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.player.jump()
                
                elif self.game_state == MENU:
                    if event.key == pygame.K_RETURN:
                        self.new_game()
                
                elif self.game_state == GAME_OVER or self.game_state == WIN:
                    if event.key == pygame.K_RETURN:
                        self.game_state = MENU

    def update(self):
        """Update all sprites and check for collisions"""
        self.all_sprites.update()
        
        # Check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                
                if self.player.pos.y < lowest.rect.centery:
                    self.player.pos.y = lowest.rect.top + 1
                    self.player.vel.y = 0
                    self.player.jumping = False
        
        # Check for coin collisions
        coin_hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in coin_hits:
            self.score += 10
            self.coin_sound.play()
            
            # Check for win condition
            if len(self.coins) == 0:
                self.game_state = WIN
        
        # Check for enemy collisions
        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if enemy_hits:
            self.player_die()

    def player_die(self):
        """Handle player death"""
        self.death_sound.play()
        self.player.lives -= 1
        
        if self.player.lives <= 0:
            self.game_state = GAME_OVER
        else:
            # Reset player position
            self.player.pos = pygame.math.Vector2(100, SCREEN_HEIGHT - 200)
            self.player.vel = pygame.math.Vector2(0, 0)

    def draw(self):
        """Draw everything to the screen"""
        self.screen.fill(SKYBLUE)
        
        if self.game_state == PLAYING:
            self.all_sprites.draw(self.screen)
            self.draw_text(f"Score: {self.score}", 22, WHITE, 10, 10)
            self.draw_text(f"Lives: {self.player.lives}", 22, WHITE, SCREEN_WIDTH - 100, 10)
        
        elif self.game_state == MENU:
            self.draw_menu()
        
        elif self.game_state == GAME_OVER:
            self.draw_game_over()
        
        elif self.game_state == WIN:
            self.draw_win_screen()
        
        pygame.display.flip()

    def draw_text(self, text, size, color, x, y):
        """Helper function to draw text on the screen"""
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_menu(self):
        """Draw the start menu"""
        self.screen.fill(SKYBLUE)
        self.draw_text(TITLE, 48, WHITE, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 4)
        self.draw_text("Arrow keys to move, Space to jump", 22, WHITE, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2)
        self.draw_text("Collect all coins to win!", 22, WHITE, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 40)
        self.draw_text("Press Enter to start", 22, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT * 3 // 4)

    def draw_game_over(self):
        """Draw the game over screen"""
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, RED, SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 4)
        self.draw_text(f"Final Score: {self.score}", 22, WHITE, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2)
        self.draw_text("Press Enter to return to menu", 22, WHITE, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT * 3 // 4)

    def draw_win_screen(self):
        """Draw the win screen"""
        self.screen.fill(SKYBLUE)
        self.draw_text("YOU WIN!", 48, YELLOW, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 4)
        self.draw_text(f"Final Score: {self.score}", 22, WHITE, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2)
        self.draw_text("Press Enter to return to menu", 22, WHITE, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT * 3 // 4)

# Main game execution
if __name__ == "__main__":
    game = Game()
    game.game_state = MENU
    game.run()
    pygame.quit()
    sys.exit()
