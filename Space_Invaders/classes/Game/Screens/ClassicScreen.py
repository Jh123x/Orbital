import pygame
import random
from pygame.locals import *
from . import Screen
from .. import *

class ClassicScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, max_fps:int, difficulty:Difficulty,
                 tracker, wave:int = 1, player_lives:int = 3,  debug:bool = False):
        """Constructor for Classic screen for the game"""

        #Call the superclass init
        super().__init__(screen_width, screen_height, State.CLASSIC, screen, 0, 0, debug)

        #Store the variables
        self.p1_score = 0
        self.wave = wave - 1
        self.sensitivity = int(sensitivity * self.screen_width/600)
        self.fps = max_fps
        self.difficulty = difficulty
        self.player_lives = player_lives
        self.over = False
        #Define a set of constants in the set
        self.session_stats= {'sf':0,'en_k':0,'el_k':0,'sl':0,'pu': 0,'mpu':0,'ek_c':0,'ek_e':0,'tut_n_clr':0,'st_1_clr':0,
                             'st_2_clr':0,'st_3_clr':0, 'st_4_clr':0,'st_5_clr':0,'st_6_clr':0,'coop':0,'pvp':0,'aivs':0,
                             'aicoop':0}
        self.max_stat = {'ek_c', 'mpu','ek_c','ek_e'}
        self.main_stats = {}
        self.tracker = tracker

        #Create the groups
        #Bullets shot by player
        self.player1_bullet = pygame.sprite.Group()

        #Bullet from Mobs
        self.mob_bullet = pygame.sprite.Group()

        #Enemyships
        self.enemies = EnemyShips(self.state)
        self.other_enemies = pygame.sprite.Group()
        
        #Blocks
        self.blocks = pygame.sprite.Group()

        #Explosions
        self.explosions = pygame.sprite.Group()

        #Spawn the players
        self.spawn_players()

        # Initialise values for tracker
        self._killed = None
        self.max_kill = None

        #Set resetted to false
        self.resetted = False

        #Reset the variables
        self.reset()

    def spawn_players(self):
        """Spawn the players"""
        #Create the player
        self.player1 = Player(self.sensitivity, self.screen_width, self.screen_height, self.screen_width//2, self.screen_height - 50, 3, self.fps, self.player1_bullet, Direction.UP, self.debug)

    def reset(self) -> None:
        """Reset the play screen and variables"""

        #Update the tracker
        self.update_trackers()

        #Reset the session tracker
        for key in self.session_stats.keys():

            #Reset the value
            self.session_stats[key] = 0

        #If already resetted
        if self.resetted:

            #Do nothing
            return

        #Store mothership cooldown
        self.ms_cooldown = 0
        self._shots = 0
        #Reset the over
        self.over = False
        
        #Zero the score and the wave
        self.p1_score = 0
        self.wave = 0

        #Set resetted to True
        self.resetted = True

        #Empty the sprite groups
        self.player1_bullet.empty()
        self.mob_bullet.empty()
        self.enemies.empty()
        self.other_enemies.empty()
        self.explosions.empty()

        #Reset the blocks to original block group
        self.blocks = BlockGroup(self.screen_width, self.screen_height, self.screen_width, self.screen_height//1.2, self.screen, 5, self.player1.get_height() + 10)

        #Reset the player
        self.player1.reset()

        #Fetch achievement stats
        self.fetch_stats()

    def fetch_stats(self, keys:tuple = None) -> dict:
        """Fetch the stats"""
        #If there are no keys
        if not keys:

            #Call the classic trackers
            keys = ("sf", "en_k","sl" ,"el_k", "ek_c")

        #For each item
        for key in keys:

            #Store the stat in the screen
            self.main_stats[key] = self.tracker.get_stat(key)

    def get_hitboxes(self) -> list:
        """Get a list of hitboxes of mobs"""
        return [(self.player1.get_coord()), tuple(x.get_coord() for x in self.player1_bullet), tuple(x.get_coord() for x in self.enemies), tuple(x.get_coord() for x in self.mob_bullet)]

    def get_enemies(self) -> tuple:
        """Get a tuple of the enemies"""
        return tuple(self.enemies)

    def comparator(self) -> int:
        """Variable used for comparison"""
        return self.get_score()

    def update_keypresses(self) -> None:
        """Update the screen based on what the player has pressed"""

        #Get all the number of keys
        keys = pygame.key.get_pressed()

        #Check if they want to pause game
        if keys[K_p] or keys[K_ESCAPE]:
            return True

        if not self.player1.is_destroyed():
            #Check player 1 keys
            if keys[K_a]:

                #Move player 1 to the left
                self.player1.move_left()

            if keys[K_d]:
                
                #Move player 1 to the right
                self.player1.move_right()

            if keys[K_SPACE]:

                #Let the player shoot
                self.player1.shoot()

    def spawn_enemy_bullets(self) -> None:
        """Spawns a bullet randomly for the enemy"""

        #Check if the enemy can shoot randomly
        rand = self.generate_random_no()*self.fps*4

        #If it does not hits the probability allow the mob to shoot
        if rand > 10:

            #Return and no need to shoot
            return

        #Get a random bullet for the entity to shoot
        if len(self.enemies):

            #Get a random enemy
            enemy = self.get_random_enemy()

        else:

            #Set enemy to none
            enemy = None

        #Make the mob shoot the bullet a random direction
        self.shoot_bullet(enemy)

    def bullet_direction(self) -> Direction:
        """Generate bullet direction for the mob"""
        return Direction.DOWN

    def shoot_bullet(self, enemy):
        """Make the mob shoot the bullet a random direction"""
        #If the set is non-empty
        if enemy:

            #Get direction of bullet
            direction = self.bullet_direction()

            #Make the mob shoot
            enemy.shoot(direction)

    def get_hitboxes_copy(self) -> pygame.Surface:
        """Get a copy of the hitboxes surface"""

        #Create a surface
        surface = pygame.Surface((self.screen_width, self.screen_height))

        #Fill the screen with black
        surface.fill((0, 0, 0))

        #Draw on the surface
        self.draw_hitboxes(surface)

        #Return the surface that is drawn on
        return surface

    def get_entities(self):
        """Get the entities for AI to process"""
        return self.enemies, self.other_enemies, self.mob_bullet

    def draw_hitboxes(self, screen = None):
        """Draw hitboxes for players and objects"""
        #Check if screen is none
        if screen == None:

            #Set to self.surface if it is none
            screen = self.surface

        #Draw the hitbox for the blocks at the bottom
        for sprite in self.blocks:
            pygame.draw.rect(screen, (0, 255, 0), sprite.rect, 0)

        #Draw hitbox for the enemies
        for sprite in self.enemies:
            c = (sprite.get_lives())*3
            pygame.draw.rect(screen, (200,5*c,5*c), sprite.rect, 0)

        #Draw the hitbox for the bosses
        for sprite in self.other_enemies:
            pygame.draw.rect(screen, (150,150,150), sprite.rect, 0)

        #Draw hitbox for the bullets
        for sprite in self.player1_bullet:
            pygame.draw.rect(screen, (100,255,0), sprite.rect, 0)
        for sprite in self.mob_bullet:
            pygame.draw.rect(screen, (25,0,255), sprite.rect, 0)

        #Draw the hitbox for the player
        pygame.draw.rect(screen, (55,255,10*self.player1.get_lives()), self.player1.rect, 0)

    def update(self) -> None:
        """Update the player and the sprites"""

        #If the game was resetted
        if self.resetted:

            #set resetted as false
            self.resetted = False

        #Reset the surface
        self.reset_surface()

        #Update the player position
        self.player1.update()

        #Update the enemy group
        self.enemies.update()

        #Update the other sprites group
        self.other_enemies.update()

        #Attempts to spawn the mothership
        self.randomly_spawn_mothership()

        #Update the explosions group
        self.explosions.update()

        #Spawn bullets for enemies
        self.spawn_enemy_bullets()

        #Update the position of all bullets
        self.player1_bullet.update()
        self.mob_bullet.update()

        #Draw the sprites
        self.draw_sprites()

        #Call superclass update
        super().update()

    def draw_sprites(self):
        """Draw the sprites"""
        #Draw bullets
        self.player1_bullet.draw(self.screen)
        self.mob_bullet.draw(self.screen)

        #Draw the enemy
        self.enemies.draw(self.screen)

        #Draw the other_mobs
        self.other_enemies.draw(self.screen)

        #Draw the explosions
        self.explosions.draw(self.screen)

        #Draw player object
        self.player1.draw(self.screen)

        #Draw the block
        self.blocks.draw(self.screen)

    def get_score(self) -> int:
        """Gets the score of the player in the current state"""
        return self.p1_score

    def generate_random_no(self) -> int:
        """Generates a random float from 0 to 1"""
        #Generate random number
        return random.random()

    def wave_random(self) -> int:
        """Generate a random number for the life of the enemy"""
        #Generate wave random
        num = int(self.difficulty.get_multiplier(self.generate_random_no()*self.wave))
        return num if num >= 1 else 1

    def get_random_enemy(self) -> EnemyShip:
        """Get a random enemy"""

        #Get a list of enemies
        lst = tuple(self.enemies)

        #Randomly choose 1 of them
        return lst[int(self.generate_random_no()* (len(lst)-1))]

    def check_block_collision(self):
        """Check collisions of the blocks"""
        #Check if the player or the enemies shot the blocks
        pygame.sprite.groupcollide(self.player1_bullet, self.blocks, True, True)
        pygame.sprite.groupcollide(self.blocks, self.mob_bullet, True, True)

    def check_other_mob_collision(self) -> int:
        """Check collisions for special mobs"""
        
        #Get list of ships collided
        sprites = list(pygame.sprite.groupcollide(self.player1_bullet, self.other_enemies, True, False).values())

        #If there are ships
        if sprites:

            #Get the first ship
            ship = sprites[0][0]

            #Destroy the ship 1 time
            ship.destroy(self.player1.get_bullet_power())

            #Remove the ship from groupp if it has 0 lives
            if ship.is_destroyed():

                #Spawn an explosion in its place
                self.spawn_explosion(ship.get_x(), ship.get_y())

                #Remove ship from all groups
                ship.kill()
                self.accumulate('en_k', 1)
                self.accumulate('el_k', 1)

                #Return the points of the ship
                return ship.get_points()

        #return 0 score
        return 0

    def accumulate(self, k, v):
        '''Accumulate a stat in the dictionary'''
        self.session_stats[k] += v

        if k in self.main_stats:
            self.main_stats[k] += v

    def update_trackers(self):
        '''Update stat tracker stats that we want to add'''
        #Update relavant stats
        for k,v in self.main_stats.items():
            if k in self.max_stat:
                self.tracker.set_max_value(k,self.session_stats[k])
            else:
                self.tracker.set_value(k,v)

            #Check if any achievements was achieved
            self.tracker.check_unlocked(k,v)

    def handle_threshold(self) -> None:
        ''' Handle updating threshold value for given statistics -> throws popup on screen'''
        if self.session_stats['en_k'] == self.main_stats['ek_c'] + 1 and self.session_stats['ek_c'] == 0:
            self.tracker.add_popup("This is the highest kills you got!")
        if self.session_stats['en_k'] >= self.main_stats['ek_c'] + 1:
            self.session_stats['ek_c'] = self.session_stats['en_k']

    def check_collisions(self):
        """Check the objects which collided"""

        #Check block collisions
        self.check_block_collision()

        #Check if player has collided with bullets
        bullet_collide = pygame.sprite.spritecollide(self.player1, self.mob_bullet, True)
        
        #If the set is not empty reduce player life
        if len(bullet_collide) > 0:

            #If it is in debug mode, print the event
            if self.debug:
                print("Player hit")

            #Destroy 1 of the player's life
            self.player1.destroy()

            # Update Statistic Tracker to track 1 Ship destroyed
            self.accumulate('sl', 1)

            #Add explosion to the player's position
            self.spawn_explosion(self.player1.get_x(), self.player1.get_y())

        #Remove bullets that collide with one another
        pygame.sprite.groupcollide(self.player1_bullet, self.mob_bullet, True, True)

        #Get list of ships destroyed
        ships = list(pygame.sprite.groupcollide(self.player1_bullet, self.enemies, True, False).values())

        #Initialise score
        score = self.check_other_mob_collision()

        #Initialise ship to None
        ship = None

        #If the list of collision is non-empty
        if ships:

            #Get the ship it collided with 
            ship = ships[0][0]

            #Destroy the first ship in the list (Ensures 1 bullet kill 1 ship only)
            ship.destroy(self.player1.get_bullet_power())

            if self.debug:
                print(f"Ship destroyed")
        
            #Remove the ship from groupp if it has 0 lives
            if ship.is_destroyed():

                #Spawn an explosion in its place
                self.spawn_explosion(ship.get_x(), ship.get_y())

                #Remove the ship from all groups
                ship.kill()

                # Track Statistics for killing ship
                self.accumulate('en_k', 1)

                #Remove sprites that collide with bullets and return the sum of all the scores
                score = ship.get_points()

        #Add score to player score
        self.p1_score += score

        #Returns destroyed ship
        return ship

    def update_achievement(self):
        """Updates achievements for the game"""
        for key,value in self.main_stats.items():
            self.tracker.check_unlocked(key, value)

    def spawn_explosion(self, x:int, y:int) -> None:
        """Spawn an explosion at specified x and y coordinate"""

        #Spawn an explosion
        self.explosions.add(Explosion(self.fps//4, x, y, self.screen_width, self.screen_height, 0, self.debug))

    def spawn_enemies(self, number:int) -> None:
        """Spawn n enemies into the game"""
        
        #Make the enemies into rows of 6
        for j in range(number//6 if number // 6 < 5 else 5):

            self.enemies.add([EnemyShip(self.sensitivity, self.screen_width//4 + i * self.screen_width//10 * self.screen_width // 600, 
                            self.screen_height//10 + EnemyShip.sprites[0].get_height() * j * self.screen_height // 800, 
                            self.wave_random(), self.screen_width,  self.screen_height, Direction.DOWN, self.mob_bullet, self.debug) for i in range(6)])

    def randomly_spawn_mothership(self) -> bool:
        """Spawns a mothership randomly, returns if mothership is spawned"""

        #If the mothership does not exist and the random roll hits
        if not self.ms_cooldown and self.generate_random_no() < 1/900:
            
            #Create the mothership
            self.other_enemies.add(MotherShip(0, 50, self.screen_width, self.screen_height, 500))

            #Set the cooldown for the mothership
            self.ms_cooldown = self.fps * 3

            #Return True to signify that mothership spawned
            return True

        #If mothership is still under cooldown
        elif self.ms_cooldown:

            #Reduce cooldown by 1
            self.ms_cooldown -= 1

        #return False if a mothership does not spawn
        return False

    def enemy_touched_bottom(self) -> bool:
        """Check if enemy touched the bottom of the screen"""
        return any(filter(lambda x: (x.get_y() + x.get_height()//2) > (self.screen_height - self.player1.get_height() - 100), self.enemies)) or \
                any(filter(lambda x: (x.get_y() + x.get_height()//2) > (self.screen_height - self.player1.get_height() - 100), self.other_enemies))

    def is_over(self) -> bool:
        """Checks if the game is over"""
        return self.over

    def draw_letters(self) -> None:
        """Draw the letters on the screen"""
        #Draw the score
        self.write_main(self.font, WHITE, f"Score : {self.p1_score}", 10, 10, Direction.LEFT)

        #Draw the live count
        self.write_main(self.font, WHITE, f"Lives : {self.player1.get_lives()}", self.screen_width - 10, 10, Direction.RIGHT)

        #Draw the wave number
        self.write_main(self.font, WHITE, f"Wave : {self.wave}",self.screen_width//2, 15)

    def get_pause_state(self) -> State:
        """Get the pause state for the game"""
        return State.PAUSE

    def get_gameover_state(self) -> State:
        """Get the gameover state for the game"""
        return State.GAMEOVER

    def end_game(self) -> None:
        """Ends the game and updates relevent statistics"""
        self.over = True

    def handle(self) -> State:
        """Handle the drawing of the classic screen"""
        
        #If it was initially resetted
        if self.resetted:

            #Set resetted to False
            self.resetted = False

        #If player is destroyed, go to gameover state
        if self.player1.is_destroyed():

            #Set the game to be over
            self.end_game()

            self.update_trackers()

            #Return the gameover state
            return self.get_gameover_state()

        #Check if any of the enemies touched the bottom of the screen
        if self.enemy_touched_bottom():

            #If it is debugging mode, print out what happened
            if self.debug:
                print("Alienship hit the player")

            #Set the game to be over
            self.end_game()
            # Update Trackers for the game variables
            self.update_trackers()
            #If so it is gameover for the player
            return self.get_gameover_state()

        #Spawn if there are no enemies 
        if not len(self.enemies):

            #Increase the wave number
            self.wave += 1

            #Reset wave powerup
            self.power_up_numbers = 0

            #Spawn the aliens
            self.spawn_enemies(int(6 * self.wave))

        if self._shots < len(self.player1_bullet):
            self.accumulate('sf', len(self.player1_bullet) - self._shots)

        #Get the number of player 1 bullets
        self._shots = len(self.player1_bullet)

        #Check object collisions
        self.check_collisions()

        # Update the max_killed if threshold is reached
        self.handle_threshold()

        #Return a list of achievement achieved
        self.update_achievement()

        #Draw the letters on the screen
        self.draw_letters()

        #Check the player keypress
        if self.update_keypresses():
            return self.get_pause_state()

        #Update the moving objs
        self.update()

        #Check if player wants to quit
        if self.check_quit():

            self.update_trackers()

            return State.QUIT

        #Return play state
        return self.state
        