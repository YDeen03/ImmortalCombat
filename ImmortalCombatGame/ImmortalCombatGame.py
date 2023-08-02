#ImmortalCombatGame.py


import pygame, random, time, json, socket, threading#import the modules
from PlayableCharacters import Fighter
from _thread import *
from Configuration import *
from Orgo import *



class Timer:

    def __init__(self, x, y, colour, size):
        self.colour = colour  # colour of text
        self.font = pygame.font.SysFont('Futura', size)  # text font
        self.time_text = self.font.render(str(config['settings']['time_amount']), True, colour)# render the timer as text on screen
        self.timer_event = pygame.USEREVENT + 1  # added toe event queue
        pygame.time.set_timer(self.timer_event,1000)  # takes parameters such as the timer_event and the delay of 100 miliseconds
        self.time_text_rect = self.time_text.get_rect()  # gets the rect dimensions of the text
        self.time_text_rect.center = (x, y)  # position of the text's center
        self.time_is_up = Titles(400, 160, "TIME UP", config['colours']['white'], 'franklingothicmedium',60)  # uses title class to define the time up text
        self.draw_time = False
        self.finished = False  # boolean variable to determine whether to go onto the victory screen when True

    def draw(self):

        for event in pygame.event.get():
            if event.type == self.timer_event: #once timer starts
                config['settings']['time_amount'] -= 1 #decrease by a second
                self.time_text = self.font.render(str(config['settings']['time_amount']), True, self.colour)# render current time
                if config['settings']['time_amount'] <= 0: #
                    self.time_text = self.font.render(str(0), True, self.colour)
                    self.time_is_up.draw()
                if config['settings']['time_amount'] == -4:
                    self.finished = True

        screen.blit(self.time_text, self.time_text_rect)


class Titles:
    def __init__(self, x, y, text, colour, style, size):
        super(Titles, self).__init__()
        font = pygame.font.SysFont(style, size)  # font set
        self.style = style  # the font style
        self.size = size  # the size of the text
        self.title = font.render(text, True, colour)  # the title
        self.rect = self.title.get_rect()  # the rect of the text itself
        self.rect.center = (x, y)  # the position determined by x and y

    def draw(self):
        screen.blit(self.title, self.rect)  # the function to blit it on screen


class WinScreen:

    def __init__(self):
        self.endscreen = True #when the fight ends
        self.quotes = [mixer.Sound("Assets/Announcer/YouWin.wav"), mixer.Sound("Assets/Announcer/Draw.wav"), mixer.Sound("Assets/Announcer/OrgoWins.wav")] #announcer quotes
        self.playsound = True #when the sound is played
        self.purple = config['colours']['purple']

    def draw(self, character_name, player): #parameters determine player name and if the boss or player wins
        win_text = Titles(400, 150, character_name, self.purple, "arial", 120) #text onto the screen
        win_text2 = Titles(400, 300, "Wins", self.purple, "arial", 120)
        win_text3 = Titles(400, 400, "**PRESS ESC TO CONTINUE**", self.purple, "arial", 20)
        pygame.mixer.music.stop() #music ends of the game

        while self.endscreen == True:
            screen.fill(config['colours']['black']) #fill the screen black
            win_text.draw() #draw the text
            win_text2.draw()
            win_text3.draw()
            if player == 0 and self.playsound == True: #if it a draw
                self.quotes[1].play(0) #play the announcer quote once
                self.playsound = False
            elif player == 1 and self.playsound == True: #if it is a player:
                self.quotes[0].play(0)
                self.playsound = False
            elif player == 2 and self.playsound == True:  # if it is a boss:
                self.quotes[2].play(0)
                self.playsound = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:# press esc to return to the main menu
                        self.endscreen = False
                        MenuScreen()

            pygame.display.update()
            clock.tick(config['settings']['fps'])  # the program will never run at more than the set fps when this function's called


class HealthBar:

    def __init__(self, x, y, hp, max_hp):
        self.x = x  # x co-ordinate position
        self.y = y  # x co-ordinate position
        self.hp = hp  # current health
        self.max_hp = max_hp  # max health

    def draw(self, hp):
        # update with new health
        self.hp = hp

        ratio = self.hp / self.max_hp  # calculate health ratio.
        pygame.draw.rect(screen, config['colours']['black'], (self.x - 5, self.y - 5, 160, 30))  # rect to outline the healthbar
        pygame.draw.rect(screen, config['colours']['maroon'], (self.x, self.y, 150, 20))  # depleted healthbar
        pygame.draw.rect(screen, config['colours']['purple'], (self.x, self.y, 150 * ratio, 20))  # health remaining


