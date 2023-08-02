#PlayableCharacters.py



import pygame,random,time,json #import the modules
from Configuration import *
from pygame import mixer
from datetime import datetime, timedelta



class Fighter(pygame.sprite.Sprite):

    def __init__(self, x, y, name, player2,online,socket=None): #takes in the parameters self,x,y,name,player2,online
        super().__init__() #calls to the superclass
        self._name = name #the characters name, this is vital as it is needed to access different files
        self._max_hp = 300 #the max health is the same among playable characters
        self.hp = self._max_hp  #the current hp for the health bar
        self.x = x #the x co-ordinate position
        self.y = y #the y co-0rdinate position
        self._2P = player2 #Boolean : if it is false, the player has the role of the left hand player regarded as player 1

        #the different damage variables later called into the functions
        self._light_dmg = random.randint(10,30)
        self._med_dmg = random.randint(30,50)
        self._high_dmg = random.randint(50,80)
        self.damage = 0 #the damage variable itself where it is then subtracted from player's hp

        self._hit_delay = datetime.now() #set to current time but later set to add 1.25 seconds to allow for delaying consecutive hit
        self._master_anim_list = [] #where the image list gets appened to so these images become the main ones on screen
        self._frame_index = 0 #the index through the aniim list
        self._action = 0 #the for loops where the images are loaded define this variable, determining the player's action
        self.ko = False #When true, allow for player controls
        self.dx = 0 #gets added to the x co-ordinate to go left or right
        self.dy = 0 #gets added to the y co-ordinate to jump or crouch
        self.grunts = [mixer.Sound(f'{self._name}/Audio/Grunt1.wav'),mixer.Sound(f'{self._name}/Audio/Grunt2.wav'),# a list of the various voice effects
                        mixer.Sound(f'{self._name}/Audio/Grunt3.wav'),mixer.Sound(f'{self._name}/Audio/Hurt1.wav'), #uses f'string to apply the name to the file directory for each character's voice
                        mixer.Sound(f'{self._name}/Audio/Hurt2.wav'),mixer.Sound(f'{self._name}/Audio/KO1.wav'),
                        mixer.Sound(f'{self._name}/Audio/SPGrunt.wav'),mixer.Sound(f'{self._name}/Audio/Victory.wav')]

        self.socket = socket #Store the socket
        self._online = online #If it is an online game
        self.crouched = False #if the player is crouched

        # The following series of for loops are used to load certain images for the animation of certain moves, self._action is a variable which has a number correlating to the order of these loops
        # For example, if i have my idle anim loop coded first, then my walking anim loop, it will be designated in that order. 0:Idle, 1:Walking

        # animation list
        # 0 Idle
        # 1 Moving
        # 2 Block
        # 3 Low Block
        # 4 Jump
        # 5 Punch1
        # 6 Punch2
        # 7 Throw
        # 8 Kick1
        # 9 Kick2
        # 10 Low Kick
        # 11 Uppercut
        # 12 Low Punch
        # 13 Taking Damage
        # 14 Taking Crouch Damage
        # 15 Special Move1
        # 16 Special Move2
        # 17 Special Move3
        # 18 Knockback
        # 19 Crouch
        # 20 Victory1
        # 21 Victory2
        # 22 Defeat

        # 0 Idle
        sub_anim_list = []
        for i in range(4):
            img = pygame.image.load(f'{self._name}/1)Idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 1 Moving
        sub_anim_list = []  # these temporary lists contain the set animation for different actions which will go into the master list
        for i in range(6):  # loops through the amount of images in the folder directory, in this case, i have 6 moving images to loop through
            img = pygame.image.load(f'{self._name}/4)Moving/{i}.png').convert_alpha()  # loads in the images in the order of i and based on self._name
            img = pygame.transform.scale(img, (
            img.get_width() * 3, img.get_height() * 3))  # increase the scale of the images by 3 times
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)  # appends to a temporary list
        self._master_anim_list.append(sub_anim_list)  # when self._action corresponds to the loop order, play that set of animations.

        # 2 Block
        sub_anim_list = []
        for i in range(2):
            img = pygame.image.load(f'{self._name}/2)Block/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 3 Low Block
        sub_anim_list = []
        for i in range(2):
            img = pygame.image.load(f'{self._name}/3)LowBlock/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 4 Jump
        sub_anim_list = []
        for i in range(3):
            img = pygame.image.load(f'{self._name}/5)Jumping/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 5 Punch 1
        sub_anim_list = []
        for i in range(0, 3):
            img = pygame.image.load(f'{self._name}/6)Punch/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 6 Punch 2
        sub_anim_list = []
        for i in range(3, 6):
            img = pygame.image.load(f'{self._name}/6)Punch/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 7 Throw
        sub_anim_list = []
        for i in range(5):
            img = pygame.image.load(f'{self._name}/9)Throw/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 8 Kick 1
        sub_anim_list = []
        for i in range(0, 5):
            img = pygame.image.load(f'{self._name}/10)Kick/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 9 Kick 2
        sub_anim_list = []
        for i in range(5, 10):
            img = pygame.image.load(f'{self._name}/10)Kick/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 10 Low Kick
        sub_anim_list = []
        for i in range(3):
            img = pygame.image.load(f'{self._name}/11)LowKick/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 11 Uppercut
        sub_anim_list = []
        for i in range(4):
            img = pygame.image.load(f'{self._name}/12)Uppercut/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 12 Low Punch
        sub_anim_list = []
        for i in range(2):
            img = pygame.image.load(f'{self._name}/7)LowPunch/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 13 Taking Damage
        sub_anim_list = []
        for i in range(0, 3):
            img = pygame.image.load(f'{self._name}/13)TakeDamage/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 14 Taking Crouch Damage
        sub_anim_list = []
        for i in range(3, 5):
            img = pygame.image.load(f'{self._name}/13)TakeDamage/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 15 Special Move 1
        sub_anim_list = []
        for i in range(5):
            img = pygame.image.load(f'{self._name}/15)SP1/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 16 Special Move 2
        sub_anim_list = []
        for i in range(3):
            img = pygame.image.load(f'{self._name}/16)SP2/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 17 Special Move 3
        sub_anim_list = []
        for i in range(2):
            img = pygame.image.load(f'{self._name}/17)SP3/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 18 Knockback
        sub_anim_list = []
        for i in range(5):
            img = pygame.image.load(f'{self._name}/14)Knockback/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 19 Crouch
        sub_anim_list = []
        for i in range(2):
            img = pygame.image.load(f'{self._name}/8)Crouch/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 20 Victory 1
        sub_anim_list = []
        for i in range(0, 4):
            img = pygame.image.load(f'{self._name}/19)Victory/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 21 Victory 2
        sub_anim_list = []
        for i in range(4, 8):
            img = pygame.image.load(f'{self._name}/19)Victory/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
                sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 22 Defeat
        sub_anim_list = []
        for i in range(5):
            img = pygame.image.load(f'{self._name}/18)Defeat/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            if self._2P == True:
                img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)

        self.image = self._master_anim_list[self._action][self._frame_index] #the current images
        self.rect = pygame.Rect(self.x, self.y, 160, 300) #the rect of the character
        self.rect.center = (x, y) # where the character is positioned
        self._counter = 0 #used for the animation loop

    def updateServer(self):
        #Tell the server each player POS, player HP
        cmd = {"Command": "MOVE", "X": self.x, "Y": self.y, "ACTION":self._action,"HP":self.hp}
        self.socket.send(json.dumps(cmd).encode())


    def update(self):
        animation_time = 5  # the time before the next , the lower the value, the faster the animation runs
        self.dx = 0  # added or subtracted value that dictates the movement
        self.dy = 0  # added or subtracted value that dictates the movement
        self.vel = 5  # velocity
        self.key = pygame.key.get_pressed()  # keyboard input allowing for holds
        self._counter += 1


        if self.ko == False: #if there isn't a knockout, the controls are active

            if not any(self.key):
                self._action = 0


            if self._2P == True and self._online != True: #offline player 2's control scheme


                if self.key[pygame.K_UP]:  # jump
                    self.jump()

                if self.key[pygame.K_LEFT]:  # move left
                    self.move("back")

                if self.key[pygame.K_DOWN]:  # crouch
                    self.crouch()
                    self.crouched = True
                    if self.rect.y >= 380 and self.crouched == True:
                        self.rect.y = 380
                else:
                    self.crouched = False

                if self.key[pygame.K_RIGHT]:  # move right
                    self.move("forward")

                elif self.key[pygame.K_KP3]:
                    self.blocking()

                elif self.key[pygame.K_KP7]:
                    self.punch()

                elif self.key[pygame.K_KP8]:
                    self.punch_combo()

                elif self.key[pygame.K_KP6]:
                    self.throw()

                elif self.key[pygame.K_KP4]:
                    self.kick()

                elif self.key[pygame.K_KP5]:
                    self.kick_combo()

                if self.crouched == True:

                    if self.key[pygame.K_KP3]:  # crouch block
                        self.l_block()

                    elif self.key[pygame.K_KP7]:
                        self.l_punch()

                    elif self.key[pygame.K_KP4]:
                        self.l_kick()

                    elif self.key[pygame.K_KP6]:
                        self.uppercut()

                elif self.key[pygame.K_8]:
                    self.sp1()

                elif self.key[pygame.K_9]:
                    self.sp2()

                elif self.key[pygame.K_0]:
                    self.sp3()


            else: #player 1's control scheme

                if self.key[pygame.K_w]:  # jump
                    self.jump()

                if self.key[pygame.K_a]:  # move left
                    self.move("back")

                if self.key[pygame.K_s]:  # crouch
                    self.crouch()
                    self.crouched = True
                    if self.rect.y >= 380 and self.crouched == True:
                        self.rect.y = 380
                else:
                    self.crouched = False

                if self.key[pygame.K_d]:  # move right
                    self.move("forward")

                elif self.key[pygame.K_b]:
                    self.blocking()

                elif self.key[pygame.K_r]:
                    self.punch()

                elif self.key[pygame.K_t]:
                    self.punch_combo()

                elif self.key[pygame.K_h]:
                    self.throw()

                elif self.key[pygame.K_f]:
                    self.kick()

                elif self.key[pygame.K_g]:
                    self.kick_combo()

                if self.crouched == True:

                    if self.key[pygame.K_s] and self.key[pygame.K_b]:  # crouch block
                        self.l_block()

                    elif self.key[pygame.K_s] and self.key[pygame.K_r]:
                        self.l_punch()

                    elif self.key[pygame.K_s] and self.key[pygame.K_f]:
                        self.l_kick()

                    elif self.key[pygame.K_s] and self.key[pygame.K_h]:
                        self.uppercut()

                elif self.key[pygame.K_1]:
                    self.sp1()

                elif self.key[pygame.K_2]:
                    self.sp2()

                elif self.key[pygame.K_3]:
                    self.sp3()



        elif self.ko == True:

            if self.hp <= 0:
                self.defeated()
            else:
                self.victory1()

        # handles gravity
        self.vel += 1
        if self.vel > 15:
            self.vel = 15
        self.dy += self.vel

        #the animation loops through
        if self._counter >= animation_time and self._frame_index < len(self._master_anim_list[self._action]) - 1:
            self._counter = 0
            self._frame_index += 1
            self.image = self._master_anim_list[self._action][self._frame_index]

        #when we near the end of the list
        if self._frame_index == len(self._master_anim_list[self._action]) - 1:
            self._frame_index = 0 #reset the counter and index
            self._counter = 0

        self.rect.x += self.dx #added to the x co-ordinate position
        self.rect.y += self.dy #added to the y co-ordinate position

        if self.rect.x >= 700: #collision boundaries against the screen
            self.rect.x = 700
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y >= 280 and self._2P == True:
            if self._online != True and not self.key[pygame.K_DOWN] or self._online == True:
                self.rect.y = 280
        if self.rect.y >= 280 and self._2P == False and not self.key[pygame.K_s]:
            self.rect.y = 280
        if self.rect.y <= 0:
            self.rect.y = 0


        screen.blit(self.image, self.rect) #blit the sprite



    def collides_with(self, sprite,isBoss):

        if isBoss == False: #player collisions
            if self.rect.colliderect(sprite.rect): #if player collides with other sprite
                if self._action == 5 or self._action == 8 and sprite._action != 2: #dependent on action
                    sprite.hurt() #output the damage for the sprite
                    sprite.hurt_type("light") #output the damage type
                elif self._action == 10 or self._action == 12 and sprite._action != 3:
                    sprite.hurt()
                    sprite.hurt_type("light")
                elif self._action == 6 or self._action == 9 or self._action == 11 and sprite._action != 2:
                    sprite.hurt()
                    sprite.hurt_type("medium")
                elif self._action == 15 or self._action == 16 or self._action == 17 and sprite._action != 2:
                    sprite.hurt()
                    sprite.hurt_type("high")
                elif self._action == 7:
                    sprite.knocked()
                    sprite.hurt_type("medium")
                elif sprite._action == 2:
                    sprite.hurt_type("blocked")
        elif isBoss == True: #collision with boss
            if self.rect.colliderect(sprite.rect): #if player collides with other sprite
                if self._action == 5 or self._action == 8 and sprite._action != 2: #dependent on action
                    sprite.hurt() #output the damage for the sprite
                    sprite.hurt_type("light") #output the damage type
                elif self._action == 10 or self._action == 12:
                    sprite.hurt()
                    sprite.hurt_type("light")
                elif self._action == 6 or self._action == 9 or self._action == 11 and sprite._action != 2:
                    sprite.hurt()
                    sprite.hurt_type("medium")
                elif self._action == 15 or self._action == 16 or self._action == 17 and sprite._action != 2:
                    sprite.hurt()
                    sprite.hurt_type("high")
                elif self._action == 7:
                    sprite.knocked()
                    sprite.hurt_type("medium")




    def can_hurt(self): #function exists to allow for hit delays rather than losing alot of health at once with one hold of a button
        if datetime.now() < self._hit_delay: #if it hasn't passed the time to allow another hit, return false
            return False

        return True #when you can hit the oppenent

    def idle(self):
        self._action = 0 #the animation loop
        return self._action

    def move(self,direction): #takes direction parameter
        self._action = 1 #the animation action
        if direction == "back": #if its back
            self.dx += -5 #subtracts x co-ordinate
        elif direction == "forward": #if its forward
            self.dx += 5 #subtracts y co-ordinate
        if self._online == True: #if it is an online game 
            self.updateServer() # send over data to the server
        return self.dx, self._action

    def blocking(self):
        self._action = 2#the animation loop
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, self.damage

    def l_block(self):
        self._action = 3 #the animation loop
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, self.damage

    def jump(self):
        self.vel = -15
        self._action = 4 #the animation loop
        sound = self.grunts[1].play(0) #sound effect for character
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound, self.vel

    def punch(self):
        self._action = 5 #the animation loop
        sound = self.grunts[0].play(0) #sound effect for character
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound

    def punch_combo(self):
        self._action = 6 #the animation loop
        sound = self.grunts[2].play(0) #sound effect for character
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound


    def l_punch(self):
        self._action = 12 #the animation loop
        sound = self.grunts[0].play(0) #sound effect for character
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound


    def throw(self):
        self.dy += 10
        self._action = 7 #the animation loop
        sound = self.grunts[1].play(0) #sound effect for character
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound


    def kick(self):
        self._action = 8 #the animation loop
        sound = self.grunts[1].play(0) #sound effect for character
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound


    def kick_combo(self):
        self._action = 9 #the animation loop
        sound = self.grunts[2].play(0) #sound effect for character
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound


    def l_kick(self):
        self._action = 10 #the animation loop
        sound = self.grunts[0].play(0) #sound effect for character
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound


    def uppercut(self):
        self._action = 11 #the animation loop
        sound = self.grunts[1].play(0) #sound effect for character
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound


    def hurt(self):
        if self.crouched == False:
            self._action = 13 #the animation loop
        elif self.crouched == True:
            self._action = 14 #the animation loop
        sound = self.grunts[4].play(0) #sound effect for character
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound


    def hurt_type(self,damage_type): #takes damage parameter
        if damage_type == "light": #if parameter == specific sctring
            self.damage += self._light_dmg #adds to the damage
        elif damage_type == "medium":
            self.damage += self._med_dmg
        elif damage_type == "high":
            self.damage += self._high_dmg
        if damage_type == "blocked":
            self.damage = random.randint(1,5)
        if self.can_hurt(): #allow the damage if the delay is over
            self.hp -= self.damage #sbtrct the damage to the health
            self._hit_delay = datetime.now() + timedelta(seconds=1.25) #delay for 1.25s
        self.damage = 0 #reset damage
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server

    def knocked(self):
        for i in range(9):
            self.x += 10
            self.y -= 10
        self._action = 18 #the animation loop
        sound = self.grunts[4].play(0) #sound effect for character
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound


    def sp1(self):
        self._action = 15 #the animation loop
        sound = self.grunts[6].play(0) #sound effect for character
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound


    def sp2(self):
        self._action = 16 #the animation loop
        sound = self.grunts[6].play(0) #sound effect for character]
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound


    def sp3(self):
        self._action = 17 #the animation loop
        sound = self.grunts[6].play(0) #sound effect for character
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound


    def defeated(self):
        self._action = 22 #the animation loop
        sound = self.grunts[5].play(0) #sound effect for character
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound


    def crouch(self):
        self._action = 19 #the animation loop
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action

    def victory1(self):
        sound = self.grunts[7].play(0) #sound effect for character
        self._action = 20 #the animation loop
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound

    def victory2(self):
        sound = self.grunts[7].play(0) #sound effect for character
        self._action = 21 #the animation loop
        if self._online == True: #if it is an online game
            self.updateServer() # send over data to the server
        return self._action, sound

