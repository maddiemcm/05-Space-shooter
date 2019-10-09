import os, sys, logging, arcade, random, time

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
MARGIN = 50
SCREEN_TITLE = "Aliens and Donuts"
MOVEMENT_SPEED = 6
FRICTION = 0.9

STARTING_LOCATION = (600,75)
BULLET_DAMAGE = 50
ENEMY_HP = 150
BOSS_HP = 1000
PLAYER_HP = 1400
KILL_SCORE = 2000
HIT_SCORE = 100

PLAYER_SCALE = 1
DONUT_SCALE = 1.25
BOSS_SCALE = .75
BULLET_SCALE = 0.4
SPRINKLE_SCALE = .15
# goal of game is to move an alien around via keyboard, shooting with spacebar at sky donuts

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("images/bullet.png", BULLET_SCALE)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage
        #makes damage an attribute of the bullet

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy

class Enemy_Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("images/sprinkle.png", SPRINKLE_SCALE)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage
        #makes damage an attribute of the bullet

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("images/alien.png", PLAYER_SCALE)
        #super is whatever arcade.sprite needs to initialize itself, do it
        (self.center_x, self.center_y) = STARTING_LOCATION
        self.hp = PLAYER_HP
        self.moving_left = False
        self.moving_right = False

class Donut(arcade.Sprite):
    def __init__(self, position, velocity):
        ''' 
        initializes a penguin enemy
        Parameter: position: (x,y) tuple
        '''
        self.donuts = ["images/donut1.png", "images/donut2.png","images/donut3.png", "images/donut4.png", "images/donut5.png"]
        donut = random.choice(self.donuts)
        super().__init__(donut, DONUT_SCALE)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.can_shoot = False

    def update(self):
        self.center_x = self.center_x + self.dx
        self.center_y = self.center_y + self.dy
        if self.center_x <= 0:
            self.dx = abs(self.dx)            
        if self.center_x >= SCREEN_WIDTH:
            self.dx = abs(self.dx) * -1
        if self.center_y <= 750:
            self.dy = abs(self.dy)
        if self.center_y >= SCREEN_HEIGHT:
            self.dy = abs(self.dy) * -1

class Second_level_donut(arcade.Sprite):
    def __init__(self, position, velocity):
        self.donuts = ["images/donut1.png", "images/donut2.png","images/donut3.png", "images/donut4.png", "images/donut5.png"]
        donut = random.choice(self.donuts)
        super().__init__(donut, DONUT_SCALE)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.can_shoot = False

    def update(self):
        self.center_x = self.center_x + self.dx
        self.center_y = self.center_y + self.dy
        if self.center_x <= 0:
            self.dx = abs(self.dx)            
        if self.center_x >= SCREEN_WIDTH:
            self.dx = abs(self.dx) * -1
        if self.center_y <= 750:
            self.dy = abs(self.dy)
        if self.center_y >= SCREEN_HEIGHT:
            self.dy = abs(self.dy) * -1

class Third_level_donut(arcade.Sprite):
    def __init__(self, position, velocity):
        self.donuts = ["images/boss.png"]
        donut = self.donuts[0]
        super().__init__(donut, BOSS_SCALE)
        self.hp = BOSS_HP
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.can_shoot = True

    def update(self):
        self.center_x = self.center_x + self.dx
        self.center_y = self.center_y + self.dy
        if self.center_x <= 0:
            self.dx = abs(self.dx)            
        if self.center_x >= SCREEN_WIDTH:
            self.dx = abs(self.dx) * -1
        if self.center_y <= 750:
            self.dy = abs(self.dy)
        if self.center_y >= SCREEN_HEIGHT:
            self.dy = abs(self.dy) * -1


