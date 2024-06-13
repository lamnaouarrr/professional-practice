import pygame #importing the pygame library
import os #importing the os library for file path operations
import random #importing the random library
pygame.font.init() #initializing pygame font
pygame.mixer.init() #initializing the mixer for sounds

WIDTH, HEIGHT = 1200, 800 #setting the width and height of the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #creating the game window with specified width and height
pygame.display.set_caption("Hazimo Raad by LAMNAOUAR AYOUB") #setting the caption for the window

#set the window icon
assets_path = os.path.join(os.path.dirname(__file__), 'assets')
ICON = pygame.image.load(os.path.join(assets_path, "gameIcon.png"))
pygame.display.set_icon(ICON) #setting the window icon

#load and resize images
RED_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "enemy_ship_black.png")), (50, 50))
GREEN_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "enemy_ship_green.png")), (50, 50))
BLUE_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "enemy_ship_blue_small.png")), (50, 50))

#player ship
YELLOW_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "ship.png")), (50, 50))

#lasers
RED_LASER = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "enemy_laser_red.png")), (10, 40))
GREEN_LASER = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "enemy_laser_green.png")), (10, 40))
BLUE_LASER = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "enemy_laser_blue.png")), (10, 40))
YELLOW_LASER = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "laser_red.png")), (10, 40))
MAX_SPEED_LASER = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "max_laser_blue.png")), (10, 40))

#background
BG = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "background-black.png")), (WIDTH, HEIGHT))
dark_surf = pygame.Surface((WIDTH, HEIGHT))
dark_surf.set_alpha(150) #set alpha for dark overlay
dark_surf.fill((0, 0, 0)) #fill surface with black

#reward gift box images
GIFT_BOX_HEALTH = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "gift_box_green.png")), (30, 30))
GIFT_BOX_COOLDOWN = pygame.transform.scale(pygame.image.load(os.path.join(assets_path, "gift_box_yellow.png")), (30, 30))

#digital font
FONT_PATH = os.path.join(assets_path, "digital-7.ttf")
FONT_SIZE = 30
main_font = pygame.font.Font(FONT_PATH, FONT_SIZE) #using the digital font
lost_font = pygame.font.Font(FONT_PATH, 60) #using the digital font for lost text
font_color = (240, 240, 240) #light gray color for text

#Load sounds
sfx_laser = pygame.mixer.Sound(os.path.join(assets_path, "sfx_laser.ogg"))
sfx_healUp = pygame.mixer.Sound(os.path.join(assets_path, "sfx_healUp.ogg"))
sfx_healDown = pygame.mixer.Sound(os.path.join(assets_path, "sfx_healDown.ogg"))
sfx_shootingSpeedUp = pygame.mixer.Sound(os.path.join(assets_path, "sfx_shootingSpeedUp.ogg"))
sfx_shootingSpeedDown = pygame.mixer.Sound(os.path.join(assets_path, "sfx_shootingSpeedDown.ogg"))
sfx_lose = pygame.mixer.Sound(os.path.join(assets_path, "sfx_lose.ogg"))

#Load background music
pygame.mixer.music.load(os.path.join(assets_path, "هزيم الرعد  طارق العربي طرقان.mp3"))
pygame.mixer.music.set_volume(0.5) #Set volume for background music

#Load button icons
speaker_none = pygame.image.load(os.path.join(assets_path, "speaker-none-bold.png"))
speaker_high = pygame.image.load(os.path.join(assets_path, "speaker-high-bold.png"))
waveform = pygame.image.load(os.path.join(assets_path, "waveform-bold.png"))
waveform_slash = pygame.image.load(os.path.join(assets_path, "waveform-slash-bold.png"))

class Laser:#defining the laser class
    def __init__(self, x, y, img):#initialization method
        self.x = x#setting the x coordinate
        self.y = y#setting the y coordinate
        self.img = img#setting the image for the laser
        self.mask = pygame.mask.from_surface(self.img)#creating a mask for collision detection

    def draw(self, window):#method to draw the laser
        window.blit(self.img, (self.x, self.y))#drawing the laser image on the window

    def move(self, vel):#method to move the laser
        self.y += vel#updating the y coordinate based on velocity

    def off_screen(self, height):#method to check if the laser is off screen
        return not(self.y <= height and self.y >= 0)#returning true if the laser is off screen

    def collision(self, obj):#method to check collision with another object
        return collide(self, obj)#returning the result of the collision check

