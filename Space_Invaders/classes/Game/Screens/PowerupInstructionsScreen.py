from . import Screen
from .. import State, PowerUp, WHITE, GREY, ImageObject

class PowerupInstructionsScreen(Screen):

    description = {
        'bullet_up' : ("Increase bullet speed","Increases the speed of the bullets"), 
            'bullet_attack_up' : ("Increase bullet Damage", "Increases the damage of the bullets"), 
            "debuff_bullet" : ("Decrease bullet Damage", "Decreases the damage of the bullet"), 
            "deflector" : ("Deflector", "Shift all enemies up"), 
            "emp" : ("EMP Bomb", "Destroy x lives of enemies (x is based on current wave)"), 
            "hp_up" : ("1 up", "Increases life of player"), 
            "shield_up" : ("Shields up", "Create blocks to shield player")
    }

    def __init__(self, screen_width:int, screen_height:int, screen, fps, debug:bool = False):
        """Constructor for the powerup instructions screen"""

        #Call the superclass
        super().__init__(screen_width, screen_height, State.POWERUP_INSTRUCTIONS, screen, 0, 0, debug)

        #Store the fps
        self.fps = fps

        #Draw the header
        self.header = self.write(Screen.title_font, WHITE, "Power Ups", self.screen_width//2, self.screen_height//5)

        #Load the powerups on the screen
        self.powerups = tuple(map(lambda x: (x[0],ImageObject(self.screen_width//2, self.screen_height//5 + self.screen_height // 15, 50, 50,x[1], debug)), PowerUp.sprites.items()))

        #Load the current page
        self.page = 1
        self.total_pages = len(PowerUp.get_powerups()) - 1

        #Set the cooldown
        self.cooldown = self.fps//5

        #Draw the back button
        self.back = self.write(Screen.end_font, WHITE, "Back", screen_width//2, screen_height//1.2)


    def check_keypresses(self) -> State:
        """Check the keypresses on the PVP instructions screen"""

        if self.cooldown:
            self.cooldown -= 1
            return self.state
        
        #If the player clicks on back
        elif self.check_clicked(self.back):
            return State.INSTRUCTIONS_MENU

        #If player clicks on next page
        elif self.page < self.total_pages and self.check_clicked(self.next):
            self.page += 1

            #Set the cooldown
            self.cooldown = self.fps//5
        
        #If player clicks on prev page
        elif self.check_clicked(self.prev) and self.page > 1:

            #Decrease the page by 1
            self.page -= 1

            #Set the cooldown
            self.cooldown = self.fps//5

        #Otherwise return current state
        return self.state

    def insert_description(self, first_px, description:str) -> None:
        """Writes the description for the powerup"""

        #Shift by screen_height //7.5 from first pixel
        first_px += + self.screen_height // 7.5

        #Splits the words
        words = description.split()
        written = 0

        #While loop to write content
        while written < len(words):

            #Accumulator
            curr = []

            #While the character limit is not exceeded
            while sum(map(lambda x : len(x),curr)) < 30 and written < len(words):

                #Add words to list
                curr.append(words[written])

                #Increase written words
                written += 1

            #Write the accumulated words
            self.write_main(Screen.end_font, WHITE, " ".join(curr), self.screen_width//2, first_px)

            #Increment first_px to next pt
            first_px += self.screen_height//15

    def handle(self) -> State:
        """Handle the drawing of the PVP instructions screen"""

        #First pixel used for alignment
        first_px = self.screen_height//5 + self.screen_height // 15 + 50

        #Unpack powerup sprites
        name,img = self.powerups[self.page]

        #Draw the powerups name
        self.write_main(Screen.end_font, WHITE, f"{self.description[name][0]}", self.screen_width // 2, first_px)

        #Draw the description
        self.insert_description(first_px, self.description[name][1])
        
        #Draw the icon
        img.draw(self.screen)

        #Draw the next button
        if self.page < self.total_pages:
            self.next = self.write_main(Screen.end_font, WHITE, "Next", self.screen_width//(4/3), self.screen_height//1.2)
        else:
            self.next = self.write_main(Screen.end_font, GREY, "Next", self.screen_width//(4/3), self.screen_height//1.2)

        #Draw the prev button
        if self.page > 1:
            self.prev = self.write_main(Screen.end_font, WHITE, "Prev", self.screen_width//4, self.screen_height//1.2)
        else:
            self.prev = self.write_main(Screen.end_font, GREY, "Prev", self.screen_width//4, self.screen_height//1.2)

        #Draw the pages
        self.write_main(Screen.end_font, WHITE, f"{self.page} / {self.total_pages}", self.screen_width//2, self.screen_height//1.1)

        #Update the screen
        self.update()

        #Check for keypresses
        return self.check_keypresses()