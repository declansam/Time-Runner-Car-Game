add_library('minim')

import os, sys, random, time, datetime
path = os.getcwd()
player = Minim(this)

# CONSTANTS USED IN THE GAME
x_res = 500
y_res = 800
powerup_w = 30
powerup_h = 30
TEXTSIZE = 15
GAME_OVER_TEXTSIZE = 50
Gameover = False
MAINCAR_X = 250 
MAINCAR_Y = 400


# Powerups class that loads the image of powerups: clock and coin
class Powerups:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = loadImage(path + '/images/' + img)
    

    def display(self):
        image(self.img, self.x, self.y-game.y_shift, powerup_w, powerup_h) 
        

    

        
        
        
# Primary vehicle class
class Vehicle:
    def __init__(self, x, y,img, w, h):
        self.x = x
        self.y = y
        self.rx = w /2                     # It's the attribute used to check the collision later on
        self.ry = h /2                     # It's the attribute used to check the collision later on
        self.imgtype = img                 # Used to generate different colored traffic cars
        self.img = loadImage(path + "/images/" + self.imgtype)
        self.img_h = h
        self.img_w = w
        self.vx = 0
        self.vy = 0
        self.tempy = 0
        self.direction = UP
        self.collision = False        # Initially, collision is set to False; later on based on collision, its value is changed to True
        self.show = True
        self.initialtime = 0

    # Method used to check if the Usercar has crossed left and right border or not. For this game, it will stay on the rightmost or leftmost part of the road, and there will be no penalty.
    def bordercheck(self, xr, xl):
        if self.x <= xr:
            self.x = xr
        elif self.x >= xl:
            self.x = xl
    
    # Display function which will be respawn usercar at the specified position 
    def display(self):
        self.update()
        if self.show == True:
            image(self.img, self.x, self.y - game.y_shift, self.img_w, self.img_h)
        if game.gameover == True:
            self.y = 300
            self.x = 300



# Usercar that places the usercar, checks the collision and checks whether the car has crossed the final line or not (if it has, attributes will be reset accordingly)
class Usercar(Vehicle):
    def __init__(self,x, y, tf):
        
        # Attribute that passes the name of the usercar image
        self.i = "car_1.png"
        self.tf = tf
        
        # SOUNDS USED IN THE GAME
        self.clock_sound = player.loadFile(path + "/sounds/clock.mp3")
        self.coin_sound = player.loadFile(path + "/sounds/coin.mp3")
        self.crash_sound = player.loadFile(path + "/sounds/crash.mp3")
        
        # Inheritance from Vehicle Class & since it's the usercar we use key_handler dictionary to control the movements
        Vehicle.__init__(self, x, y, self.i, 45, 79)
        self.key_handler = {LEFT:False, RIGHT:False}

    
    # Collison Check from behind: if the user car's front hood crashes with another car from rear end, this method will return True    
    def collisionCheckBehind(self,other):
        if self.x + 5 < other.x + other.img_w and self.x + 5 > other.x or (self.x + self.img_w) - 5 > other.x and (self.x + self.img_w) - 5 < other.x + other.img_w:
                if self.distance(other) <= other.img_h + 6 and (other.y + other.ry) <= self.y:
                    return True 
                
    
    def collisionCheckUp(self,other):
        if self.x + 5 < other.x + other.img_w and self.x + 5 > other.x or (self.x + self.img_w) - 5 > other.x and (self.x + self.img_w) - 5 < other.x + other.img_w:
                if self.distance(other) <= other.img_h + 6 and other.y >= self.y + self.img_h:
                    return True         
    
    # Sideways collision check: if the user car crashes with other car from LEFT or RIGHT this method will return TRUE
    def collisionCheckSide(self,other):        
        if self.collisionCheckBehind(other):
            return False
        
        # if condition to check sideway collision from LEFT - here we check if the topleft end of usercar is within x-range of traffic car, and then if y-coordinates range of user car is within y-range of other car or not, if yes, it's a collision. 
        # Here 5 doesn't carry in-game meaning. It is used so that the excess transparent background of the images used do not interefere with collision check. 
        if self.x + 5 < other.x + other.img_w and self.x + 5 > other.x:
            if other.y + other.img_h  > self.y > other.y or other.y + other.img_h > self.y + self.img_h > other.y:
                self.x = other.x + other.img_w +5
                return True
            
        # Similarly from sideway collision from RIGHT   
        elif (self.x + self.img_w) - 5 > other.x and (self.x + self.img_w) - 5 < other.x + other.img_w:
             if other.y + other.img_h > self.y > other.y or other.y + other.img_h >= self.y + self.img_h > other.y:
                self.x = other.x - self.img_w - 5
                return True
        else:
            return False
    
    # Method to check if usercar has collected powerups or not, if yes, it returns True. To do this, all the four sides of the usercar is used to compare the location of powerups. 
    def powerupCollision(self, target):
        if self.x < target.x + powerup_w and self.x +self.img_w > target.x and self.y < target.y +powerup_h and self.img_h +self.y > target.y:
            return True
        
    def movement(self):
    
    # movement: initially, it is set to initial speed, and SIDEWAYS movement control is only possible when there is no collision.    
        if self.key_handler[LEFT] == True and self.collision == False:
            self.vx = -10
        elif self.key_handler[RIGHT] == True and self.collision ==  False:
            self.vx = 10
        else: 
            self.vx = 0
            
        if self.direction == UP:
            self.vy = self.tf

