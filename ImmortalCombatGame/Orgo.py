#Orgo.py


import pygame,random,time
from pygame import mixer
from datetime import datetime, timedelta
from Configuration import *


class OrgoBoss(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()  # calls to the superclass
        self._name = 'Orgo' # the characters name, this is vital as it is needed to access different files
        self._max_hp = 400  # the max health is the same among playable characters
        self.hp = self._max_hp  # the current hp for the health bar
        self.x = x  # the x co-ordinate position
        self.y = y  # the y co-ordinate position

        # the different damage variables later called into the functions
        self._light_dmg = random.randint(10, 30)
        self._med_dmg = random.randint(30, 60)
        self._high_dmg = random.randint(70, 90)
        self.damage = 0  # the damage variable itself where it is then subtracted from player's hp

        self.hit_delay = datetime.now()  # set to current time but later set to add 1.25 seconds to allow for delaying consecutive hit
        self._master_anim_list = []  # where the image list gets append to so these images become the main ones on screen
        self._frame_index = 0  # the index through the aniim list
        self._action = 0  # the for loops where the images are loaded define this variable
        self.ko = False  # When true, allow for player controls
        self.dx = 0  # gets added to the x co-ordinate to go left or right
        self.dy = 0  # gets added  to the y co-ordinate to jump or crouch
        self.grunts = [mixer.Sound(f'{self._name}/Audio/Grunt1.wav'), mixer.Sound(f'{self._name}/Audio/Grunt2.wav'),# a list of the various voice effects
                       mixer.Sound(f'{self._name}/Audio/Hurt.wav'), mixer.Sound(f'{self._name}/Audio/KO.wav'),# uses f'string to apply the name to the file directory for each character's voice
                       mixer.Sound(f'{self._name}/Audio/SPGrunt.wav'), mixer.Sound(f'{self._name}/Audio/Victory.wav')]







        # The following series of for loops are used to load certain images for the animation of certain moves, self._action is a variable which has a number correlating to the order of these loops
        # For example, if i have my idle anim loop coded first, then my walking anim loop, it will be designated in that order. 0:Idle, 1:Walking

        # animation list
        # 0 Idle
        # 1 Moving
        # 2 Block
        # 3 Jump
        # 4 Punch1
        # 5 Punch2
        # 6 Taking Damage
        # 7 Knockback
        # 8 Special Move1
        # 9 Special Move2
        # 10 Special Move3
        # 11 Throw
        # 12 Victory
        # 13 Defeat

        #0 Idle
        sub_anim_list = []
        for i in range(7):# these temporary lists contain the set animation for different actions which will go into the master list
            img = pygame.image.load(f'{self._name}/1)Idle/{i}.png')# loops through the amount of images in the folder directory, in this case, i have 7 idle images to loop through
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))# loads in the images in the order of i and based on self._name
            img = pygame.transform.flip(img, img.get_width(), False)# increase the scale of the images by 3 times
            sub_anim_list.append(img)# appends to a temporary list
        self._master_anim_list.append(sub_anim_list)# when self._action corresponds to the loop order, play that set of animations

        #1 Moving
        sub_anim_list = []
        for i in range(8):
            img = pygame.image.load(f'{self._name}/3)Moving/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        #2 Block
        sub_anim_list = []
        img = pygame.image.load(f'{self._name}/2)Block/0.png')
        img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
        img = pygame.transform.flip(img, img.get_width(), False)
        sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        #3 Jump
        sub_anim_list = []
        for i in range(2):
            img = pygame.image.load(f'{self._name}/4)Jumping/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)


        #4 Punch 1
        sub_anim_list = []
        for i in range(0,4):
            img = pygame.image.load(f'{self._name}/5)Punch/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        #5 Punch 2
        sub_anim_list = []
        for i in range(5,9):
            img = pygame.image.load(f'{self._name}/5)Punch/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        #6 Take Damage
        sub_anim_list = []
        for i in range(4):
            img = pygame.image.load(f'{self._name}/6)TakeDamage/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)


        #7 Knockback
        sub_anim_list = []
        for i in range(6):
            img = pygame.image.load(f'{self._name}/7)Knockback/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)


        # 8 Special Move 1
        sub_anim_list = []
        for i in range(5):
            img = pygame.image.load(f'{self._name}/8)SP1/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 9 Special Move 2
        sub_anim_list = []
        for i in range(0,5):
            img = pygame.image.load(f'{self._name}/9)SP2/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)


        # 10 Special Move 3
        sub_anim_list = []
        for i in range(5):
            img = pygame.image.load(f'{self._name}/10)SP3/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)


        # 11 Throw
        sub_anim_list = []
        for i in range(3):
            img = pygame.image.load(f'{self._name}/11)Throw/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 12 Victory
        sub_anim_list = []
        for i in range(3):
            img = pygame.image.load(f'{self._name}/12)Victory/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        # 13 Defeat
        sub_anim_list = []
        for i in range(3):
            img = pygame.image.load(f'{self._name}/13)Defeat/0.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            img = pygame.transform.flip(img, img.get_width(), False)
            sub_anim_list.append(img)
        self._master_anim_list.append(sub_anim_list)

        self.image = self._master_anim_list[self._action][self._frame_index]  # the current images
        self.rect = pygame.Rect(self.x, self.y, 160, 300)  # the rect of the character
        self.rect.center = (x, y)  # where the character is positioned
        self._counter = 0  # used for the animation loop

    def update(self,sprite):
        animation_time = 5  # the time before the next , the lower the value, the faster the animation runs
        self.dx = 0  # added or subtracted value that dictates the movement
        self.dy = 0  # added or subtracted value that dictates the movement
        self.vel = 5  # velocity
        self.key = pygame.key.get_pressed()  # keyboard input allowing for holds
        self._counter += 1
        self.nodes = {"idle": self.idle(),
                           "move_forward": self.move("forward"),
                           "move_back": self.move("back"),
                           "jump": self.jump(),
                           "block": self.blocking(),
                           "punch": self.punch(),
                           "punch2": self.punch_combo(),
                           "sp1": self.sp1(),
                           "sp2": self.sp2(),
                           "sp3": self.sp3(),
                           "throw": self.throw()}



        if self.ko == False:
            AI(self.nodes.get("idle"),sprite) #first node

        elif self.ko == True:
            self.knocked()

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

        if self.rect.x >= 700:
            self.rect.x = 700
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y >= 260:
            self.rect.y = 260
        if self.rect.y <= 0:
            self.rect.y = 0


        screen.blit(self.image, self.rect)




    def collides_with(self, sprite):

        if self.rect.colliderect(sprite.rect):  # if player collides with other sprite
            if self._action == 5 or self._action == 8 and sprite._action != 2:  # dependent on action
                sprite.hurt()  # output the damage for the sprite
                sprite.hurt_type("light")  # output the damage type
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

    def can_hurt(self): #function exists to allow for hit delays rather than losing alot of health at once with one hold of a button
        if datetime.now() < self.hit_delay: #if it hasn't passed the time to allow another hit, return false
            return False

        return True #when you can hit the oppenent

    def idle(self):
        self._action = 0
        return self._action

    def move(self,direction): #takes direction parameter
        self._action = 1 #the animation action
        if direction == "back": #if its back
            self.dx -= 5 #subtracts x co-ordinate
        elif direction == "forward": #if its forward
            self.dx += 5 #subtracts y co-ordinate
        return self.dx, self._action

    def blocking(self):
        self._action = 1 #the animation loop
        return self._action, self.damage


    def jump(self):
        self.vel = -15
        self._action = 3
        sound = self.grunts[1].play(0)
        return self._action, sound, self.vel

    def punch(self):
        self._action = 4
        sound = self.grunts[0].play(0)
        return self._action, sound

    def punch_combo(self):
        self._action = 5
        sound = self.grunts[4].play(0)
        return self._action, sound


    def hurt(self):
        self._action = 6
        sound = self.grunts[2].play(0)
        return self._action, sound


    def hurt_type(self,damage_type): #takes damage parameter
        if damage_type == "light": #if parameter == specific sctring
            self.damage += self._light_dmg #adds to the damage
        elif damage_type == "medium":
            self.damage += self._med_dmg
        elif damage_type == "high":
            self.damage += self._high_dmg
        elif damage_type == "blocked":
            self.damage = random.randint(3,8)
        if self.can_hurt(): #allow the damage if the delay is over
            self.hp -= self.damage #subtrct the damage to the health
            self._hit_delay = datetime.now() + timedelta(seconds=1.25) #delay for 1.25s
        self.damage = 0 #reset damage



    def knocked(self):
        for i in range(6):
            if random.random() > 0.5:
                    self.dx += 10
            if random.random() > 0.5:
                self.dy -= 5
        self._action = 7
        sound = self.grunts[2].play(0)
        return self._action, sound


    def sp1(self):
        self._action = 8
        sound = self.grunts[4].play(0)
        return self._action, sound


    def sp2(self):
        self._action = 9
        sound = self.grunts[4].play(0)
        return self._action, sound


    def sp3(self):
        self._action = 10
        sound = self.grunts[4].play(0)
        return self._action, sound

    def throw(self):
        self.dy += 11
        self._action = 7
        sound = self.grunts[4].play(0)
        return self._action, sound

    def victory(self):
        sound = self.grunts[5].play(0)
        self._action = 12
        return self._action, sound


    def defeated(self):
        self._action = 13
        sound = self.grunts[3].play(0)
        return self._action, sound







class AI:

    def __init__(self,data,target):

        self.target = target #the 2nd player
        self.active = True #Ai active
        self.left = None  # to left node in the tree
        self.right = None  # to the right node in the tree
        self.data = data #the nodes
        self.status = "FAILURE" #status of action
        self.blackboard = self.blackboard_dict()

    def insert_data(self, data):
        if self.data is None:  # if there is data within the root
            self.data = data  # data remains the same
        else:
            if self.status == "FAILURE":
                if self.left is None:  # if theres no data in the left child
                    self.left = AI(data,target)
                    self.status = "RUNNING"
                else:
                    self.left.insert_data(data)
                if self.right is None:  # if theres no data in the right child
                    self.right = AI(data,target)
                    self.status = "RUNNING"
                else:
                    self.right.insert_data(data)

    def blackboard_dict(self):
        enemy_act = {"x":self.target.x,"y":self.target.x,"action":self.target._action}
        return enemy_act

    def update(self):
        while self.active == True: #active AI
            if self.enemy_act["x"] < self.x: #if boss is further away from player
                self.insert_data(self.nodes.get("move_forward")) #move toward
            if self.enemy_act["x"] == self.x - 10: #if the player is close
                if (3 > random.randint(1,10) > 1): #rnadom action to occur
                    self.insert_data(self.nodes.get("punch"))
                elif (6 >random.randint(1,10) > 4):
                    self.insert_data(self.nodes.get("punch2"))
                elif (10> random.randint(1,10) > 7):
                    self.insert_data(self.nodes.get("move_back"))
            else:
                self.insert_data(self.nodes.get("idle")) #else remain idle