class Fight:

    def __init__(self):
        self.colours = [config['colours']['steel'], config['colours']['purple'], config['colours']['light_blue'],
                        config['colours']['black'], config['colours']['red'],config['colours']['white']]
        self.background_img = pygame.image.load('Assets/stage1.jpg') #load the sbackground

        self.player1 = Fighter(200, 430, 'Sapphire', False, False) #set the fighters
        self.player1_name = Titles(80, 100, self.player1._name, self.colours[0], 'franklingothicmedium', 24)#fighter name
        self.player1_hp = HealthBar(50, 50, self.player1.hp, self.player1._max_hp)#fighter health bar

        self.player2 = Fighter(600, 430, 'Drifter', True, False)
        self.player2_name = Titles(730, 100, self.player2._name, self.colours[0], 'franklingothicmedium', 24)
        self.player2_hp = HealthBar(600, 50, self.player2.hp, self.player2._max_hp)

        self.quotes = [mixer.Sound("Assets/Announcer/Fight!.wav"), mixer.Sound("Assets/Announcer/KO.wav")]
        self.fight_timer = Timer(380, 50, self.colours[0], 60)
        self.who_wins = WinScreen()

    def current_fps(self,size,colour): #change size + colour
        self.fps_txt = str(int(clock.get_fps())) #turn the current fps into a string
        self.fps_surface = pygame.font.SysFont('Arial', size).render(self.fps_txt, True, colour) #set the surface for it to be blit later
        return self.fps_surface #return the surface


    def win_conditions(self):
        if self.player2.hp <= 0:  # if p2 health 0 or less
            self.quotes[1].play(0)
            time.sleep(1)
            self.who_wins.draw(self.player1._name, 1)  # p1 wins
            self.reset()
        elif self.player1.hp <= 0:  # if p1 health 0 or less
            self.quotes[1].play(0)
            time.sleep(1)
            self.who_wins.draw(self.player2._name, 1)  # p2 wins
            self.reset()

        if self.fight_timer.finished == True:  # if timer has finished
            if self.player1.hp > self.player2.hp:  # if p1 has greater health
                self.who_wins.draw(self.player1._name, 1)  # p1 wins
            elif self.player2.hp > self.player1.hp:  # if p1 has greater health
                self.who_wins.draw(self.player2._name, 1)  # p2 wins
            elif self.player1.hp == self.player2.hp:  # if each player has the same amount of health
                self.who_wins.draw("No-one", 0)  # it is a draw
            self.reset()


    def run(self):
        self.gameplay = True
        playsound = True

        while self.gameplay == True:

            screen.blit(self.background_img, (0, 0))  # draw background
            if playsound == True:
                self.quotes[0].play(0)
                playsound = False

            self.player1_name.draw()  # draw fighters' names
            self.player2_name.draw()

            self.player1_hp.draw(self.player1.hp)  # draw healthbars
            self.player2_hp.draw(self.player2.hp)

            self.fight_timer.draw()  # draw the timer

            self.player1.update()  # draws the sprites onscreen
            self.player2.update()

            self.player1.collides_with(self.player2, False)  # calls the collision function
            self.player2.collides_with(self.player1, False)

            screen.blit(self.current_fps(24,self.colours[0]), (10,10))  # blit FPS

            self.win_conditions()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            clock.tick(config['settings']['fps'])  # the program will never run at more than the set fps when this function's called
            pygame.display.update()  # updates what is on screen

    def reset(self):
        self.gameplay = False
        self.player1 = Fighter(200, 430, 'Sapphire', False, False)
        self.player1_name = Titles(80, 100, self.player1._name, self.colours[0], 'franklingothicmedium', 24)
        self.player1_hp = HealthBar(50, 50, self.player1.hp, self.player1._max_hp)

        self.player2 = Fighter(600, 430, 'Drifter', True, False)
        self.player2_name = Titles(730, 100, self.player2._name, self.colours[0], 'franklingothicmedium', 24)
        self.player2_hp = HealthBar(600, 50, self.player2.hp, self.player2._max_hp)

        self.who_wins = WinScreen()
        config['settings']['time_amount'] = 60


