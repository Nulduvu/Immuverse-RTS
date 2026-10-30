# -- IMPORT --
import asyncio
import pygame # importer pygame
from pygame import Vector2, Surface # importer les classes utilisées régulièrement de pygame
from camera import camera, move_camera # importer les variable de caméra
from player_units import add_player_unit, draw_player_units # importer les fonctions d'unités
from player_units import draw_selection_area, get_units_in_selection # importer les fonctions de séléction

pygame.init() # initialisé toute les fonctionnalité de pygame


# -- LES CONSTANTE DE PYGAME --
SCREEN_SIZE: Vector2 = Vector2(480, 270) # la taille de la fenêtre de jeu
SCREEN: Surface = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN | pygame.SCALED) # créer la fenêtre de jeu
BACKGROUND_COLOR: pygame.Color = pygame.Color("black") # la couleur de l'arrière-plan du jeu, ici blanc
CLOCK: pygame.Clock = pygame.Clock() # créer une horloge pygame pour gérer le temps en jeu

# -- VARIABLES DE SELECTION --
selection_started: bool = False
selection_start_pos: tuple[float, float] = (0, 0)
selection_end_pos: tuple[float, float] = (0, 0)

# -- LES PREMIERE UNITES --
unit_sprite: Surface = pygame.image.load("assets/sprites/white_blood_cell_1.png")
add_player_unit(Vector2(0, 0), (32, 32), unit_sprite)
add_player_unit(Vector2(123, 87), (32, 32), unit_sprite)
add_player_unit(Vector2(200, 87), (32, 32), unit_sprite)


# -- LA BOUCLE DE JEU --
async def main():
    global selection_started, selection_start_pos, selection_end_pos

    is_running = True  # défini si le jeu est actuellement en train de tourner
    while is_running:
        key_state: pygame.key.ScancodeWrapper = pygame.key.get_pressed()  # récupérer toutes les touches pressées

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # détecter si le joueur ferme la fenêtre de jeu
                is_running = False
            if event.type == pygame.KEYDOWN:  # détecter si le joueur appuie sur une touche du clavier
                if event.key == pygame.K_ESCAPE:  # détecter un clique sur la touche échap du clavier
                    is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # détecter un clique de la souris
                if event.button == 1:
                    selection_start_pos = (pygame.mouse.get_pos()[0] - camera.x, pygame.mouse.get_pos()[1] - camera.y)
                    selection_started = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selection_end_pos = (pygame.mouse.get_pos()[0] - camera.x, pygame.mouse.get_pos()[1] - camera.y)
                    selection_started = False

                    get_units_in_selection(selection_start_pos, selection_end_pos, key_state)

        await asyncio.sleep(0)

        delta: float = CLOCK.tick(60) / 1000  # bloquer la vitesse du jeu à 60 image par seconde et récupérer delta

        move_camera(key_state, delta)  # déplacer la caméra en fonction des touches pressées

        SCREEN.fill(BACKGROUND_COLOR)  # remplir l'arrière-plan avec la couleur de BACKGROUND_COLOR
        draw_player_units(SCREEN, camera)  # déssiner les unités du joueur sur la fenêtre de jeu

        if selection_started:
            selection_actual_pos: tuple[float, float] = (pygame.mouse.get_pos()[0] - camera.x,
                                                         pygame.mouse.get_pos()[1] - camera.y)

            draw_selection_area(SCREEN, camera, selection_start_pos, selection_actual_pos)

        pygame.display.flip()  # mettre à jour l'affichage

    pygame.quit()


# -- DEBUT DE LA BOUCLE DE JEU --
asyncio.run(main())
