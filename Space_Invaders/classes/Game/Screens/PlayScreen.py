import pygame
import random
from pygame.locals import *
from . import Screen
from .. import *

class PlayScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, max_fps:int, difficulty: Difficulty, wave:int = 1, player_lives:int = 3, debug:bool = False):
        """The Play screen
            Arguments:
                screen_width: Width of the game in pixels (int)
                screen_height: Height of the game in pixels (int)
                screen: Surface where the play screen is blited to (pygame.Surface)
                sensitivity: Sensitivity of the player controls (int)
                max_fps: fps at which the game is run at (int)
                wave: The wave which the game starts at (int): default = 1
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

        #Create the groups
        #Bullets shot by player
        self.up_bullets = pygame.sprite.Group()

        #Bullet from Mobs
        self.down_bullets = pygame.sprite.Group()

        #Enemyships
        self.enemies = EnemyShips(self.state)

        #Explosions
        self.explosions = pygame.sprite.Group()

        #Create the player
        self.player = Player(sensitivity, screen_width, screen_height, screen_width//2, screen_height - 50, 3, max_fps, self.up_bullets, Direction.UP, debug)

        #Reset the variables
        self.reset()

    def get_hitboxes(self) -> list:
        """Get a list of hitboxes of mobs"""
        return [(self.player.get_coord()), tuple(x.get_coord() for x in self.up_bullets), tuple(x.get_coord() for x in self.enemies), tuple(x.get_coord() for x in self.down_bullets)]

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
            enemy = random.sample(set(self.enemies),1)

            #Get the first enemy of the set
            enemy = enemy[0]

            #Make the enemy shoot
            enemy.shoot()

    def draw_hitboxes(self):
        """Draw hitboxes for players and objects"""

        #Draw hitbox for the enemies
        for sprite in self.enemies:
            pygame.draw.rect(self.surface, (255,0,0), sprite.rect, 0)

        #Draw hitbox for the bullets
        for sprite in self.up_bullets:
            pygame.draw.rect(self.surface, (255,0,0), sprite.rect, 0)
        for sprite in self.down_bullets:
            pygame.draw.rect(self.surface, (255,0,0), sprite.rect, 0)

        #Draw the hitbox for the player
        pygame.draw.rect(self.surface, (255,0,0), self.player.rect, 0)

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

        #Update the explosions group
        self.explosions.update()

        #Spawn bullets for enemies
        self.spawn_enemy_bullets()

        #Update the position of all bullets
        self.up_bullets.update()
        self.down_bullets.update()
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
        self.explosions.draw(self.screen)

        #Draw player object
        self.player.draw(self.surface)

        #Call superclass update
        super().update()

    def get_score(self) -> int:
        """Gets the score of the player in the current state
            Arguments:
                No arguments
            Returns:
                Return an integer as a score (int)
        """
        return self.score

    def reset(self) -> None:
        """Reset the play screen and variables
            Arguments:
                No arguments
            Returns: 
                No returns
        """
        #Zero the score and the wave
        self.score = 0
        self.wave = 0

        #Empty the sprite groups
        self.up_bullets.empty()
        self.down_bullets.empty()
        self.enemies.empty()
        self.explosions.empty()

        #Reset the player
        self.player.reset()

    def check_collisions(self) -> int:
        """Check the objects which collided
            Arguments:
                No arguments
            Returns:
                No returns
        """
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
            self.explosions.add(Explosion(self.fps//2, self.player.get_x(), self.player.get_y(), self.screen_width, self.screen_height))

        #Remove bullets that collide with one another
        pygame.sprite.groupcollide(self.up_bullets, self.down_bullets, True, True)

        #Get list ships destroyed
        ships = list(pygame.sprite.groupcollide(self.up_bullets, self.enemies, True, False).values())

        #Print debug message
        if self.debug:
            print(ships)

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
                self.explosions.add(Explosion(self.fps//4, ship.get_x(), ship.get_y(), self.screen_width, self.screen_height, 0, self.debug))

                #Remove the ship from all groups
                ship.kill()

                #Remove sprites that collide with bullets and return the sum of all the scores
                return ship.get_points()

        #If nothing is destroyed return 0 points
        return 0


    def spawn_enemies(self, number:int) -> None:
        """Spawn enemies into the game
            Arguments: 
                number: Number of enemies to spawn (int)
            Returns: 
                No returns
        """
        #If number < 6
        if number <= 6:

            #Spawn them in 1 row
            self.enemies.add([EnemyShip(self.sensitivity, self.screen_width//4 + i*self.screen_width//10, self.screen_height//10, random.randint(1,self.difficulty.get_multiplier(self.wave)), self.screen_width,  self.screen_height, Direction.DOWN, self.down_bullets, self.debug) for i in range(number)])
        else:
            #Otherwise make them into rows of 6
            for j in range(number//6 if number // 6 < 5 else 5):
                self.enemies.add([EnemyShip(self.sensitivity, self.screen_width//4 + i*self.screen_width//10, self.screen_height//10 + EnemyShip.sprites[0].get_height() * j, random.randint(1,self.difficulty.get_multiplier(self.wave)), self.screen_width,  self.screen_height, Direction.DOWN, self.down_bullets, self.debug) for i in range(6)])

    def enemy_touched_bottom(self) -> bool:
        """Check if any enemies have touched the bottom of the screen"""
        return len(tuple(filter(lambda x: x.get_y() + x.get_height()//2 > self.screen_height - self.player.get_height(), self.enemies ))) > 0
        
    def handle(self) -> State:
        """Handle the drawing of the play state
            Arguments:
                No arguments
            Returns:
                No returns
        """
        #If player is destroyed, go to gameover state
        if self.player.is_destroyed():
            return State.GAMEOVER

        #Check if any of the enemies touched the bottom of the screen
        if self.enemy_touched_bottom():

            #If it is debugging mode, print out what happened
            if self.debug:
                print("Alienship hit the player")
                
            #If so it is gameover for the player
            return State.GAMEOVER

        #Spawn if there are no enemies 
        if not len(self.enemies):

            #Increase the wave number
            self.wave += 1

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
