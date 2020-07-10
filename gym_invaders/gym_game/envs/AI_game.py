import pygame
import numpy as np
import matplotlib.pyplot as plt
try:
    from .classes import *
except ImportError:
    from classes import *

class PyGame_2D(object):
    def __init__(self, settings:str, t:str = 'Play'):
        """Pygame_2d object for AI to be trained on"""

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
        d["powerup_img_path"] = list_dir(form_abs_path(__file__,"images/powerups"))
        d["mothership_img_path"] = list_dir(form_abs_path(__file__,"images/bosses/mothership"))

        #Load sprites
        load_sprites((Player, Bullet, EnemyShip, Explosion, PowerUp, MotherShip), 
                    (d["player_img_paths"], d["bullet_img_paths"], d["enemy_img_paths"], d["explosion_img_paths"], d["powerup_img_path"], d["mothership_img_path"]))

        #Load sounds
        self.sound = Sound({}, False, False)

        #Load the sounds into the relavant Sprites
        Bullet.sound = self.sound

        #Add explosion sound
        Explosion.sound = self.sound

        #Initialise pygame
        pygame.init()
        pygame.font.init()

        self.screen_width = 600
        self.screen_height = 800
        self.fps = 60

        #Init screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        #Init playscreen
        self.state = self.create_screen()

        self.written = False

        #Set fps
        self.clock = pygame.time.Clock()

        #Player Object
        self.player = self.state.player
        self.nextState = -1

    def create_screen(self) -> Screen:
        """Create the playscreen by default"""
        return PlayScreen(self.screen_width, self.screen_height, self.screen, 5, self.fps, Difficulty(4))

    def mainloop(self) -> None:
        """Mainloop"""
        running = True
        while running:

            #Clock the fps
            self.clock.tick(self.fps)

            #Fill background with black
            self.screen.fill((0,0,0))

            #Draw the play screen
            self.nextState = self.state.handle()

            #Draw the hitbox
            self.state.draw_hitboxes()

            #Print score if the game is over
            if self.nextState == State.GAMEOVER:

                #Print the score and quit the game
                print(f"Score: {self.state.get_score()}")

            #Update the display with the screen
            pygame.display.update()
            
            #print(self.get_space_boolean())
            #If the state is quit or player closes the game
            for item in pygame.event.get():
                if item.type == pygame.QUIT:
                    running = False

    def action(self, number:int) -> None:
        """Performs the action based on the number
            0: Shoot
            1: move left
            2: move_right
            3: Do nothing
        """
        self.get_action()[number]()

    def get_wave(self):
        return self.state.get_wave()

    def move_shoot(self, b:bool) -> bool:
        '''
        To encompass both move_left and shoot, and move_right and shoot action
        from Original Space Invaders Gym Environment
        '''
        if b:
            self.player.move_left()
            return self.player.shoot
        self.player.move_right()
        return self.player.shoot

    def get_action(self) -> tuple:
        """List of actions that the player can take (tuple of functions)"""
        return (self.player.shoot, 
                self.player.move_left, 
                self.player.move_right, 
                lambda : 1, 
                self.move_shoot(True),
                self.move_shoot(False))

    def get_space(self):
        """
        Returns the pixel space of the screen
        Performs preliminary Preprocessing by making values
        """

        #load the hitbox
        self.state.draw_hitboxes()

        #Returns the array
        return pygame.surfarray.array3d(self.state.surface) 

    def show_space(self):
        """Show the space in a matplotlib diagram"""
        image_transp = np.transpose(self.get_space())
        plt.imshow(image_transp, interpolation='none')
        plt.show()

    def is_over(self) -> bool:
        '''Returns if game state is over or quit'''
        return self.state.is_over()

    def get_score(self) -> int:
        """Get the current score"""
        return self.state.get_score()

    def reset(self) -> None:
        '''Wrapper method for reseting the screen'''
        self.state.reset()

    def get_player(self) -> tuple:
        '''Get the player character position -- for Debugging Purposes'''
        return (self.player.get_x(),self.player.get_y())

    def get_player_lives(self):
        """Get the number of lives of the player"""
        return self.player.get_lives()

    def get_enemies(self) -> tuple:
        '''Get positions of each enemy'''
        return tuple(map(lambda e: (e.get_x(),e.get_y()), self.state.get_enemies()))

    def handle(self):
        '''Draws the hitboxes of each enemy after updating the state of the enemy'''
        self.state.handle()
        self.state.draw_hitboxes()

    def close(self):
        self.state.close()

if __name__ == '__main__':
    settings = "settings.cfg"
    game = PyGame_2D(settings)
    game.mainloop()
    