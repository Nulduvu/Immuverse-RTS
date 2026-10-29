import pygame
from pygame import Vector2


CAMERA_SPEED: int = 200 # vitesse de la caméra

camera: Vector2 = Vector2(0, 0) # position de la caméra


# déplacer la caméra en fonction des touches pressées
def move_camera(key_state: pygame.key.ScancodeWrapper, delta: float) -> None:
    global camera

    # récupérer la valeur de déplacement de la caméra sur les deux axes en fonction des touches pressées
    camera_deplacement_x: float = (key_state[pygame.K_q] - key_state[pygame.K_d]) * CAMERA_SPEED * delta
    camera_deplacement_y: float = (key_state[pygame.K_z] - key_state[pygame.K_s]) * CAMERA_SPEED * delta

    camera.x += camera_deplacement_x  # déplacer la caméra en axe X
    camera.y += camera_deplacement_y  # déplacer la caméra en axe Y

    return