class BossMode(Fight):

    def __init__(self):
        super().__init__()
        self.background_img = pygame.image.load('Assets/stage4.jpg') #boss stage

        self.player2 = OrgoBoss(600, 400) #the boss object
        self.player2_name = Titles(730, 100, self.player2._name, config['colours']['steel'], 'franklingothicmedium', 24)
        self.player2_hp = HealthBar(600, 50, self.player2.hp, self.player2._max_hp)


    def run_char_select(self):
        self.char_select = True

        while self.char_select == True:
            self.mouse = pygame.mouse.get_pos()  # receives the x and y co-ordinates of the mouse

            screen.fill(self.colours[4])
            screen.blit(main_font.render("Developed by Yousuf", True, self.colours[5]), (20, 10))

            mode1 = pygame.Rect(100, 300, 200, 150)
            mode2 = pygame.Rect(500, 300, 200, 150)
            mode3 = pygame.Rect(100, 520, 100, 50)

            pygame.draw.rect(screen, self.colours[2], mode1)  # draws the button and colour of them onto screen
            pygame.draw.rect(screen, self.colours[2], mode2)
            pygame.draw.rect(screen, self.colours[3], mode3)

            if 300 > self.mouse[0] > 100 and 450 > self.mouse[1] > 300:  # If mouse's position or the mouse hovers over the buttons
                pygame.draw.rect(screen, self.colours[2], mode1, 6)  # Therefore button outline changes colour
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:  # If user left click the mouse when mouse position equals to position of button
                    self.click = True
                    self.player1 = Fighter(200, 430, "Sapphire", False, False) #Saphire is chosen
                    self.run() #run the fight
                    self.char_select = False

            if 700 > self.mouse[0] > 500 and 450 > self.mouse[1] > 300:
                pygame.draw.rect(screen, self.colours[2], mode2, 6)
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                    self.click = True
                    self.player1 = Fighter(200, 430, "Drifter", False, False) #Drifter is chosen
                    self.run() #run the fight
                    self.char_select = False


            if 200 > self.mouse[0] > 100 and 570 > self.mouse[1] > 520:
                pygame.draw.rect(screen, self.colours[2], mode3, 6)
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                    self.click = True
                    MenuScreen() #head back to the menu
                    self.char_select = False

            # Renders the text on screen with screen.blit, choose the character
            screen.blit(pygame.font.SysFont('franklingothicmedium', 50).render("CHOOSE YOUR FIGHTER", True, self.colours[3]), (145, 100))

            screen.blit(pygame.font.SysFont('franklingothicmedium', 20).render("And Fight the Champion.", True, self.colours[4]), (280, 150))

            screen.blit(main_font.render("Sapphire", True, self.colours[3]), (160, 360))

            screen.blit(main_font.render("Drifter", True, self.colours[3]), (570, 360))

            screen.blit(main_font.render("Back", True, self.colours[5]), (110, 530))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()  # updates what is on screen
            clock.tick(config['settings']['fps'])  # the program will never run at more than the set fps when this function's called

    def run(self):
        self.gameplay = True#gameplay occurs
        pygame.mixer.music.load("Assets/Music/BossMusic.wav")
        pygame.mixer.music.play(-1)

        while self.gameplay == True:


            screen.blit(self.background_img, (0, 0))  # draw background

            self.player1_name.draw()  # draw fighters' names
            self.player2_name.draw()

            self.player1_hp.draw(self.player1.hp)  # draw healthbars
            self.player2_hp.draw(self.player2.hp)

            self.fight_timer.draw()  # draw the timer

            self.player1.update()  # draws the sprites onscreen
            self.player2.update(self.player1)

            self.player1.collides_with(self.player2, True)  # calls the collision function
            self.player2.collides_with(self.player1)

            screen.blit(self.current_fps(24,config['colours']['steel']), (10,10))  # blit FPS

            if self.player2.hp <= 0:  # if p2 health 0 or less
                self.quotes[1].play(0)
                time.sleep(1)
                self.who_wins.draw(self.player1._name, 1)  # p1 wins
                self.reset()
            elif self.player1.hp <= 0:  # if p1 health 0 or less
                self.quotes[1].play(0)
                time.sleep(1)
                self.who_wins.draw(self.player2._name, 2)  # p2 wins
                self.reset()

            if self.fight_timer.finished == True:  # if timer has finished
                if self.player1.hp > self.player2.hp:  # if p1 has greater health
                    self.who_wins.draw(self.player1._name, 1)  # p1 wins
                elif self.player2.hp > self.player1.hp:  # if p1 has greater health
                    self.who_wins.draw(self.player2._name, 1)  # p2 wins
                elif self.player1.hp == self.player2.hp:  # if each player has the same amount of health
                    self.who_wins.draw("No-one", 0)  # it is a draw
                self.reset()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            clock.tick(config['settings']['fps'])  # the program will never run at more than the set fps when this function's called
            pygame.display.update()  # updates what is on screen


