# avatars/software_developer.py

import pygame
from config.settings import TEXT_COLOR


class SoftwareDeveloperAvatar:
    """Avatar representing a Software Developer character with detailed pixel art."""
    
    def __init__(self, x, y, size=80):
        self.x = x
        self.y = y
        self.size = size
        self.emotion = "neutral"  # neutral, focused, frustrated, excited
        self.animation_timer = 0.0
        
    def update(self, delta_time):
        """Update animation state."""
        self.animation_timer += delta_time
        if self.animation_timer > 1.0:
            self.animation_timer = 0.0
    
    def set_emotion(self, emotion):
        """Set the avatar's emotion state."""
        self.emotion = emotion
    
    def draw(self, screen):
        """Draw the software developer avatar on the surface."""
        scale = self.size / 80  # Base size is 80
        center_x = self.x
        top_y = self.y - 60
        
        skin_color = (219, 186, 154)
        hair_color = (59, 68, 86)
        jacket_color = (73, 110, 156)
        shirt_color = (234, 241, 248)
        laptop_color = (72, 86, 110)
        screen_color = (206, 228, 246)

        head = [
            (center_x - max(26, int(30 * scale)), top_y + max(26, int(30 * scale))),
            (center_x - max(14, int(18 * scale)), top_y + max(4, int(8 * scale))),
            (center_x + max(14, int(18 * scale)), top_y + max(4, int(8 * scale))),
            (center_x + max(26, int(30 * scale)), top_y + max(26, int(30 * scale))),
            (center_x + max(18, int(22 * scale)), top_y + max(62, int(68 * scale))),
            (center_x - max(18, int(22 * scale)), top_y + max(62, int(68 * scale))),
        ]
        hair = [
            (head[0][0] - max(2, int(3 * scale)), head[0][1] + max(2, int(3 * scale))),
            (center_x - max(18, int(20 * scale)), top_y),
            (center_x + max(22, int(24 * scale)), top_y + max(2, int(4 * scale))),
            (head[3][0] + max(2, int(3 * scale)), head[3][1] + max(1, int(2 * scale))),
            (center_x + max(12, int(14 * scale)), top_y + max(20, int(24 * scale))),
            (center_x - max(8, int(10 * scale)), top_y + max(14, int(16 * scale))),
        ]
        torso_top = top_y + max(78, int(86 * scale))
        torso_bottom = top_y + max(236, int(244 * scale))
        torso = [
            (center_x - max(62, int(70 * scale)), torso_bottom),
            (center_x - max(42, int(50 * scale)), torso_top + max(14, int(16 * scale))),
            (center_x - max(12, int(16 * scale)), torso_top),
            (center_x + max(12, int(16 * scale)), torso_top),
            (center_x + max(42, int(50 * scale)), torso_top + max(14, int(16 * scale))),
            (center_x + max(62, int(70 * scale)), torso_bottom),
        ]
        shirt = [
            (center_x - max(18, int(22 * scale)), torso_top + max(2, int(4 * scale))),
            (center_x + max(18, int(22 * scale)), torso_top + max(2, int(4 * scale))),
            (center_x + max(8, int(10 * scale)), torso_top + max(38, int(44 * scale))),
            (center_x - max(8, int(10 * scale)), torso_top + max(38, int(44 * scale))),
        ]
        neck = [
            (center_x - max(12, int(14 * scale)), head[5][1] - max(2, int(3 * scale))),
            (center_x + max(12, int(14 * scale)), head[4][1] - max(2, int(3 * scale))),
            (center_x + max(18, int(20 * scale)), torso_top + max(6, int(8 * scale))),
            (center_x - max(18, int(20 * scale)), torso_top + max(6, int(8 * scale))),
        ]
        laptop = [
            (center_x - max(54, int(62 * scale)), top_y + max(170, int(178 * scale))),
            (center_x + max(54, int(62 * scale)), top_y + max(170, int(178 * scale))),
            (center_x + max(68, int(78 * scale)), top_y + max(218, int(226 * scale))),
            (center_x - max(68, int(78 * scale)), top_y + max(218, int(226 * scale))),
        ]
        laptop_screen = [
            (center_x - max(40, int(46 * scale)), top_y + max(164, int(172 * scale))),
            (center_x + max(40, int(46 * scale)), top_y + max(164, int(172 * scale))),
            (center_x + max(50, int(58 * scale)), top_y + max(194, int(202 * scale))),
            (center_x - max(50, int(58 * scale)), top_y + max(194, int(202 * scale))),
        ]

        pygame.draw.polygon(screen, jacket_color, torso)
        pygame.draw.polygon(screen, shirt_color, shirt)
        pygame.draw.polygon(screen, skin_color, neck)
        pygame.draw.polygon(screen, skin_color, head)
        pygame.draw.polygon(screen, hair_color, hair)
        pygame.draw.polygon(screen, laptop_color, laptop)
        pygame.draw.polygon(screen, screen_color, laptop_screen)
        pygame.draw.line(screen, TEXT_COLOR, (center_x - max(10, int(12 * scale)), top_y + max(34, int(38 * scale))), (center_x - max(2, int(4 * scale)), top_y + max(34, int(38 * scale))), 2)
        pygame.draw.line(screen, TEXT_COLOR, (center_x + max(2, int(4 * scale)), top_y + max(34, int(38 * scale))), (center_x + max(10, int(12 * scale)), top_y + max(34, int(38 * scale))), 2)
        pygame.draw.line(screen, TEXT_COLOR, (center_x - max(8, int(10 * scale)), top_y + max(52, int(56 * scale))), (center_x + max(8, int(10 * scale)), top_y + max(52, int(56 * scale))), 2)
