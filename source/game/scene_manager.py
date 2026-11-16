# game/scene_manager.py

import pygame

from config.settings import BG_COLOR


class SceneManager:
    def __init__(self):
        self.current_scene = None
        self.pending_scene = None
        self.transition_phase = None
        self.transition_progress = 1.0
        self.transition_in_duration = 0.35
        self.transition_out_duration = 0.24
        self.transition_surface = None
        self.veil_surface = None

    def set_scene(self, scene):
        if self.current_scene is None:
            self.current_scene = scene
            self.pending_scene = None
            self.transition_phase = "in"
            self.transition_progress = 0.0
            return

        self.pending_scene = scene
        self.transition_phase = "out"
        self.transition_progress = 0.0

    def handle_event(self, event):
        if not self.current_scene or self.transition_phase is not None:
            return False

        return self.current_scene.handle_event(event)

    def update(self, delta_time):
        if self.current_scene:
            self.current_scene.update(delta_time)

        if self.transition_phase is None:
            return

        duration = self.transition_in_duration if self.transition_phase == "in" else self.transition_out_duration
        self.transition_progress = min(1.0, self.transition_progress + (delta_time / duration))

        if self.transition_progress < 1.0:
            return

        if self.transition_phase == "out":
            self.current_scene = self.pending_scene
            self.pending_scene = None
            self.transition_phase = "in"
            self.transition_progress = 0.0
            return

        self.transition_phase = None
        self.transition_progress = 1.0

    def render(self, screen):
        if not self.current_scene:
            return

        if self.transition_phase is None:
            self.current_scene.render(screen)
            return

        self._ensure_transition_surface(screen.get_size())
        self.transition_surface.fill(BG_COLOR)
        self.current_scene.render(self.transition_surface)

        progress = self.transition_progress
        if self.transition_phase == "out":
            eased = 1 - pow(1 - progress, 3)
            scale = 1.0 + (0.04 * eased)
            alpha = int(255 * (1 - eased))
            lift = -int(eased * 24)
            veil_alpha = int(eased * 55)
        else:
            eased = 1 - pow(1 - progress, 3)
            scale = 0.92 + (0.08 * eased)
            alpha = int(255 * eased)
            lift = int((1 - eased) * 28)
            veil_alpha = int((1 - eased) * 40)

        scaled_size = (
            max(1, int(screen.get_width() * scale)),
            max(1, int(screen.get_height() * scale)),
        )
        scaled_surface = pygame.transform.scale(self.transition_surface, scaled_size)
        scaled_surface.set_alpha(alpha)

        screen.fill(BG_COLOR)
        destination = scaled_surface.get_rect(center=screen.get_rect().center)
        destination.y += lift
        screen.blit(scaled_surface, destination)

        veil = self._ensure_veil_surface(screen.get_size())
        veil.fill((255, 255, 255, 0))
        veil.fill((255, 255, 255, veil_alpha))
        screen.blit(veil, (0, 0))

    def _ensure_transition_surface(self, size):
        if self.transition_surface is None or self.transition_surface.get_size() != size:
            self.transition_surface = pygame.Surface(size).convert()

    def _ensure_veil_surface(self, size):
        if self.veil_surface is None or self.veil_surface.get_size() != size:
            self.veil_surface = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()
        return self.veil_surface