class LocalVersus(Fight):

    def __init__(self):
        super().__init__()

    def run_stage_select(self):
        self.stage_select = True


        while self.stage_select == True:
            self.mouse = pygame.mouse.get_pos()  # receives the x and y co-ordinates of the mouse

            screen.fill(self.colours[3])

            mode1 = pygame.Rect(30, 400, 150, 100)
            mode2 = pygame.Rect(230, 400, 150, 100)
            mode3 = pygame.Rect(430, 400, 150, 100)
            mode4 = pygame.Rect(630, 400, 150, 100)

            pygame.draw.rect(screen, self.colours[1], mode1)  # draws the button and colour of them onto screen
            pygame.draw.rect(screen, self.colours[1], mode2)
            pygame.draw.rect(screen, self.colours[1], mode3)

            if 180 > self.mouse[0] > 30 and 500 > self.mouse[1] > 400:  # If mouse's position or the mouse hovers over the buttons
                pygame.draw.rect(screen, self.colours[2], mode1, 6)  # Therefore button outline changes colour
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:  # If user left click the mouse when mouse position equals to position of button
                    self.click = True
                    self.background_img = pygame.image.load('Assets/stage1.jpg')
                    pygame.mixer.music.load("Assets/Music/FightMusic.wav")
                    pygame.mixer.music.play(-1)
                    self.run()



            if 380 > self.mouse[0] > 230 and 500 > self.mouse[1] > 400:
                pygame.draw.rect(screen, self.colours[2], mode2, 6)
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                    self.click = True
                    self.background_img = pygame.image.load('Assets/stage3.jpg')
                    pygame.mixer.music.load("Assets/Music/FightMusic3.wav")
                    pygame.mixer.music.play(-1)
                    self.run()



            if 580 > self.mouse[0] > 430 and 500 > self.mouse[1] > 400:
                pygame.draw.rect(screen, self.colours[2], mode3, 6)
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                    self.click = True
                    self.background_img = pygame.image.load('Assets/stage2.jpg')
                    pygame.mixer.music.load("Assets/Music/FightMusic2.wav")
                    pygame.mixer.music.play(-1)
                    self.run()

            if 780 > self.mouse[0] > 630 and 500 > self.mouse[1] > 400:
                pygame.draw.rect(screen, self.colours[2], mode4, 6)
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                    self.click = True
                    MenuScreen()
                    self.stage_select = False

            screen.blit(pygame.font.SysFont('arial', 90).render("CHOOSE THE ARENA", True, self.colours[5]), (20, 120))

            screen.blit(main_font.render("AND GET READY TO FIGHT IN IMMORTAL COMBAT", True, self.colours[4]), (40, 220))

            screen.blit(main_font.render("Frozen Forest", True, self.colours[3]), (40, 440))

            screen.blit(main_font.render("Wrestling", True, self.colours[3]), (240, 440))

            screen.blit(main_font.render("Blue Box?", True, self.colours[3]), (440, 440))

            screen.blit(main_font.render("Back", True, self.colours[5]), (640, 440))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()  # updates what is on screen
            clock.tick(config['settings']['fps'])  # the program will never run at more than the set fps when this function's called


class Server:
    # Server will create and position 2 player objects, and tell the clients where and who they are controlling
    def __init__(self):
        self.client_list = []#store the clients connecting to the game

        self.host = "127.0.0.1"  # IP address used for the clients to connect to
        self.port = 12345  # endpoint for communication between the clients sending and receiving data

        self.player_map = {}  # This will map a connection to a player object

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Set socket parameters


        self.player1 = Fighter(200, 430, 'Sapphire', False, True)
        self.player1_name = Titles(80, 100, self.player1._name, config['colours']['steel'], 'franklingothicmedium', 24)
        self.player1_hp = HealthBar(50, 50, self.player1.hp, self.player1._max_hp)

        self.player2 = Fighter(600, 430, 'Drifter', True, True)
        self.player2_name = Titles(730, 100, self.player2._name, config['colours']['steel'], 'franklingothicmedium', 24)
        self.player2_hp = HealthBar(600, 50, self.player2.hp, self.player2._max_hp)

        self.fight_timer = Timer(380, 50, config['colours']['steel'], 60)
        self.who_wins = WinScreen()

    def process_action(self, commands, connection):
        player_action = self.player_map[connection]
        # The connection tells us who performed the action

        num = list(range(0,23)) #any action num from 0 to 22
        if commands["Action"] == num: #if the ation is any num
            player_action._action = num #then self.action is num

        cmd = {"Command": "ACTIONS",  "Action": commands["Action"]}
        for client in self.client_list: #send the command ito each client
            if client != connection:  # if the client is not the one that sent the move
                client.send(json.dumps(cmd).encode())

    def process_move(self, commands, connection): #Player movement is told to the other client.
        player_move = self.player_map[connection]  # Based on the connection, work out which player moved
        player_move.x = commands["X"]
        player_move.y = commands["Y"]
        # Change the x and y position of the player on the server
        for client in self.client_list:  # loop through all connections
            if client != connection:  # if the client is not the one that sent the move
                cmd = {"Command": "MOVE_OTHER", "X": player_move.x, "Y": player_move.y}
                client.send(json.dumps(cmd).encode())  # Tell the other client to move the "Enemy"

    def process_message(self, data, connection):
        commands = json.loads(data.decode()) #receive the command
        if commands["Command"] == "MOVE":  # Get the command sent
            self.process_move(commands, connection) #process that command to that function
        if commands["Command"] == "Action":
            self.process_action(commands, connection)

        print(commands)#print the commands sent over

    def setup(self):#create and position 2 player objects, and tell the clients where and who they are controlling
        self.player_map[self.client_list[0]] = self.player1  # p1 is linked to the first connection that came in
        self.player_map[self.client_list[1]] = self.player2  # p2 is linked to the second connection

        cmd = {"Command": "SETUP", "You": {"Action": self.player1._action, "X": self.player1.x, "Y": self.player1.y, "Name":self.player1._name, "1/2P":self.player1._2P},
               "Other": {"Action": self.player2._action, "X": self.player2.x, "Y": self.player2.y, "Name":self.player2._name, "1/2P":self.player2._2P}}

        self.client_list[0].send(json.dumps(cmd).encode())

        # Send the first connection the details for setup of the players
        cmd = {"Command": "SETUP", "Other": {"Action": self.player1._action, "X": self.player1.x, "Y": self.player1.y, "Name":self.player1._name, "1/2P":self.player1._2P},
               "You": {"Action": self.player2._action, "X": self.player2.x, "Y": self.player2.y, "Name":self.player2._name, "1/2P":self.player2._2P}}

        self.client_list[1].send(json.dumps(cmd).encode())# Sending it to client 1 instead of client 0


    def handle_client(self, connection):
        while True:  # Loop forever to ensure the thread stays alive
            try:  # using a try-except to keep the thread alive.
                data = connection.recv(2048)  # Receive up to 2048 bytes from the socket.
                if data:
                    self.process_message(data, connection)  # If we have some data then call the process message
            except Exception as e:
                print("Error", e)

    def initialise(self):
        self.s.bind((self.host, self.port)) #bind the port to the server
        print("Server has started successfully")  # Bind the self.host and self.port to listen for connections on
        self.s.listen(2) #listen for 2 clients to connect
        while True:
            connection, address = self.s.accept()  # This line will cause a pause for the next connection
            print("New connection from", address)
            self.client_list.append(connection)# Add the client into the client list
            # thread runs function and doesn't make the main loop depend on the threaded client function to accept conncetion once it finishes
            threading.Thread(target=self.handle_client, args=(connection,)).start()# Start the thread to listen for incoming data  from the client
            cmd = {"Command": "WAIT"}# Tell the client to wait, because we need 2 connections to play
            connection.send(json.dumps(cmd).encode())
            if len(self.client_list) == 2: # When we have more than one client
                self.setup()  # Get the clients to setup the 2 players and positions
                for client in self.client_list:
                    cmd = {"Command": "START"}  #tell every client to START
                    client.send(json.dumps(cmd).encode())