class Ship:#defining the ship class
    COOLDOWN = 30#cooldown period for shooting

    def __init__(self, x, y, health=100):#initialization method
        self.x = x#setting the x coordinate
        self.y = y#setting the y coordinate
        self.health = health#setting the health
        self.ship_img = None#initializing the ship image
        self.laser_img = None#initializing the laser image
        self.lasers = []#list to store lasers
        self.cool_down_counter = 0#cooldown counter

    def draw(self, window):#method to draw the ship
        window.blit(self.ship_img, (self.x, self.y))#drawing the ship image on the window
        for laser in self.lasers:#drawing each laser
            laser.draw(window)#calling the draw method of laser

    def move_lasers(self, vel, objs, gift_boxes):#method to move lasers
        self.cooldown()#calling the cooldown method
        for laser in self.lasers[:]:#moving each laser
            laser.move(vel)#calling the move method of laser
            if laser.off_screen(HEIGHT):#removing the laser if off screen
                self.lasers.remove(laser)#removing the laser from the list
            else:#checking for collision with enemies
                for obj in objs[:]:#iterating over enemies
                    if laser.collision(obj):#checking for collision
                        if isinstance(obj, RewardEnemy):#checking if the enemy is a reward enemy
                            gift_box = GiftBox(obj.x, obj.y, obj.reward_type)#creating a gift box at the enemy's position
                            gift_boxes.append(gift_box)#adding the gift box to the list
                        objs.remove(obj)#removing the enemy from the list
                        if laser in self.lasers:#removing the laser from the list if it still exists
                            self.lasers.remove(laser)#removing the laser from the list

    def cooldown(self):#method to handle cooldown
        if self.cool_down_counter >= self.COOLDOWN:#resetting the cooldown counter if it exceeds the cooldown period
            self.cool_down_counter = 0#resetting the cooldown counter
        elif self.cool_down_counter > 0:#incrementing the cooldown counter
            self.cool_down_counter += 1#incrementing the cooldown counter

    def shoot(self):#method to shoot a laser
        if self.cool_down_counter == 0:#checking if the cooldown counter is zero
            laser_img = MAX_SPEED_LASER if self.firing_speed == 6 else self.laser_img#using blue laser image if at max speed
            laser = Laser(self.x + self.get_width()//2 - laser_img.get_width()//2, self.y, laser_img)#creating a new laser in the middle of the ship
            self.lasers.append(laser)#adding the laser to the list
            self.cool_down_counter = 1#resetting the cooldown counter
            if sound_enabled:
                sfx_laser.play()#playing the laser sound

    def get_width(self):#method to get the width of the ship
        return self.ship_img.get_width()#returning the width of the ship

    def get_height(self):#method to get the height of the ship
        return self.ship_img.get_height()#returning the height of the ship

class Player(Ship):#defining the player class inheriting from ship
    def __init__(self, x, y, health=100):#initialization method
        super().__init__(x, y, health)#calling the initialization method of the parent class
        self.ship_img = YELLOW_SPACE_SHIP#setting the ship image
        self.laser_img = YELLOW_LASER#setting the laser image
        self.mask = pygame.mask.from_surface(self.ship_img)#creating a mask for collision detection
        self.max_health = health#setting the maximum health
        self.firing_speed = 1#setting the initial firing speed

    def move_lasers(self, vel, objs, gift_boxes):#method to move lasers
        self.cooldown()#calling the cooldown method
        for laser in self.lasers[:]:#moving each laser
            laser.move(vel)#calling the move method of laser
            if laser.off_screen(HEIGHT):#removing the laser if off screen
                self.lasers.remove(laser)#removing the laser from the list
            else:#checking for collision with enemies
                for obj in objs[:]:#iterating over enemies
                    if laser.collision(obj):#checking for collision
                        if isinstance(obj, RewardEnemy):#checking if the enemy is a reward enemy
                            gift_box = GiftBox(obj.x, obj.y, obj.reward_type)#creating a gift box at the enemy's position
                            gift_boxes.append(gift_box)#adding the gift box to the list
                        objs.remove(obj)#removing the enemy from the list
                        if laser in self.lasers:#removing the laser from the list if it still exists
                            self.lasers.remove(laser)#removing the laser from the list

    def draw(self, window):#method to draw the player
        super().draw(window)#calling the draw method of the parent class
        self.healthbar(window)#calling the healthbar method

    def healthbar(self, window):#method to draw the health bar
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))#drawing the red background of the health bar
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))#drawing the green foreground of the health bar

    def take_damage(self, amount):#method to handle damage
        self.health -= amount#reducing the health
        if self.health > 0:#only decrease firing speed if the player is still alive
            self.firing_speed = max(1, self.firing_speed - 1)#reducing the firing speed but ensuring it doesn't go below 1
            self.COOLDOWN = 30 // self.firing_speed#adjusting cooldown based on firing speed
            if sound_enabled:
                sfx_healDown.play()#playing the damage sound