# checking for collision
        
        
        
        # To move the usercar through the traffic car/ truck, we used self.invulnerability which is 0  at first, but is changed gradually. Once again, it is gradually decreased so that the car goes through it. However, there will be a reduction of time.
        game.invulnerability -= 1                    
        for car in game.cars:
            
            if self.collisionCheckBehind(car):
                self.crash_sound.rewind()
                self.crash_sound.play()
                if game.invulnerability > 0:
                    pass
                else:
                      
                    game.moretime -=2
                    game.invulnerability = 10
                
                # We use for loop once again so that when the user car collides with these traffic cars/ trucks, all of them will be be shifted backwards by twice their length    
                for i in game.cars:
                        i.y += i.img_h * 2 
                
                self.vy = 15
                self.collision = True
                
                        
                    
                    
            if self.collisionCheckSide(car):
                self.collision = True
                print("Collision True")
                
            else:
                self.collision = False
               

        # Collision check for powerups
        # If there is collision with coins, score is increased by 1 and it is removed from the screen
        for coin in game.coin_powerup:
             if self.powerupCollision(coin):
                print('OK')
                game.score += 1
                self.coin_sound.rewind()
                self.coin_sound.play()
                
                game.coin_powerup.remove(coin)
                     
        # If there is a collision with clocks, time is increased by 2 seconds and it is removed from the screen
        for clock in game.clock_powerup:
            if self.powerupCollision(clock):
                print('OK')
                game.moretime += 2
                self.clock_sound.rewind()
                self.clock_sound.play()
                game.clock_powerup.remove(clock)


                    
   
    def display(self):
        self.update()
        

        if self.show:
            image(self.img, self.x, self.y - game.y_shift, self.img_w, self.img_h)
        
    # Update method that constantly updates the x and y coordinates of the userclass. Also, it checks for border collision        
    def update(self):
        self.movement()
        self.x +=  self.vx
        self.y = self.y + self.vy 
        self.bordercheck(103, 350)
        
        
        #SHIFTING so that it looks like the background is moving. Here, as soon as the usercar reaches the middle point of the screen, background starts moving.
        if self.y <= 800//2:
            game.y_shift += self.vy

        elif self.y > game.h//2:
            game.y_shift = 0
        
        
    
    # Distance checking method used inside backwards collision method
    def distance(self, other):
        return (((self.x) - (other.x))**2 + ((self.y) - (other.y))**2)**0.5
    


# TrafficCar class (inherited from Vehicle class) that randomly generates two numbers which corresponds to either blue car or yellow car
class TrafficCar(Vehicle):
    def __init__(self, x, y):
        self.cartype = random.randint(0,1)
        if self.cartype == 1:
            self.i = "car_2.png"
        elif self.cartype == 0:
            self.i = "car_3.png"
            
        Vehicle.__init__(self, x, y, self.i, 43, 79)
        self.vy =  2
        
     # update method that keeps traffic car in motion   
    def update(self):
        self.y -= self.vy

# Truck class that inherits from the vehicle class and passes the arguments to load the image.        
class Truck(Vehicle):
    def __init__(self, x, y):
            
        Vehicle.__init__(self, x, y, "truck_1.png" , 50, 120)
        self.vy =  2
        
        
    def update(self):
        self.y -= self.vy

        



