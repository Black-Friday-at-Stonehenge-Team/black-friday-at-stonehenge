import pygame
import serial
import serial.tools.list_ports
from core.background import Background
from core.font import Font
from core.text import Text
from core.state import State
from core.logs import get_logger

logger = get_logger("OptionsState")


class OptionsState(State):
    def __init__(self, game, previous_state=None):
        super().__init__(game)
        self.previous_state = previous_state
        logger.info("Options state initialized")

        # Background
        self.background = Background(image="menu_1.png")

        # Fonts
        self.title_font = Font(
            "antiquity-print.ttf",
            55,
            (255, 255, 255),
            shadow=True,
            shadow_offset=(3, 3),
            shadow_color=(0, 0, 0),
        )
        self.option_font = Font(
            "antiquity-print.ttf",
            30,
            (255, 255, 255),
            shadow=True,
            shadow_offset=(2, 2),
            shadow_color=(0, 0, 0),
        )
        self.instruction_font = Font(
            "antiquity-print.ttf",
            20,
            (255, 255, 255),
            shadow=True,
            shadow_offset=(1, 1),
            shadow_color=(0, 0, 0),
        )

        # Get available ports
        self.available_ports = self._get_available_ports()
        self.available_ports.append(("Back to Menu", ""))

        # Menu options
        self.selected_option = 0

        # Current port display
        self.current_port = f"Current Port: {game.sound_port}"

    def _get_available_ports(self):
        """Get list of available COM ports with descriptions"""
        ports = []
        try:
            for port in serial.tools.list_ports.comports():
                port_desc = f"{port.device} - {port.description}"
                ports.append((port_desc, port.device))

            # If no ports found, add a placeholder
            # to indicate no ports available
            if not ports:
                ports.append(("No ports available", ""))

            return ports
        except Exception as e:
            logger.error(f"Error getting serial ports: {str(e)}")
            return [("Error listing ports", "")]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(
                        self.available_ports
                    )
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(
                        self.available_ports
                    )
                elif event.key == pygame.K_RETURN:
                    self.handle_menu_selection()
                elif event.key == pygame.K_ESCAPE:
                    self.back_to_menu()

    def handle_menu_selection(self):
        selected_port_info = self.available_ports[self.selected_option]

        if selected_port_info[1] == "":  # Back option or no ports available
            self.back_to_menu()
        else:
            # Set the selected port
            self.game.sound_port = selected_port_info[1]
            logger.info(f"Selected port: {self.game.sound_port}")

            # Update the current port display
            self.current_port = f"Current Port: {self.game.sound_port}"

            # Reset sound controller to use new port
            from core.sound_controller import SoundController

            SoundController._instance = None  # Force recreation with new port

    def back_to_menu(self):
        from .menu_state import MenuState

        self.game.set_state(MenuState(self.game))

    def update(self):
        pass

    def render(self):
        # Render the background
        self.background.render(self.game.screen)

        # Render the title
        title_text = Text(
            "SOUND OPTIONS",
            self.title_font,
            position=(
                self.game.width // 2
                - self.title_font.render("SOUND OPTIONS").get_width() // 2,
                self.game.height // 8,
            ),
        )
        title_text.render(self.game.screen)

        # Render current port
        current_port_text = Text(
            self.current_port,
            self.option_font,
            position=(
                self.game.width // 2
                - self.option_font.render(self.current_port).get_width() // 2,
                self.game.height // 4,
            ),
        )
        current_port_text.render(self.game.screen)

        # Render available ports
        port_y_start = self.game.height // 3
        visible_items = 6  # Number of items visible at once

        # Calculate range of visible items
        start_idx = max(0, self.selected_option - visible_items // 2)
        end_idx = min(start_idx + visible_items, len(self.available_ports))

        # Adjust start_idx if we have fewer items at the end
        start_idx = max(0, min(start_idx, len(self.available_ports) - visible_items))

        # Render the port options
        for i in range(start_idx, end_idx):
            port_info = self.available_ports[i]
            is_selected = i == self.selected_option

            color = (255, 0, 0) if is_selected else (255, 255, 255)
            port_font = Font(
                "antiquity-print.ttf",
                30,
                color,
                shadow=True,
                shadow_offset=(2, 2),
                shadow_color=(0, 0, 0),
            )

            # Show a limited port name to fit on screen
            display_text = port_info[0]
            if len(display_text) > 40:
                display_text = display_text[:37] + "..."

            port_text = Text(
                display_text,
                port_font,
                position=(
                    self.game.width // 2
                    - port_font.render(display_text).get_width() // 2,
                    port_y_start + (i - start_idx) * 50,
                ),
            )
            port_text.render(self.game.screen)

        # Render the instructions
        instructions_text = Text(
            "Use ARROW KEYS and ENTER to select, ESC to go back",
            self.instruction_font,
            position=(
                self.game.width // 2
                - self.instruction_font.render(
                    "Use ARROW KEYS and ENTER to select, ESC to go back"
                ).get_width()
                // 2,
                self.game.height - 50,
            ),
        )
        instructions_text.render(self.game.screen)

        pygame.display.flip()
