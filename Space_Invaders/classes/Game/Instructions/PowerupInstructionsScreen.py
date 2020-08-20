from .. import State, PowerUp, WHITE, GREY, ImageObject, MenuTemplate


class PowerupInstructionsScreen(MenuTemplate):
    description = {
        'bullet_up': ("Increase bullet speed", "Increases the speed of the bullets"),
        'bullet_attack_up': ("Increase bullet Damage", "Increases the damage of the bullets"),
        "debuff_bullet": ("Decrease bullet Damage", "Decreases the damage of the bullet"),
        "deflector": ("Deflector", "Shift all enemies up"),
        "emp": ("EMP Bomb", "Destroy x lives of enemies (x is based on current wave)"),
        "hp_up": ("1 up", "Increases life of player"),
        "shield_up": ("Shields up", "Create blocks to shield player")
    }

    def __init__(self, screen_width: int, screen_height: int, screen, fps, debug: bool = False):
        """Constructor for the powerup instructions screen"""

        # Store the fps
        self.fps = fps

        # Call the superclass
        super().__init__(screen_width, screen_height, State.POWERUP_INSTRUCTIONS, screen, debug)

    def preprocess(self):
        """Load other variables which will be used later"""
        # Load the powerups on the screen
        self.items = tuple(map(lambda x: (x[0], ImageObject(self.screen_width // 2,
                                                            self.screen_height // 5 + self.screen_height // 15, 50, 50,
                                                            x[1], self.debug)), PowerUp.sprites_dict.items()))

        # Load the current page
        self.page = 1
        self.total_pages = len(self.items)

    def write_lines(self):
        """Write the header"""

        # Draw the header
        self.header = self.write(self.title_font, WHITE, "Power Ups", self.screen_width // 2, self.screen_height // 5)

        # Draw the back button
        self.back = self.write(self.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height // 1.2)

        # Write data onto the main screen
        self.main_write()

    def get_rects(self) -> tuple:
        """Get the rects within the game"""
        return (self.prev, self.back, self.next)

    def get_effects(self) -> tuple:
        """Get the effects within the game"""
        return (self.dec_page, self._back, self.inc_page)

    def _back(self):
        """The command to run when the player backs"""
        # Reset the page when player backs
        self.page = 1

        # Return the instructions menu screen
        return State.INSTRUCTIONS_MENU

    def inc_page(self):
        """Function to be executed when player clicks next"""

        # If current page is less than next page
        if self.page < self.total_pages:
            # Increment the page by 1
            self.page += 1

        # Return the current state
        return self.state

    def dec_page(self):
        """Function to execute when player clicks prev"""

        # If it is more than page 1
        if self.page > 1:
            # Decrease the page by 1
            self.page -= 1

        # Return the current state
        return self.state

    def insert_description(self, first_px, description: str) -> None:
        """Writes the description for the powerup"""

        # Shift by screen_height //7.5 from first pixel
        first_px += + self.screen_height // 7.5

        # Splits the words
        words = description.split()
        written = 0

        # While loop to write content
        while written < len(words):

            # Accumulator
            curr = []

            # While the character limit is not exceeded
            while sum(map(lambda x: len(x), curr)) < 20 and written < len(words):
                # Add words to list
                curr.append(words[written])

                # Increase written words
                written += 1

            # Write the accumulated words
            self.write_main(self.end_font, WHITE, " ".join(curr), self.screen_width // 2, first_px)

            # Increment first_px to next pt
            first_px += self.screen_height // 15

    def main_write(self):
        """Writing the main information onto the screen"""

        # First pixel used for alignment
        first_px = self.screen_height // 5 + self.screen_height // 15 + 50

        # Unpack powerup sprites
        name, img = self.items[self.page - 1]

        # Draw the powerups name
        self.write_main(self.end_font, WHITE, f"{self.description[name][0]}", self.screen_width // 2, first_px)

        # Draw the description
        self.insert_description(first_px, self.description[name][1])

        # Draw the icon
        img.draw(self.screen)

        # Draw page related items
        self.draw_pages()

    def draw_pages(self):
        """Draw page related items"""
        # Draw the next button
        if self.page < self.total_pages:
            self.next = self.write_main(self.end_font, WHITE, "Next", self.screen_width // (4 / 3),
                                        self.screen_height // 1.2)
        else:
            self.next = self.write_main(self.end_font, GREY, "Next", self.screen_width // (4 / 3),
                                        self.screen_height // 1.2)

        # Draw the prev button
        if self.page > 1:
            self.prev = self.write_main(self.end_font, WHITE, "Prev", self.screen_width // 4, self.screen_height // 1.2)
        else:
            self.prev = self.write_main(self.end_font, GREY, "Prev", self.screen_width // 4, self.screen_height // 1.2)

        # Draw the pages
        self.write_main(self.end_font, WHITE, f"{self.page} / {self.total_pages}", self.screen_width // 2,
                        self.screen_height // 1.1)

    def handle(self) -> State:
        """Handle the drawing of the PVP instructions screen"""

        # Do the main writing on the screen
        self.main_write()

        # Call the superclass handle
        return super().handle()