class Client(Fight):

    def __init__(self):
        super().__init__()
        self.host = "127.0.0.1"#IP address used for the clients to connect to
        self.port = 12345 #endpoint for communication between the clients sending and receiving data

        self.background_img = pygame.image.load('Assets/stage1.jpg') #fight background

        self.fight_timer = Timer(380, 50, config['colours']['steel'], 60)
        self.who_wins = WinScreen()

        self.WAIT = True #waiting for players
        self.p1 = None #the player to this client
        self.enemy = None #the other player

        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)# Set socket parameters

    def setup(self,command,sock):
        #pull in the p1 and enemy variables
        #create the Player objects using data sent from the server
        self.p1 = Fighter(command["You"]["X"],command["You"]["Y"],command["You"]["Name"],command["You"]["1/2P"],True,sock)
        self.p1_name = Titles(80, 100, self.p1._name, config['colours']['steel'], 'franklingothicmedium', 24)
        self.p1_hp = HealthBar(50, 50, self.p1.hp, self.p1._max_hp)

        self.p1.rect.x = command["You"]["X"]
        self.p1.x = command["You"]["X"]
        self.p1.rect.y = command["You"]["Y"]
        self.p1.y = command["You"]["Y"]

        #Now setup the enemy Player instance using data from the server
        self.enemy = Fighter(command["Other"]["X"], command["Other"]["Y"], command["Other"]["Name"], command["Other"]["1/2P"],True)
        self.enemy_name = Titles(730, 100, self.enemy._name, config['colours']['steel'], 'franklingothicmedium', 24)
        self.enemy_hp = HealthBar(600, 50, self.enemy.hp, self.enemy._max_hp)

        self.enemy.rect.x = command["Other"]["X"]
        self.enemy.x = command["Other"]["X"]
        self.enemy.rect.y = command["Other"]["Y"]
        self.enemy.y = command["Other"]["Y"]



    def move_enemy(self,command):
        self.enemy.rect.x = command["X"]#data from the server to move the enemy
        self.enemy.dx = command["X"]#We want to update the x position and the rect.x position
        self.enemy.rect.y = command["Y"]
        self.enemy.dy = command["Y"]

    def enemy_action(self,command):
        self.enemy._action = command["Action"]# data from the server for enemy action

    def process_command(self,command,sock):
        print(command) #Function will take a command like server version of the function
        #Print command for debugging
        if command["Command"] == "WAIT":
            self.WAIT = True #wait for the game to start
        elif command["Command"] == "START":
            self.WAIT = False #False when the game begins
        elif command["Command"] == "SETUP":
            self.setup(command,sock) #Run setup function
        elif command["Command"] == "MOVE_OTHER":
            self.move_enemy(command) #Run move_enemy function
        elif command["Command"] == "ACTIONS":
            self.enemy_action(comand) #Run enemy_action function

    def receive_messages(self,sock):
        response = "" #empty respomse
        while True:
            response = sock.recv(2048).decode()#decode data senft from server
            if response:#If the server sent something then process it
                self.process_command(json.loads(response),sock)


    def start_client(self):
        self.s.connect((self.host,self.port))#connect to the server
        print("Connection granted")
        threading.Thread(target=self.receive_messages, args=(self.s,)).start() #listen for incoming data from server


        while self.WAIT == True:
            print("Waiting for clients to connect")
            time.sleep(1) #avoid console being flooded with waits

        print("GAME HAS STARTED")

        self.gameplay = True
        pygame.mixer.music.load("Assets/Music/FightMusic.wav") #load in the fight music
        pygame.mixer.music.play(-1)  # play the music indefinitely in this function

        while self.gameplay == True:


            screen.blit(self.background_img, (0, 0))  # draw background


            self.p1_name.draw()  # draw fighters' names
            self.enemy_name.draw()

            self.p1_hp.draw(self.p1.hp)  # draw healthbars
            self.enemy_hp.draw(self.enemy.hp)

            self.fight_timer.draw()  # draw the timer

            self.p1.update()  # draws the sprites onscreen
            self.enemy.update()

            self.p1.collides_with(self.enemy, False)  # calls the collision function
            self.enemy.collides_with(self.p1, False)

            screen.blit(self.current_fps(24,config['colours']['steel']), (10,10))  # blit config['settings']['fps']

            if self.enemy.hp <= 0:  # if p2 health 0 or less
                self.quotes[1].play(0)
                time.sleep(1)
                self.who_wins.draw(self.player1._name, 1)  # p1 wins
                self.reset()
            elif self.p1.hp <= 0:  # if p1 health 0 or less
                self.quotes[1].play(0)
                time.sleep(1)
                self.who_wins.draw(self.enemy._name, 1)  # p2 wins
                self.reset()

            if self.fight_timer.finished == True:
                if self.p1.hp > self.enemy.hp:
                    self.who_wins.draw(self.p1._name, 1)
                elif self.enemy.hp > self.p1.hp:
                    self.who_wins.draw(self.enemy._name, 1)
                elif self.p1.hp == self.enemy.hp:
                    self.who_wins.draw("No-one", 0)
                self.reset()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            clock.tick(config['settings']['fps'])  # the program will never run at more than the set fps when this function's called
            pygame.display.flip()  # updates what is on screen

        self.s.close() # Close the socket connection to the server cleanly