# Game class where all the previous classes are instantiated    
class Game:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.maincar = Usercar(MAINCAR_X, MAINCAR_Y, -15)
        self.bg = loadImage(path + "/images/background.png")              # Background image of the road is loaded
        self.finish = loadImage(path + "/images/finish.png")              # Image of the finish line (at the end) is loaded
        self.cars = []                                                    # List to store all the trafficcars and trucks 
        self.clock_powerup = []                                           # List to store all the clock powerups 
        self.coin_powerup = []                                            # List to store all the coins shown on the screen
        self.y_shift = 0                                                  # Attribute to remove certain sectionsof the background when the usercar is moving. Initially it is set to 0. 
        self.gameover = False                                             # At first, gameover is set to False 
        self.score = 0
        self.moretime= 0 
        self.time_left = 30
        self.finishline = -3000                                           # Position of the finish line 
        self.mouse_x = 0
        self.mouse_y = 0
        self.display_type = 0
        self.time_start = time.time()                                     # Here we set time_start using time module. Later we subtract this value from time.time() to calculate increasing time
        
        
        self.invulnerability = 0
        # BACKGROUND SOUND
        self.bg_sound = player.loadFile(path + "/sounds/background.mp3")
        self.bg_sound.loop() 
        
                                                                                                  
        
        
        
        # Here, randomly trucks, cars and powerups are generated, instantiated and appended to their respective lists.
        for i in range(4):
            # self.cars.append(TrafficCar(random.randrange(105,230,0), random.randrange(300, 801, 100)))
            self.cars.append(TrafficCar(105 + 60 * i, random.randrange(300, 801, 100)))
            
        for i in range(4):
            self.cars.append(Truck(300 - 50 * i, random.randrange(-200, -740, -150)))
            
        for i in range(3):
            self.cars.append(TrafficCar((203 + 50 * i), random.randrange(-1000, -1600, -100)))
        
        for i in range(3):
            self.cars.append(Truck((120 + 60* i), random.randrange(-1700, -2200, -180)))
            
         # Powerup generation   
        for i in range(6):
            self.clock_powerup.append(Powerups(random.randrange(105, 245, 60), random.randrange(400,-2600, -200), "clock.png"))
        for i in range(20):
            self.coin_powerup.append(Powerups(random.randrange(105, 245, 50), random.randrange(400,-2600, -150), "coin.png"))
        for i in range(10):
            self.coin_powerup.append(Powerups(random.randrange(200, 310, 50), random.randrange(-1500, -2800, -80), "coin.png"))
         
         
      
    # Reset method that changes all the values to a specific value when this method is called

    def newReset(self, speed, totaltime):
        self.w = 500
        self.h = 800
        self.maincar = Usercar(MAINCAR_X, MAINCAR_Y, speed)
        self.cars = [] 
        self.clock_powerup = []
        self.coin_powerup = []
        self.y_shift = 0
        self.gameover = False
        self.score = 0
        self.moretime= 0
        self.time_left = totaltime
        self.finishline = -3000
        self.mouse_x = 0
        self.mouse_y = 0
        self.display_type = 1
        self.time_start = time.time()
        

        for i in range(4):
            # self.cars.append(TrafficCar(random.randrange(105,230,0), random.randrange(300, 801, 100)))
            self.cars.append(TrafficCar(105 + 60 * i, random.randrange(300, 801, 100)))
            
        for i in range(4):
            self.cars.append(Truck(300 - 50 * i, random.randrange(-200, -740, -150)))
            
        for i in range(3):
            self.cars.append(TrafficCar((203 + 50 * i), random.randrange(-1000, -1600, -100)))
        
        for i in range(3):
            self.cars.append(Truck((120 + 60* i), random.randrange(-1700, -2200, -180)))
            
            
            
        for i in range(6):
            self.clock_powerup.append(Powerups(random.randrange(105, 245, 60), random.randrange(400,-2600, -200), "clock.png"))
        for i in range(20):
            self.coin_powerup.append(Powerups(random.randrange(105, 245, 50), random.randrange(400,-2600, -150), "coin.png"))
        for i in range(10):
            self.coin_powerup.append(Powerups(random.randrange(200, 310, 50), random.randrange(-1500, -2800, -80), "coin.png"))
   
    
    
    # Display method to display all the game features
    def display(self):
        
        # SHIFTING display. Here modulus operator is used to calculate the right section to be removed, and the left section that should compensate the former removal  
        h_top = self.y_shift % self.h
        h_bottom = self.h - h_top
            
        image(self.bg, 0, 0, self.w, h_bottom, 0, h_top, self.w, self.h)      
        image(self.bg, 0, h_bottom, self.w, h_top, 0, 0, self.w, h_top)
        # print(self.maincar.x, self.maincar.y)
        image(self.finish, 106, self.finishline-self.y_shift , 288, 100 )                    # Similarly, the position of the finish line is adjusted using y_shift attribute
        
        # Displaying score on the screen
        self.display_score()
        
        # Displaying usercar and all the traffic cars/ trucks
        for car in self.cars:
            car.display()
        self.maincar.display()
        
        
        # Displaying coins and clocks on the screen
        for clock in self.clock_powerup:
            clock.display()
        for coin in self.coin_powerup:
            coin.display()
        
        # If the user reaches the finish line, display type 3, ie, a display with featuers like 'play again, next level, final score' is displayed
        if self.maincar.y <= self.finishline+100:
            self.display_type = 3
        
    
        
     # Display method to show score (it was called above)   
    def display_score(self):
        textSize(TEXTSIZE)
        fill(205)
        text("Score: " + str(self.score), x_res - 95, 25)
        self.display_time()
     
    # Display method to show timer (it was called above)   
    def display_time(self):
        textSize(TEXTSIZE)
        fill(205)
        
        
        # Here, we subtract everytime from time_left attribute which is the required time given to each level
        self.countdown = (self.time_left - int((time.time()- self.time_start)*10)/10) + self.moretime
        if self.countdown>0:
            text("Time: " + str(self.countdown), x_res - 495, 25)
        else:
            text("Time: " + str(0), x_res - 495, 25)
            self.display_type = 2

    # Method that uses the cursor location information from Processing's cursor tracking feature
    def mouseValue(self, x,y):
        self.mouse_x = x
        self.mouse_y = y
        print(self.mouse_x, self.mouse_y)
       
            
    # Display method that displays 'play game' screen at the very beginning of the game
    def start_display(self):
        image(self.bg, 0, 0, x_res, y_res,)
        fill(230,230,250)
        noStroke()
        rect(104, 200, 290, 290, 28)
        fill(75,0,130)
        noStroke()
        rect(175, 300, 150, 60, 28)
        textSize(40)
        fill(205)
        text("PLAY ", 204, 345)
        
        
        # The use must click on a particular area to start the game. These if-conditions determine the position of the cursor and checks if it's clicked or not.
        if 175 <= self.mouse_x <= 325 and 300<= self.mouse_y <= 360:
            print("sss")
            self.display_type = 1
            self.time_start= time.time()
            self.mouseValue(0,0)
    
        
        
   
   
   
   # Gameover display shown at the end when the usercar runs out of time. 
    def display_gameover(self):
        
        image(self.bg, 0, 0, x_res, y_res,)
        fill(230,230,250)
        noStroke()
        rect(104, 200, 290, 290, 28)
        fill(75,0,130)
        noStroke()
        rect(175, 220, 150, 60, 28)
        rect(175, 300, 150, 60, 28)
        rect(175, 380, 150, 60, 28)
        textSize(24)
        fill(205)
        text("GAMEOVER", 183, 340)
        text("PLAY AGAIN", 181, 340-80)
        text("Score : " + str(self.score), 194, 340+80)
        
        
        
        # Once again, if conditions are used to check where mouse has been clicked, and if it's the correct position, reset methods are called, and the game starts again
        if 175 <= self.mouse_x <= 325 and 220<= self.mouse_y <= 280:
            self.display_type = 1
            self.time_start= time.time()
            self.mouseValue(0,0)
            self.newReset(-15, 30)

    def display_Levelup(self):
        
        image(self.bg, 0, 0, x_res, y_res,)
        fill(230,230,250)
        noStroke()
        rect(104, 200, 290, 290, 28)
        fill(75,0,130)
        noStroke()
        rect(175, 220, 150, 60, 28)
        rect(175, 300, 150, 60, 28)
        rect(175, 380, 150, 60, 28)
        textSize(24)
        fill(205)
        text("YOU WON!", 183, 340)
        text("     PLAY  ", 181, 340-80)
        text("Score : " + str(self.score), 194, 340+80)
        if 175 <= self.mouse_x <= 325 and 220<= self.mouse_y <= 280:
            self.display_type = 1
            self.time_start= time.time()
            self.mouseValue(0,0)
            LEVEL = 2
            self.newReset(-25, 17)
        
        



    



        
    

game = Game(500,800)
def setup():
    size(x_res, y_res)
    
def draw():
    if frameCount % 5 == 0:
        if game.display_type == 0:
            game.start_display()
        elif game.display_type == 1:
            game.display()
        elif game.display_type == 2:
            game.display_gameover()
        elif game.display_type == 3:
            game.display_Levelup()        
            
# Processing function to check LEFT, RIGHT, UP arrows for the movement of the car
def keyPressed():
    if keyCode == LEFT:
        game.maincar.key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.maincar.key_handler[RIGHT] = True
    elif keyCode == UP:
        start = time.time()
        game.maincar.key_handler[UP] = True

# Processing function to check the key release of keyboard 
def keyReleased():
    if keyCode == LEFT:
        game.maincar.key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.maincar.key_handler[RIGHT] = False

# Mouse click verifying function of processing         
def mouseClicked():
    game.mouseValue(mouseX, mouseY)
    
    
        
        
