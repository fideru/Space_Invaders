import pygame
from pygame.sprite import Sprite


################# - Settings - #################
# class for game settings definition.
class Settings:

    def __init__(self):
        # Screen Settings
        self.screen_width = 1180
        self.screen_height = 620
        self.bg_color = (0, 100, 125)

        # Ship Settings
        self.ship_speed = 1
        self.ship_limit = 3

        # Bullet Speed Settings
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (150, 150, 150)

        #alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10

        #fleet direction settings positive right/negative left
        self.fleet_direction = 1


################## - Assets - ##################
# class for battleship assets
class Ship(Sprite):

    def __init__(self, game_settings, screen):
        # Initialize position of ship
        self.game_settings = game_settings
        self.screen = screen

        # load ship Asset
        self.image = pygame.image.load('assets/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Ship Reposition/restarting position (Center bottom)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store decimal value for ship center
        self.center = float(self.rect.centerx)
        self.bottoms = float(self.rect.bottom)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    # Update Ship Position Based on the Movement Flag
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_settings.ship_speed
            # rect.centerx += 1
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.game_settings.ship_speed
            # rect.centerx -= 1
        elif self.moving_up and self.rect.top > 0:
            self.bottoms -= self.game_settings.ship_speed
            # rect.bottom -=1
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottoms += self.game_settings.ship_speed
            # rect.bottom += 1

        # Update rect object from self.center.
        self.rect.centerx = self.center
        self.rect.bottom = self.bottoms

    def blitme(self):
        # Draw asset at position indicated.
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        #Center ship to screen
        self.center = self.screen_rect.centerx
        self.bottoms = self.screen_rect.bottom


# Class to manage bullets from ship
class Bullet(Sprite):
    # bullet asset settings
    def __init__(self, game_settings, screen, ship):
        # Create bullet object at the ship position
        super(Bullet, self).__init__()
        self.screen = screen

        # Create bullets rect at position 0,0 and corret position
        self.rect = pygame.Rect(0, 0, game_settings.bullet_width, game_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store bullet position as decimal value
        self.y = float(self.rect.y)

        # Bullet Speed and Color Loader
        self.color = game_settings.bullet_color
        self.speed = game_settings.bullet_speed

    # bullet movement update settings
    def update(self):
        # Position of the bullet
        self.y -= self.speed
        # Update rect position
        self.rect.y = self.y

    # draw bullet function
    def draw_bullet(self):
        # Draw bullet in screen
        pygame.draw.rect(self.screen, self.color, self.rect)


# class for alien assets
class Alien(Sprite):

    def __init__(self, game_settings, screen):
        #Initialize position of alien
        super(Alien, self).__init__()
        self.game_settings = game_settings
        self.screen = screen

        # load alien Asset
        self.image = pygame.image.load('assets/Evil_Doers.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Ship Reposition/restarting position (Center bottom)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store Alien exact position
        self.x = float(self.rect.x)

    #Draw alien at specified position
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    #Screen Edge direction change
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    #move aliens in left or right direction
    def update(self):
        self.x += (self.game_settings.alien_speed_factor * self.game_settings.fleet_direction)
        self.rect.x = self.x


# Track stats for game.
class GameStats:

    # Initialize stats
    def __init__(self, game_settings):
        #Start Invaders from Python in an active state
        self.game_active = True

        self.game_settings = game_settings
        self.reset_stats()

    # Change stats that are modified during gameplay
    def reset_stats(self):
        self.ships_left = self.game_settings.ship_limit