class Window(arcade.Window):

    def __init__(self, width, height, title):

        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        

        self.set_mouse_visible(False)

        self.background = None 

        self.total_time = 0.0

    def intro(self):

        arcade.draw_text(f"Welcome to Aliens vs. Donuts!", 150, 750, arcade.color.WHITE, 60)
        arcade.draw_text(f"Hit all of the donuts until they disappear", 300, 550, arcade.color.WHITE, 30)
        arcade.draw_text(f"LEFT and RIGHT arrow keys to move. SPACE to shoot", 200, 440, arcade.color.WHITE, 30)
        arcade.draw_text(f"Click to START", 425, 75, arcade.color.WHITE, 40)


    def level_1(self):
        for i in range(10):
            x = 120 * (i+.75)
            y = 875
            dx = 3
            dy = 1.5
            donut = Donut((x,y), (dx,dy))
            
            self.donut_list.append(donut) 

        self.total_time = 0.0

    def level_2(self):
        for i in range(20):
            x = random.randint(MARGIN, SCREEN_WIDTH - MARGIN)
            y = 875
            velocities_x = [2,-2]
            velocities_y = [2,-2]
            dx = random.choice(velocities_x)
            dy = random.choice(velocities_y)
            donut = Second_level_donut((x,y), (dx,dy))

            self.donut_list.append(donut)

        self.total_time = 0.0

    def level_3(self):
        for i in range(1):
            x = 600
            y = 775
            dx = 2
            dy = 0
            donut = Third_level_donut((x,y), (dx,dy))

            self.donut_list.append(donut)
        
        self.total_time = 0.0

    def level_4(self):
        for i in range(1):
            x = 600 * (i+1.5) 
            y = 775
            dx = 2
            dy = 0
            donut = Third_level_donut((x,y), (dx,dy))

            self.donut_list.append(donut)
        for i in range(1):
            x = 600 * (i+1.5) 
            y = 775
            dx = -2
            dy = 0
            donut = Third_level_donut((x,y), (dx,dy))

            self.donut_list.append(donut)
        
        self.total_time = 0.0
    
    def level_5(self):
        for i in range(3):
            x = 400 * (i+1.0) 
            y = 775
            dx = 2
            dy = 0
            donut = Third_level_donut((x,y), (dx,dy))

            self.donut_list.append(donut)
        
        self.total_time = 0.0


    def winner(self):

        arcade.draw_text(f"You've won!", 420, 490, arcade.color.WHITE, 60)
        arcade.draw_text(f"Total Score: {self.score - self.time_penalty}", 460, 410, arcade.color.WHITE, 30)
        arcade.draw_text(f"Level: {self.level}", 535, 365, arcade.color.WHITE, 30)

        self.total_time = 0.0



    def end(self):
        arcade.draw_text(f"You lose :(", 440, 490, arcade.color.WHITE, 60)
        arcade.draw_text(f"Total Score: {self.score - self.time_penalty}", 460, 410, arcade.color.WHITE, 30)
        arcade.draw_text(f"Level: {self.level}", 535, 365, arcade.color.WHITE, 30)

        self.total_time = 0.0


    def setup(self):
        
        self.level = 0
        self.won = False
        self.died = False
    
        #sprite lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.donut_list = arcade.SpriteList()
        self.donut_bullet_list = arcade.SpriteList()

        #set up the player
        self.score = 0
        self.time_penalty = 0
        self.player = Player()
        self.player_list.append(self.player)

        self.background = arcade.load_texture("images/background.jpg")

        self.intro()

    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()
        
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT,self.background)

        if self.won:	             
            self.winner()		         
        elif self.died:	         
            self.end()
        elif self.level == 0:
            self.intro()
        else:
             # Draw all the sprites.
            self.donut_list.draw()
            self.player_list.draw()
            self.bullet_list.draw()
            self.donut_bullet_list.draw()
            minutes = int(self.total_time) // 60
            seconds = int(self.total_time) % 60
            output = f"Total Time Elapsed: {minutes:02d}:{seconds:02d}"
            arcade.draw_text(output, 890, 50, arcade.color.WHITE, 22)
 
        # Render the text
        arcade.draw_text(f"Score: {self.score}", 10, 75, arcade.color.WHITE, 22)

        arcade.draw_text(f"Level: {self.level}", 10, 105, arcade.color.WHITE, 22)
 
        arcade.draw_text(f"ALIENS VS. DONUTS", 940, 15, arcade.color.WHITE, 22)

        arcade.draw_text (f"Time penalty points: {self.time_penalty}", 10, 45, arcade.color.WHITE, 22)

        arcade.draw_text (f"Player Health Points: {self.player.hp}", 10, 15, arcade.color.WHITE, 22)


    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """

        if key == arcade.key.LEFT:
            self.player.moving_left = True
        elif key == arcade.key.RIGHT:
            self.player.moving_right = True
        elif key == arcade.key.SPACE:
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)


    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """

        if key == arcade.key.LEFT:
            self.player.moving_left = False
        if key == arcade.key.RIGHT:
            self.player.moving_right = False

    def on_mouse_press(self, x, y, button, modifiers):
        
        if self.level == 0:
            self.level += 1
            self.level_1()

    def update(self, delta_time):

        self.total_time += delta_time
        
        if self.total_time >= 15 and self.level == 1:
            self.time_penalty = self.time_penalty + 2
        
        if self.total_time >= 20 and self.level == 2:
            self.time_penalty = self.time_penalty + 2
        
        if self.total_time >= 15 and self.level == 3:
            self.time_penalty = self.time_penalty + 2

        if self.total_time >= 25 and self.level == 4:
            self.time_penalty = self.time_penalty + 2

        if self.total_time >= 35 and self.level == 5:
            self.time_penalty = self.time_penalty + 2
      

        if self.player.moving_left:
            self.player.center_x = self.player.center_x - MOVEMENT_SPEED
        if self.player.center_x <= 0:
                self.player.center_x = 0
        if self.player.moving_right:
            self.player.center_x = self.player.center_x + MOVEMENT_SPEED
        if self.player.center_x >= SCREEN_WIDTH:
                self.player.center_x = SCREEN_WIDTH

        self.donut_list.update()
        
        for e in self.donut_list:
            e.update()

            damage = arcade.check_for_collision_with_list(e,self.bullet_list)
            for d in damage:
                e.hp = e.hp - d.damage
                d.kill()
                if e.hp <= 0:
                    e.kill()
                    self.score = self.score + KILL_SCORE
                else:
                    self.score = self.score + HIT_SCORE

        self.bullet_list.update()
        
        
        self.donut_bullet_list.update()

        for e in self.donut_list:
            if (e.can_shoot and random.random() < .05):
                self.donut_bullet_list.append(Enemy_Bullet((e.center_x, e.center_y - 15), (0, -10), 100))

        damage = arcade.check_for_collision_with_list(self.player,self.donut_bullet_list)
        for d in damage: 
            self.player.hp = self.player.hp - d.damage
            d.kill()
            if self.player.hp <= 0:
                self.player.kill()
                self.died = True
                            

        if len(self.donut_list) == 0 and self.level == 1:
            self.level += 1
            self.level_2()
        elif len(self.donut_list) == 0 and self.level == 2:
            self.level += 1
            self.level_3()
        elif len(self.donut_list) == 0 and self.level == 3:
            self.level += 1
            self.level_4()
        elif len(self.donut_list) == 0 and self.level == 4:
            self.level += 1
            self.level_5()

        elif len(self.donut_list) == 0 and self.level == 5:
            self.won = True

        #However I lose
        if True == False:
            self.died = True

        


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