class Enemy(Ship):#defining the enemy class inheriting from ship
    COLOR_MAP = {#dictionary to map colors to ship and laser images
                "red": (RED_SPACE_SHIP, RED_LASER),#mapping red color
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),#mapping green color
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)#mapping blue color
                }

    def __init__(self, x, y, color, health=100):#initialization method
        super().__init__(x, y, health)#calling the initialization method of the parent class
        self.ship_img, self.laser_img = self.COLOR_MAP[color]#setting the ship and laser images based on color
        self.mask = pygame.mask.from_surface(self.ship_img)#creating a mask for collision detection

    def move(self, vel):#method to move the enemy
        self.y += vel#updating the y coordinate based on velocity

    def shoot(self):#method to shoot a laser
        if self.cool_down_counter == 0:#checking if the cooldown counter is zero
            laser = Laser(self.x + self.get_width()//2 - self.laser_img.get_width()//2, self.y, self.laser_img)#creating a new laser in the middle of the ship
            self.lasers.append(laser)#adding the laser to the list
            self.cool_down_counter = 1#resetting the cooldown counter

    def move_lasers(self, vel, obj):#method to move lasers
        self.cooldown()#calling the cooldown method
        for laser in self.lasers[:]:#moving each laser
            laser.move(vel)#calling the move method of laser
            if laser.off_screen(HEIGHT):#removing the laser if off screen
                self.lasers.remove(laser)#removing the laser from the list
            elif laser.collision(obj):#checking for collision
                obj.take_damage(10)#reducing the health of the object and updating its firing speed
                self.lasers.remove(laser)#removing the laser from the list

class RewardEnemy(Enemy):#defining the reward enemy class inheriting from enemy
    def __init__(self, x, y, color, health=100):#initialization method
        super().__init__(x, y, color, health)#calling the initialization method of the parent class
        self.reward_type = random.choice(['health', 'cooldown'])#randomly choosing the reward type

    def apply_reward(self, player):#method to apply the reward to the player
        if self.reward_type == 'health':#if the reward is health
            player.health = min(player.max_health, player.health + 20)#increasing the player's health
            if sound_enabled:
                sfx_healUp.play()#playing the health up sound
        elif self.reward_type == 'cooldown':#if the reward is cooldown
            player.firing_speed = min(6, player.firing_speed + 1)#increasing the player's firing speed but capping it at 6
            player.COOLDOWN = 30 // player.firing_speed#adjusting cooldown based on firing speed
            if sound_enabled:
                sfx_shootingSpeedUp.play()#playing the shooting speed up sound

class GiftBox:#defining the gift box class
    def __init__(self, x, y, reward_type):#initialization method
        self.x = x#setting the x coordinate
        self.y = y#setting the y coordinate
        self.reward_type = reward_type#setting the reward type
        if reward_type == 'health':
            self.img = GIFT_BOX_HEALTH#setting the image for the health gift box
        else:
            self.img = GIFT_BOX_COOLDOWN#setting the image for the cooldown gift box
        self.mask = pygame.mask.from_surface(self.img)#creating a mask for collision detection

    def draw(self, window):#method to draw the gift box
        window.blit(self.img, (self.x, self.y))#drawing the gift box image on the window

    def move(self, vel):#method to move the gift box
        self.y += vel#updating the y coordinate based on velocity

    def off_screen(self, height):#method to check if the gift box is off screen
        return not(self.y <= height and self.y >= 0)#returning true if the gift box is off screen

    def collision(self, obj):#method to check collision with another object
        return collide(self, obj)#returning the result of the collision check

    def apply_reward(self, player):#method to apply the reward to the player
        if self.reward_type == 'health':#if the reward is health
            player.health = min(player.max_health, player.health + 20)#increasing the player's health
            if sound_enabled:
                sfx_healUp.play()#playing the health up sound
        elif self.reward_type == 'cooldown':#if the reward is cooldown
            player.firing_speed = min(6, player.firing_speed + 1)#increasing the player's firing speed but capping it at 6
            player.COOLDOWN = 30 // player.firing_speed#adjusting cooldown based on firing speed
            if sound_enabled:
                sfx_shootingSpeedUp.play()#playing the shooting speed up sound

def collide(obj1, obj2):#function to check collision between two objects
    offset_x = obj2.x - obj1.x#calculating the offset in x direction
    offset_y = obj2.y - obj1.y#calculating the offset in y direction
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None#checking if the masks overlap

def main():#main function to run the game
    run = True#variable to keep the game loop running
    FPS = 60#frames per second
    level = 0#initial level
    lives = 5#initial lives
    gift_box_vel = 2#slower velocity of gift boxes

    enemies = []#list to store enemies
    gift_boxes = []#list to store gift boxes
    wave_length = 5#initial wave length
    enemy_vel = 1#velocity of enemies

    player_vel = 5#velocity of player
    laser_vel = 5#velocity of lasers

    player = Player(300, 630)#creating a player object

    clock = pygame.time.Clock()#creating a clock object

    lost = False#variable to check if the game is lost
    lost_count = 0#counter for the lost time

    #flags for enabling/disabling sound and music
    global sound_enabled, music_enabled
    sound_enabled = True
    music_enabled = True

    #play background music
    pygame.mixer.music.play(-1)#playing background music in a loop

    def redraw_window():#function to redraw the window
        WIN.blit(BG, (0,0))#drawing the background
        WIN.blit(dark_surf, (0,0))#drawing the dark overlay
        #draw text
        lives_label = main_font.render(f"lives: {lives}", 1, font_color)#rendering the lives text
        level_label = main_font.render(f"level: {level}", 1, font_color)#rendering the level text
        firing_label = main_font.render(f"firing speed: {player.firing_speed}", 1, font_color)#rendering the firing speed text
        health_label = main_font.render(f"hp: {player.health}/{player.max_health}", 1, font_color)#rendering the health text

        WIN.blit(lives_label, (10, 10))#drawing the lives text
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))#drawing the level text
        WIN.blit(firing_label, (10, 40))#drawing the firing speed text
        WIN.blit(health_label, (10, 70))#drawing the health text

        for enemy in enemies:#drawing each enemy
            enemy.draw(WIN)#calling the draw method of enemy

        for gift_box in gift_boxes:#drawing each gift box
            gift_box.draw(WIN)#calling the draw method of gift box

        player.draw(WIN)#drawing the player

        if lost:#if the game is lost
            lost_label = lost_font.render("you lost!!", 1, font_color)#rendering the lost text
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))#drawing the lost text

        #Draw buttons for sound and music
        sound_button = speaker_high if sound_enabled else speaker_none
        music_button = waveform if music_enabled else waveform_slash
        WIN.blit(sound_button, (WIDTH - sound_button.get_width() - 50, 40))
        WIN.blit(music_button, (WIDTH - music_button.get_width() - 50, 90))

        pygame.display.update()#updating the display

    while run:#game loop
        clock.tick(FPS)#setting the fps
        redraw_window()#calling the redraw window function

        if lives <= 0 or player.health <= 0:#checking if the player is out of lives or health
            lost = True#setting the lost variable to true
            lost_count += 1#incrementing the lost count

        if lost:#if the game is lost
            pygame.mixer.music.stop()#stopping the background music
            if lost_count > FPS * 3:#if the lost screen is shown for 3 seconds
                run = False#ending the game loop
                if sound_enabled:
                    sfx_lose.play()#playing the lose sound
            else:#continuing to show the lost screen
                continue#skipping the rest of the loop

        if len(enemies) == 0:#if all enemies are destroyed
            level += 1#incrementing the level
            wave_length += 5#increasing the wave length
            for i in range(wave_length):#creating new enemies
                if i < 2:#creating reward enemies
                    enemy = RewardEnemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))#creating a reward enemy
                else:#creating normal enemies
                    enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))#creating a normal enemy
                enemies.append(enemy)#adding the enemy to the list

        for event in pygame.event.get():#handling events
            if event.type == pygame.QUIT:#if the quit event is triggered
                quit()#quitting the game
            if event.type == pygame.MOUSEBUTTONDOWN:#handling mouse button down events
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if WIDTH - 100 < mouse_x < WIDTH - 50 and 40 < mouse_y < 90:#checking if sound button is clicked
                    sound_enabled = not sound_enabled#toggling sound
                    sfx_laser.set_volume(1.0 if sound_enabled else 0.0)#setting volume
                    sfx_healUp.set_volume(1.0 if sound_enabled else 0.0)
                    sfx_healDown.set_volume(1.0 if sound_enabled else 0.0)
                    sfx_shootingSpeedUp.set_volume(1.0 if sound_enabled else 0.0)
                    sfx_shootingSpeedDown.set_volume(1.0 if sound_enabled else 0.0)
                    sfx_lose.set_volume(1.0 if sound_enabled else 0.0)
                if WIDTH - 100 < mouse_x < WIDTH - 50 and 90 < mouse_y < 140:#checking if music button is clicked
                    music_enabled = not music_enabled#toggling music
                    pygame.mixer.music.set_volume(0.5 if music_enabled else 0.0)#setting volume

        keys = pygame.key.get_pressed()#getting the keys pressed
        if keys[pygame.K_a] and player.x - player_vel > 0:#moving the player left
            player.x -= player_vel#updating the x coordinate
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:#moving the player right
            player.x += player_vel#updating the x coordinate
        if keys[pygame.K_w] and player.y - player_vel > 0:#moving the player up
            player.y -= player_vel#updating the y coordinate
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:#moving the player down
            player.y += player_vel#updating the y coordinate
        if keys[pygame.K_SPACE]:#shooting a laser
            player.shoot()#calling the shoot method

        for enemy in enemies[:]:#moving each enemy
            enemy.move(enemy_vel)#calling the move method of enemy
            enemy.move_lasers(laser_vel, player)#moving the lasers of enemy

            if random.randrange(0, 2*60) == 1:#randomly shooting a laser
                enemy.shoot()#calling the shoot method of enemy

            if collide(enemy, player):#checking collision with player
                player.take_damage(10)#reducing the health of the player and decreasing the firing speed
                enemies.remove(enemy)#removing the enemy from the list
            elif enemy.y + enemy.get_height() > HEIGHT:#if the enemy goes off screen
                lives -= 1#reducing the lives of the player
                enemies.remove(enemy)#removing the enemy from the list

        for gift_box in gift_boxes[:]:#moving each gift box
            gift_box.move(gift_box_vel)#calling the move method of gift box
            if gift_box.off_screen(HEIGHT):#removing the gift box if off screen
                gift_boxes.remove(gift_box)#removing the gift box from the list
            elif gift_box.collision(player):#checking collision with player
                gift_box.apply_reward(player)#applying the reward to the player
                gift_boxes.remove(gift_box)#removing the gift box from the list

        player.move_lasers(-laser_vel, enemies, gift_boxes)#moving the lasers of player

def main_menu():#function for the main menu
    title_font = pygame.font.Font(FONT_PATH, 70)#font for the title
    run = True#variable to keep the menu loop running
    while run:#menu loop
        WIN.blit(BG, (0,0))#drawing the background
        WIN.blit(dark_surf, (0,0))#drawing the dark overlay
        title_label = title_font.render("press the mouse to begin...", 1, font_color)#rendering the title text
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))#drawing the title text
        pygame.display.update()#updating the display
        for event in pygame.event.get():#handling events
            if event.type == pygame.QUIT:#if the quit event is triggered
                run = False#ending the menu loop
            if event.type == pygame.MOUSEBUTTONDOWN:#if the mouse button is pressed
                main()#calling the main function
    pygame.quit()#quitting the game

main_menu()#calling the main menu function
