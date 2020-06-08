import pygame
import numpy
from classes import *

class PyGame_2D(object):
    def __init__(self, settings:str):
        """Pygame_2d object for AI to be trained on"""

        #Read the configuration file for space invaders
        settings = "settings.cfg"

        #Read the configuration file for space invaders
        all_cfg = read_all(form_abs_path(__file__,settings))
        
        #Main configurations
        config = all_cfg['Space Invaders']
        config['icon_img_path'] = form_abs_path(__file__, config['icon_img_path'])

        #Load all
        d = load_all(("bullet_img_paths",), ("Bullet Sprites",), all_cfg, __file__)

        #Load the other sprites 
        d["player_img_paths"] = list_dir(form_abs_path(__file__, "images/player"))
        d["enemy_img_paths"] = list_dir(form_abs_path(__file__, "images/enemies"))
        d["explosion_img_paths"] = list_dir(form_abs_path(__file__, "images/explosions"))
        
        #DBPath
        db_path = form_abs_path(__file__,'data/test.db')

        #Sound
        sound_path = dict(zip(all_cfg["Sounds"].keys(),list(map(lambda x: form_abs_path(__file__, x), all_cfg["Sounds"].values()))))

        #Load sprites
        load_sprites((Player, Bullet, EnemyShip, Explosion), (d["player_img_paths"], d["bullet_img_paths"], d["enemy_img_paths"], d["explosion_img_paths"]))

        #Load sounds
        self.sound = Sound(asyncio.run(load_sound(sound_path)), False, False)

        #Load the sounds into the relavant Sprites
        Bullet.sound = self.sound

        #Add explosion sound
        Explosion.sound = self.sound

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
        self.state = PlayScreen(screen_width, screen_height, self.screen, 5, fps, Difficulty(4))

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
            #print("hello from mainloop")

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

    def get_space(self) -> numpy.array:
        """Returns the pixel space of the screen"""
        return pygame.surfarray.array2d(self.state.screen)

    def get_space_boolean(self) -> list:
        """Returns the pixel space of the screen in terms of boolean"""
        f = numpy.vectorize(lambda x: 0 if x == 0 else 1)
        return f(self.get_space())

    def is_over(self):
        '''Returns if game state is over or quit'''
        return self.player.is_destroyed()

    def is_playing(self):
        return self.nextState ==State.PLAY

    def get_score(self):
        """Get the current score"""
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
    