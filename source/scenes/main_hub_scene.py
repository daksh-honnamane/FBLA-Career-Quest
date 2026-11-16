# scenes/main_hub_scene.py

import pygame
from config.settings import BG_COLOR, TEXT_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_NAME, ACCENT_COLOR, ROUNDED_RADIUS
from utils.ui import draw_panel
from utils.paths import asset_path
from utils.save_manager import delete_save_data, load_save
from scenes.chef_scene import ChefScene
from scenes.doctor_scene import DoctorScene
from scenes.software_developer_scene import SoftwareDeveloperScene
from assets.avatars import ChefAvatar, DoctorAvatar, SoftwareDeveloperAvatar

class MainHubScene:
    def __init__(self, game):
        self.game = game
        self.save = load_save()
        self._font_cache = {}

        # Career info: name + placeholder color
        self.careers = [
            {"name": "Software Developer", "color": (180, 200, 255), "available": True},
            {"name": "Chef", "color": (255, 180, 180), "available": True},
            {"name": "Doctor", "color": (180, 255, 180), "available": True},
        ]

        # Create avatars for each career
        self.avatars = [
            SoftwareDeveloperAvatar(0, 0, size=80),  # Will be positioned in render
            ChefAvatar(0, 0, size=80),
            DoctorAvatar(0, 0, size=80),
        ]

        self.current_career_index = 0
        self.square_margin = 40
        self.square_width = (SCREEN_WIDTH - self.square_margin * 5) // 4
        self.square_height = self.square_width  # square

        self.font = pygame.font.SysFont(FONT_NAME, 24)
        self.title_font = pygame.font.SysFont(FONT_NAME, 38, bold=True)
        self.small_font = pygame.font.SysFont(FONT_NAME, 18)
        self.coming_font = pygame.font.SysFont(FONT_NAME, 24)
        self.complete_font = pygame.font.SysFont(FONT_NAME, 18)
        self.job_box_height = 40  # small box for job name
        self.feedback_message = "Select a career world to begin your workday."
        self.show_reset_dialog = False
        self.show_leaderboard = False
        self.selected_career_report = None  # For viewing detailed report
        self._star_icon_source = None
        self._star_icon_cache = {}
        self.modal_animation_name = None
        self.modal_animation_progress = 1.0
        self.modal_animation_duration = 0.22
        
        # Animation state for career swipe
        self.animation_active = False
        self.animation_progress = 0.0  # 0.0 to 1.0
        self.animation_duration = 0.55  # seconds
        self.animation_direction = 0  # 1 for right, -1 for left
        self.next_career_index = 0  # Target index during animation

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._is_modal_animating():
                return True
            return self.handle_click(event.pos)

        return False

    def update(self, delta_time):
        # Update animation progress
        if self.animation_active:
            self.animation_progress += delta_time / self.animation_duration
            if self.animation_progress >= 1.0:
                self.animation_progress = 1.0
                self.current_career_index = self.next_career_index
                self.animation_active = False

        if self.modal_animation_progress < 1.0:
            self.modal_animation_progress = min(
                1.0,
                self.modal_animation_progress + (delta_time / self.modal_animation_duration),
            )
            if self.modal_animation_progress >= 1.0:
                self.modal_animation_name = None

    def handle_click(self, pos):
        # Handle leaderboard interactions first if it's open
        if self.show_leaderboard:
            return self._handle_leaderboard_click(pos)
        
        if self.show_reset_dialog:
            if self._get_reset_confirm_rect().collidepoint(pos):
                delete_save_data()
                self.save = load_save()
                self.show_reset_dialog = False
                self.game.running = False
                return True
            elif self._get_reset_cancel_rect().collidepoint(pos):
                self.show_reset_dialog = False
                return True
            return False

        if self._get_reset_button_rect().collidepoint(pos):
            self.show_reset_dialog = True
            self._start_modal_animation("reset")
            return True
        
        if self._get_leaderboard_button_rect(self.game.screen.get_width(), self.game.screen.get_height()).collidepoint(pos):
            self.show_leaderboard = True
            self._start_modal_animation("leaderboard")
            return True

        width, height = self.game.screen.get_size()
        
        # Check left arrow
        if self._get_left_arrow_rect(width, height).collidepoint(pos):
            if not self.animation_active:
                self.animation_active = True
                self.animation_progress = 0.0
                self.animation_direction = -1
                self.next_career_index = (self.current_career_index - 1) % len(self.careers)
            return True
        
        # Check right arrow
        if self._get_right_arrow_rect(width, height).collidepoint(pos):
            if not self.animation_active:
                self.animation_active = True
                self.animation_progress = 0.0
                self.animation_direction = 1
                self.next_career_index = (self.current_career_index + 1) % len(self.careers)
            return True

        # Check career card click
        career_rect = self._get_current_career_rect(width, height)
        if career_rect.collidepoint(pos):
            career = self.careers[self.current_career_index]
            
            if career["name"] == "Software Developer" and career["available"]:
                self.game.scene_manager.set_scene(SoftwareDeveloperScene(self.game))
            elif career["name"] == "Chef" and career["available"]:
                self.game.scene_manager.set_scene(ChefScene(self.game))
            elif career["name"] == "Doctor" and career["available"]:
                self.game.scene_manager.set_scene(DoctorScene(self.game))
            else:
                self.feedback_message = "More career worlds are coming soon."
            return True

        return False

    def _handle_leaderboard_click(self, pos):
        """Handle clicks while leaderboard is open."""
        width, height = self.game.screen.get_size()

        # If viewing a report, check back button
        if self.selected_career_report:
            back_rect = self._get_report_back_rect(width, height)
            if back_rect.collidepoint(pos):
                self.selected_career_report = None
                return True
            return False

        # Check close button
        close_rect = self._get_leaderboard_close_rect(width, height)
        if close_rect.collidepoint(pos):
            self.show_leaderboard = False
            self.selected_career_report = None
            return True
        
        # Check career clicks in leaderboard
        careers_data = self._get_ranked_careers()
        for i, career_data in enumerate(careers_data):
            career_rect = self._get_leaderboard_career_rect(i, width, height)
            if career_rect.collidepoint(pos):
                self.selected_career_report = career_data["name"]
                return True
        
        return False

    def get_career_rect(self, index, width, height):
        card_count = len(self.careers)
        self.square_width = (width - self.square_margin * (card_count + 1)) // card_count
        self.square_height = self.square_width
        x = self.square_margin + index * (self.square_width + self.square_margin)
        y = (height - self.square_height) // 2
        return pygame.Rect(x, y, self.square_width, self.square_height)

    def _get_current_career_rect(self, width, height):
        """Get rect for the currently displayed career card (centered)."""
        center_x = width // 2
        card_size = min(300, (width - 200) // 3)
        x = center_x - card_size // 2
        y = (height - card_size) // 2
        return pygame.Rect(x, y, card_size, card_size)
    
    def _get_left_arrow_rect(self, width, height):
        """Get rect for left arrow button."""
        arrow_size = 60
        return pygame.Rect(20, height // 2 - arrow_size // 2, arrow_size, arrow_size)
    
    def _get_right_arrow_rect(self, width, height):
        """Get rect for right arrow button."""
        arrow_size = 60
        return pygame.Rect(width - 80, height // 2 - arrow_size // 2, arrow_size, arrow_size)
    
    def _draw_arrow(self, screen, rect, direction):
        """Draw left or right arrow button styled like other game buttons."""
        draw_panel(screen, rect, (215, 225, 235), border_color=ACCENT_COLOR, border_width=2)
        
        # Draw arrow triangle
        cx, cy = rect.center
        arrow_size = 18
        if direction == "left":
            points = [(cx + arrow_size // 2, cy - arrow_size // 2),
                     (cx - arrow_size // 2, cy),
                     (cx + arrow_size // 2, cy + arrow_size // 2)]
        else:  # right
            points = [(cx - arrow_size // 2, cy - arrow_size // 2),
                     (cx + arrow_size // 2, cy),
                     (cx - arrow_size // 2, cy + arrow_size // 2)]
        pygame.draw.polygon(screen, TEXT_COLOR, points)

    def render(self, screen):
        screen.fill(BG_COLOR)

        width, height = screen.get_width(), screen.get_height()
        title_font = self._get_scaled_font(38, minimum=38, bold=True)
        subtitle_font = self._get_scaled_font(18, minimum=18)
        label_font = self._get_scaled_font(24, minimum=20)

        title_surface = title_font.render("Career Hub", True, TEXT_COLOR)
        screen.blit(title_surface, (40, 35))
        subtitle = subtitle_font.render(self.feedback_message, True, TEXT_COLOR)
        screen.blit(subtitle, (40, 35 + title_surface.get_height() + 8))

        # Draw left and right arrows
        left_arrow_rect = self._get_left_arrow_rect(width, height)
        right_arrow_rect = self._get_right_arrow_rect(width, height)
        self._draw_arrow(screen, left_arrow_rect, "left")
        self._draw_arrow(screen, right_arrow_rect, "right")
        
        # Draw current career card with animation
        square_rect = self._get_current_career_rect(width, height)
        
        # Calculate animation offset
        if self.animation_active:
            # Easing function for smoother animation (ease-in-out)
            progress = self.animation_progress
            eased_progress = progress * progress * (3 - 2 * progress)  # Smoothstep
            travel = width + square_rect.width
            offset = travel * eased_progress
            
            # Right arrow -> current slides LEFT out, next slides in from LEFT (reversed)
            # Left arrow  -> current slides RIGHT out, next slides in from RIGHT (reversed)
            current_offset = -offset * self.animation_direction
            current_rect = square_rect.move(round(current_offset), 0)
            
            # Only draw if visible
            if -current_rect.width < current_rect.x < width + current_rect.width:
                self._draw_career_card(screen, current_rect, self.current_career_index, label_font)
            
            # Next card starts fully offscreen on the opposite side
            next_offset = (travel - offset) * self.animation_direction
            next_rect = square_rect.move(round(next_offset), 0)
            
            if -next_rect.width < next_rect.x < width + next_rect.width:
                self._draw_career_card(screen, next_rect, self.next_career_index, label_font)
        else:
            # No animation - draw current career normally
            self._draw_career_card(screen, square_rect, self.current_career_index, label_font)

        # Draw career counter
        counter_text = subtitle_font.render(f"{self.current_career_index + 1} / {len(self.careers)}", True, TEXT_COLOR)
        counter_rect = counter_text.get_rect(center=(width // 2, height - 50))
        screen.blit(counter_text, counter_rect)

        reset_button_rect = self._get_reset_button_rect()
        draw_panel(screen, reset_button_rect, (215, 225, 235), border_color=ACCENT_COLOR, border_width=2)
        reset_text = subtitle_font.render("Reset Data", True, TEXT_COLOR)
        reset_text_rect = reset_text.get_rect(center=reset_button_rect.center)
        screen.blit(reset_text, reset_text_rect)
        
        # Draw leaderboard button
        leaderboard_button_rect = self._get_leaderboard_button_rect(width, height)
        draw_panel(screen, leaderboard_button_rect, (215, 225, 235), border_color=ACCENT_COLOR, border_width=2)
        leaderboard_text = subtitle_font.render("Leaderboard", True, TEXT_COLOR)
        leaderboard_text_rect = leaderboard_text.get_rect(center=leaderboard_button_rect.center)
        screen.blit(leaderboard_text, leaderboard_text_rect)

        if self.show_leaderboard:
            self._render_leaderboard(screen, width, height, title_font, subtitle_font, label_font)
        elif self.show_reset_dialog:
            self._render_reset_dialog(screen, width, height, subtitle_font)

    def _draw_career_card(self, screen, rect, career_index, label_font):
        """Draw a career card at the given rect position."""
        career = self.careers[career_index]
        
        draw_panel(screen, rect, career["color"], border_color=ACCENT_COLOR, border_width=3)

        avatar = self.avatars[career_index]
        avatar.x = rect.centerx
        avatar.y = rect.centery - 60
        avatar.draw(screen)

        job_box_rect = pygame.Rect(
            rect.x,
            rect.y + rect.height - self.job_box_height,
            rect.width,
            self.job_box_height
        )
        draw_panel(screen, job_box_rect, (200, 200, 200), border_color=ACCENT_COLOR, border_width=2)

        text_surface = label_font.render(career["name"], True, TEXT_COLOR)
        screen.blit(text_surface, text_surface.get_rect(center=job_box_rect.center))

        if not career["available"]:
            overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (80, 80, 80, 110), overlay.get_rect(), border_radius=ROUNDED_RADIUS)
            screen.blit(overlay, rect.topleft)
            coming_text = self.coming_font.render("Coming Soon", True, TEXT_COLOR)
            screen.blit(coming_text, coming_text.get_rect(center=(rect.centerx, rect.centery)))

        if career["name"] in self.save.get("completed_careers", []):
            complete_text = self.complete_font.render("Completed", True, TEXT_COLOR)
            screen.blit(complete_text, complete_text.get_rect(midtop=(rect.centerx, rect.bottom + 8)))

    def _get_scaled_font(self, size, minimum=18, bold=False):
        width, height = self.game.screen.get_size()
        scale = max(1.0, min(width / SCREEN_WIDTH, height / SCREEN_HEIGHT))
        scaled_size = max(minimum, int(size * scale))
        cache_key = (scaled_size, bold)
        if cache_key not in self._font_cache:
            self._font_cache[cache_key] = pygame.font.SysFont(FONT_NAME, scaled_size, bold=bold)
        return self._font_cache[cache_key]

    def _get_reset_button_rect(self):
        width, height = self.game.screen.get_size()
        return pygame.Rect(width - 180, height - 70, 140, 40)

    def _get_reset_dialog_rect(self):
        width, height = self.game.screen.get_size()
        return pygame.Rect((width - 380) // 2, (height - 190) // 2, 380, 190)

    def _get_reset_confirm_rect(self):
        dialog_rect = self._get_reset_dialog_rect()
        return self._get_reset_confirm_rect_from_rect(dialog_rect)

    def _get_reset_cancel_rect(self):
        dialog_rect = self._get_reset_dialog_rect()
        return self._get_reset_cancel_rect_from_rect(dialog_rect)

    def _get_reset_confirm_rect_from_rect(self, dialog_rect):
        return pygame.Rect(dialog_rect.x + 45, dialog_rect.bottom - 70, 130, 42)

    def _get_reset_cancel_rect_from_rect(self, dialog_rect):
        return pygame.Rect(dialog_rect.right - 175, dialog_rect.bottom - 70, 130, 42)
    
    def _get_leaderboard_button_rect(self, width, height):
        """Get rect for leaderboard button."""
        return pygame.Rect(40, height - 70, 140, 40)
    
    def _get_ranked_careers(self):
        """Get completed careers ranked by total stars."""
        completed = self.save.get("completed_careers", [])
        reports = self.save.get("career_reports", {})
        
        ranked = []
        for career_name in completed:
            report = reports.get(career_name, {})
            total_stars = sum(report.values()) if report else 0
            ranked.append({
                "name": career_name,
                "total_stars": total_stars,
                "report": report
            })
        
        # Sort by stars (descending)
        ranked.sort(key=lambda x: x["total_stars"], reverse=True)
        return ranked
    
    def _get_leaderboard_rect(self, width, height):
        """Get the main leaderboard modal rect."""
        margin = 60
        return pygame.Rect(margin, margin, width - margin * 2, height - margin * 2)
    
    def _get_leaderboard_close_rect(self, width, height):
        """Get close button rect for leaderboard."""
        board_rect = self._get_leaderboard_rect(width, height)
        return self._get_leaderboard_close_rect_from_rect(board_rect)

    def _get_leaderboard_close_rect_from_rect(self, board_rect):
        button_height = 40
        return pygame.Rect(board_rect.right - 100, board_rect.y + 20, 80, button_height)
    
    def _get_leaderboard_career_rect(self, index, width, height):
        """Get rect for a career entry in the leaderboard."""
        board_rect = self._get_leaderboard_rect(width, height)
        return self._get_leaderboard_career_rect_from_rect(index, board_rect)

    def _get_leaderboard_career_rect_from_rect(self, index, board_rect):
        start_y = board_rect.y + 80
        entry_height = 60
        margin = 20
        return pygame.Rect(board_rect.x + margin, start_y + index * entry_height, board_rect.width - margin * 2, entry_height - 10)

    def _start_modal_animation(self, name):
        self.modal_animation_name = name
        self.modal_animation_progress = 0.0

    def _is_modal_animating(self):
        return self.modal_animation_progress < 1.0

    def _get_modal_animation_amount(self, name):
        if self.modal_animation_name == name and self.modal_animation_progress < 1.0:
            progress = self.modal_animation_progress
            return progress * progress * (3 - 2 * progress)
        return 1.0

    def _blit_modal_surface(self, screen, modal_surface, base_rect, amount):
        scale = 0.92 + (0.08 * amount)
        width = max(1, int(base_rect.width * scale))
        height = max(1, int(base_rect.height * scale))
        scaled_surface = pygame.transform.scale(modal_surface, (width, height))
        scaled_surface.set_alpha(int(255 * amount))
        destination = scaled_surface.get_rect(center=base_rect.center)
        destination.y += int((1 - amount) * 18)
        screen.blit(scaled_surface, destination)
    
    def _get_report_back_rect(self, width, height):
        """Get back button rect for career report view."""
        return self._get_leaderboard_close_rect(width, height)
    
    def _render_leaderboard(self, screen, width, height, title_font, subtitle_font, label_font):
        """Render the leaderboard modal."""
        board_rect = self._get_leaderboard_rect(width, height)

        amount = self._get_modal_animation_amount("leaderboard")
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(90 * amount)))
        screen.blit(overlay, (0, 0))

        modal_surface = pygame.Surface(board_rect.size, pygame.SRCALPHA)
        local_rect = modal_surface.get_rect()
        draw_panel(modal_surface, local_rect, (245, 245, 245), border_color=ACCENT_COLOR, border_width=3)

        if self.selected_career_report:
            self._render_career_report(modal_surface, local_rect, subtitle_font, label_font)
        else:
            self._render_leaderboard_list(modal_surface, local_rect, title_font, subtitle_font, label_font)

        self._blit_modal_surface(screen, modal_surface, board_rect, amount)
    
    def _render_leaderboard_list(self, screen, board_rect, title_font, subtitle_font, label_font):
        """Render the list of careers ranked by stars."""
        # Title
        title = title_font.render("Leaderboard", True, TEXT_COLOR)
        screen.blit(title, (board_rect.x + 20, board_rect.y + 20))
        
        # Close button
        close_rect = self._get_leaderboard_close_rect_from_rect(board_rect)
        draw_panel(screen, close_rect, (235, 190, 190), border_color=ACCENT_COLOR, border_width=2)
        close_text = subtitle_font.render("Close", True, TEXT_COLOR)
        screen.blit(close_text, close_text.get_rect(center=close_rect.center))
        
        # Leaderboard entries
        ranked = self._get_ranked_careers()
        if not ranked:
            no_careers = subtitle_font.render("No completed careers yet", True, TEXT_COLOR)
            screen.blit(no_careers, (board_rect.x + 20, board_rect.y + 100))
            return
        
        for i, career_data in enumerate(ranked):
            entry_rect = self._get_leaderboard_career_rect_from_rect(i, board_rect)
            
            # Draw entry background
            draw_panel(screen, entry_rect, (220, 230, 240), border_color=ACCENT_COLOR, border_width=1)
            
            # Draw rank, career name, and stars
            rank_text = label_font.render(f"{i + 1}.", True, TEXT_COLOR)
            career_text = label_font.render(career_data["name"], True, TEXT_COLOR)
            stars_value = subtitle_font.render(str(career_data["total_stars"]), True, ACCENT_COLOR)
            star_icon = self._get_star_icon(subtitle_font.get_height())
            
            screen.blit(rank_text, (entry_rect.x + 10, entry_rect.y + 10))
            screen.blit(career_text, (entry_rect.x + 50, entry_rect.y + 10))
            star_y = entry_rect.y + (entry_rect.height - star_icon.get_height()) // 2
            value_x = entry_rect.right - 28 - stars_value.get_width()
            star_x = value_x - star_icon.get_width() - 8
            screen.blit(star_icon, (star_x, star_y))
            screen.blit(stars_value, (value_x, entry_rect.y + 10))
    
    def _render_career_report(self, screen, board_rect, subtitle_font, label_font):
        """Render a detailed career report matching the results screen."""
        title_font = self._get_scaled_font(38, minimum=28, bold=True)
        
        # Back button
        back_rect = self._get_leaderboard_close_rect_from_rect(board_rect)
        draw_panel(screen, back_rect, (200, 220, 200), border_color=ACCENT_COLOR, border_width=2)
        back_text = subtitle_font.render("Back", True, TEXT_COLOR)
        screen.blit(back_text, back_text.get_rect(center=back_rect.center))
        
        # Title
        career_name = self.selected_career_report
        title = title_font.render(f"{career_name} Report", True, TEXT_COLOR)
        screen.blit(title, (board_rect.x + 30, board_rect.y + 30))
        
        # Get report data
        reports = self.save.get("career_reports", {})
        report = reports.get(self.selected_career_report, {})
        
        # Display skills with better formatting
        y = board_rect.y + 100
        skill_order = ["timing", "precision", "organization", "composure", "debugging", "logic", "efficiency", "speed", "diagnosis", "communication", "precision"]
        
        for skill_name in skill_order:
            if skill_name in report:
                score = report[skill_name]
                # Skill name with label
                skill_text = label_font.render(f"{skill_name.replace('_', ' ').title()}", True, TEXT_COLOR)
                screen.blit(skill_text, (board_rect.x + 40, y))
                
                # Filled star rating using the shared star asset
                self._draw_star_rating(screen, board_rect.x + 280, y, int(score), label_font.get_height())
                
                # Score
                score_text = label_font.render(f"{int(score)}/5", True, TEXT_COLOR)
                screen.blit(score_text, (board_rect.x + board_rect.width - 100, y))
                
                y += 50

    def _render_reset_dialog(self, screen, width, height, subtitle_font):
        amount = self._get_modal_animation_amount("reset")
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(90 * amount)))
        screen.blit(overlay, (0, 0))

        dialog_rect = self._get_reset_dialog_rect()
        modal_surface = pygame.Surface(dialog_rect.size, pygame.SRCALPHA)
        local_rect = modal_surface.get_rect()
        draw_panel(modal_surface, local_rect, (245, 245, 245), border_color=ACCENT_COLOR, border_width=3)

        question_text = subtitle_font.render("Reset all data?", True, TEXT_COLOR)
        question_rect = question_text.get_rect(center=(local_rect.centerx, local_rect.y + 55))
        modal_surface.blit(question_text, question_rect)

        confirm_rect = self._get_reset_confirm_rect_from_rect(local_rect)
        cancel_rect = self._get_reset_cancel_rect_from_rect(local_rect)
        draw_panel(modal_surface, confirm_rect, (235, 190, 190), border_color=ACCENT_COLOR, border_width=2)
        draw_panel(modal_surface, cancel_rect, (200, 220, 200), border_color=ACCENT_COLOR, border_width=2)

        confirm_text = subtitle_font.render("Yes", True, TEXT_COLOR)
        cancel_text = subtitle_font.render("No", True, TEXT_COLOR)
        modal_surface.blit(confirm_text, confirm_text.get_rect(center=confirm_rect.center))
        modal_surface.blit(cancel_text, cancel_text.get_rect(center=cancel_rect.center))

        self._blit_modal_surface(screen, modal_surface, dialog_rect, amount)

    def _draw_star_rating(self, screen, x, y, value, target_height):
        clamped_value = max(0, min(5, value))
        if clamped_value == 0:
            return

        star_icon = self._get_star_icon(target_height)
        spacing = max(4, star_icon.get_width() // 5)

        for index in range(clamped_value):
            screen.blit(star_icon, (x + index * (star_icon.get_width() + spacing), y))

    def _get_star_icon(self, target_height):
        scaled_height = max(14, int(target_height))
        cached_icon = self._star_icon_cache.get(scaled_height)
        if cached_icon is not None:
            return cached_icon

        if self._star_icon_source is None:
            self._star_icon_source = pygame.image.load(str(asset_path("star.png"))).convert_alpha()

        scale_ratio = scaled_height / self._star_icon_source.get_height()
        scaled_width = max(1, int(self._star_icon_source.get_width() * scale_ratio))
        scaled_icon = pygame.transform.smoothscale(self._star_icon_source, (scaled_width, scaled_height))
        self._star_icon_cache[scaled_height] = scaled_icon
        return scaled_icon