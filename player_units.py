import pygame
from pygame import Vector2, Surface

player_units_count: int = 0 # nombre d'unités du joueur
player_units: list[list] = [] # les unités du joueur avec leur information (telle que leur vie, force, type, ECT...)
player_selected_units: list[int] = [] # unités sélectionnées par le joueur (leurs index uniquement)


# déssiner les unités du joueur sur la fenêtre de jeu
def draw_player_units(screen: Surface, camera: Vector2) -> None:
    for unit in range(player_units_count):
        unit_position: Vector2 = player_units[unit][0]
        unit_size: tuple[int, int] = player_units[unit][1]
        unit_sprite: Surface = player_units[unit][2]

        if unit in player_selected_units:
            pygame.draw.rect(screen, (255, 255, 255), ((unit_position.x - 5) + camera.x, (unit_position.y - 5) + camera.y, unit_size[0] + 10, unit_size[1] + 10))

        screen.blit(unit_sprite, unit_position + camera)

    return

# ajouter une unité au joueur
def add_player_unit(unit_position: Vector2, unit_size: tuple[int, int], unit_sprite: Surface) -> None:
    global player_units_count, player_units

    player_units_count += 1

    resized_sprite: Surface = pygame.transform.scale(unit_sprite, unit_size)
    unit_rect: pygame.Rect = pygame.Rect(unit_position.x, unit_position.y, unit_size[0], unit_size[1])
    unit: list = [unit_position, unit_size, resized_sprite, unit_rect]
    player_units.append(unit)

    return

# récupérer la zone de séléction a partir de la position de départ et de fin du clique
def get_selection_area(selection_start_pos: tuple[float, float], selection_end_pos: tuple[float, float]) -> pygame.Rect:
    selection_area: pygame.Rect = pygame.Rect(0, 0, 0, 0)

    selection_area.left = selection_start_pos[0] if selection_start_pos[0] < selection_end_pos[0] else selection_end_pos[0]
    selection_area.top = selection_start_pos[1] if selection_start_pos[1] < selection_end_pos[1] else selection_end_pos[1]

    selection_area.width = selection_end_pos[0] - selection_start_pos[0] if selection_end_pos[0] > selection_start_pos[0] else selection_start_pos[0] - selection_end_pos[0]
    selection_area.height = selection_end_pos[1] - selection_start_pos[1] if selection_end_pos[1] > selection_start_pos[1] else selection_start_pos[1] - selection_end_pos[1]

    return selection_area

# dessiner la zone de séléction sur l'écran
def draw_selection_area(screen: Surface, camera: Vector2, selection_start_pos: tuple[float, float], selection_end_pos: tuple[float, float]) -> None:
    selection_area: pygame.Rect = get_selection_area(selection_start_pos, selection_end_pos)

    pygame.draw.rect(screen, (255, 0, 0), (selection_area.x + camera.x, selection_area.y + camera.y, selection_area.width, selection_area.height))

    return

# récupérer les unités dans la séléction
def get_units_in_selection(selection_start_pos: tuple[float, float], selection_end_pos: tuple[float, float], key_state: pygame.key.ScancodeWrapper) -> None:
    global player_selected_units

    selection_area: pygame.Rect = get_selection_area(selection_start_pos, selection_end_pos)

    if not key_state[pygame.K_LCTRL]:
        player_selected_units = []

    for unit in player_units:
        if unit[3].colliderect(selection_area):
            player_selected_units.append(player_units.index(unit))

    return