import pygame
from pygame.sprite import Group
from settings import Settings, Ship, GameStats
import functions as gf


# Game Initialization Function.
def run_game():
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("Test Game Space Invaders")

    # Create instance to store game stats
    stats = GameStats(game_settings)

    # Ship Asset Creation
    ship = Ship(game_settings, screen)

    # Group to store bullets in
    bullets = Group()

    #Group to store aliens in
    aliens = Group()

    #create fleet of aliens
    gf.create_fleet(game_settings, screen, ship, aliens)


    # Event Control (Such as Clicks or button press)
    while True:
        gf.check_events(game_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(game_settings, screen, aliens, ship, bullets)
        gf.update_aliens(game_settings, stats, screen, aliens, ship, bullets)
        gf.update_screen(game_settings, screen, aliens, ship, bullets)


run_game()