class PvP:

    def __init__(self):
        self.client = Client()
        self.server = Server()



    def connecting(self):
        wait_screen = True

        while wait_screen == True:
            self.mouse = pygame.mouse.get_pos()  # receives the x and y co-ordinates of the mouse

            screen.fill(config['colours']['red'])
            screen.blit(main_font.render("Developed by Yousuf", True, config['colours']['black']), (20, 10))

            mode1 = pygame.Rect(100, 300, 200, 150) #draw the rects for the botton
            mode2 = pygame.Rect(500, 300, 200, 150)
            mode3 = pygame.Rect(100, 520, 100, 50)

            pygame.draw.rect(screen, config['colours']['steel'], mode1)  # draws the button and colour of them onto screen
            pygame.draw.rect(screen, config['colours']['steel'], mode2)
            pygame.draw.rect(screen, config['colours']['black'], mode3)

            if 300 > self.mouse[0] > 100 and 450 > self.mouse[1] > 300:  # If mouse's position or the mouse hovers over the buttons
                pygame.draw.rect(screen, config['colours']['purple'], mode1, 6)  # Therefore button outline changes colour
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:  # If user left click the mouse when mouse position equals to position of button
                    self.click = True
                    pygame.draw.rect(screen, config['colours']['purple'], mode1)
                    threading.Thread(target=self.server.initialise, args=()).start()  # Start the thread to listen for incoming data  from the client
                    #self.server.initialise()
                    #exec(open("ICServer.py").read())

            if 700 > self.mouse[0] > 500 and 450 > self.mouse[1] > 300:
                pygame.draw.rect(screen, config['colours']['purple'], mode2, 6)
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                    self.click = True
                    pygame.draw.rect(screen, config['colours']['purple'], mode2)
                    self.client.start_client()

            if 200 > self.mouse[0] > 100 and 570 > self.mouse[1] > 520:
                pygame.draw.rect(screen, config['colours']['purple'], mode3, 6)
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                    self.click = True
                    MenuScreen()  # head back to the menu
                    wait_screen = False

            # Renders the text on screen with screen.blit, choose the character
            screen.blit(pygame.font.SysFont('franklingothicmedium', 84).render("MULTIPLAYER", True, config['colours']['light_blue']),(145, 100))

            screen.blit(main_font.render("Start Server", True, config['colours']['black']), (150, 360))

            screen.blit(main_font.render("Join Game", True, config['colours']['black']), (550, 360))

            screen.blit(main_font.render("Back", True, config['colours']['white']), (110, 530))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            pygame.display.update()  # updates what is on screen
            clock.tick(config['settings']['fps'])  # the program will never run at more than the set fps when this function's called



