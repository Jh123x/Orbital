import pygame
try:
    from .classes import *
except:
    from classes import *

class PyGame_2D(object):
    def __init__(self, settings:str):
        #Read the configuration file for space invaders
        #all_cfg = read_all(settings)
        #print(all_cfg)
        config = read_settings(settings,"Space Invaders")

        #Get the player sprites
        player_img_paths = tuple(read_settings(settings, "Player Sprites").values())

        #Get the bullet sprites Enemy Sprites
        bullet_img_paths = tuple(read_settings(settings, "Bullet Sprites").values())

        #Get the enemy sprites
        enemy_img_paths = tuple(read_settings(settings, "Enemy Sprites").values())

        #Get the background sprites
        background_img_paths = tuple(read_settings(settings, "Background").values())

        #Get the explosion image path
        explosion_img_paths = tuple(read_settings(settings, "Explosion Sprites").values())

        #Get the settings
        settings = read_settings(settings, "Player")

        # #Main configurations
        # config = all_cfg['Space Invaders']
        #
        # #Get the player sprites
        # player_img_paths = all_cfg["Player Sprites"].values()
        #
        # #Get the bullet sprites Enemy Sprites
        # bullet_img_paths = all_cfg["Bullet Sprites"].values()
        #
        # #Get the enemy sprites
        # enemy_img_paths = all_cfg["Enemy Sprites"].values()
        #
        # #Get the background sprites
        # background_img_paths = all_cfg["Background"].values()
        #
        # #Get the explosion image path
        # explosion_img_paths = all_cfg["Explosion Sprites"].values()
        #
        # #Get the settings
        # settings = all_cfg["Player"]

        #Load player ship images into Player object 
        add_to_sprite(Player, player_img_paths)

        #Load Bullet images into Bullet Object 
        add_to_sprite(Bullet, bullet_img_paths)

        #Load enemy ships into enemy ship objects 
        add_to_sprite(EnemyShip, enemy_img_paths)

        #Load the backgrounds into Background obj
        add_to_sprite(Background, background_img_paths)

        #Load the sprites for the explosion
        add_to_sprite(Explosion, explosion_img_paths)

        #Initialise pygame
        pygame.init()
        pygame.font.init()

        screen_width = 600
        screen_height = 800
        fps = 60

        self.written = False

        #Init screen
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        #Set fps
        self.clock = pygame.time.Clock()

        #Init playscreen
        self.state = PlayScreen(screen_width, screen_height, self.screen, 5, fps)

        #Player Object
        self.player = self.state.player
        self.nextState = -1
    


    def mainloop(self) -> None:
        """Mainloop"""
        screen_width = 600
        screen_height = 800
        fps = 60
        running = True
        while running:

            #Clock the fps
            self.clock.tick(fps)

            #Fill background with black
            self.screen.fill((0,0,0))

            #Draw the play screen
            self.nextState = self.state.handle()

            #Print score if the game is over
            if self.nextState == State.GAMEOVER:
                print(f"Score: {self.state.get_score()}")

            #Update the display with the screen
            pygame.display.update()
            print("hello from mainloop")

            #If the state is quit or player closes the game
            if pygame.QUIT in tuple(map(lambda x: x.type, pygame.event.get())):
                running = False

    def action(self, number:int):
        """Performs the action based on the number
            0: Shoot
            1: move left
            2: move_right
        """
        self.get_action()[number]()


    def get_action(self) -> tuple:
        """List of actions that the player can take (tuple of functions)"""
        return (self.player.shoot, self.player.move_left, self.player.move_right)

    def get_hitboxes(self) -> list:
        """Get the hitboxes of the """
        return self.state.get_hitboxes()

    def get_space(self) -> list:
        """Returns the pixel space of the screen"""
        return pygame.surfarray.array2d(self.state.screen)
    def is_over(self):
        '''Returns if game state is over or quit'''
        return self.nextState == State.GAMEOVER
    def is_playing(self):
        return self.nextState ==State.PLAY
    def get_score(self):
        return self.state.get_score()
    def reset(self):
        '''Wrapper method for reseting the screen'''
        self.state.reset()
    def get_player(self):
        '''get the player character position -- for Debugging Purposes'''
        return (self.player.get_x(),self.player.get_y())
    def get_enemies(self):
        '''Get positions of each enemy'''
        enemy_grp = self.state.get_enemies()
        l = []
        for e in enemy_grp:
            l.append((e.get_x(),e.get_y()))
        return l
if __name__ == '__main__':
    settings = "settings.cfg"
    game = PyGame_2D(settings)
    game.mainloop()
    
