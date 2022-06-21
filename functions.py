import sys
import pygame
from settings import Alien, Bullet, Settings, Ship, GameStats
from time import sleep


################## - Functions     - ##################
################## - Event Control - ##################

# Collision response
def ship_hit(game_settings, stats, screen, aliens, ship, bullets):
    if stats.ships_left > 0:
        #Decrease number of ships left
        stats.ships_left -= 1

        #empty list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #Reset fleet and ship position
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()

        #Time before reset
        sleep(1)
    else:
        stats.game_active = False
        #sys.exit()


# Keydown event control
def check_keydown_events(event, game_settings, screen, ship, bullets):
    # Movement Event Control
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_UP:
            ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            new_bullet = Bullet(game_settings, screen, ship)
            bullets.add(new_bullet)


# Keyup event control
def check_keyup_events(event, ship):
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False
        elif event.key == pygame.K_UP:
            ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            ship.moving_down = False


# Keyboard/click event control function
def check_events(game_settings, screen, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Movement Event Control
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets)

        # Button Release Event Control
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


################## - Update Control - ##################
# Update images on screen and flip to new screen
def update_screen(game_settings, screen, aliens, ship, bullets):
    # Screen Color Controller
    screen.fill(game_settings.bg_color)

    # Bullet Redraw bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()


    ship.blitme()
    aliens.draw(screen)

    # Game Closing Statement
    pygame.display.flip()


# Update position of bullets and removes out of screen assets
def update_bullets(game_settings, screen, aliens, ship, bullets):
    # Check for collisions then delete bullet and alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    #Repopulating fleet
    if len(aliens) == 0:
        bullets.empty()
        game_settings.bullet_speed += 0.5
        game_settings.fleet_drop_speed += 0.5
        game_settings.alien_speed_factor += 0.5
        create_fleet(game_settings, screen, ship, aliens)
    #bullets position
    bullets.update()

    # Remove bullets from out of screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    print(len(bullets))


# Create fleet of aliens
def create_fleet(game_settings, screen, ship, aliens):
    #Find number of aliens in a row

    alien = Alien(game_settings, screen)
    number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)

    #create fleet row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, screen, aliens, alien_number, row_number)


#Determining number of aliens in a row
def get_number_aliens_x(game_settings, alien_width):
    #Available space
    available_space_x = game_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


#Creating aliens
def create_alien(game_settings, screen, aliens, alien_number, row_number):
    #Create alien a set it into place
    #Spacing between aliens = 1 alien width
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


#Determine number of alien rows
def get_number_rows(game_settings, ship_height, alien_height):
    #Max row calculation
    available_space_y = (game_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


# Check position of fleet
def check_fleet_edges(game_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break


#Change direction of fleet
def change_fleet_direction(game_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


#Aliens touch the bottom action
def check_aliens_bottom(game_settings, stats, screen, aliens, ship, bullets):
    #Check if aliens touch the bottom of screen.
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(game_settings, stats, screen, aliens, ship, bullets)
            break


#Determine movement of aliens
def update_aliens(game_settings, stats, screen, aliens, ship, bullets):
    check_fleet_edges(game_settings, aliens)
    aliens.update()

    #Alien ship crash
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, stats, screen, aliens, ship, bullets)

    #Look for aliens reaching bottom call function
    check_aliens_bottom(game_settings, stats, screen, aliens, ship, bullets)