class MenuScreen:

    def __init__(self):

        self._background = pygame.image.load('Assets/menubackground.png')  # uses png picture to screen main menu background
        self._logo = pygame.image.load('Assets/Game logo.png').convert_alpha()

        self.click = False  # to detect a user click
        self._game_modes = [LocalVersus(), BossMode(), PvP()]  # list of game modes classes
        self.mouse = pygame.mouse.get_pos()  # retrieves the x and y co-ordinates of the mouse
        self.fullscreen = config['settings']['fullscreen'] #the fullscreen option
        self.fps = config['settings']['fps'] #game FPS
        self.colours = [config['colours']['steel'],config['colours']['purple'],config['colours']['light_blue'],
                        config['colours']['black'],config['colours']['red']]

        pygame.mixer.music.load("Assets/Music/MenuMusic.wav")
        pygame.mixer.music.play(-1)

    def run_main_menu(self):
        self.menu_run = True  # boolean value

        while self.menu_run == True:
            self.mouse = pygame.mouse.get_pos()  # receives the x and y co-ordinates of the mouse


            screen.blit(self._background, (0, 0))
            screen.blit(self._logo, (100, 0))
            screen.blit(main_font.render("Developed by Yousuf", True, self.colours[4]), (20, 10))

            mode1 = pygame.Rect(300, 280, 200, 50)  # sets the size of each button and position on screen
            mode2 = pygame.Rect(300, 340, 200, 50)
            mode3 = pygame.Rect(300, 400, 200, 50)
            mode4 = pygame.Rect(300, 460, 200, 50)
            mode5 = pygame.Rect(300, 520, 200, 50)

            pygame.draw.rect(screen, self.colours[0], mode1)  # draws the button and colour of them onto screen
            pygame.draw.rect(screen, self.colours[0], mode2)
            pygame.draw.rect(screen, self.colours[0], mode3)
            pygame.draw.rect(screen, self.colours[0], mode4)
            pygame.draw.rect(screen, self.colours[0], mode5)

            if 500 > self.mouse[0] > 300 and 330 > self.mouse[1] > 280:  # If mouse's position hovers over the buttons
                pygame.draw.rect(screen, self.colours[1], mode1, 6)  # Therefore button outline changes colour
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:  # If user left click the mouse when mouse position equals to position of button
                    self.click = True
                    self._game_modes[0].run_stage_select()

            if 500 > self.mouse[0] > 300 and 390 > self.mouse[1] > 340:
                pygame.draw.rect(screen, self.colours[1], mode2, 6)
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                    self.click = True
                    self._game_modes[1].run_char_select()

            if 500 > self.mouse[0] > 300 and 450 > self.mouse[1] > 400:
                pygame.draw.rect(screen, self.colours[1], mode3, 6)
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                    self.click = True
                    self._game_modes[2].connecting()

            if 500 > self.mouse[0] > 300 and 510 > self.mouse[1] > 460:
                pygame.draw.rect(screen, self.colours[1], mode4, 6)
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                    self.click = True
                    self.run_option_menu()

            if 500 > self.mouse[0] > 300 and 570 > self.mouse[1] > 520:
                pygame.draw.rect(screen, self.colours[1], mode5, 6)
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                    self.click = True
                    break

            # Renders the text on screen with screen.blit
            screen.blit(main_font.render("Local Versus", True, self.colours[3]), (310, 300))

            screen.blit(main_font.render("Fight The Champion", True, self.colours[3]), (310, 360))

            screen.blit(main_font.render("Multiplayer", True, self.colours[3]), (310, 420))

            screen.blit(main_font.render("Options", True, self.colours[3]), (310, 480))

            screen.blit(main_font.render("Quit", True, self.colours[3]), (310, 540))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()  # updates what is on screen
            clock.tick(self.fps)  # the program will never run at more than the set fps when this function's called

    def run_option_menu(self):
        global screen
        self.option_run = True


        while self.option_run == True:
            self.mouse = pygame.mouse.get_pos()  # receives the x and y co-ordinates of the mouse

            screen.fill(self.colours[0])

            mode1 = pygame.Rect(50, 80, 200, 100)
            mode2 = pygame.Rect(50, 200, 200, 100)
            mode3 = pygame.Rect(50, 320, 200, 100)
            mode4 = pygame.Rect(50, 440, 200, 100)

            pygame.draw.rect(screen, self.colours[2], mode1)  # draws the button and colour of them onto screen
            pygame.draw.rect(screen, self.colours[2], mode2)
            pygame.draw.rect(screen, self.colours[2], mode3)
            pygame.draw.rect(screen, self.colours[3], mode4)

            if 250 > self.mouse[0] > 50 and 180 > self.mouse[1] > 80:  # If mouse's position or the mouse hovers over the buttons
                pygame.draw.rect(screen, self.colours[1], mode1, 6)  # Therefore button outline changes colour
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:  # If user left click the mouse when mouse position equals to position of button
                    self.click = True
                    self.controls_screen()

            if 250 > self.mouse[0] > 50 and 300 > self.mouse[1] > 200:
                pygame.draw.rect(screen, self.colours[1], mode2, 6)
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                    self.click = True
                    if self.fullscreen == False:
                        screen = pygame.display.set_mode((config['settings']['screen_width'], config['settings']['screen_height']),pygame.FULLSCREEN)  # the screen size
                        self.fullscreen = True
                    elif self.fullscreen == True:
                        screen = pygame.display.set_mode((config['settings']['screen_width'], config['settings']['screen_height'])) # the screen size
                        self.fullscreen = False


            if 250 > self.mouse[0] > 50 and 420 > self.mouse[1] > 320:
                pygame.draw.rect(screen, self.colours[1], mode3, 6)
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                    self.click = True
                    if config['settings']['time_amount'] == 30: #change the writing based on the setting change
                        config['settings']['time_amount'] = 60
                        time.sleep(0.35) #small delay for the transition
                    elif config['settings']['time_amount'] == 60:
                        config['settings']['time_amount'] = 999
                        time.sleep(0.35)
                    elif config['settings']['time_amount'] == 999:
                        config['settings']['time_amount'] = 30
                        time.sleep(0.35)

            if 250 > self.mouse[0] > 50 and 540 > self.mouse[1] > 440:
                pygame.draw.rect(screen, self.colours[1], mode4, 6)
                if pygame.mouse.get_pressed(num_buttons=3)[0] == 1:
                    self.click = True
                    self.run_main_menu()
                    self.option_run = False

            screen.blit(pygame.font.SysFont('arial', 120).render("OPTIONS", True, self.colours[4]), (290, 220))

            screen.blit(main_font.render("View Controls", True, self.colours[3]), (60, 120))

            if self.fullscreen == False: #If it isn't on fullscreen, blit this
                screen.blit(main_font.render("Full Screen : OFF", True, self.colours[3]), (60, 240))
            elif self.fullscreen == True: #else if it is on fullscreen, blit thisw
                screen.blit(main_font.render("Full Screen : ON", True, self.colours[3]), (60, 240))

            if config['settings']['time_amount'] == 30:
                screen.blit(main_font.render("Round Timer = 30", True, self.colours[3]), (60, 360))
            elif config['settings']['time_amount'] == 60:
                screen.blit(main_font.render("Round Timer = 60", True, self.colours[3]), (60, 360))
            elif config['settings']['time_amount'] == 999:
                screen.blit(main_font.render("Round Timer = 999", True, self.colours[3]), (60, 360))

            screen.blit(main_font.render("Back", True, config['colours']['white']), (60, 480))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()  # updates what is on screen
            clock.tick(self.fps)  # the program will never run at more than the set fps when this function's called

    def multiblit(self, text, style, colour, x, y):
        h = style.get_height()  # height of the font
        lines = text.split('\n')  # split the text up
        for i, ll in enumerate(lines):  # render each line with the inclusion the newline
            txt_surface = style.render(ll, True, colour)  # render the text
            screen.blit(txt_surface, (x, y + (i * h)))  # blitted onto the screen

    def controls_screen(self):
        self.c_screen = True

        while self.c_screen == True:
            screen.fill(self.colours[4])
            self.text = """<CONTROLS>                               **PRESS ANY KEY TO RETURN**
                              \nPLAYER1 | PLAYER2:
                              \nW | UP: Jump\nA | LEFT: Move left\nS | DOWN: Crouch\nD | RIGHT: Move Right
                              \nR | NUMPAD7: Punch\nF | NUMPAD4: Kick\nB | NUMPAD3: Block\nH | NUMPAD6: Throw
                              \nS + B | DOWN + NUMPAD3: Low Block\nS + R | DOWN + NUMPAD7: Low Punch\nS + F | DOWN + NUMPAD4: Low Kick
                              \nT | NUMPAD8: Punches \nG | NUMPAD5: Kicks\nS + H | DOWN + NUMPAD6: Uppercut
                              \n1 | 8: Special 1\n2 | 9: Special 2\n3 | 0: Special 3"""

            self.multiblit(self.text, main_font, config['colours']['white'], 10, 10)  # blit the lines of text

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:  # press any key to return to the option menu
                    self.c_screen = False
                    self.run_option_menu()

            clock.tick(self.fps)  # the program will never run at more than the set fps when this function's called
            pygame.display.update()  # updates what is on screen


if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    m = MenuScreen()
    m.run_main_menu()
