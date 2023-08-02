#Configuration.py


import pygame, random, time #import modules

#settings

pygame.init() #initalise pygame
clock = pygame.time.Clock() #pygame clock
main_font = pygame.font.SysFont('franklingothicmedium', 19) #generalised text font
pygame.display.set_caption('Immortal Combat') #window caption

#dictionary in a dictionary of the config settings
config = {'settings':
               {'fullscreen':False, #fullscreen is off
                'time_amount':60, #the amount of time
                'fps':60, # controls the frames per second
                'screen_width':800, #controls the screen width
                'screen_height':600}, #controls the screen height
          'colours':
                {'maroon':(105, 4, 23),
                'light_blue':(44, 235, 245),
                'red':(255,37,28),
                'orange':(255,165,0),
                'black':(0,0,0),
                'white':(255,255,255),
                'steel':(176,196,222),
                'purple':(198, 19, 240)}}

time_count = 60

screen = pygame.display.set_mode((config['settings']['screen_width'], config['settings']['screen_height'])) # the screen size


#animation list action order
# The following series of for loops are used to load certain images for the animation of certain moves, self.action is a variable which has a number correlating to the order of these loops
# For example, if i have my idle anim loop coded first, then my walking anim loop, it will be designated in that order. 0:Idle, 1:Walking

# Animation list
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


# Animation list Orgo
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
