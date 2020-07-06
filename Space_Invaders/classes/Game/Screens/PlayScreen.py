import pygame
import random
from pygame.locals import *
from . import Screen
from .. import *

class PlayScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, max_fps:int, difficulty: Difficulty, wave:int = 1, player_lives:int = 3, powerup_chance:float = 0.1, debug:bool = False):
        """The Play screen
            Arguments:
                screen_width: Width of the game in pixels (int)
                screen_height: Height of the game in pixels (int)
                screen: Surface where the play screen is blited to (pygame.Surface)
                sensitivity: Sensitivity of the player controls (int)
                max_fps: fps at which the game is run at (int)
                wave: The wave which the game starts at (int): default = 1
                player lives: Life player starts with
                powerup_chance: Chance of spawning powerups (0 to disable)
                debug: Boolean indicating debug mode (bool): default = False

            Methods:
                update_keypresses: Update the player's keypress to update the screen
                spawn_enemy_bullets: Make the enemies shoot randomly
                update: Update the movement of the sprites
                get_score: Get the current score of the player
                reset: Reset the play state
                check_collisions: Check for collisions between the entities and the bullets
                spawn_enemies: Spawn enemy mobs
                handle: handles the drawing of the play screen onto the surface
        """

        #Call the superclass init
        super().__init__(screen_width, screen_height, State.PLAY, screen, 0, 0, debug)

        #Store the variables
        self.score = 0
        self.wave = wave - 1 
        self.sensitivity = sensitivity
        self.fps = max_fps
        self.difficulty = difficulty
        self.over = False
        self.powerup_chance = powerup_chance

        #Create the groups
        #Bullets shot by player
        self.up_bullets = pygame.sprite.Group()

        #Bullet from Mobs
        self.down_bullets = pygame.sprite.Group()

        #Enemyships
        self.enemies = EnemyShips(self.state)

        #Blocks
        self.blocks = pygame.sprite.Group()

        #Explosions
        self.explosions = pygame.sprite.Group()

        #Power ups
        self.powerups = pygame.sprite.Group()

        #Create the player
        self.player = Player(sensitivity, screen_width, screen_height, screen_width//2, screen_height - 50, 3, max_fps, self.up_bullets, Direction.UP, debug)

        #Reset the variables
        self.reset()

    def reset(self) -> None:
        """Reset the play screen and variables
            Arguments:
                No arguments
            Returns: 
                No returns
        """

        #Reset powerup number
        self.powerup_numbers = 0

        #Reset no mothership
        self.mothership = None

        #Store mothership cooldown
        self.ms_cooldown = 0

        #Reset the over
        self.over = False
        
        #Zero the score and the wave
        self.score = 0
        self.wave = 0

        #Empty the sprite groups
        self.up_bullets.empty()
        self.down_bullets.empty()
        self.enemies.empty()
        self.explosions.empty()
        self.blocks.empty()
        self.powerups.empty()

        #Reset the player
        self.player.reset()

    def get_hitboxes(self) -> list:
        """Get a list of hitboxes of mobs"""
        return [(self.player.get_coord()), tuple(x.get_coord() for x in self.up_bullets), tuple(x.get_coord() for x in self.enemies), tuple(x.get_coord() for x in self.down_bullets)]

    def get_enemies(self) -> tuple:
        """Get a tuple of the enemies"""
        return tuple(self.enemies)

    def update_keypresses(self) -> None:
        """Update the screen based on what the player has pressed
            Arguments:
                No arguments
            Returns:
                No returns
        """
        #Check the keys the player has pressed
        keys = pygame.key.get_pressed()

        #If the player has click 'Left' or 'a' move the player to the left
        if keys[K_a] or keys[K_LEFT]: 
            self.player.move_left()

        #If the player has click 'right' or 'd' move the player to the right
        if keys[K_d] or keys[K_RIGHT]:
            self.player.move_right()

        #Check if the player pressed spacebar to spawn a bullet
        if keys[K_SPACE]:

            #Make the player shoot
            self.player.shoot()

        #Check for debug keypresses
        if self.debug:

            #if 'q' is pressed
            if keys[K_q]:

                #Deduct the life of the player 
                self.player.destroy()

    def spawn_enemy_bullets(self) -> None:
        """Spawns a bullet randomly for the enemy
            Arguments: 
                No arguments
            Returns: 
                No returns
        """

        #Check if the enemy can shoot randomly
        rand = random.randint(0,self.fps*50)

        #If it does not hits the probability allow the mob to shoot
        if rand > self.fps:

            #Print debug statements
            if self.debug:
                print(f"Random generated: {rand}")

            #Return and no need to shoot
            return

        #Get a random bullet for the entity to shoot
        if len(self.enemies):

            #Get a random enemy
            enemy = self.get_random_enemy()

            #Make the enemy shoot
            enemy.shoot()

    def draw_hitboxes(self) -> None:
        """Draw hitboxes for players and objects"""
        #Draw the hitbox for the blocks at the bottom
        for sprite in self.blocks:
            pygame.draw.rect(self.surface, (0, 255, 0), sprite.rect, 0)

        #Draw hitbox for the enemies
        for sprite in self.enemies:
            c = (sprite.get_lives())*3
            pygame.draw.rect(self.surface, (200,5*c,5*c), sprite.rect, 0)

        #Draw hitbox for the bullets
        for sprite in self.up_bullets:
            pygame.draw.rect(self.surface, (100,255,0), sprite.rect, 0)
        for sprite in self.down_bullets:
            pygame.draw.rect(self.surface, (25,0,255), sprite.rect, 0)

        #Draw the hitbox for the player
        pygame.draw.rect(self.surface, (55,255,10*self.player.get_lives()), self.player.rect, 0)

        #If mothership exists
        if self.mothership:
            
            #Draw the hitbox for the mothership
            pygame.draw.rect(self.surface, (5, 50, 5), self.mothership.rect, 0)

        #Draw for powerups
        for p_up in self.powerups:
            pygame.draw.rect(self.surface, (255,255,10*p_up.get_power_type()), p_up.rect, 0)

    def update_powerups(self) -> None:
        """Update and draw the powerups"""
        #Update powerups
        self.powerups.update()

        #Draw the powerups
        self.powerups.draw(self.screen)

    def update(self) -> None:
        """Update the sprites
            Arguments: 
                No arguments
            Returns:
                No returns
        """
        #Reset the surface
        self.reset_surface()

        #Update the player position
        self.player.update()

        #Update the enemy group
        self.enemies.update()

        #Attempts to spawn the mothership
        self.randomly_spawn_mothership()

        #If mothership exists
        if self.mothership:

            #Update the mothership
            self.mothership.update()

        #Update the explosions group
        self.explosions.update()

        #Spawn bullets for enemies
        self.spawn_enemy_bullets()

        #Update the position of all bullets
        self.up_bullets.update()
        self.down_bullets.update()

        #Update powerups
        self.update_powerups()

        #Draw the sprites
        self.draw_sprites()

        #Call superclass update
        super().update()

    def draw_sprites(self):
        """Draw the sprites"""
        #Draw bullet
        self.up_bullets.draw(self.surface)
        self.down_bullets.draw(self.surface)

        #Print debug message
        if self.debug:
            print(f"Number of player bullets: {len(self.up_bullets)}")

        #Draw the enemy
        self.enemies.draw(self.surface)

        #Print debug message
        if self.debug:
            print(f"Number of enemies: {len(self.enemies)}")

        #Draw the explosions
        self.explosions.draw(self.surface)

        #Draw player object
        self.player.draw(self.surface)

        #Draw the block
        self.blocks.draw(self.screen)

        #If the mothership exists
        if self.mothership:

            #Draw the mothership
            self.mothership.draw(self.surface)

        #Uncomment this to draw the hitbox instead
        # self.draw_hitboxes()

    def get_score(self) -> int:
        """Gets the score of the player in the current state
            Arguments:
                No arguments
            Returns:
                Return an integer as a score (int)
        """
        return self.score

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
        lst = list(self.enemies)
        return lst[int(self.generate_random_no()* (len(lst)-1))]

    def check_powerup_collision(self):
        """Check the collisions of the powerups"""
        #If there are powerups
        if len(self.powerups):

            #Check if player hit the powerups
            hit = pygame.sprite.groupcollide(self.up_bullets, self.powerups, True, True)

            #If player hit the powerups
            if len(hit):

                #For each list of powerups hit
                for l in hit.values():

                    #For each power up in powerup list
                    for p in l:

                        #Mutate player and current screen
                        p.get_ability()(self,self.player)

    def check_block_collision(self):
        """Check collisions of the blocks"""
        #If block exists
        if len(self.blocks):

            #Check if the player or the enemies shot the blocks
            pygame.sprite.groupcollide(self.up_bullets, self.blocks, True, True)
            pygame.sprite.groupcollide(self.blocks, self.down_bullets, True, True)

    def check_collisions(self) -> int:
        """Check the objects which collided
            Arguments:
                No arguments
            Returns:
                No returns
        """
        #Check block collisions
        self.check_block_collision()

        #Check collisions of powerups
        self.check_powerup_collision()

        #Check if player has collided with bullets
        bullet_collide = pygame.sprite.spritecollide(self.player, self.down_bullets, True)
        
        #If the set is not empty reduce player life
        if len(bullet_collide) > 0:

            #If it is in debug mode, print the event
            if self.debug:
                print("Player hit")

            #Destroy 1 of the player's life
            self.player.destroy()
            
            #Add explosion to the player's position
            self.spawn_explosion(self.player.get_x(), self.player.get_y())

        #Remove bullets that collide with one another
        pygame.sprite.groupcollide(self.up_bullets, self.down_bullets, True, True)

        #Get list of ships destroyed
        ships = list(pygame.sprite.groupcollide(self.up_bullets, self.enemies, True, False).values())

        #Print debug message
        if self.debug:
            print(ships)

        #Initialise score
        score = 0

        #If the list of collision is non-empty
        if ships:

            #Get the ship it collided with 
            ship = ships[0][0]

            #Destroy the first ship in the list (Ensures 1 bullet kill 1 ship only)
            ship.destroy()

            if self.debug:
                print(f"Ship destroyed")
        
            #Remove the ship from groupp if it has 0 lives
            if ship.is_destroyed():

                #Spawn an explosion in its place
                self.spawn_explosion(ship.get_x(), ship.get_y())

                #Remove the ship from all groups
                ship.kill()

                #If powerups are not disabled
                if self.powerup_chance > 0:

                    #Roll for chance of powerup spawning
                    if self.generate_random_no() < self.powerup_chance:

                        #Spawn the powerup
                        self.spawn_powerups(ship.get_x(), ship.get_y())

                    #If the power has not spawned during the wave
                    elif self.powerup_numbers == 0 and len(self.enemies) == 0:

                        #Spawn the powerup
                        self.spawn_powerups(ship.get_x(), ship.get_y())

                #Remove sprites that collide with bullets and return the sum of all the scores
                score = ship.get_points()

        #Check if ship has collided with bullets
        if self.mothership and len(pygame.sprite.spritecollide(self.mothership, self.up_bullets, True)) > 0:

            #Get points of mothership and add it to score
            score += self.mothership.get_points()

            #If so delete the mothership
            self.mothership = None

        #If nothing is destroyed return 0 points
        return score

    def spawn_explosion(self, x:int, y:int) -> None:
        """Spawn an explosion at specified x and y coordinate"""

        #Spawn an explosion
        self.explosions.add(Explosion(self.fps//4, x, y, self.screen_width, self.screen_height, 0, self.debug))

    def spawn_powerups(self, x:int, y:int) -> None:
        """Spawn a powerup at specified x and y coordinate"""

        #Spawn the powerup
        self.powerups.add(PowerUp(x, y, 50, 50, random.randint(0,PowerUp.get_no_powerups()-1), self.fps * 3))

        #Increase the number of powerups
        self.powerup_numbers += 1

    def spawn_enemies(self, number:int) -> None:
        """Spawn enemies into the game
            Arguments: 
                number: Number of enemies to spawn (int)
            Returns: 
                No returns
        """
        #If number <= 6
        if number <= 6:

            #Spawn them in 1 row
            self.enemies.add([EnemyShip(self.sensitivity, self.screen_width//4 + i*self.screen_width//10, self.screen_height//10, self.wave_random(), self.screen_width,  self.screen_height, Direction.DOWN, self.down_bullets, self.debug) for i in range(number)])
        #
        else:
            #Otherwise make them into rows of 6
            for j in range(number//6 if number // 6 < 5 else 5):
                self.enemies.add([EnemyShip(self.sensitivity, self.screen_width//4 + i*self.screen_width//10, self.screen_height//10 + EnemyShip.sprites[0].get_height() * j, self.wave_random(), self.screen_width,  self.screen_height, Direction.DOWN, self.down_bullets, self.debug) for i in range(6)])

    def randomly_spawn_mothership(self) -> bool:
        """Spawns a mothership randomly, returns if mothership is spawned"""

        #If the mothership does not exist and the random roll hits
        if not self.ms_cooldown and self.generate_random_no() < 1/900:
            
            #Create the mothership
            self.mothership = MotherShip(0, 50, self.screen_width, self.screen_height, 500)

            #Set the cooldown for the mothership
            self.ms_cooldown = self.fps * 3

            #Return True to signify that mothership spawned
            return True

        #If mothership is still under cooldown
        elif self.ms_cooldown:

            #Reduce cooldown by 1
            self.ms_cooldown -= 1

        #If it is not on cooldown and mothership still exists
        elif not self.ms_cooldown and self.mothership:

            #Set mothership to None
            self.mothership = None

        #return False if a mothership does not spawn
        return False

    def enemy_touched_bottom(self) -> bool:
        """Check if enemy touched the bottom of the screen"""
        return any(filter(lambda x: (x.get_y() + x.get_height()//2) > (self.screen_height - self.player.get_height() - 100), self.enemies))

    def is_over(self) -> bool:
        """Checks if the game is over"""
        return self.over
        
    def handle(self) -> State:
        """Handle the drawing of the play state
            Arguments:
                No arguments
            Returns:
                No returns
        """
        #If player is destroyed, go to gameover state
        if self.player.is_destroyed():
            #Set the game to be over
            self.over = True

            #Return the gameover state
            return State.GAMEOVER

        #Check if any of the enemies touched the bottom of the screen
        if self.enemy_touched_bottom():

            #If it is debugging mode, print out what happened
            if self.debug:
                print("Alienship hit the player")

            #Set the game to be over
            self.over = True
                
            #If so it is gameover for the player
            return State.GAMEOVER

        #Spawn if there are no enemies 
        if not len(self.enemies):

            #Increase the wave number
            self.wave += 1

            #Reset wave powerup
            self.power_up_numbers = 0

            #Spawn the aliens
            self.spawn_enemies(int(6 * self.wave))

        #Check object collisions
        self.score += self.check_collisions()

        #Draw the score
        self.write_main(Screen.font, WHITE, f"Score : {self.score}", 10, 10, Direction.LEFT)

        #Draw the live count
        self.write_main(Screen.font, WHITE, f"Lives : {self.player.get_lives()}", self.screen_width - 10, 10, Direction.RIGHT)

        #Draw the wave number
        self.write_main(Screen.font, WHITE, f"Wave : {self.wave}",self.screen_width//2, 15)

        #Check the player keypress
        self.update_keypresses()

        #Update the moving objs
        self.update()

        #Check if the player wants to pause
        if len(list(filter(lambda x: x.type == pygame.KEYDOWN and x.key == K_p, pygame.event.get()))):
            return State.PAUSE

        #Return play state
        return self.state
