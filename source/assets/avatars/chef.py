# avatars/chef.py

import pygame
from config.settings import TEXT_COLOR


class ChefAvatar:
    """Avatar representing a Chef character with detailed pixel art."""
    
    def __init__(self, x, y, size=80):
        self.x = x
        self.y = y
        self.size = size
        self.emotion = "neutral"  # neutral, happy, focused, stressed
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
        """Draw the chef avatar on the surface."""
        scale = self.size / 80  # Base size is 80
        center_x = self.x
        top_y = self.y - 60
        
        skin_color = (219, 186, 154)
        hair_color = (92, 76, 62)
        hat_color = (249, 247, 242)
        band_color = (230, 224, 214)
        coat_color = (247, 247, 244)
        apron_color = (214, 198, 171)

        hat_top = [
            (center_x - max(38, int(44 * scale)), top_y + max(48, int(52 * scale))),
            (center_x - max(28, int(34 * scale)), top_y + max(22, int(24 * scale))),
            (center_x - max(6, int(8 * scale)), top_y + max(16, int(18 * scale))),
            (center_x + max(18, int(20 * scale)), top_y + max(20, int(22 * scale))),
            (center_x + max(36, int(40 * scale)), top_y + max(44, int(48 * scale))),
            (center_x + max(22, int(26 * scale)), top_y + max(60, int(66 * scale))),
            (center_x - max(18, int(22 * scale)), top_y + max(62, int(68 * scale))),
        ]
        hat_band = [
            (center_x - max(42, int(48 * scale)), top_y + max(60, int(64 * scale))),
            (center_x + max(42, int(48 * scale)), top_y + max(60, int(64 * scale))),
            (center_x + max(34, int(38 * scale)), top_y + max(76, int(82 * scale))),
            (center_x - max(34, int(38 * scale)), top_y + max(76, int(82 * scale))),
        ]
        head = [
            (center_x - max(26, int(30 * scale)), top_y + max(82, int(88 * scale))),
            (center_x - max(16, int(20 * scale)), top_y + max(62, int(66 * scale))),
            (center_x + max(16, int(20 * scale)), top_y + max(62, int(66 * scale))),
            (center_x + max(26, int(30 * scale)), top_y + max(82, int(88 * scale))),
            (center_x + max(18, int(22 * scale)), top_y + max(120, int(126 * scale))),
            (center_x - max(18, int(22 * scale)), top_y + max(120, int(126 * scale))),
        ]
        hair = [
            (center_x - max(26, int(30 * scale)), top_y + max(82, int(86 * scale))),
            (center_x - max(12, int(16 * scale)), top_y + max(58, int(60 * scale))),
            (center_x + max(22, int(24 * scale)), top_y + max(62, int(64 * scale))),
            (center_x + max(28, int(32 * scale)), top_y + max(86, int(90 * scale))),
            (center_x + max(8, int(10 * scale)), top_y + max(76, int(80 * scale))),
            (center_x - max(16, int(18 * scale)), top_y + max(74, int(78 * scale))),
        ]
        coat_top = top_y + max(136, int(144 * scale))
        coat_bottom = top_y + max(236, int(244 * scale))
        coat = [
            (center_x - max(68, int(76 * scale)), coat_bottom),
            (center_x - max(48, int(54 * scale)), coat_top + max(14, int(16 * scale))),
            (center_x - max(18, int(22 * scale)), coat_top),
            (center_x + max(18, int(22 * scale)), coat_top),
            (center_x + max(48, int(54 * scale)), coat_top + max(14, int(16 * scale))),
            (center_x + max(68, int(76 * scale)), coat_bottom),
        ]
        apron = [
            (center_x - max(22, int(24 * scale)), coat_top + max(4, int(6 * scale))),
            (center_x + max(22, int(24 * scale)), coat_top + max(4, int(6 * scale))),
            (center_x + max(14, int(16 * scale)), coat_top + max(52, int(58 * scale))),
            (center_x - max(14, int(16 * scale)), coat_top + max(52, int(58 * scale))),
        ]
        neck = [
            (center_x - max(12, int(14 * scale)), head[5][1] - max(2, int(3 * scale))),
            (center_x + max(12, int(14 * scale)), head[4][1] - max(2, int(3 * scale))),
            (center_x + max(18, int(20 * scale)), coat_top + max(6, int(8 * scale))),
            (center_x - max(18, int(20 * scale)), coat_top + max(6, int(8 * scale))),
        ]

        pygame.draw.polygon(screen, hat_color, hat_top)
        pygame.draw.polygon(screen, band_color, hat_band)
        pygame.draw.polygon(screen, skin_color, neck)
        pygame.draw.polygon(screen, skin_color, head)
        pygame.draw.polygon(screen, hair_color, hair)
        pygame.draw.polygon(screen, coat_color, coat)
        pygame.draw.polygon(screen, apron_color, apron)
        pygame.draw.line(screen, TEXT_COLOR, (center_x - max(10, int(12 * scale)), top_y + max(94, int(100 * scale))), (center_x - max(2, int(4 * scale)), top_y + max(94, int(100 * scale))), 2)
        pygame.draw.line(screen, TEXT_COLOR, (center_x + max(2, int(4 * scale)), top_y + max(94, int(100 * scale))), (center_x + max(10, int(12 * scale)), top_y + max(94, int(100 * scale))), 2)
        pygame.draw.line(screen, TEXT_COLOR, (center_x - max(8, int(10 * scale)), top_y + max(112, int(118 * scale))), (center_x + max(8, int(10 * scale)), top_y + max(112, int(118 * scale))), 2)
