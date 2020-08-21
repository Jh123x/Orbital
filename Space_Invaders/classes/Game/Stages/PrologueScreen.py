from . import StoryTemplate
from .. import AchievmentTracker, State, ImageObject, WHITE, Direction


class PrologueScreen(StoryTemplate):
    def __init__(self, screen_width: int, screen_height: int, screen, sensitivity: int, max_fps: int,
                 tracker: AchievmentTracker, debug: bool):
        # Call the superclass init method
        super().__init__(screen_width, screen_height, screen, State.PROLOGUE, sensitivity, max_fps,
                         0, tracker, debug)

        # Commander brief image
        self.bg = ImageObject(self.screen_width // 2, int(self.screen_height * 285 / 800), 600, 570,
                              StoryTemplate.sprites_dict["commander_brief"], debug)
        self.bg.scale(self.screen_width, int(self.screen_height * 57 / 80))

        # Image of the commander
        self.commander = ImageObject(self.screen_width // 2, int(self.screen_height * 210 / 800), 217, 217,
                                     StoryTemplate.sprites_dict['silloette_commander'], debug)
        self.commander.scale(int(217 * screen_width // 600), int(217 * screen_height // 800))

        # Textbox
        self.tb = ImageObject(self.screen_width // 2, int(self.screen_height * 685 / 800), 600, 230,
                              StoryTemplate.sprites_dict['textbox'], debug)
        self.tb.scale(self.screen_width, int(self.screen_height * 23 / 80))

    def update_trackers(self, *args):
        """Override update trackers to do nothing"""
        pass

    def win_condition(self) -> bool:
        """Override the win condition method"""
        return False

    def get_stage_name(self) -> str:
        """Get the stage name"""
        return "Prologue"

    def draw_bg(self):
        """Draw the background"""
        # Draw the commander brief
        self.bg.draw(self.screen)

        # Draw the textbox
        self.tb.draw(self.screen)

    def pre_cutscene(self):
        """The pre_cutscene for the class"""

        # Insert the Icon for the char speaking
        self.commander.draw(self.screen)

        # Draw the background
        self.draw_bg()

        # Draw the next button
        self.next_btn = self.write_main(self.end_font, WHITE, "Next", int(580 / 600 * self.screen_width),
                                        self.tb.rect.top - 30, Direction.RIGHT)

        # Lower cd of click if it is still on cooldown
        if self.click_cd:
            self.click_cd -= 1

        # Check if the next button is clicked
        if self.check_clicked(self.next_btn) and not self.click_cd:
            # Increment the clicks
            self.clicks += 1

            # Reset the cooldown
            self.click_cd = self.fps // 5

        # Write the character name text
        self.write_main(self.end_font, WHITE, "Dill Bates", 33, self.tb.rect.top + 15, Direction.LEFT)

        # Pixel vars for alignment
        first_px = self.tb.rect.top + 75
        left_px = 40

        if self.clicks == 0:

            # Write the character speech text
            self.render_speech(first_px, left_px,
                               ("In the year 2134, a certain virus has ravaged humanity for ",
                                "years and caused a great depression that lasts for years on ",
                                "end, only to end in a brutal war to end all wars, lasting ",
                                "until 2151"))

        elif self.clicks == 1:

            # Write part 2 of the speech
            self.render_speech(first_px, left_px, ("Throughout this war, a central figure was key",
                                                   " to bringing peace to the world, a military genius",
                                                   " and masterful strategist. With blood and iron, he",
                                                   " forged a lasting coalition, to bring order to the",
                                                   " world in ruins."))

        elif self.clicks == 2:
            self.render_speech(first_px, left_px, ("However, at the last step, he was mortally wounded",
                                                   " and cryogenically frozen. His legacy and symbol of",
                                                   " unity for years to come as the United Federation of",
                                                   " Earth"))
        elif self.clicks == 3:
            self.render_speech(first_px, left_px,("The year is now 2185.",
                                                  "Humanity has advanced and prospered after the great war,",
                                                  " advances in Physics and Robotics has allowed us to colonise",
                                                  " multiple areas in the Solar System including Mars, Titan and",
                                                  " even research outposts in Pluto. Humanity is well on it’s way",
                                                  " to taking its first steps out of the Solar System.",))

        elif self.clicks == 4:
            self.render_speech(first_px, left_px, ("Then… an intense radio wave burst through the solar system.",))

        elif self.clicks == 5:
            self.render_speech(first_px, left_px, ("A call from the void, an unknown force that affected many Data",
                                                   " Centers and Robots across the Solar System. Causing automated ",
                                                   "assets to malfunction. The grinding gears that fueled humanity’s",
                                                   " expansion came to a sudden halt. For a while, nothing extremely ",
                                                   "anomalous occurred, besides robots sometimes going missing, and ",
                                                   "small random errors in autonomous movements"))

        elif self.clicks == 6:
            self.render_speech(first_px, left_px, ("Then they came...",
                                                   "Reports came in from across the Federation, from Pluto,",
                                                   " being wiped out and Mars under siege."))

        elif self.clicks == 7:
            self.render_speech(first_px, left_px, ("Now they stand at the gates of the last line of defence of ",
                                                   "Humanity, Arkbird, the International Space Fortress, where ",
                                                   "work on the final effort to turn the tides has just been ",
                                                   "completed. "))

        elif self.clicks == 8:
            self.render_speech(first_px, left_px, ("Commander, it has been a long time since we prevailed and ",
                                                   "united under your guidance.",
                                                   "Commander, please lend us your strength, and defend earth ",
                                                   "and the solar system as the Space Defender."))

        else:
            # Reset the clicks
            self.clicks = 0

            # Move to the next scene
            self.next_scene()

        # Return the current state
        return self.state

    def post_cutscene(self):
        """Plays the post cutscene for the story"""
        return self.get_victory_state()

    def handle(self):
        # If it is the pre_cutscene stage
        if self.curr == 0:
            return self.pre_cutscene()

        # If it is the post_cutscene state
        else:
            return self.post_cutscene()
