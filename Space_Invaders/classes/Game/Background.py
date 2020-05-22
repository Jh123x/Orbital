import pygame

class Background(pygame.sprite.Sprite):
    #To store the background sprites
    sprites = []

    def __init__(self, bg_no:int, game_width:int, game_height:int):
        """Constructor for the background class"""

        #Calls the superclass
        super().__init__()

        #Gets the background image if any
        self.image = Background.sprites[bg_no - 1] if bg_no >= len(Background.sprites) else None
        self.rect = None

        #If there is a background image get the rect for it
        if self.image != None:

            #Scale the image to the correct size
            self.image = pygame.transform.scale(self.image, (game_width, game_height))

            #Get the rect
            self.rect = self.image.get_rect()

            #Set the top left of rect to top left of the game
            self.rect.left, self.rect.top = 0,0

    def is_present(self) -> bool:
        """Check if there is a valid background"""
        return self.image

    def update(self, screen) -> None:
        """Blit the background to the screen"""
        screen.blit(self.image, self.rect)