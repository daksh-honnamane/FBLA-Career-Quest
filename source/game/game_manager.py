# game/game_manager.py

import random

import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, BG_COLOR
from game.scene_manager import SceneManager
from scenes.startup_scene import StartupScene
from utils.paths import asset_path

class GameManager:
    def __init__(self):
        self.base_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.window = self._create_window(self.base_size)
        self.screen = pygame.Surface(self.base_size).convert()
        self.viewport_rect = self._calculate_viewport(self.window.get_size())
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.click_sounds = self._load_click_sounds()
        self._letterbox_overlay = None
        self._letterbox_overlay_size = None

        self.scene_manager = SceneManager()
        self.scene_manager.set_scene(StartupScene(self))

    def _create_window(self, size):
        flags = pygame.RESIZABLE
        try:
            return pygame.display.set_mode(size, flags, vsync=1)
        except (TypeError, pygame.error):
            return pygame.display.set_mode(size, flags)

    def _refresh_window_metrics(self):
        display_surface = pygame.display.get_surface()
        if display_surface is not None:
            self.window = display_surface
            self.viewport_rect = self._calculate_viewport(display_surface.get_size())

    def _get_letterbox_overlay(self):
        window_size = self.window.get_size()
        if self._letterbox_overlay is None or self._letterbox_overlay_size != window_size:
            self._letterbox_overlay = pygame.Surface(window_size, pygame.SRCALPHA).convert_alpha()
            self._letterbox_overlay_size = window_size
        return self._letterbox_overlay

    def _load_click_sounds(self):
        asset_directory = asset_path()
        click_sound_paths = sorted(asset_directory.glob("click_*.ogg"))

        sounds = []
        for sound_path in click_sound_paths:
            try:
                sounds.append(pygame.mixer.Sound(str(sound_path)))
            except pygame.error:
                return []

        return sounds

    def _play_click_sound(self):
        if not self.click_sounds:
            return

        random.choice(self.click_sounds).play()

    def _calculate_viewport(self, window_size):
        window_width = max(1, int(window_size[0]))
        window_height = max(1, int(window_size[1]))
        base_width, base_height = self.base_size
        scale = min(window_width / base_width, window_height / base_height)
        render_width = max(1, int(base_width * scale))
        render_height = max(1, int(base_height * scale))
        return pygame.Rect(
            (window_width - render_width) // 2,
            (window_height - render_height) // 2,
            render_width,
            render_height,
        )

    def _translate_mouse_event(self, event):
        if not hasattr(event, "pos"):
            return event

        if not self.viewport_rect.collidepoint(event.pos):
            return None

        base_width, base_height = self.base_size
        translated_x = int((event.pos[0] - self.viewport_rect.x) * base_width / self.viewport_rect.w)
        translated_y = int((event.pos[1] - self.viewport_rect.y) * base_height / self.viewport_rect.h)

        event_data = event.dict.copy()
        event_data["pos"] = (translated_x, translated_y)

        if "rel" in event_data:
            event_data["rel"] = (
                int(event_data["rel"][0] * base_width / self.viewport_rect.w),
                int(event_data["rel"][1] * base_height / self.viewport_rect.h),
            )

        return pygame.event.Event(event.type, event_data)

    def _is_modal_overlay_active(self):
        current_scene = self.scene_manager.current_scene
        return bool(current_scene and (getattr(current_scene, "show_reset_dialog", False) or getattr(current_scene, "show_leaderboard", False)))

    def _get_window_background_color(self):
        if not self._is_modal_overlay_active():
            return BG_COLOR

        return tuple(max(0, channel - 80) for channel in BG_COLOR)

    def run(self):
        while self.running:
            delta_time = min(self.clock.tick(FPS) / 1000.0, 0.05)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type in (pygame.VIDEORESIZE, pygame.WINDOWSIZECHANGED):
                    self._refresh_window_metrics()
                elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                    translated_event = self._translate_mouse_event(event)
                    if translated_event is not None:
                        button_clicked = self.scene_manager.handle_event(translated_event)
                        if translated_event.type == pygame.MOUSEBUTTONDOWN and translated_event.button == 1 and button_clicked:
                            self._play_click_sound()
                else:
                    self.scene_manager.handle_event(event)

            self.scene_manager.update(delta_time)
            self.scene_manager.render(self.screen)
            self._refresh_window_metrics()

            self.window.fill(self._get_window_background_color())
            scaled_surface = pygame.transform.smoothscale(self.screen, self.viewport_rect.size)
            self.window.blit(scaled_surface, self.viewport_rect)

            # Dim any letterboxed space outside the game viewport when a modal is active.
            if self._is_modal_overlay_active():
                overlay = self._get_letterbox_overlay()
                overlay.fill((0, 0, 0, 0))

                top_rect = pygame.Rect(0, 0, self.window.get_width(), self.viewport_rect.top)
                bottom_rect = pygame.Rect(0, self.viewport_rect.bottom, self.window.get_width(), self.window.get_height() - self.viewport_rect.bottom)
                left_rect = pygame.Rect(0, self.viewport_rect.top, self.viewport_rect.left, self.viewport_rect.height)
                right_rect = pygame.Rect(self.viewport_rect.right, self.viewport_rect.top, self.window.get_width() - self.viewport_rect.right, self.viewport_rect.height)

                for rect in (top_rect, bottom_rect, left_rect, right_rect):
                    if rect.width > 0 and rect.height > 0:
                        pygame.draw.rect(overlay, (0, 0, 0, 90), rect)

                self.window.blit(overlay, (0, 0))

            pygame.display.flip()