# avatars/doctor.py

import pygame
from config.settings import TEXT_COLOR


class DoctorAvatar:
    """Avatar representing a Doctor character with detailed pixel art."""
    
    def __init__(self, x, y, size=80):
        self.x = x
        self.y = y
        self.size = size
        self.emotion = "neutral"  # neutral, confident, concerned, focused
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
        """Draw the doctor avatar on the surface."""
        scale = self.size / 80  # Base size is 80
        center_x = self.x
        top_y = self.y - 60
        
        skin_color = (219, 186, 154)
        hair_color = (88, 74, 68)
        coat_color = (248, 248, 247)
        scrub_color = (171, 203, 219)

        head = [
            (center_x - max(26, int(30 * scale)), top_y + max(28, int(32 * scale))),
            (center_x - max(14, int(18 * scale)), top_y + max(6, int(8 * scale))),
            (center_x + max(14, int(18 * scale)), top_y + max(6, int(8 * scale))),
            (center_x + max(26, int(30 * scale)), top_y + max(28, int(32 * scale))),
            (center_x + max(18, int(22 * scale)), top_y + max(64, int(70 * scale))),
            (center_x - max(18, int(22 * scale)), top_y + max(64, int(70 * scale))),
        ]
        hair = [
            (center_x - max(26, int(30 * scale)), top_y + max(26, int(28 * scale))),
            (center_x - max(12, int(16 * scale)), top_y + max(2, int(4 * scale))),
            (center_x + max(22, int(24 * scale)), top_y + max(6, int(8 * scale))),
            (center_x + max(28, int(32 * scale)), top_y + max(30, int(34 * scale))),
            (center_x + max(8, int(10 * scale)), top_y + max(20, int(22 * scale))),
            (center_x - max(16, int(18 * scale)), top_y + max(18, int(20 * scale))),
        ]
        torso_top = top_y + max(80, int(88 * scale))
        torso_bottom = top_y + max(236, int(244 * scale))
        coat = [
            (center_x - max(66, int(74 * scale)), torso_bottom),
            (center_x - max(46, int(52 * scale)), torso_top + max(12, int(14 * scale))),
            (center_x - max(18, int(20 * scale)), torso_top),
            (center_x + max(18, int(20 * scale)), torso_top),
            (center_x + max(46, int(52 * scale)), torso_top + max(12, int(14 * scale))),
            (center_x + max(66, int(74 * scale)), torso_bottom),
        ]
        scrub = [
            (center_x - max(20, int(24 * scale)), torso_top + max(2, int(4 * scale))),
            (center_x + max(20, int(24 * scale)), torso_top + max(2, int(4 * scale))),
            (center_x + max(10, int(12 * scale)), torso_top + max(44, int(48 * scale))),
            (center_x - max(10, int(12 * scale)), torso_top + max(44, int(48 * scale))),
        ]
        neck = [
            (center_x - max(12, int(14 * scale)), head[5][1] - max(2, int(3 * scale))),
            (center_x + max(12, int(14 * scale)), head[4][1] - max(2, int(3 * scale))),
            (center_x + max(18, int(20 * scale)), torso_top + max(6, int(8 * scale))),
            (center_x - max(18, int(20 * scale)), torso_top + max(6, int(8 * scale))),
        ]

        pygame.draw.polygon(screen, coat_color, coat)
        pygame.draw.polygon(screen, scrub_color, scrub)
        pygame.draw.polygon(screen, skin_color, neck)
        pygame.draw.polygon(screen, skin_color, head)
        pygame.draw.polygon(screen, hair_color, hair)
        pygame.draw.line(screen, TEXT_COLOR, (center_x - max(10, int(12 * scale)), top_y + max(36, int(40 * scale))), (center_x - max(2, int(4 * scale)), top_y + max(36, int(40 * scale))), 2)
        pygame.draw.line(screen, TEXT_COLOR, (center_x + max(2, int(4 * scale)), top_y + max(36, int(40 * scale))), (center_x + max(10, int(12 * scale)), top_y + max(36, int(40 * scale))), 2)
        pygame.draw.line(screen, TEXT_COLOR, (center_x - max(8, int(10 * scale)), top_y + max(54, int(58 * scale))), (center_x + max(8, int(10 * scale)), top_y + max(54, int(58 * scale))), 2)
        pygame.draw.line(screen, TEXT_COLOR, (center_x - max(18, int(20 * scale)), torso_top + max(18, int(22 * scale))), (center_x, torso_top + max(58, int(64 * scale))), 3)
        pygame.draw.line(screen, TEXT_COLOR, (center_x + max(18, int(20 * scale)), torso_top + max(18, int(22 * scale))), (center_x, torso_top + max(58, int(64 * scale))), 3)
        pygame.draw.circle(screen, TEXT_COLOR, (center_x, torso_top + max(60, int(66 * scale))), max(4, int(5 * scale)))
