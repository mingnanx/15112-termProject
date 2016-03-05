#CS112  Term Project 
#Mingnan Xu + Section G + mingnanx

from tkinter import *
import random
import copy

############################## References and Citation ########################

###############################################################################
# Animation FrameWork from Carnegie Mellon University 15-112
# from Event Based Animation part 3 event-example0.py
# URL: http://www.cs.cmu.edu/~112/notes/notes-animations.html
# Including init(data),mousePressed(event,data),keyPressed(event,data)
# timerFired(data), redrawAll(data) run() functions.
#
# SplashScreen Structure from Carnegie Mellon University 15-112
# from Event Based Animation part 3 Worked Examples 1 Mode Demo
# URL: http://www.cs.cmu.edu/~112/notes/notes-animations-examples.html#modeDemo
#
# Poker Images from Carnegie Mellon University 15-112
# from Event Based Animation part 3 Worked Examples 4 Image Demo
# http://www.cs.cmu.edu/~112/notes/notes-animations-examples.html#imagesDemo
# Including loadPlayingCardImages(data) function
###############################################################################


def playCasino():
    #Run this function for playing the casino game
    width,height = 800,600
    #top level function call the run function
    run(width,height)
    
class Poker(object):
    #Poker class represent all the cards
    def __init__(self,cardRank):
        suits = "cdhsx"
        numOfRank = 13
        self.cardRank = cardRank
        self.rank = (cardRank%numOfRank)+1
        self.suit = suits[cardRank//numOfRank]
        self.faceUp = False   #True to let the back face up
        self.x = 0
        self.y = 0

    def getPlayingCardImage(self,data):
        #return the corresponding card image
        return data.cardImages[self.cardRank]

    def drawPoker(self,data,canvas,position):
        #draw the poker
        if self.faceUp==False:  #when the back is down
            image = self.getPlayingCardImage(data)
            (left,top) = position
            canvas.create_image(left, top, anchor=NW, image=image)
        else: #when the back face up
            image = data.cardImages[52]
            (left,top) = position
            canvas.create_image(left, top, anchor=NW, image=image)
            

    def __eq__(self,other):
        #rewrite the equal
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        #rewrite the hash
        return hash(self.rank,sel.suit)


def createNewValidCardHelper(data):
#Method for creating a valid card (not already exist)
    card = Poker(random.randint(0,51))
    if card not in data.PlayerCards:
        data.PlayerCards.append(card)
        return card
    return Poker(53)

def createNewValidCard(data):
    #method used to create a new valid card
    created = []
    while(len(created)<1):
        card = createNewValidCardHelper(data)
        if card.suit!="x":
            created.append(card)
    return created[0]
        

class BlackJackDealer(object):
    #black jack dealer class
    def __init__(self):
        self.cards = []

    def initializeBJDealer(self,data):
        #initialize the black jack dealer
        #add one card if the total is less than 2
        if len(self.cards)<2:          
            card1 = createNewValidCard(data)
            (card1.x,card1.y)=(0,100)
            if len(self.cards)>0:
                card1.faceUp = True
            self.cards.append(card1)


    def drawDealer(self,canvas,data):
        #draw the dealer of blackjack
        if data.runDealer == True:
            canvas.create_text (550,65,text = str(self.getDealerSum()),
                                fill = "white",font = "bold 28")
        p = 60  #position factor
        for card in self.cards:
            position = (p+card.x,card.y)
            card.drawPoker(data,canvas,position)
            p += 80

    def getDealerSum(self):
        #return the sum of all cards according to dealer rule
        currSum = 0
        for card in self.cards:
            if card.rank==1:continue
            if card.rank in [11,12,13]:
                currSum += 10
            else:              
                currSum += card.rank
        for card in self.cards:
            if card.rank==1:
                if currSum >10:
                    currSum+=1
                else:
                    currSum+=11  #special case for A
        return currSum

    def runDealer(self,data):
        #when ready, function to run the dealer
        if(self.getDealerSum()<17):  #it will stop when reach 17
            newCard = createNewValidCard(data)
            newCard.y = 100
            self.cards.append(newCard)
        
        

def findSumOfA(currSum,numOfA):  #static function
    #helper function dealing with A
    for i in range(numOfA,-1,-1):
        if currSum+i*11+(numOfA-i)*1<22:
            return i*11+(numOfA-i)*1
    return numOfA*1
     

class BlackJackPlayer(object):
    #Black Jack Player class
    def __init__(self):
        self.cards = []

    def initializeBJPlayer(self,data):
        #initialize player if number of cards less than 2
        if len(self.cards)<2:
            card1 = createNewValidCard(data)
            (card1.x,card1.y)=(0,400)
            self.cards.append(card1)

    def drawPlayer(self,canvas,data):
        #draw the card of player
        canvas.create_text (550,355,text = str(self.getPlayerSum()),
                                fill = "white",font = "bold 28")
        p = 60  #position factor
        for card in self.cards:
            position = (p+card.x,card.y)
            card.drawPoker(data,canvas,position)
            p += 80

    def getPlayerSum(self):
        #Find the total sum, need some helper function to find the 21
        currSum = 0
        for card in self.cards:
            if card.rank==1:continue
            if card.rank in [11,12,13]:
                currSum += 10
            else:              
                currSum += card.rank
        numOfA = 0
        for card in self.cards:
            if card.rank==1:
                numOfA+=1
        Asum = findSumOfA(currSum,numOfA) #Special case of A
        return currSum+Asum

    def addCard(self,data):
        #method when player to call for another card
        if self.getPlayerSum()<21 and len(self.cards)>=2:
            card1 = createNewValidCard(data)
            (card1.x,card1.y) = (0,400)
            self.cards.append(card1)
            
        

class Chip(object):
    #Chip class representing the chip to use
    def __init__(self):
        self.x = 400
        self.y = 300
        self.v = random.randint(40,60)  #velocity of chip to move

    def draw(self,canvas):
        #draw the chip
        outerSize = 25
        innerSize = 20
        canvas.create_oval(self.x-outerSize,self.y-outerSize,
                           self.x+outerSize,self.y+outerSize,width=4,
                           outline = "white", dash = (5,10),
                           fill = "red")
        canvas.create_oval(self.x-innerSize,self.y-innerSize,
                           self.x+innerSize,self.y+innerSize,
                           fill = "red", outline = "white", width = 3)
        canvas.create_text(self.x,self.y,text = "10", fill = "white",
                           font = "bold 15")
        
    def moveUp(self):
        #method for moving up
        self.y -= self.v

    def moveDown(self):
        #method for moving down
        self.y += self.v

    def moveRight(self):
        #method for moving right
        self.x += self.v


class ChipOfTen(Chip):
    #Class ChipOfTen inheritate Chip class
    def __init__(self):
        super().__init__()
        self.value = 10


class ChipOfFifty(Chip):
    #Class ChipOfFifty inheritate Chip class
    def __init__(self):
        super().__init__()
        self.value = 50

    def draw(self,canvas):
        #rewrite the draw method
        outerSize = 25
        innerSize = 20
        canvas.create_oval(self.x-outerSize,self.y-outerSize,
                           self.x+outerSize,self.y+outerSize,width=4,
                           outline = "white", dash = (5,10),
                           fill = "blue")
        canvas.create_oval(self.x-innerSize,self.y-innerSize,
                           self.x+innerSize,self.y+innerSize,
                           fill = "blue", outline = "white", width = 3)
        canvas.create_text(self.x,self.y,text = "50", fill = "white",
                           font = "bold 15")

class ChipOfHundred(Chip):
    #Class ChipOfHundred inheritate Chip class
    def __init__(self):
        super().__init__()
        self.value = 100

    def draw(self,canvas):
        #rewrite the draw method
        outerSize = 25
        innerSize = 20
        canvas.create_oval(self.x-outerSize,self.y-outerSize,
                           self.x+outerSize,self.y+outerSize,width=4,
                           outline = "white", dash = (5,10),
                           fill = "black")
        canvas.create_oval(self.x-innerSize,self.y-innerSize,
                           self.x+innerSize,self.y+innerSize,
                           fill = "black", outline = "white", width = 3)
        canvas.create_text(self.x,self.y,text = "100", fill = "white",
                           font = "bold 15")

        
        

class FlyImage(object):
    #FlyImage class for splash screen
    def __init__(self,image,direction):
        self.image = image
        self.v = 20
        self.name = None
        self.direction = direction
        if self.direction==1:
            self.y = 0
            self.x = random.randint(100,700)
        elif self.direction == 2:
            self.y = 600
            self.x = random.randint(100,700)
        
        elif self.direction==3:
            self.x = 0
            self.y = random.randint(100,500)
        elif self.direction==4:
            self.x = 800
            self.y = random.randint(100,500)

    def move(self):
        #move randomly
        v = self.v
        if self.direction==1:
            self.y+=v
        elif self.direction==2:
            self.y-=v
        elif self.direction==3:
            self.x+=v
        elif self.direction==4:
            self.x-=v

    def draw(self,canvas):
        #draw the image
        image = self.image
        left,top = self.x,self.y
        canvas.create_image(left, top, anchor=NW, image=image)
        
            
    def isClickedOn(self,x,y):
        #see if it is click on the photo
        return abs(x-self.x)<150 and abs(y-self.y)<100

    def isClickedOn2(self,x,y):
        #see if it is click on the photo
        return abs(x-self.x)<70 and abs(y-self.y)<70

    def toMoney(self,data):
        #change the icon to a money when pressed
        self.v = 80
        add = random.choice([10,20,30])
        data.playerBank += add
        if add==10:
            self.image = PhotoImage(file = "ALLGIF/Dollar.gif")
        if add == 20:
            self.image = PhotoImage(file = "ALLGIF/Money.gif")
        if add == 30:
            self.image = PhotoImage(file = "ALLGIF/Money2.gif")
        
       
        
def initFlyImage(data):
    #initialize the fly image
    image1 = PhotoImage(file = "ALLGIF/mc.gif")
    image2 = PhotoImage(file = "ALLGIF/lv.gif")
    i1 = FlyImage(image1,3)
    i1.name = "mc"
    i2 = FlyImage(image2,2)
    i2.name = "lv"
    data.flyImage += [i1,i2]

def updateFlyImage(data):
    #update the flying image
    for i in data.flyImage:
        if i.x<0 or i.x>800 or i.y<0 or i.y>600:
            data.flyImage.remove(i)
    if len(data.flyImage)>=6:
        return
    newFile = random.choice(["mc.gif","lv.gif"])
    if newFile=="mc.gif":
        newImage = PhotoImage(file = "ALLGIF/"+newFile)
        newI = FlyImage(newImage,random.choice([1,2,3,4]))
        newI.name = "mc"
        data.flyImage.append(newI)
    elif newFile=="lv.gif": 
        newImage = PhotoImage(file = "ALLGIF/"+newFile)
        newI = FlyImage(newImage,random.choice([1,2,3,4]))
        newI.name = "lv"
        data.flyImage.append(newI)


def updateRandomImage(data):
    #updating the random image
    for i in data.randomImage:
        if i.x<0 or i.x>800 or i.y<0 or i.y>600:
            data.randomImage.remove(i)
    newFile = random.choice(["Zc.gif","Za.gif","Zb.gif","Ze.gif","Zf.gif"])
    newImage = PhotoImage(file = "ALLGIF/"+newFile)
    newI = FlyImage(newImage,random.choice([1,2,3,4]))
    data.randomImage.append(newI)
    

####################################
# Animation FrameWork from Carnegie Mellon University 15-112
# from Event Based Animation part 3 event-example0.py
# URL: http://www.cs.cmu.edu/~112/notes/notes-animations.html
# Including init(data),mousePressed(event,data),keyPressed(event,data)
# timerFired(data), redrawAll(data) functions.

# SplashScreen Structure from Carnegie Mellon University 15-112
# from Event Based Animation part 3 Worked Examples 1 Mode Demo
# URL: http://www.cs.cmu.edu/~112/notes/notes-animations-examples.html#modeDemo
#################################### 
def init(data):
    #function from Animation Framework from Carnegie Mellon University 15-112
    #from Event Based Animation part 3 event-example0.py
    #URL: http://www.cs.cmu.edu/~112/notes/events-example0.py
    data.i1 = PhotoImage(file = "ALLGIF/Za.gif")
    data.i2 = PhotoImage(file = "ALLGIF/Zb.gif")
    data.i3 = PhotoImage(file = "ALLGIF/Zc.gif")
    data.i4 = PhotoImage(file = "ALLGIF/lv.gif")
    data.i5 = PhotoImage(file = "ALLGIF/mc.gif")
    data.i6 = PhotoImage(file = "ALLGIF/Sn.gif")
    data.i7 = PhotoImage(file = "ALLGIF/Ze.gif")
    data.i8 = PhotoImage(file = "ALLGIF/Zf.gif")
    data.gamei1 = PhotoImage(file = "ALLGIF/game1.gif")
    data.gamei2 = PhotoImage(file = "ALLGIF/game2.gif")
    data.instructionI = PhotoImage(file = "ALLGIF/Instructions.gif")
    data.mode = "SplashScreen"
    data.timerDelay = 150  #timer delay
    data.backgroundImage = PhotoImage(file="ALLGIF/Casino-1.gif")
    data.back = "lv"
    data.flyImage = []
    data.randomImage = []
    data.counter = 0
    data.TXInstruction = True
    data.BJInstruction = True
    loadPlayingCardImages(data) #initialize poker image
    initFlyImage(data)
    data.playerBank = 3000  #starting money
    data.AIDifficulty = "Hard"
    data.TXDealer = "AI"
    initSnake(data)  #initialize snake
    initBJ(data)  #initialize blackjack
    initTX(data)  #initialize texas poker


#URL of all background images used for this project:  #############
#https://www.google.com/search?q=casino+images&espv=2&biw=830&bih=928&source
#http://godaddycasino.com/images/Casino-Games-Background-680x510%5B1%5D.jpg
#http://us.cdn4.123rf.com/168nwm/vireakchand/9429506-red-poker-background.jpg
#http://godaddycasino.com/green-wallpapers-backgrounds-for-powerpoint.jpg



    
def loadPlayingCardImages(data):
# Poker Images from Carnegie Mellon University 15-112
# from Event Based Animation part 3 Worked Examples 4 Image Demo
# http://www.cs.cmu.edu/~112/notes/notes-animations-examples.html#imagesDemo
  
#Pre-Load all card image from default file
    cards = 55 # cards 1-52, back, joker1, joker2
    data.cardImages = [ ]
    for card in range(cards):
        rank = (card%13)+1
        suit = "cdhsx"[card//13]
        filename = "playing-card-gifs/%s%d.gif" % (suit, rank)
        data.cardImages.append(PhotoImage(file=filename))

def mousePressed(event, data):
    #function from Animation Framework from Carnegie Mellon University 15-112
    #from Event Based Animation part 3 event-example0.py
    #URL: http://www.cs.cmu.edu/~112/notes/events-example0.py
#mouse control
    if data.mode =="SplashScreen":
        splashScreenMousePressed(event,data)
    if data.mode =="Snake":
        snakeMousePressed(event,data)
    if data.mode =="BJ":
        blackJackMousePressed(event, data)
    if data.mode=="TX":
        TXMousePressed(event,data)
    if data.mode=="Instruction":
        InstructionMousePressed(event,data)
        

def keyPressed(event, data):
    #function from Animation Framework from Carnegie Mellon University 15-112
    #from Event Based Animation part 3 event-example0.py
    #URL: http://www.cs.cmu.edu/~112/notes/events-example0.py

    #Key Operations
    if data.mode == "SplashScreen":
        splashScreenKeyPressed(event,data)
    if data.mode =="Snake":
        snakeKeyPressed(event,data)
    if data.mode=="BJ":
        blackJackKeyPressed(event, data)
    if data.mode=="TX":
        TXKeyPressed(event,data)
    if data.mode=="Instruction":
        InstructionKeyPressed(event,data)

def timerFired(data):

    #function from Animation Framework from Carnegie Mellon University 15-112
    #from Event Based Animation part 3 event-example0.py
    #URL: http://www.cs.cmu.edu/~112/notes/events-example0.py

    if data.mode == "SplashScreen":
        splashScreenTimerFired(data)
    #time control
    if data.mode =="Snake":
        snakeTimerFired(data)
    if data.mode=="BJ":
        blackJackTimerFired(data)
    if data.mode=="TX":
        TXTimerFired(data)
    if data.mode=="Instruction":
        InstructionTimerFired(data)
    
def redrawAll(canvas, data):
    #function from Animation Framework from Carnegie Mellon University 15-112
    #from Event Based Animation part 3 event-example0.py
    #URL: http://www.cs.cmu.edu/~112/notes/events-example0.py

#redraw based on the mode
    if data.mode == "SplashScreen":splashScreenRedrawAll(canvas,data)
    if data.mode == "BJ":blackJackRedrawAll(canvas, data)
    if data.mode == "Snake":snakeRedrawAll(canvas,data)
    if data.mode=="TX":TXRedrawAll(canvas,data)
    if data.mode=="Instruction":InstructionRedrawAll(canvas,data)

def rgbString(red, green, blue):
    #rgbString function from Carnegie Mellon University
    # 15-112 lecture notes week 7
    #URL: http://www.cs.cmu.edu/~112/notes/notes-graphics.html
    return "#%02x%02x%02x" % (red, green, blue)

#####################################################
### Instruction####
def InstructionMousePressed(event,data):
    if 360<event.x<400 and 250<event.y<300:
        data.mode = "Snake"
        data.timerDelay = 500

def InstructionKeyPressed(event,data):
    if event.keysym=="Escape":
        data.mode = "SplashScreen"

def InstructionTimerFired(data):
    pass

def InstructionRedrawAll(canvas,data):
    color = rgbString(50,60,210)
    canvas.create_rectangle(-5,-5,805,605,fill=color)
    canvas.create_text(400,50,text="INSTRUCTION",
                       fill = "White",font = "Aharoni 40 bold")
    
    canvas.create_text(50,100,anchor = NW,text = """
->To EARN MONEY:
            Click on the little icons on welcome screen
            Icons for earn money:






            or earn by play the snake game here:
""" ,fill = rgbString(193,255,193),font = "Tekton 12")

    
    canvas.create_text(50,300,anchor = NW, text = """
->To CHANGE THEME OF BACKGROUND:
    click on the Las Vegas or Monte Carlo icons on welcome screen
""",fill = rgbString(193,255,193), font = "Tekton 12")

    canvas.create_text(50,400,anchor = NW, text = "Las Vegas:",
                       fill = rgbString(193,255,193),font = "Tekton 12")

    canvas.create_text(300,400,anchor = NW, text = "Monte Carlo:",
                       fill = rgbString(193,255,193), font = "Tekton 12")

    canvas.create_text(50,500,anchor = NW, text =
                "Back to splashscreen from any game, press ESC",
                       fill = rgbString(193,255,193), font = "Tekton 12")
    
    canvas.create_image(140,170,anchor = NW, image = data.i1)
    canvas.create_image(250,170,anchor = NW, image = data.i2)
    canvas.create_image(360,170,anchor = NW, image = data.i3)
    canvas.create_image(470,170,anchor = NW, image = data.i7)
    canvas.create_image(140,370,anchor = NW, image = data.i4)
    canvas.create_image(400,370,anchor = NW, image = data.i5)
    canvas.create_image(360,250,anchor = NW, image = data.i6)
    canvas.create_image(580,170,anchor = NW, image = data.i8)

    canvas.create_text(50,500,anchor = NW, text = """
->To BEGIN GAME: click on the game pictures or press the corresponding number
    The maximum amount of bet allowed for BlackJack game is $300,
    The maximum amount of bet allowed for Texas Poker at each round is $300
""", fill = rgbString(193,255,193), font = "Tekton 12")
#####################################################        
### Splash Screen ###
def splashScreenMousePressed(event,data):
    #splashscreen mouse pressed
    for i in data.randomImage:
        if i.isClickedOn2(event.x,event.y):
            i.toMoney(data)
            return
    if 30<event.x<250 and 420<event.y<580:
        data.mode = "TX"
        initTX(data)
        data.timerDelay = 80
        return
    if 550<event.x<780 and 420<event.y<580:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
        data.mode = "BJ"
        initBJ(data)
        data.timerDelay = 80
        return
    elif 340<event.x<460 and 530<event.y<550:
        data.mode = "Instruction"
        return
    #splash screen mouse mode
    for i in data.flyImage:
        if i.isClickedOn(event.x,event.y):
            if i.name=="mc":
                data.back = "mc"
            elif i.name=="lv":
                data.back = "lv"
            return


def splashScreenKeyPressed(event,data):
    #splash screen key operation
    if (event.keysym=="1"):
        data.mode = "TX"
        data.timerDelay = 80
        initTX(data)
    if (event.keysym=="2"):
        data.mode = "BJ"
        initBJ(data)
        data.timerDelay = 80
    if (event.keysym=="3"):
        data.mode = "Instruction"
    if (event.keysym=="Escape"):data.mode = "SplashScreen"

def splashScreenTimerFired(data):
    #splash screen timer fired
    data.counter = data.counter+1 if data.counter<50 else 0
    if data.counter==25:
        updateFlyImage(data)
    if data.counter %14==0:
        updateRandomImage(data)
    for i in data.flyImage:
        i.move()
    for i in data.randomImage:
        i.move()

def splashScreenRedrawAll(canvas,data):
    #splash screen redraw all
    color = selectColor(data)
    canvas.create_image(0, 0,anchor=NW, image=data.backgroundImage)
    canvas.create_image(30,420,anchor = NW, image = data.gamei1)
    canvas.create_text(30,400,text = "1.TEXAS POKER", fill = color,
                       anchor = NW,font = "Aharoni 14 bold")
    canvas.create_text(645,400,text = "2.BLACK JACK", fill = color,
                       anchor = NW,font = "Aharoni 14 bold")
    canvas.create_image(550,420,anchor = NW, image = data.gamei2)
    canvas.create_image(data.width/2,540,image = data.instructionI)
    for i in data.flyImage:
        i.draw(canvas)
    for i in data.randomImage:
        i.draw(canvas)
    color2 = selectColor2(data)
    canvas.create_text(data.width/2,15
                       ,text = "Player Bank $: "+str(data.playerBank)
                       ,fill="cyan",
                       font = "tahoma 14 bold")
    canvas.create_text(data.width/2+2,320,text="""
         WELCOME
MINGNAN's CASINO""",fill=color2,
                       font = "Aharoni 26 bold")

    

def selectColor(data):
    #select color for the text
    if data.counter%8==0:
        return "white"
    elif data.counter%8==1:
        return "pink"
    elif data.counter%8==2:
        return "grey"
    elif data.counter%8==3:
        return "yellow"
    elif data.counter%8==4:
        return "orange"
    elif data.counter%8==5:
        return "purple"
    elif data.counter%8==6:
        return "cyan"
    elif data.counter%8==7:
        return "green"
    
def selectColor2(data):
    red = random.randint(0,255)
    blue = random.randint(0,255)
    green = random.randint(0,255)
    return rgbString(red,green,blue)
    

    
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@### BLACK JACK  #######
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@### BLACK JACK  #######


def initBJ(data):
    #blackjack initialization
    data.step = 0
    data.addChip = True
    data.initialize = False
    data.runDealer = False
    data.countMoney = True
    data.counter = 0
    data.PlayerCards = []
    data.BJDealer = BlackJackDealer()
    data.BJPlayer = BlackJackPlayer()
    if data.back =="lv":
        data.BJbackground = PhotoImage(file="ALLGIF/B-J.gif")
    elif data.back=="mc":
        data.BJbackground = PhotoImage(file="ALLGIF/MCBBJ.gif")
    data.BJgameover = False
    data.winner = None
    data.chips = []
    data.input = 0
    data.drawTip = False
    data.drawBJRule = False
    data.drawOverMax = False
    data.noMoney = False
    data.drawNoMoney = False


def doubleChips(data):
    #method for double chips
    exist = copy.deepcopy(data.chips)
    for c in exist:
        data.chips.append(c)

def tripleChips(data):
    exist = copy.deepcopy(data.chips)
    for c in exist:
        data.chips.append(c)
        data.chips.append(c)

def getBJChipsSum(data):
    total = 0
    for c in data.chips:
        total += c.value
    return total
    
def blackJackMousePressed(event, data):
    if data.drawBJRule:
        data.drawBJRule = False
        return 
    if 330<event.x<570 and 280<event.y<330 and data.BJInstruction:
        data.drawBJRule = True
        return

    if data.BJInstruction:
        return
    if 60<event.x<140 and 500<event.y<530:
        data.BJInstruction = True
    #click on start
    if 50<event.x<100 and 450<event.y<500 and len(data.chips)==0:
        data.drawTip = True
        
    if 50<event.x<100 and 450<event.y<500 and len(data.chips)>0:
        data.initialize = True
        data.addChip = False
        data.drawOverMax = False

    if 100<event.x<150 and 450<event.y<500 and data.BJgameover:
        initBJ(data)
        
    #click on adding chips
    if data.addChip:       
        if getBJChipsSum(data)>=300:
            data.drawOverMax = True
            return
        
        if (50<event.x<100 and 100<event.y<150
            and getBJChipsSum(data)+10<=300) :
            if data.playerBank<=0:
                data.drawNoMoney = True
                return
            data.drawTip = False
            data.chips.append(ChipOfTen())
            data.input+=10
            data.playerBank-=10
        if (50<event.x<100 and 150<event.y<200
            and getBJChipsSum(data)+50<=300):
            if data.playerBank<=0:
                data.drawNoMoney = True
                return
            data.chips.append(ChipOfFifty())
            data.input+=50
            data.playerBank-=50
            data.drawTip = False
        if (50<event.x<100 and 200<event.y<250
            and getBJChipsSum(data)+100<=300):
            if data.playerBank<=0:
                data.drawNoMoney = True
                return
            data.drawTip = False
            data.chips.append(ChipOfHundred())
            data.input+=100
            data.playerBank-=100

    #click on stand for run dealer
    if 50<event.x<120 and 300<event.y<350 and len(data.BJDealer.cards)==2:
        #when ready to go for game
        data.runDealer = True
        data.BJDealer.cards[1].faceUp=False

    #click on add by player
    if 50<event.x<120 and 350<event.y<400:
        #add new card by player
        data.BJPlayer.addCard(data)
        if data.BJPlayer.getPlayerSum()>21:
            data.BJgameover = True
            data.winner = "DEALER"
            data.counter = 20

    #click on double by player
    if (50<event.x<120 and 400<event.y<450
        and len(data.BJDealer.cards)==2 and len(data.BJPlayer.cards)==2):
        if data.BJPlayer.getPlayerSum==21:
            return
        doubleChips(data)
        data.BJPlayer.addCard(data)
        if data.BJPlayer.getPlayerSum()>21:
            data.BJgameover = True
            data.winner = "DEALER"
        data.BJDealer.cards[1].faceUp = False
        if data.BJPlayer.getPlayerSum()>21:
            return
        data.runDealer = True

def blackJackKeyPressed(event, data):
    #keypressed for blackjack (just for debugging)
    if event.keysym=="Escape":
        data.mode = "SplashScreen"
        data.timerDelay = 150
    if data.BJInstruction and event.keysym=="space":
        data.BJInstruction = False
    if event.keysym=="r":initBJ(data)
    if data.BJgameover: pass
    if event.keysym=="a" and len(data.BJDealer.cards)==2:
        data.runDealer = True
        data.BJDealer.cards[1].faceUp=False
    if event.keysym=="q":
        data.BJPlayer.addCard(data)
        if data.BJPlayer.getPlayerSum()>21:
            data.BJgameover = True
            data.winner = "DEALER"
    if event.keysym=="d" and len(data.BJDealer.cards)==2 and len(data.BJPlayer.cards)==2:
        data.BJPlayer.addCard(data)
        if data.BJPlayer.getPlayerSum()>21:
            data.BJgameover = True
            data.winner = "DEALER"
        data.BJDealer.cards[1].faceUp = False
        data.runDealer = True
    if event.keysym=="p":
        print(data.drawNoMoney)


def blackJackTimerFired(data):
    #case when gameover
    if data.BJgameover==True and data.counter>18:
        for c in data.chips:
            if data.winner=="DEALER":
                c.moveUp()
                if data.countMoney:
                    data.countMoney=False
            elif data.winner=="PLAYER":
                c.moveDown()
                if data.countMoney:  #add money for player
                    data.playerBank+=2*data.input;data.countMoney=False
            else:
                c.moveRight()
                if data.countMoney:
                    data.playerBank+=data.input  #tie game
                    data.countMoney=False
            #remove it when outof screen
            if c.y>600 or c.y<0:
                data.chips.remove(c)
            elif c.x>800:
                data.chips.remove(c)

    #case to initialize the game
    if data.initialize==True:
        data.counter = data.counter+1 if data.counter<16 else 0
        if data.counter==2:
            data.BJDealer.initializeBJDealer(data)
        if data.counter==9:
            #to control the time interval
            data.BJPlayer.initializeBJPlayer(data)
        if len(data.BJPlayer.cards)==2:
            if data.BJPlayer.getPlayerSum()==21:
                tripleChips(data)
                data.BJgameover=True
                data.BJDealer.cards[1].faceUp = False
                if data.BJDealer.getDealerSum()==21:
                    data.winner = "TIE"
                else:
                    data.winner = "PLAYER"
            data.initialize=False
            
    #move the card to desired position
    for card in data.BJDealer.cards:
        if card.x<200:
            card.x+=100
    for card in data.BJPlayer.cards:
        if card.x<200:card.x+=100

    if data.BJgameover:
        data.counter+=1
    
    #case when dealer is running
    if data.runDealer==True:
        data.counter +=1
        if data.BJgameover:return
        if data.counter%8==0:
            data.BJDealer.runDealer(data)
        if data.BJDealer.getDealerSum()>=17:
            data.BJgameover = True
            dscore = data.BJDealer.getDealerSum()
            pscore = data.BJPlayer.getPlayerSum()
            if dscore>21 or (dscore<pscore and pscore<=21):
                data.winner = "PLAYER"
                doubleChipsandRelocate(data)
            elif (pscore<dscore and dscore<=21) or pscore>21:
                data.winner = "DEALER"
            else:
                data.winner = "TIE"
        
def doubleChipsandRelocate(data):
    #double the chips and relocate it
    data.newChip = copy.deepcopy(data.chips)
    start = 250
    for i in range(len(data.chips)):
        data.newChip[i].x = start+i*50
        data.newChip[i].y = 250
    data.chips+=data.newChip


            
def relocateChips(data):
    #method to relocate chip for drawing
    start = 230
    for i in range(len(data.chips)):
        data.chips[i].x = start+i*18
    

def blackJackRedrawAll(canvas, data):
    if data.BJInstruction:
        drawBJInstruction(canvas,data)
        return
    #RedrawAll method in blackjack mode
    canvas.create_image(0, 0,anchor=NW, image=data.BJbackground)
    #draw the player score
    color = "white" if data.back == "lv" else "yellow"
    #draw the money
    canvas.create_text(data.width/2,15
                       ,text = "Player Bank $: "+str(data.playerBank)
                       ,fill=color,
                       font = "tahoma 14 bold")


    drawBJButton(canvas,data)  #draw all buttons
    canvas.create_text(100,50,text="Black Jack",fill = color,
                       font = "Aharoni 26 bold")
    canvas.create_text(600,300,text="BET: " + str(data.input),fill = color,
                       font = "Aharoni 25 bold")
    if data.drawNoMoney:
        canvas.create_text(400,300,text = "No Enough Money!!",
                           fill = color,font = "bold 26")
        return
    data.BJDealer.drawDealer(canvas,data)
    data.BJPlayer.drawPlayer(canvas,data)
    
    if len(data.chips)>0 and data.winner!="TIE":
        relocateChips(data)
    if len(data.BJDealer.cards)==0:
        canvas.create_text(400,550,text = "Click on START to begin",
                           fill = color, font = "Aharoni 20 bold")
    elif len(data.BJPlayer.cards)==2 and not data.BJgameover:
        canvas.create_text(400,550,text = """
Click on HIT for another card, on STAND when ready, or DOUBLE to double chips
""",fill = color, font = "Aharoni 14 bold")
    elif len(data.BJPlayer.cards)>2 and not data.BJgameover:
        canvas.create_text(400,550,text = """
Click on HIT for another card, on STAND when ready
""",fill = color, font = "Aharoni 18 bold")
    elif data.BJgameover:
        canvas.create_text(400,550,text = "Click on REMATCH for new game",
                           fill = color, font = "Aharoni 18 bold")
    for c in data.chips:
        c.draw(canvas)  #draw all the chips
    if data.drawTip == True:
        canvas.create_text(data.width/2-20,data.height/2
                           ,text="Please Bet Before Start"
                           , fill="yellow", font = "bold 20")
    if data.BJgameover == True:
        if data.winner=="TIE":
            canvas.create_text(data.width/2,data.height/2,
                               text = "TIE GAME",
                               fill = selectColor2(data),font="Aharoni 20 bold")
            return
        canvas.create_text(data.width/2,data.height/2
                           ,text = "%s WIN!!!" %(data.winner)
                           ,fill = selectColor2(data)
                           ,font = "Aharoni 30 bold")
    if data.drawOverMax:
        canvas.create_text(450,250,text = "Over Max Amount, Click START",
                           font = "bold 16",fill = color)

def drawBJButton(canvas,data):
    #draw all the button for blackjack
    c1 = rgbString(192,255,62)  
    c2 = rgbString(84,139,84)
    c3 = rgbString(205,102,0)
    canvas.create_rectangle(50,450,100,500,fill = c1,width=0)
    canvas.create_text(75,475,text = "START",font = "Aharoni 12 bold",
                       fill = c2)
    canvas.create_rectangle(60,500,140,530,fill = "orange",width=0)
    canvas.create_text(100,515,text = "INSTRUCTION",
    font = "Aharoni 8 bold",
                       fill = c3)
    if data.BJgameover:
        c1 = selectColor2(data)
    canvas.create_rectangle(101,450,160,500,fill=c1,width=0)
    canvas.create_text(132,475,text=
"""
 RE
MATCH
""",font = "Aharoni 10 bold",
                       fill = c2)
    
    canvas.create_rectangle(50,100,100,150,fill="red",width=0)
    canvas.create_text(75,125,text = "+10",font = "Aharoni 14 bold",
                       fill = "black")
    canvas.create_rectangle(50,150,100,200,fill="blue",width=0)
    canvas.create_text(75,175,text = "+50",font = "Aharoni 14 bold",
                       fill = "yellow")
    canvas.create_rectangle(50,200,100,250,fill="black",width=0)
    canvas.create_text(75,225,text = "+100",font = "Aharoni 14 bold",
                       fill = "white")

    canvas.create_rectangle(50,300,120,350,fill=rgbString(238,174,239),width=0)
    canvas.create_text(85,325,text="STAND",font = "Aharoni 14 bold",
                       fill = "purple")
    canvas.create_rectangle(50,350,120,400,fill="white",width=0)
    canvas.create_text(85,375,text="HIT",font = "Aharoni 14 bold",
                       fill = "red")

    canvas.create_rectangle(50,400,120,450,fill=rgbString(72,209,204),width=0)
    canvas.create_text(85,425,text="DOUBLE",font = "Aharoni 13 bold",
                       fill = rgbString(0,134,139))
    
def drawBJInstruction(canvas,data):
    canvas.create_rectangle(-5,-5,805,605,fill = rgbString(135,206,250))
    canvas.create_text(400,50,text = "Black Jack Instruction",
                       fill = "purple", font = "bold 28")

    if data.drawBJRule:
        canvas.create_rectangle(100,100,700,500,fill = "pink")
        canvas.create_text(data.width/2,data.height/2,text="""
- The goal of blackjack is to beat the dealer's hand without going over 21
- Face cards are worth 10, Ace worth 1 or 11, which ever makes better hand
- Each player starts with 2 cards, one of dealer's cards is hidden
- To HIT, is to add another card
- To STAND is ready for battle
- If you go over 21, you bust, and dealer win
- Dealer will hit until cards total 17 or higher.
- DOUBLE means to hit, the bet is double and you only get one more card



Click on anywhere to back game
""",fill = "blue",font = "14")
        return  #when draw the rule and tips
    
    canvas.create_text(30,100,anchor = NW, text = """
-> Click on START button to begin the game

-> If you want to hit, click on HIT

-> When ready for the game, click on STAND

-> When gameover, click on REMATCH
""", font = "bold 16")
    
    canvas.create_text(30,280, anchor = NW, text = """
-> For rules of Black Jack, click here:""",
 font = "bold 16")
    canvas.create_text(400,300,anchor = NW, text = "Rule of BlackJack",
                       fill = "red", font ="bold 18")

    canvas.create_text(200,450,anchor = NW, text = """
When you are ready, press SPACE to begin!!
""",font = "bold 16",fill = "blue")
    

#@@@@@@@@@@@@@@@@@@@@@@@@@@@  @  TEXAS POKER  @   @@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@  @  TEXAS POKER  @   @@@@@@@@@@@@@@@@@@
def initTX(data):
    #Initialize Texas Poker
    data.counter = 0
    data.TXTableCards = []  #for the table cards
    data.PlayerCards = []   #used to keep track of all the existing cards
    if data.back=="lv":
        data.TXbackground = PhotoImage(file="ALLGIF/T-X.gif")
    elif data.back=="mc":
        data.TXbackground = PhotoImage(file="ALLGIF/MCB.gif")
    data.initializePlayer = False
    data.initializeGame = False
    data.flip = False
    data.ready = False
    data.addChip = False
    data.TXgameover = False
    initDicts(data)
    data.AI = TexasPokerAI()
    data.TXPlayer = TexasPokerPlayer()
    data.winner = None
    data.playerChips = []
    data.AIChips = []
    data.input = 0
    data.dPause = True
    data.check = False
    data.clickOnCheck = False
    data.drawSim = False
    data.maxInput = 300
    data.drawOverMax = False
    data.chooseMode = False
    data.countPlayerMoney = True
    data.countAIMoney = True
    data.drawTXHand = False
    data.SBChip = ChipOfFifty()  #small blind
    data.switchDealer = True
    data.canClickOnRaise = False
    data.noMoney = False
    data.drawNoMoney = False
    if data.playerBank<1200:
        data.noMoney = True
    if data.TXDealer=="Player":
        data.AIDecisionMaking = True
    else:
        data.AIDecisionMaking = False


def TXMousePressed(event,data):
    #mouse pressed for Texas Poker

    #MODE button
    if (50<event.x<100 and 450<event.y<500 and data.chooseMode == False
        and data.TXInstruction):
        data.chooseMode = True
        return

    #CHOOSE MODE button
    if data.chooseMode and 50<event.x<150 and 450<event.y<530:
        data.chooseMode = False
        if 50<event.x<100 and 450<event.y<490:
            data.AIDifficulty = "Easy"
        elif 50<event.x<100 and 490<event.y<530:
            data.AIDifficulty = "Medium"
        elif 100<event.x<150 and 450<event.y<490:
            data.AIDifficulty = "Hard"
        elif 100<event.x<150 and 490<event.y<530:
            data.AIDifficulty = "Expert"
        return

    #for showing the hand picture
    if (data.TXInstruction and data.drawTXHand == False
        and 430<event.x<500 and 250<event.y<310):
        data.drawTXHand = True
        return

    if data.drawTXHand:
        data.drawTXHand = False
    
    if data.TXInstruction:return
    #RESTART button
    if 100<event.x<180 and 450<event.y<500 and data.TXgameover:
        initTX(data)

    #TIP button
    if 50<event.x<120 and 380<event.y<410:
        data.p = data.TXPlayer.simulateGame(data)
        data.drawSim = not data.drawSim


    #INSTRUCTION button
    if 50<event.x<150 and 350<event.y<380:
        data.TXInstruction = True
    
    #ADD CHIP buttons
    if data.addChip and not data.check:
        if getPlayerChipsSum(data)>=getMaxPossibleInput(data):
            data.drawOverMax = True
            
        if (50<event.x<100 and 100<event.y<150 and data.drawOverMax ==False
            and getPlayerChipsSum(data)+10<=getMaxPossibleInput(data)):
            data.playerChips.append(ChipOfTen())
            data.input+=10
            data.playerBank-=10
            data.canClickOnRaise = True
            #if valueMatch(data):data.check = True;data.addChip = False
        if (50<event.x<100 and 150<event.y<200 and data.drawOverMax ==False
            and getPlayerChipsSum(data)+50<=getMaxPossibleInput(data)):
            data.playerChips.append(ChipOfFifty())
            data.input+=50
            data.playerBank-=50
            data.canClickOnRaise = True
            #if valueMatch(data):data.check = True;data.addChip = False
        if (50<event.x<100 and 200<event.y<250 and data.drawOverMax==False
            and getPlayerChipsSum(data)+100<=getMaxPossibleInput(data)):
            data.drawTip = False
            data.playerChips.append(ChipOfHundred())
            data.playerBank-=100
            data.canClickOnRaise = True
            #if valueMatch(data):data.check = True;data.addChip = False

        if (100<event.x<125 and 125<event.y<225 and data.drawOverMax==False
            and getPlayerChipsSum(data)<=getAIChipsSum(data)):
            data.TXPlayer.matchAI(data)
            data.check = True
        
    #FOLD button 
    if 50<event.x<100 and 250<event.y<300:
        data.TXgameover = True
        data.winner = "AI"
        data.drawOverMax = False

    #RAISE button
    if (50<event.x<100 and 300<event.y<350 and len(data.TXTableCards)>2
        and data.canClickOnRaise
        and not getAIChipsSum(data)>getPlayerChipsSum(data)):
        data.drawOverMax = False
        if data.check: print("Please Click On Next");return
        data.clickOnCheck = True
        if valueMatch(data):
            data.check = True
            data.addChip = False
        else:
            data.AI.makeDecision(data)
            if valueMatch(data):
                data.check = True
            if data.AI.decision=="FOLD":
                data.TXgameover = True
                data.winner = "PLAYER"
                data.drawOverMax = False

    
    #CHECK button
    if (100<event.x<150 and 300<event.y<350 and len(data.TXTableCards)>2
        and not data.canClickOnRaise):
        data.drawOverMax = False
        if data.check:
            print("Please Click On Next")
            return
        data.clickOnCheck = True
        if data.TXDealer=="Player" and valueMatch(data):
            data.check = True
            data.addChip = False
            return
        data.AI.makeDecision(data)
    
        if valueMatch(data):
            data.check = True
            data.addChip = False
        if data.AI.decision=="FOLD":
            data.TXgameover = True
            data.winner = "PLAYER"
            data.drawOverMax = False

    #START button
    if 50<event.x<100 and 450<event.y<500:
        if data.playerBank<1200:
            data.drawNoMoney = True
            return
        data.check = True
        data.initializePlayer = True
        if data.TXDealer == "AI":
            data.playerBank -= 50


    #NEXT button
    if (150<event.x<200 and 300<event.y<350 and len(data.TXPlayer.cards)>1):
        #case when not ready
        if data.check == False:
            if not data.clickOnCheck:
                print("Please check or raise")
                return
            elif getPlayerChipsSum(data)<getAIChipsSum(data):
                print("Please Match or Fold")
                return
            elif getPlayerChipsSum(data)>getAIChipsSum(data):
                print("Please click on Raise")
                return
            else:print("Please Click On Check")

        #case when no card on table
        elif len(data.TXTableCards)<3:
            data.initializeGame = True
            data.check = False
            data.canClickOnRaise = False
            data.drawOverMax = False
            if data.TXDealer=="Player":
                data.AIDecisionMaking = True
            if data.drawSim:
                data.p = data.TXPlayer.simulateGame(data)
            
        #case when 3 cards on table but all not faceup
        elif len(data.TXTableCards)==3 and data.flip == False:
            data.flip = True
            data.counter = 0
            data.check = False
            data.canClickOnRaise = False
            data.drawOverMax = False
            if data.TXDealer=="Player":
                data.AIDecisionMaking = True
            if data.drawSim:
                data.p = data.TXPlayer.simulateGame(data)

        else: #case when 3 cards on table
            if len(data.TXTableCards)<5: #case when total cards less than 5
                addTXCards(data)
                data.drawOverMax = False
                data.AI.fillDicts(data)
                data.TXPlayer.fillDicts(data)
                fillDicts(data)
                data.check = False
                data.canClickOnRaise = False
                if data.TXDealer=="Player":
                    data.AI.makeDecision(data)
                if data.drawSim:
                    data.p = data.TXPlayer.simulateGame(data)
            else:  #case when 5 card and ready to check for winner
                findWinner(data)
                for c in data.AI.cards:
                    c.faceUp = False
                data.TXgameover = True
                data.drawOverMax = False




        
    
def TXKeyPressed(event,data):
    #TX Key pressed
    
    if data.TXInstruction and event.keysym=="space":
        data.TXInstruction = False
        return

    #key pressed, for debugging use
    if data.drawSim:
        data.drawSim = False
        return
    if event.keysym=="Escape":
        data.mode = "SplashScreen"
        data.timerDelay = 150 
    if event.keysym=="r":initTX(data)
    if event.keysym=="w":
        data.AI.getHighestHands()
        print(data.AI.hand)
    if event.keysym=="s":
        print(data.AI.simulateGame(data))
        print(data.TXPlayer.simulateGame(data))
    if event.keysym=="p":
        print(getMaxPossibleInput(data))
    if event.keysym=="d":
        data.p = data.TXPlayer.simulateGame(data)
        print(data.p)
        data.drawSim = not data.drawSim 
    if event.keysym=="q":
        for c in data.AI.allCards:
            c.faceUp = False
        
    return

def TXTimerFired(data):
    #timer fired for Texas Poker
    data.counter = data.counter+1 if data.counter<16 else 0
    #to control animation
    
    if data.TXgameover==True:  #case when already game over
        #move the chips and count for money
        if data.switchDealer:
            if data.TXDealer == "Player":
                data.TXDealer = "AI"
            else:
                data.TXDealer = "Player"
            data.switchDealer = False
            
        for c in data.playerChips:
            if data.winner=="PLAYER":
                c.moveDown()
                if data.countPlayerMoney:
                    data.playerBank+=getPlayerChipsSum(data)
                    data.countPlayerMoney = False
            elif data.winner=="AI":
                c.moveUp()
            else:
                c.moveRight()
                if data.countPlayerMoney:
                    data.playerBank+=getPlayerChipsSum(data)
                    data.countPlayerMoney = False
            
            if c.x<0 or c.x>800 or c.y<0 or c.y>600:
                data.playerChips.remove(c)

        #add value from AIChip
        for c in data.AIChips:
            if data.winner=="PLAYER":
                c.moveDown()
                if data.countAIMoney:
                    data.playerBank+=getAIChipsSum(data)
                    data.countAIMoney = False
            elif data.winner=="AI":
                c.moveUp()
            else:c.moveRight()
            if c.x<0 or c.x>800 or c.y<0 or c.y>600:
                data.AIChips.remove(c)
        
        if data.winner=="PLAYER":
            data.SBChip.moveDown()
            if data.countPlayerMoney:
                data.playerBank += 50
                data.countMoney = False
        elif data.winner=="AI":
            data.SBChip.moveUp()
        else:
            data.SBChip.moveRight()
        
    #case for run out first 4 cards
    cardsOut = 0
    if data.initializePlayer:
        if data.counter==3:
            data.AI.initialize(data);cardsOut+=1
        if data.counter == 6:
            data.TXPlayer.initialize(data)
            cardsOut+=1
        if data.counter == 9:
            data.AI.initialize(data);cardsOut+=1
        if data.counter == 12:
            data.TXPlayer.initialize(data);cardsOut+=1
        if len(data.TXPlayer.cards)==2 and len(data.AI.cards)==2:
            data.initializePlayer = False

        data.TXPlayer.fillDicts(data)
        data.AI.fillDicts(data)

    ##case for initializing game   
    if data.initializeGame and valueMatch(data):
        if data.counter == 2:
            initializeTXGame(data)
        if data.counter == 9:
            initializeTXGame(data)
        if len(data.TXTableCards)>=3:
            if data.TXDealer=="Player" and data.AIDecisionMaking:
                data.AI.makeDecision(data)
                data.AIDecisionMaking = False
            data.addChip=True
            data.initialize = False
            
    #flip over the cards
    if data.flip:
        if data.counter == 3:
            data.TXTableCards[0].faceUp = False
        if data.counter == 6:
            data.TXTableCards[1].faceUp = False
        if data.counter == 9:
            data.TXTableCards[2].faceUp = False
        data.addChip = True
    
        data.AI.fillDicts(data)
        data.TXPlayer.fillDicts(data)
        if data.TXDealer=="Player" and data.AIDecisionMaking:
            data.AI.makeDecision(data)
            data.AIDecisionMaking = False
   
    #case to move all the cards for animation
    for c in data.TXTableCards:
        if c.x<200:
            c.x += 100
        elif c.x<230:
            c.x += 30

    for c in data.AI.cards:
        if c.x>600:
            c.x-=100

    for c in data.TXPlayer.cards:
        if c.x<200:
            c.x+=100

def AllCardFlip(data):
    #function to test if all the cards all flip up
    for c in data.TXTableCards:
        if c.faceUp:
            return False
    return True

  
def relocateChipsTX(data):
    #relocate all the chips of TX for draw them
    x1,x2 = 330,480
    y1,y2 = 90,90
    dx,dy = 25,10
    for i in range(len(data.playerChips)):
        incrX = i//15
        incrY = i%15
        data.playerChips[i].x = x1 + incrX*dx
        data.playerChips[i].y = y1 + incrY*dy

    for i in range(len(data.AIChips)):
        incrX = i//12
        incrY = i%12
        data.AIChips[i].x = x2 + incrX*dx
        data.AIChips[i].y = y2 + incrY*dy
    data.SBChip.x,data.SBChip.y = 440,220

def TXRedrawAll(canvas,data):
    if data.TXInstruction:
        drawTXInstruction(canvas,data)
        return
    #Redraw all for texas poker
    canvas.create_image(0, 0,anchor=NW, image=data.TXbackground)
    if data.back == "lv":color1 = "green"
    elif data.back == "mc":color1 = "red"
    color2 = "white" if data.back=="lv" else "yellow"
    #canvas.create_rectangle(100,450,700,600,fill = color1,width=0)
    canvas.create_text(data.width/2,15
                       ,text = "Player Bank $: "+str(data.playerBank)
                       ,fill=color2,
                       font = "tahoma 14 bold")
    canvas.create_text(400,440,text="Press TIPS to see hands and probability",
                       fill = color2,font = "Aharoni 16")
    canvas.create_text(400,500,text = "TEXAS POKER",fill = "white"
                       ,font = "Aharoni 25 bold")
    canvas.create_text(240,50,text = "PLAYER",fill = color2,
                       font = "Aharoni 16 bold")
    canvas.create_text(620,50,text = "AI", fill = color2,
                       font = "Aharoni 16 bold")
    
    if data.drawOverMax:
        canvas.create_text(240,400,anchor = NW,text="Maximum Allowed Amount!!",
                           fill = color2, font = "bold 16")
    drawTXButton(canvas,data)
    if data.drawNoMoney:
        canvas.create_text(300,300,anchor = NW,text = "No Enough Money!!",
                           fill = color2,font = "bold 16")
        return
        
    if data.drawSim:
        drawTXTexts(canvas,data)
    x = 0;y = 300
    for c in data.TXTableCards:
        position = (c.x+x,280)
        c.drawPoker(data,canvas,position)
        x+=80
    i = 0
    for c in data.AI.cards:
        position = (c.x+i,data.AI.y)
        i+=20
        c.drawPoker(data,canvas,position)
    i = 0
    for c in data.TXPlayer.cards:
        position = (c.x+i,data.TXPlayer.y)
        i+=20
        c.drawPoker(data,canvas,position)

    if not data.TXgameover:
        relocateChipsTX(data)

    for c in data.playerChips:
        c.draw(canvas)
    for c in data.AIChips:
        c.draw(canvas)
    if len(data.AI.cards)!=0:    
        data.SBChip.draw(canvas)

    drawSmallBlind(canvas,data)

    color = "yellow"
    if data.back == "mc":
        color = "cyan"
            
    if data.winner!=None:
        canvas.create_text(440,230,text=data.winner+" WIN!!!",
                      font = "Aharoni 28 bold",fill=selectColor2(data))
    if data.TXgameover:
        canvas.create_text(400,540,text = "Click REMATCH"
                               ,fill=color,
                           font = "Aharoni 18 bold")
        return
    if data.addChip and not data.check:
        if valueMatch(data):
            canvas.create_text(390,537,text = """
      Value Match, If you raised or matched AI, click on RAISE
If you wish to raise, click on the values, or to check, click on CHECK"""
                               ,fill=color,
                           font = "Aharoni 14 bold")
        else:
            if getAIChipsSum(data)>getPlayerChipsSum(data):
                canvas.create_text(400,540
                ,text = "AI raised, Please Match, Raise or Fold"
                                   ,fill=color,
                               font = "Aharoni 18 bold")
            else:
                canvas.create_text(400,540,text = "Click on RAISE",
                                   fill = color, font = "bold 25")
    elif len(data.TXPlayer.cards)>=2:
        canvas.create_text(400,540,text = "Value Matched, Please Click on NEXT"
                           ,fill = color,
                           font = "Aharoni 18 bold")
    else:
        canvas.create_text(400,540,text = "Click START to Begin",fill=color,
                           font = "Aharoni 18 bold")
    if len(data.TXTableCards)>=3:
        canvas.create_text(400,590,
                           text =
"""Player Input: %d      Max Input Allowed: %d    AI Input: %d""" %
                           (getPlayerChipsSum(data),getMaxPossibleInput(data),
                            getAIChipsSum(data)),fill = color
                           ,font = "Aharoni 13 bold")

def drawSmallBlind(canvas,data):
    #Function to draw the small blind and dealer
    if data.TXDealer=="AI":
        canvas.create_oval(120,25,180,85,fill="purple",width=0)
        canvas.create_oval(660,25,720,85,fill="yellow",width=0)
        canvas.create_text(150,50,text = """
SMALL
 BLIND""",font = "bold 10"
                           ,fill = "white")
        canvas.create_text(690,55,text = "DEALER",font = "bold 10",
                           fill = "black")
    else:
        canvas.create_oval(120,25,180,85,fill="yellow",width=0)
        canvas.create_oval(660,25,720,85,fill="purple",width=0)
        canvas.create_text(150,55,text = "DEALER",font = "bold 10",
                           fill = "black")
        canvas.create_text(690,50,text = """
SMALL
 BLIND""",font = "bold 10",
                           fill = "white")
        
def drawTXInstruction(canvas,data):
    #Function to draw texas poker instruction
    data.handPicture = PhotoImage(file = "ALLGIF/Hand.gif")
    data.TXTip = PhotoImage(file = "ALLGIF/Txtip.gif")

    canvas.create_rectangle(-5,-5,805,605,fill = rgbString(135,206,250))
    canvas.create_text(400,50,text = "Texas Poker Instruction",
                       fill = "purple", font = "bold 28")
    if data.drawTXHand:
        canvas.create_image(400,300,image = data.handPicture)
        return
    canvas.create_text(30,100,anchor = NW, text = """
-> Click on START button to begin the game, follow the dynamic instruction

-> When ready for battle, click on CHECK, and follow the dynamic instruction

-> When the game over, click on REMATCH for new game
""", font = "bold 16")
    
    canvas.create_text(30,240, anchor = NW, text = """
-> For rules of Texas Poker hand, click here:

-> If need tips for hands and probability during game, click on TIPS
""", font = "bold 16")
    canvas.create_text(60,330,anchor = NW,text="""
You and AI will alternate to be the Dealer and Small Blind.
Small Blind needs to invest $50 before start.
And your bank should be at least $1200 to start a new game.
""",font = "13")
    canvas.create_text(30,400, anchor = NW, text = """
-> Select AI difficulty, click on MODE, default difficulty is Hard
""",font = "bold 16")
    canvas.create_text(200,450,anchor = NW, text = """
When you are ready, press SPACE to begin!!
""",font = "bold 16",fill = "blue")
    canvas.create_rectangle(50,450,100,500,fill = rgbString(50,50,100))
    canvas.create_text(75,475,text = "MODE")
    canvas.create_text(80,515,text = "AI Difficulty:" + data.AIDifficulty,
                       font = "bold 10")
    canvas.create_image(440,250,anchor = NW, image = data.TXTip)
    
    if data.chooseMode:
        #For changing the mode
        canvas.create_rectangle(50,450,100,530,fill="white",width=0)
        canvas.create_rectangle(100,450,150,530,fill="white",width=0)
        canvas.create_oval(50,450,100,490,fill="pink")
        canvas.create_text(75,470,text="EASY")
        canvas.create_oval(50,490,100,530,fill="grey")
        canvas.create_text(75,510,text="MEDIUM")
        canvas.create_oval(100,450,150,490,fill="orange")
        canvas.create_text(125,470,text = "HARD")
        canvas.create_oval(100,490,150,530,fill="cyan")
        canvas.create_text(125,510,text = "EXPERT")
        

    

def drawTXButton(canvas,data):
    #Draw texas poker button
    canvas.create_rectangle(100,300,150,350,fill=rgbString(238,174,239),width=0)
    canvas.create_text(125,325,text = "CHECK",fill = "purple",
                       font = "Aharoni 12 bold")
    color =rgbString(113,198,113) if data.back == "lv" else rgbString(198
                                                                   ,113,113)
    color2 = color
    color3 = rgbString(46,139,88) if data.back=="lv" else rgbString(176,
                                                                    23,31)
    if data.TXgameover:
        color2 = selectColor2(data)
    canvas.create_rectangle(101,450,180,500,fill=color2,width=0)
    canvas.create_text(140,475,text="REMATCH",fill = color3,
                       font = "Aharoni 12 bold")
    canvas.create_rectangle(50,380,120,410,fill=color,width=0)
    canvas.create_text(85,395,text = "TIPS",fill=color3,
                       font = "Aharoni 12")
    
    canvas.create_rectangle(150,300,200,350,fill=rgbString(131,111,255)
                            ,width=0)
    canvas.create_text(175,325,text="NEXT",fill = rgbString(75,5,130),
                       font = "Aharoni 12 bold")
    canvas.create_rectangle(50,100,100,150,fill="red",width=0)
    canvas.create_text(75,125,text = "+10",fill="black",
                       font = "Aharoni 14 bold")
    canvas.create_rectangle(50,150,100,200,fill="blue",width=0)
    canvas.create_text(75,175,text = "+50",fill = "yellow",
                       font = "Aharoni 14 bold")
    canvas.create_rectangle(50,200,100,250,fill="black",width=0)
    canvas.create_text(75,225,text = "+100",fill = "white",
                       font = "Aharoni 12 bold")
    canvas.create_rectangle(100,125,130,225,fill = rgbString(238,238,0),width=0)
    canvas.create_text(115,175,text=
                       """
M
A
T
C
H
""",font = "Aharoni 12 bold",fill = rgbString(255,127,0))
    canvas.create_rectangle(50,250,100,300,fill=rgbString(117,118,119),width=0)
    canvas.create_text(75,275,text="FOLD",fill=rgbString(63,64,65),
                       font ="Aharoni 12 bold" )
    canvas.create_rectangle(50,300,100,350,fill = "white",width=0)
    canvas.create_text(75,325,text="RAISE",fill = "red",
                       font = "Aharoni 12 bold")
    canvas.create_rectangle(50,350,150,380,fill="orange",width=0)
    canvas.create_text(100,365,text = "INSTRUCTION",fill = rgbString(205,102,0)
                       ,font = "Aharoni 10 bold")
    canvas.create_rectangle(50,450,100,500,fill = color,width=0)
    canvas.create_text(75,475,text = "START",fill = color3,
                       font = "Aharoni 12 bold")



    

def drawTXTexts(canvas,data):
    #Draw Texas Poker texts
    canvas.create_rectangle(0,380,800,580,fill="black",width=0)
    fillDicts(data)
    if isRoyalFlushing(data):
        canvas.create_text(100,400,text="Royal Flush",fill="red")
    else:
        canvas.create_text(100,400,text="Royal Flush",fill="white")
    if isStraightFlushing(data):
        canvas.create_text(200,400,text="Straight Flush", fill = "red")
    else:
        canvas.create_text(200,400,text="Straight Flush",fill="white")

    if isFlushing(data):
        canvas.create_text(500,400,text = "Flush", fill = "red")
    else:
        canvas.create_text(500,400,text="Flush",fill = "white")

    if isFourOfKind(data):
        canvas.create_text(300,400,text = "FourOfKind", fill = "red")
    else:
        canvas.create_text(300,400,text="FourOfKind",fill = "white")

    if isStraight(data):
        canvas.create_text(600,400,text="Straight",fill = "red")
    else:
        canvas.create_text(600,400,text="Straight",fill="white")

    if isFullHouse(data):
        canvas.create_text(400,400,text="FullHouse", fill = "red")
    else:
        canvas.create_text(400,400,text="FullHouse",fill="white")

    if isDoublePair(data):
        canvas.create_text(300,420,text="Double Pair",fill="red")
    else:
        canvas.create_text(300,420,text="Double Pair",fill="white")

    if isTriple(data):
        canvas.create_text(400,420,text="Triple", fill = "red")
    else:
        canvas.create_text(400,420,text="Triple",fill="white")

    if isPair(data):
        canvas.create_text(500,420,text = "Pair",fill = "red")
    else:
        canvas.create_text(500,420,text="Pair",fill = "white")
    drawSimulation(canvas,data)
    canvas.create_text(400,443,text="Press Anykey to Back Game",fill="yellow")


class TexasPokerAI(object):
    #Texas Poker AI
    def __init__(self):
        #constructor
        self.x = 600
        self.y = 80
        self.cards = []
        self.suit = dict()
        self.rank = dict()
        self.hand = [None,None]
        for i in range(1,14):
            self.rank[i] = 0
        for s in "cdhs":
            self.suit[s] = 0
        self.allCards = []
        self.decision = None
        self.simulation = []

    def initialize(self,data):
        #initialize the game
        if len(self.cards)<2:
            c = createNewValidCard(data)
            c.x = 800
            c.faceUp = True
            self.cards.append(c)

    def clearDict(self):
        #helper function for filling the probability dictionary
        for i in range(1,14):
            self.rank[i] = 0
        for s in "cdhs":
            self.suit[s] = 0
        
    def fillDicts(self,data):
        #fill the dictionary
        self.clearDict()
        for c in data.TXTableCards:
            if c.faceUp == False:
                rank = c.rank
                suit = c.suit
                self.rank[rank] += 1
                self.suit[suit] += 1
        for c in self.cards:
            rank = c.rank
            suit = c.suit
            self.rank[rank] += 1
            self.suit[suit] += 1
        self.allCards.clear()
        self.allCards += self.cards
        for c in data.TXTableCards:
            if not c.faceUp:
                self.allCards.append(c)

    def fillSimulationDicts(self,data):
        #helper function for fill out all the simulation dicts
        self.clearDict()
        self.simulation.clear()
        self.simulation += self.cards
        for c in data.TXTableCards:
            if not c.faceUp:
                self.simulation.append(c)
        cardNeed = 7-len(self.simulation)

        before = copy.deepcopy(data.PlayerCards)
        #used to clean the PlayerCards

        
        for i in range(cardNeed):
            c = createNewValidCard(data)
            self.simulation.append(c)
        data.PlayerCards.clear()
        for b in before:
            data.PlayerCards.append(b)
        for c in self.simulation:
            rank = c.rank
            suit = c.suit
            self.rank[rank]+=1
            self.suit[suit]+=1
            

    
##test the hands of TX
    def isFlushing(self):
        #return if the hand is flushing
        for suit in self.suit:
            if self.suit[suit]>=5:
                return True
        return False

    def getFlushingNum(self):
        #return other number for comparison
        suit = None
        for s in self.suit:
            if self.suit[s]>=5:
                suit = s
        nums = []
        for c in self.allCards:
            if c.suit == suit:
                if c.rank == 1:
                    nums.append(14)
                else:
                    nums.append(c.rank)
        return [max(nums)]

    def isRoyalFlushing(self):
        #return if the hand is royal flushing
        if not self.isFlushing():return False
        if not self.rank[1]>=1:return False
        for i in range(10,14):
            if not self.rank[i]>=1: return False
        return True

    def isFourOfKind(self):
        #return if the hand is four of kind
        for rank in self.rank:
            if self.rank[rank]>=4:
                return True
        return False

    def getFourOfKindNum(self):
        #return all the number for comparison
        four = None
        for r in self.rank:
            if r >=4:
                four = r
        result = []
        if four==1:four = 14
        result.append(four)
        for c in self.allCards:
            if c.rank!=four:
               result.append(c.rank)
        return result

    def isStraight(self):
        #return if the hand is straight
        if self.hasConsecutiveCard(10,13) and self.rank[1]>=1:
            return True
        for i in range(1,9):
            if self.hasConsecutiveCard(i,i+4):
                return True
        return False

    def getStraightNum(self):
        #return all the number for comparison
        if self.hasConsecutiveCard(10,13) and self.rank[1]>=1:
            return 10
        start = None
        for i in range(1,9):
            if self.hasConsecutiveCard(i,i+4):
                start = i
        return [start]


    def isStraightFlushing(self):
        #return if the hand is straight flush
        return self.isFlushing() and self.isStraight()

    def isDoublePair(self):
        #return if the hand is double pair
        pairs = 0
        for rank in self.rank:
            if self.rank[rank]>=2:pairs+=1
        return pairs>=2

    def getDoublePairNum(self):
        #return all the number for comparison
        pairs = []
        for rank in self.rank:
            if self.rank[rank]>=2:
                pairs.append(rank)
        nums = []
        for c in self.allCards:
            r = c.rank
            if r not in pairs:
                if r==1:
                    nums.append(14)
                else:
                    nums.append(r)
        for i in range(len(pairs)):
            if pairs[i]==1:pairs[i]=14      
        pairs.sort()
        pairs.reverse()
        if len(pairs)==3:
            num = pairs[-1]
            return pairs+[num]
        return pairs+[max(nums)]
    
    def hasConsecutiveCard(self,start,end):
        #helper function for testing straight case
        for i in range(start,end+1):
            if not self.rank[i]>=1:
                return False
        return True

    def isPair(self):
        #return if the hand is pair
        for rank in self.rank:
            if self.rank[rank]>=2:
                return True
        return False

    def getPairNum(self):
        #return all the number for comparision
        pair = None
        for r in self.rank:
            if self.rank[r]>=2:
                pair = r
        nums = []
        for c in self.allCards:
            if c.rank!=pair:
                if c.rank==1:
                    nums.append(14)
                else:
                    nums.append(c.rank)
        nums.sort()
        nums.reverse()
        if pair==1:
            pair = 14
        return [pair]+ nums[:3] if len(nums)>3 else [pair]+nums
    
    def isTriple(self):
        #return if the hand is triple
        for rank in self.rank:
            if self.rank[rank]>=3:
                return True
        return False

    def getTripleNum(self):
        #return all the number for comparision
        triple = None
        nums = []
        result = []
        for rank in self.rank:
            if self.rank[rank] >=3:
                triple = rank
        for c in self.allCards:
            if c.rank!=triple:
                if c.rank==1:
                    nums.append(14)
                else:
                    nums.append(c.rank)
        nums.sort()
        nums.reverse()
        if triple == 1: triple = 14
        result.append(triple)
        return result + nums[:2] if len(nums)>1 else result+nums

    def getHandNum(self):
        #return all the number for comparision
        nums = []
        for c in self.allCards:
            r = c.rank
            if r == 1:
                nums.append(14)
            else:
                nums.append(r)
        nums.sort()
        nums.reverse()
        return nums[:5] if len(nums)>5 else nums
        
            

    def isFullHouse(self):
        #return if the hand is flushing
        if not self.isTriple():return False
        triple = None
        for rank in self.rank:
            if self.rank[rank]>=3:
                triple = rank
        double = None
        for rank in self.rank:
            if self.rank[rank]>=2 and rank!=triple:
                double = rank
        return (triple!=None and double!=None)

    def getFullHouseNum(self):
        #return all the number for comparision
        triple = None
        for rank in self.rank:
            if self.rank[rank]>=3:
                triple = rank
        double = None
        for rank in self.rank:
            if self.rank[rank]>=2 and rank!=triple:
                double = rank
        if triple==1:triple = 14
        if double==1:double = 14
        return [triple,double]

    def test(self):
        #testing function
        print(self.isPair(),self.isTriple(),self.isDoublePair(),
              self.isStraight(), self.isFlushing(),self.isFullHouse())
    

    def getHighestHands(self):
        #return the highest hands possible
        if self.isRoyalFlushing():self.hands[0] = "RoyalFlush"
        elif self.isStraightFlushing():
            self.hand[0] = "StraightFlush"
            self.hand[1] = self.getStraightNum()
        elif self.isFourOfKind():
            self.hand[0] = "FourOfKind"
            self.hand[1] = self.getFourOfKindNum()
        elif self.isFullHouse():
            self.hand[0] = "FullHouse"
            self.hand[1] = self.getFullHouseNum()
        elif self.isFlushing():
            self.hand[0] = "Flushing"
            self.hand[1] = self.getFlushingNum()
        elif self.isStraight():
            self.hand[0] = "Straight"
            self.hand[1] = self.getStraightNum()
        elif self.isTriple():
            self.hand[0] = "ThreeOfKind"
            self.hand[1] = self.getTripleNum()
        elif self.isDoublePair():
            self.hand[0] = "DoublePair"
            self.hand[1] = self.getDoublePairNum()
        elif self.isPair():
            self.hand[0] = "Pair"
            self.hand[1] = self.getPairNum()
        else:
            self.hand[0] = "High"
            self.hand[1] = self.getHandNum()       
        return self.hand
        
    def makeDecisionHard(self,data):
        #AI Decision Hard Mode
        #It Make Decision Based on probability and the current opponent input
        #Kind of Agressive
        p = self.simulateGame(data)
        m = getMaxPossibleInput(data)
        sumAI = getAIChipsSum(data)
        sumP = getPlayerChipsSum(data)
        goodHandRank = ["Straight"
                    ,"Flushing","FullHouse","FourOfKind","StraightFlush"
                    ,"RoyalFlush"]
        normalHandRank = ["Pair","DoublePair","ThreeOfKind"]
        #When their value matches
        if valueMatch(data):
            if isPlayerBetter(data):
                diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                for s in goodHandRank:
                    if p[s]==1:
                        self.raiseMoney(data,diff)
                        return
                    elif p[s]>0.5:
                        self.raiseMoney(data,round(diff*0.5,-1))
                        return
                for s in normalHandRank:
                    if p[s]>0.8:
                        self.raiseMoney(data,round(diff*0.15,-1))
                        return
                self.decision = "Check" if p["Pair"]<0.75 else "Raise"
                if self.decision=="Check":
                    return
                else:
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    raiseValue = random.choice([
                        round(diff*0.6,-1),round(diff*0.4,-1),
                        round(diff*0.3,-1),round(diff*0.2,-1)])
                    decision = random.choice([0,1,2,3])
                    if decision==0:  #choose to battle randomly
                        self.raiseMoney(data,raiseValue)
                    else:    #according to self probability
                        if p["RoyalFlush"]>0.001:
                            self.raiseMoney(data,round(diff*0.8,-1))
                        elif p["StraightFlush"]>0.001:
                            self.raiseMoney(data,round(diff*0.8,-1))
                        elif p["FourOfKind"]>0.0045:
                            self.raiseMoney(data,round(diff*0.8,-1))
                        elif p["FullHouse"]>0.01:
                            self.raiseMoney(data,round(diff*0.6,-1))
                        elif p["Flushing"]>0.09:
                            self.raiseMoney(data,round(diff*0.5,-1))
                        elif p["Straight"]>0.12:
                            self.raiseMoney(data,round(diff*0.4,-1))
                        elif p["ThreeOfKind"]>0.2:
                            self.raiseMoney(data,round(diff*0.4,-1))
                        elif p["DoublePair"]>0.25:
                            self.raiseMoney(data,round(diff*0.3,-1))
                        elif p["Pair"]>0.6:
                            self.raiseMoney(data,round(diff*0.2,-1))
                        return
            else:
                diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                if p["RoyalFlush"]>0.002:
                    self.raiseMoney(data,round(diff*0.8,-1))
                elif p["StraightFlush"]>0.008:
                    self.raiseMoney(data,round(diff*0.9,-1))
                elif p["FourOfKind"]>0.004:
                    self.raiseMoney(data,round(diff*0.8,-1))
                elif p["FullHouse"]>0.05:
                    self.raiseMoney(data,round(diff*0.6,-1))
                    print("d")
                elif p["Flushing"]>0.11:
                    self.raiseMoney(data,round(diff*0.7,-1))
                elif p["Flushing"]>0.09:
                    self.raiseMoney(data,round(diff*0.5,-1))
                elif p["Straight"]>0.2:
                    print("a")
                    self.raiseMoney(data,round(diff*0.6,-1))
                elif p["Straight"]>0.12:
                    self.raiseMoney(data,round(diff*0.4,-1))
                elif p["ThreeOfKind"]>0.35:
                    self.raiseMoney(data,round(diff*0.6,-1))
                    print("b")
                elif p["ThreeOfKind"]>0.2:
                    self.raiseMoney(data,round(diff*0.4,-1))
                elif p["DoublePair"]>0.5:
                    self.raiseMoney(data,round(diff*0.5,-1))
                elif p["DoublePair"]>0.25:
                    self.raiseMoney(data,round(diff*0.3,-1))
                elif p["Pair"]>0.9:
                    self.raiseMoney(data,round(diff*0.6,-1))
                    print("c")
                elif p["Pair"]>0.8:
                    self.raiseMoney(data,random.choice(
                        [round(diff*0.3,-1),round(diff*0.2,-1)]))
                return

        #case when player has more money input
        elif sumP > sumAI:
            if isPlayerBetter(data):
                diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                for s in goodHandRank:
                    if p[s]>0.4:
                        self.matchPlayer(data)
                        diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                        self.raiseMoney(data,diff)
                        return
                for s in normalHandRank:
                    if p[s]>0.9:
                        self.matchPlayer(data)
                        diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.5,-1))
                        return
                for s in normalHandRank:
                    if p[s]>0.8:
                        self.matchPlayer(data)
                        diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.2,-1))
                        return
                if p["RoyalFlush"]>0.15:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.9,-1))
                elif p["RoyalFlush"]>0.0013:
                    self.matchPlayer(data)
                elif p["StraightFlush"]>0.05:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff,-1))
                elif p["StraightFlush"]>0.0015:
                    self.matchPlayer(data)
                elif p["FourOfKind"]>0.08:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAiChipsSum(data)
                    self.raiseMoney(data,round(diff*0.8,-1))
                elif p["FourOfKind"]>0.05:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.2,-1))
                elif p["FullHouse"]>0.1:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.5,-1))
                elif p["FullHouse"]>0.09:
                    self.matchPlayer(data)
                elif p["Flushing"]>0.2:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*1,-1))
                elif p["Flushing"]>0.1:
                    self.raiseMoney(data,round(diff*0.7,-1))
                elif p["Straight"]>0.2:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.5,-1))
                elif p["Straight"]>0.09:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.2,-1))
                elif p["Straight"]>0.05:
                    self.matchPlayer(data)
                elif p["ThreeOfKind"]>0.6:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.9,-1))
                elif p["ThreeOfKind"]>0.2:
                    self.matchPlayer(data)
                elif p["DoublePair"]>0.5:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.1,-1))
                elif p["DoublePair"]>0.2:
                    self.matchPlayer(data)
                elif p["Pair"]>0.85:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.3,-1))
                elif p["Pair"]>0.75:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.15,-1))
                elif p["Pair"]>0.7:
                    self.matchPlayer(data)
                else:
                    self.decision = "FOLD"
            else:        
                if p["RoyalFlush"]>0.1:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.8,-1))
                elif p["RoyalFlush"]>0.001:
                    self.matchPlayer(data)
                elif p["StraightFlush"]>0.05:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.9,-1))
                elif p["StraightFlush"]>0.0015:
                    self.matchPlayer(data)
                elif p["FourOfKind"]>0.08:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAiChipsSum(data)
                    self.raiseMoney(data,round(diff*0.8,-1))
                elif p["FourOfKind"]>0.05:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.2,-1))
                elif p["FullHouse"]>0.1:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.5,-1))
                elif p["FullHouse"]>0.05:
                    self.matchPlayer(data)
                elif p["Flushing"]>0.2:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*1,-1))
                elif p["Flushing"]>0.1:
                    self.matchPlayer(data)
                elif p["Straight"]>0.4:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff,-1))
                elif p["Straight"]>0.12:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.4,-1))
                elif p["ThreeOfKind"]>0.6:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.9,-1))
                elif p["ThreeOfKind"]>0.2:
                    self.matchPlayer(data)
                elif p["DoublePair"]>0.5:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.1,-1))
                elif p["DoublePair"]>0.25:
                    self.matchPlayer(data)
                elif p["Pair"]>0.85:
                    self.matchPlayer(data)
                    diff = getMaxPossibleInput(data) - getAIChipsSum(data)
                    self.raiseMoney(data,round(diff*0.3,-1))
                elif p["Pair"]>0.65:
                    self.matchPlayer(data)
                else:
                    self.decision = "FOLD"

                #Coefficient here should be adjusted according to more test


    def compareProbability(self,p1,p2):
        #A function used to estimate the score of current states
        #Based on both self hands and the table cards
        goodHandRank = ["Straight"
                    ,"Flushing","FullHouse","FourOfKind","StraightFlush"
                    ,"RoyalFlush"]
        normalHandRank = ["Pair","DoublePair","ThreeOfKind"]
        goodHand = 0
        normalHand = 0
        for s in goodHandRank:
            if (p1[s]-p2[s])>=0.01:
                goodHand +=1
            if p1[s]<=p2[s]:
                if p2[s]>=0.9:
                    goodHand -= 10
                elif p2[s]>=0.3:
                    goodHand -= 5
                elif p2[s]>=0.2:
                    goodHand -= 3
                elif p2[s]-p1[s]>=0.01 and s!="Straight":
                    goodHand -= 1
                elif p2[s]-p1[s]>=0.08:
                    goodHand -= 1
            if p1[s]>0.1:
                goodHand +=1
            if p1[s]>0.9:
                goodHand +=10
        for s in normalHandRank:
            if (p1[s]-p2[s])>=0.1:
                normalHand += 1
            if p1[s]<=p2[s]:
                if p2[s]>=0.9:
                    normalHand -= 3
                elif p2[s] - p1[s] >=0.1:
                    normalHand -= 1         
            if p1[s] > 0.25:
                normalHand += 1
            if p1[s]>0.9:
                normalHand += 3
        return (normalHand,goodHand)    
        
    
    def makeDecisionExpert(self,data):
        #A really sophisticate AI compare self probability with user's

        p1 = self.simulateGame(data)
        p2 = data.TXPlayer.simulateGame(data)
        m = getMaxPossibleInput(data)
        sumAI = getAIChipsSum(data)
        sumP = getPlayerChipsSum(data)
        print(m,sumAI,sumP)
        pData = self.compareProbability(p1,p2)
        (n,g) = (pData[0],pData[1])
        #n represents the estimated score for normal hands
        #g represents the estimated score for good hands
        diff = getMaxPossibleInput(data) - getAIChipsSum(data)
        hand = self.getHighestHands()
        inputPer = (sumP-sumAI)/m


        #case 1
        if len(data.TXTableCards)==3 and not AllCardFlip(data):
        #case when only 2 cards available
            if sumP > sumAI: 
                if n<0:
                    if data.TXDealer=="Player":
                        if inputPer>0.5:
                            self.decision = "FOLD"
                            #just fold it for bad card
                        else:
                            self.matchPlayer(data)
                    else:
                        highestNum = hand[1][0]
                        if highestNum <=5 or inputPer>0.3:
                            self.decision="FOLD"
                        else:
                            self.matchPlayer(data) #match if got larger than 5
                elif n<3:
                    highestNum = hand[1][0]
                    if data.TXDealer=="AI" and highestNum <= 4:
                        if inputPer > 0.2:
                            self.decision = "FOLD"
                        else:
                            self.matchPlayer(data)
                    elif highestNum <=12:
                        self.matchPlayer(data)
                    else:
                        self.matchPlayer(data)
                        if getInputPercent(data)>=0.6:
                            return
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.1,-1))
                else:
                    highestNum = hand[1][0]
                    self.matchPlayer(data)
                    if getInputPercent(data)>=0.7:
                        return
                    diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                    moneyToRaise = random.choice([0.2,0.1,0.15])
                    self.raiseMoney(data,round(diff*moneyToRaise,-1))
            else:
                if n<0:
                    return
                if n<3:
                    highestNum = hand[1][0]
                    if highestNum>=12:
                        self.matchPlayer(data)
                        if getInputPercent(data)>=0.5:
                            return
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.2,-1))
                    else:
                        self.matchPlayer(data)
                else:
                    if data.TXDealer == "AI":
                        self.matchPlayer(data)
                        if getInputPercent(data)>=0.6:
                            return
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.1,-1))
                    else:
                        if getInputPercent(data)>=0.7:
                            return
                        self.matchPlayer(data)
                        self.raiseMoney(data,round(diff*0.2,-1))


        #case 2
        elif len(data.TXTableCards)==3 and AllCardFlip(data):
            #case when three cards are flipped over
            if sumP > sumAI:
                if g<0:
                    if data.TXDealer=="AI":
                        if inputPer > 0.4:
                            self.decision = "FOLD"
                        else:
                            self.matchPlayer(data)
                    else:
                        highestNum = hand[1][0]
                        if highestNum <7:
                            self.decision="FOLD"
                        else:
                            if getInputPercent(data)>=0.3:
                                self.matchPlayer(data)
                            else:
                                self.decision = "FOLD"
                elif n<-1:
                    highestNum = hand[1][0]
                    if g>=10:
                        self.matchPlayer(data)
                    elif data.TXDealer=="AI":
                        if highestNum <8 and inputPer > 0.3:
                            self.decision="FOLD"
                        else:
                            self.matchPlayer(data)
                    else:
                        if highestNum <7 and inputPer>0.4:
                            self.decision="FOLD"
                        else:
                            self.matchPlayer(data)
                elif g<10:
                    if n<3:
                        self.matchPlayer(data)
                    else:
                        highestNum = hand[1][0]
                        if data.TXDealer=="AI":
                            if highestNum <=8:
                                self.matchPlayer(data)
                            else:
                                self.matchPlayer(data)
                                if getInputPercent(data)>=0.5:
                                    return
                                diff = (getMaxPossibleInput(data)
                                        -getAIChipsSum(data))
                                self.raiseMoney(data,round(diff*0.1,-1))
                        else:
                            if highestNum <=6:
                                self.matchPlayer(data)
                            else:
                                self.matchPlayer(data)
                                if getInputPercent(data)>0.5:
                                    return
                                diff = getMaxPossibleInput(data)
                                -getAIChipsSum(data)
                                self.raiseMoney(data,round(diff*0.1,-1))
                else:
                    highestNum = hand[1][0]
                    if data.TXDealer=="AI":
                        self.matchPlayer(data)
                    else:
                        self.matchPlaye(data)
                        if g>=20:
                            a = random.choice([0,0,1])
                            diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                            if a==1:
                                self.raiseMoney(data,round(diff,-1))
                        if getInputPercent(data)>0.8:
                            return
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.3,-1))

                            
            else:  #case when they value matches
                if g<0:
                    return
                elif n<-1:
                    if g>=10:
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.1,-1))
                    elif data.TXDealer=="Player":
                        if getInputPercent(data)>=0.5:
                            return
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.1,-1))
                    else:
                        return   
                elif g<10:
                    if n<3:
                        return
                    else:
                        highestNum = hand[1][0]
                        if data.TXDealer=="AI":
                            if highestNum <10:
                                return
                            else:
                                if getInputPercent(data)>=0.4:
                                    return
                                diff = (getMaxPossibleInput(data)
                                        -getAIChipsSum(data))
                                self.raiseMoney(data,round(diff*0.1,-1))
                        else:
                            if highestNum <=6:
                                return
                            else:
                                if getInputPercent(data)>=0.6:
                                    return
                                diff = (getMaxPossibleInput(data)
                                        -getAIChipsSum(data))
                                self.raiseMoney(data,round(diff*0.1,-1))                        
                else:
                    if data.TXDealer=="AI":
                        if getInputPercent(data)>=0.8:
                            return
                        diff = getMaxPossibleInput-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.3,-1))
                    else:
                        if g>=20:
                            if getInputPercent(data)>=0.8:
                                return
                            diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                            self.raiseMoney(data,round(diff*0.1,-1))


        #case 3
        elif len(data.TXTableCards)==4:
            #case when 4 cars on the table
            if sumP > sumAI:
                if g<0:
                    if n>=3:
                        self.matchPlayer(data)
                        
                    elif data.TXDealer=="AI":
                        if getInputPercent(data)>=0.5:
                            self.matchPlayer(data)
                        else:
                            if inputPer>0.4:
                                self.decision="FOLD"
                            else:
                                self.matchPlayer(data)
                    else:
                        highestNum = hand[1][0]
                        if highestNum <=5:
                            self.decision="FOLD"
                        else:
                            if getInputPercent(data)>=0.45:
                                self.matchPlayer(data)
                            else:
                                self.decision = "FOLD"
                elif n<0:
                    highestNum = hand[1][0]
                    if g>=10:
                        self.matchPlayer(data)
                    elif data.TXDealer=="AI":
                        if highestNum <=5 and inputPer>0.4:
                            self.decision="FOLD"
                        else:
                            if getInputPercent(data)>=0.3:
                                self.matchPlayer(data)
                            elif inputPer < 0.35:
                                self.matchPlayer(data)
                            else:
                                self.decision = "FOLD"
                    else:
                        if highestNum <=6:
                            if inputPer > 0.4:
                                self.decision="FOLD"
                            else:
                                self.matchPlayer(data)
                        else:
                            if getInputPercent(data)>=0.3:
                                self.matchPlayer(data)
                            elif inputPer < 0.25:
                                self.matchPlayer(data)
                            else:
                                self.decision="FOLD"
                elif g<10:
                    if n<3:
                        self.matchPlayer(data)
                    else:
                        highestNum = hand[1][0]
                        if data.TXDealer=="AI":
                            if highestNum <=8:
                                self.matchPlayer(data)
                            else:
                                self.matchPlayer(data)
                                if getInputPercent(data)>=0.8:
                                    return
                                diff = (getMaxPossibleInput(data)
                                        -getAIChipsSum(data))
                                self.raiseMoney(data,round(diff*0.1,-1))
                        else:
                            if highestNum <=6:
                                self.matchPlayer(data)
                            else:
                                self.matchPlayer(data)
                                if getInputPercent(data)>=0.8:
                                    return
                                diff = (getMaxPossibleInput(data)
                                        -getAIChipsSum(data))
                                self.raiseMoney(data,round(diff*0.15,-1))
                else:
                    highestNum = hand[1][0]
                    if data.TXDealer=="AI":
                        if g>=20:
                            diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                            self.raiseMoney(data,round(diff*0.4,-1))
                        self.matchPlayer(data)
                        if getInputPercent(data)>=0.9:
                            return
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.3,-1))

                            
                    else:
                        self.matchPlaye(data)
                        if g>=20:
                            diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                            self.raiseMoney(data,round(diff*0.8,-1))
                        if getInputPercent(data)>=0.9:
                            return
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.3,-1))

                            
            else:  #case when they value matches
                if g<0:
                    return
                elif n<0:
                    if g>=10:
                        if getInputPercent(data)>=0.7:
                            return
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.08,-1))
                    elif data.TXDealer=="Player":
                        if getInputPercent(data)>=0.5:
                            return
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.05,-1))
                    else:
                        return   
                elif g<10:
                    if n<3:
                        a = random.choice([0,0,0,1])
                        if a==1 and getInputPercent(data)<=0.5:
                            diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                            self.raiseMoney(data,round(diff*0.05,-1))
                        else:
                            return
                    else:
                        highestNum = hand[1][0]
                        if data.TXDealer=="AI":
                            if highestNum <8:
                                return
                            else:
                                diff = (getMaxPossibleInput(data)
                                        -getAIChipsSum(data))
                                if getInputPercent(data)>=0.6:
                                    return
                                self.raiseMoney(data,round(diff*0.1,-1))
                        else:
                            if highestNum <=6:
                                return
                            else:
                                diff = (getMaxPossibleInput(data)
                                        -getAIChipsSum(data))
                                if getInputPercent(data)>=0.7:
                                    return
                                self.raiseMoney(data,round(diff*0.1,-1))                        
                else:
                    if data.TXDealer=="AI":
                        if getInputPercent(data)>=0.8:
                            return
                        diff = getMaxPossibleInput-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.3,-1))
                    else:
                        diff = getMaxPossibleInput-getAIChipsSum(data)
                        if getInputPercent(data)>=0.6:
                            return
                        self.raiseMoney(data,round(diff*0.1,-1))
                        if g>=20:
                            diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                            self.raiseMoney(data,round(diff,-1))
                    #not invest more here if already good hand
                            #try earn more next round

                     
        #case 4
        elif len(data.TXTableCards)==5:
            #case when 4 cars on the table
            if sumP > sumAI:
                if g<0:
                    if n>=6:
                        self.matchPlayer(data)
                        if getInputPercent(data)>=0.7:
                            return
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.1,-1))
                    elif n>=3:
                        self.matchPlayer(data)
                    elif data.TXDealer=="AI":
                        if getInputPercent(data)>=0.8:
                            self.matchPlayer(data)
                        else:
                            if inputPer<0.4:
                                self.matchPlayer(data)
                            else:
                                self.decision = "FOLD"
                    else:
                        highestNum = hand[1][0]
                        if highestNum <=5:
                            self.decision="FOLD"
                        else:
                            if getInputPercent(data)>=0.7:
                                self.matchPlayer(data)
                            else:
                                self.decision = "FOLD"
                elif n<0:
                    highestNum = hand[1][0]
                    if g>=10:
                        self.matchPlayer(data)
                        if getInputPercent(data)>=0.9:
                            return
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*0.2,-1))
                    elif g>=2:
                        self.matchPlayer(data)
                    elif data.TXDealer=="AI":
                        if highestNum <=5 and inputPer>0.5:
                            self.decision="FOLD"
                        else:
                            if getInputPercent(data)>=0.5:
                                self.matchPlayer(data)
                            elif inputPer <= 0.25:
                                self.matchPlayer(data)
                            else:
                                self.decision = "FOLD"
                    else:
                        if highestNum <=6:
                            if getInputPercent(data)>=0.5 and inputPer<0.8:
                                self.matchPlayer(data)
                            else:
                                self.decision = "FOLD"
                        else:
                            if getInputPercent(data)>=0.4:
                                self.matchPlayer(data)
                            elif inputPer < 0.3:
                                self.matchPlayer(data)
                            else:
                                self.decision="FOLD"
                elif g<10:
                    if n<3:  #both player no good hands
                        highestNum = hand[1][0]
                        if highestNum>=10:
                            self.matchPlayer(data)
                        elif highestNum>=6:
                            if getInputPercent(data)>=0.3:
                                self.matchPlayer(data)
                            else:
                                self.decision = "FOLD"
                        else:
                            self.decision = "FOLD"
                    else:  #have good normal hands
                        highestNum = hand[1][0]
                        if data.TXDealer=="AI":
                            if highestNum <=8:
                                self.matchPlayer(data)
                                if getInputPercent(data)>=0.5:
                                    return
                                diff = (getMaxPossibleInput(data)
                                        -getAIChipsSum(data))
                                self.raiseMoney(data,round(diff*0.1,-1))
                            else:
                                self.matchPlayer(data)
                                if getInputPercent(data)>=0.6:
                                    return
                                diff = (getMaxPossibleInput(data)
                                        -getAIChipsSum(data))
                                self.raiseMoney(data,round(diff*0.3,-1))
                        else:
                            if highestNum <=6:
                                self.matchPlayer(data)
                                if getInputPercent(data)>=0.55:
                                    return
                                diff = (getMaxPossibleInput(data)
                                        -getAIChipsSum(data))
                                self.raiseMoney(data,round(diff*0.1,-1))
                            else:
                                self.matchPlayer(data)
                                if getInputPercent(data)>=0.75:
                                    return
                                diff = (getMaxPossibleInput(data)
                                        -getAIChipsSum(data))
                                self.raiseMoney(data,round(diff*0.25,-1))
                else:
                    highestNum = hand[1][0]
                    ratio = random.choice([1,0.9,0.8,0.7,0.6,0.4,0.4,
                                           0.2,0.1,0.1,0.2,0.3,0.05])
                    if data.TXDealer=="AI":
                        self.matchPlayer(data)
                        if getInputPercent(data)>=0.9:
                            return
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*ratio,-1))
                            
                    else:
                        self.matchPlayer(data)
                        if getInputPercent(data)>=0.9:
                            return
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*ratio,-1))

                            
            else:  #case when they value matches
                if g<0:
                    return
                elif n<0:
                    if g>5:
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        if getInputPercent(data)>=0.8:
                            return
                        self.raiseMoney(data,round(diff*0.2,-1))
                    elif data.TXDealer=="Player":
                        highestNum = hand[1][0]
                        if highestNum<=7:
                            return
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        if getInputPercent(data)>=0.7:
                            return
                        self.raiseMoney(data,round(diff*0.05,-1))
                    else:
                        return   
                elif g<10:  
                    if n<3:  #both of player not have really good hands
                        ratio = random.choice([0,0,0,0,0.1,0.15,0.6])
                        #randomly scare the player when both have no good hand
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        if getInputPercent(data)>=0.8:
                            return
                        self.raiseMoney(data,round(diff*ratio,-1))
                    else:
                        highestNum = hand[1][0]
                        if data.TXDealer=="AI":
                            if highestNum <3:
                                return
                            else:
                                ratio = random.choice([0.1,0.2,0.1,0,0.1,0.2])
                                if getInputPercent(data)>=0.9:
                                    return
                                diff = (getMaxPossibleInput(data)
                                        -getAIChipsSum(data))
                                self.raiseMoney(data,round(diff*ratio,-1))
                        else:
                            if highestNum <4:
                                return
                            else:
                                ratio = random.choice([0.2,0.1,0.3,0.1,0.1])
                                if getInputPercent(data)>=0.9:
                                    return
                                diff = (getMaxPossibleInput(data)
                                        -getAIChipsSum(data))
                                self.raiseMoney(data,round(diff*ratio,-1))                        
                else:  #really good hands
                    ratio = random.choice([0.7,0.8,0.6,0.7,0.4,1,1])
                    if data.TXDealer=="AI":
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*ratio,-1))
                    else:
                        diff = getMaxPossibleInput(data)-getAIChipsSum(data)
                        self.raiseMoney(data,round(diff*ratio,-1))                        
                
                    

    def makeDecision(self,data):
        #AI decision according to the difficulty
        if data.AIDifficulty=="Easy":
            self.makeDecisionEasy(data)
        if data.AIDifficulty=="Medium":
            self.makeDecisionMedium(data)
        if data.AIDifficulty=="Hard":
            self.makeDecisionHard(data)
        if data.AIDifficulty =="Expert":
            self.makeDecisionExpert(data)

    def matchPlayer(self,data):
        #match the player
        diff = getPlayerChipsSum(data)-getAIChipsSum(data)
        while(diff>0):
            if diff>=100:
                data.AIChips.append(ChipOfHundred())
                diff-=100
            elif diff>=50:
                data.AIChips.append(ChipOfFifty())
                diff-=50
            else:
                data.AIChips.append(ChipOfTen())
                diff-=10


    def raiseMoney(self,data,diff):
        #raise money
        while(diff>0 and getAIChipsSum(data)<getMaxPossibleInput(data)):
            if diff>=100:
                data.AIChips.append(ChipOfHundred())
                diff-=100
            elif diff>=50:
                data.AIChips.append(ChipOfFifty())
                diff-=50
            else:
                data.AIChips.append(ChipOfTen())
                diff-=10
        
    
    def makeDecisionEasy(self,data):
        #Easy AI Mode, Just try to match player, never fold
        if valueMatch(data):
            return
                                
        if getPlayerChipsSum(data)>getAIChipsSum(data):
            self.matchPlayer(data)
                                

    
        
    def makeDecisionMedium(self,data):
        #Medium AI Mode, decision based on current input ceiling and
        #self probability, but fold randomly when player raise
        p = self.simulateGame(data)
        m = getMaxPossibleInput(data)
        sumAI = getAIChipsSum(data)
        sumP = getPlayerChipsSum(data)
        if sumP>sumAI:
            self.decision = random.choice(["FOLD","RAISE","RAISE","RAISE"])
            if self.decision=="FOLD":
                return
            self.matchPlayer(data)
            diff = m-getAIChipsSum(data)
            if p["RoyalFlush"]>0.0005:
                
                for i in range(1):
                    self.raiseMoney(data,random.choice([diff,
                                                    diff-20,
                                                    diff-50,]))

                
            elif p["StraightFlush"]>0.0008:
                self.raiseMoney(data,random.choice([diff-50,
                                                    diff-20,
                                                    round(diff/2,-1),
                                                    round(diff/2,-1)]))
                                    
                

            elif p["FourOfKind"]>0.001:
                self.raiseMoney(data,random.choice([diff-50,
                                                    diff-100,
                                                    round(diff/2,-1)]))

            elif p["DoublePair"]>0.2 or p["ThreeOfKind"]>0.15:
                self.raiseMoney(data,random.choice([diff,
                                                    diff-20,
                                                    diff-50,]))
            elif p["Pair"]>0.4:
                self.raiseMoney(data,random.choice([diff,diff-50]))
        
        else:
            d = random.choice([0,1,2,3])
            if d!=3:
                return
            else:
                diff = m-getAIChipsSum(data)
                if p["StraightFlush"]>0.0008:
                    self.raiseMoney(data,random.choice([diff-50,
                                                    diff-20,
                                                    round(diff/2,-1),
                                                    round(diff/2,-1)]))
                                    
                

                elif p["FourOfKind"]>0.001:
                    self.raiseMoney(data,random.choice([diff-50,
                                                    diff-100,
                                                    round(diff/2,-1)]))
                elif p["Pair"]>0.6:
                    self.raiseMoney(data,random.choice([diff,diff-50]))

    #Series of Function to get largest possible at this time
    def simulateGame(self,data):
        #simulate through game
        result = dict()  #used to store the simulation result
        handRank = ["High","Pair","DoublePair","ThreeOfKind","Straight","Flushing",
                "FullHouse","FourOfKind","StraightFlush","RoyalFlush"]
        for s in handRank:
            result[s] = 0  #initailize the result
        trial = 2000  #number of trial for Monte Carlo
        for i in range(trial):
            self.fillSimulationDicts(data)   #fill the dictionary for simulation
            if self.isRoyalFlushing():
                result["RoyalFlush"]+=1
            if self.isStraightFlushing():
                result["StraightFlush"]+=1
            if self.isFourOfKind():
                result["FourOfKind"]+=1
            if self.isFullHouse():
                result["FullHouse"]+=1
            if self.isFlushing():
                result["Flushing"]+=1
            if self.isStraight():
                result["Straight"]+=1
            if self.isTriple():
                result["ThreeOfKind"]+=1
            if self.isDoublePair():
                result["DoublePair"]+=1
            if self.isPair():
                result["Pair"]+=1
           
            result["High"]+=1

        for s in result:
            result[s] = result[s]/trial
        self.fillDicts(data)
        
        return result

def isPlayerBetter(data):
    #function for hard AI mode to test if player input indicates player
    #got a good hand
    sumAI = getAIChipsSum(data)
    sumP = getPlayerChipsSum(data)
    m = getMaxPossibleInput(data)
    return sumP/m>=0.5

class TexasPokerPlayer(TexasPokerAI):
    #texas poker player inheritate TexasPokerAI class
    def initialize(self,data):
        #rewrite the initialize function
        if len(self.cards)<2:
            c = createNewValidCard(data)
            c.x = 100
            self.cards.append(c)

    def matchAI(self,data):
        #match the player
        diff = getAIChipsSum(data)-getPlayerChipsSum(data)
        while(diff>0):
            if diff>=100:
                data.playerChips.append(ChipOfHundred())
                diff-=100
            elif diff>=50:
                data.playerChips.append(ChipOfFifty())
                diff-=50
            else:
                data.playerChips.append(ChipOfTen())
                diff-=10

def getInputPercent(data):
    #Function to retrurn the current input percentage respect to total max
    AI = 0
    m = getMaxPossibleInput(data)
    for c in data.AIChips:
        AI += c.value
    return AI/m

##       Helper Functions for Texas Poker      ##
#################################################
def getAIChipsSum(data):
    #get all AI chips sum
    total = 0
    for c in data.AIChips:
        total += c.value
    return total

def getPlayerChipsSum(data):
    #get all Player chips sum
    total = 0
    for c in data.playerChips:
        total += c.value
    return total

def valueMatch(data):
    #return if the AI value matches Player value
    return getAIChipsSum(data)==getPlayerChipsSum(data)
        

#################
################# Helper functions for Texas Poker
#################
def initDicts(data):
    #initialize the dictionary
    data.playerSuit = dict()  #used to keep track of all public cards
    data.playerRank = dict()
    for i in range(1,14):
        data.playerRank[i] = 0
    for s in "cdhs":
        data.playerSuit[s] = 0 

def addTXCards(data):
    #add cards for texas table card
    if 2<len(data.TXTableCards)<5:
        c = createNewValidCard(data)
        data.TXTableCards.append(c)

def initializeTXGame(data):
    #initialize the texas poker first three table card
    if len(data.TXTableCards)<3:
        c = createNewValidCard(data)
        c.faceUp = True
        data.TXTableCards.append(c)

def fillDicts(data):
    #fill the dictionary
    initDicts(data)
    for c in data.TXTableCards:
        if c.faceUp == False:
            rank = c.rank
            suit = c.suit
            data.playerRank[rank] += 1
            data.playerSuit[suit] += 1
    for c in data.TXPlayer.cards:
        rank = c.rank
        suit = c.suit
        data.playerRank[rank]+=1
        data.playerSuit[suit]+=1
    
def findWinner(data):
    #Method used to compare who is winner
    playerInfo = data.TXPlayer.getHighestHands()
    AIInfo = data.AI.getHighestHands()
    playerOrder = getHandOrder(playerInfo)
    AIOrder = getHandOrder(AIInfo)
    if playerOrder>AIOrder:data.winner = "PLAYER"
    elif playerOrder<AIOrder:data.winner = "AI"
    else:
        w = None
        if playerOrder==0:
            w = getHighOrder(playerInfo[1],AIInfo[1])
        elif playerOrder==1:
            w = getPairOrder(playerInfo[1],AIInfo[1])
        elif playerOrder==2:
            w = getDoublePairOrder(playerInfo[1],AIInfo[1])
        elif playerOrder==3:
            w = getTripleOrder(playerInfo[1],AIInfo[1])
        elif playerOrder==4:
            w = getStraightOrder(playerInfo[1],AIInfo[1])
        elif playerOrder==5:
            w = getFlushingOrder(playerInfo[1],AIInfo[1])
        elif playerOrder==6:
            w = getFullHouseOrder(playerInfo[1],AIInfo[1])
        elif playerOrder==7:
            w = getFourOfKindOrder(playerInfo[1],AIInfor[1])
        elif playerOrder==8:
            w = getStraightOrder(playerInfo[1],AIInfo[1])

        #select winner            
        if w==None:
            data.winner = "TIE"
        elif w==1:
            data.winner = "PLAYER"
        elif w==2:
            data.winner = "AI"
        else:
            data.winner = "NONE"


###Function to find winner when the hand is equal
def getHighOrder(L1,L2):
    #case for high
    length = min(len(L1),len(L2))
    for i in range(length):
        if L1[i]==1:L1[i] = 14
        if L2[i]==1:L2[i] = 14
        if L1[i]!=L2[i]:
            if L1[i]>L2[i]:return 1
            elif L1[i]<L2[i]:return 2
    return None

def getPairOrder(L1,L2):
    #case for pair
    length = min(len(L1),len(L2))
    for i in range(length):
        if L1[i]==1:L1[i] = 14
        if L2[i]==1:L2[i] = 14
        if L1[i]!=L2[i]:
            if L1[i]>L2[i]:return 1
            elif L1[i]<L2[i]:return 2
    return None

def getDoublePairOrder(L1,L2):
    #case for double pair
    length = min(len(L1),len(L2))
    for i in range(length):
        if L1[i]==1:L1[i] = 14
        if L2[i]==1:L2[i] = 14
        if L1[i]!=L2[i]:
            if L1[i]>L2[i]:return 1
            elif L1[i]<L2[i]:return 2
    return None

def getTripleOrder(L1,L2):
    #case for triple
    length = min(len(L1),len(L2))
    for i in range(length):
        if L1[i]==1:L1[i] = 14
        if L2[i]==1:L2[i] = 14
        if L1[i]!=L2[i]:
            if L1[i]>L2[i]:return 1
            elif L1[i]<L2[i]:return 2
    return None

def getStraightOrder(L1,L2):
    #case for straight
    if L1>L2:return 1
    elif L1<L2:return 2
    else:
        return None

def getFlushingOrder(L1,L2):
    #case for flushing
    if L1>L2: return 1
    elif L1<L2: return 2
    else:return None

def getFullHouseOrder(L1,L2):
    #case for fullhouse
    if L1[0]>L2[0]:return 1
    elif L1[0]<L2[0]:return 2
    else:
        if L1[1]>L2[1]:return 1
        elif L1[1]<L2[1]:return 2
        else: return None

def getFourOfKindOrder(L1,L2):
    #case fourOfKind
    length = min(len(L1),len(L2))
    for i in range(length):
        if L1[i]==1:L1[i] = 14
        if L2[i]==1:L2[i] = 14
        if L1[i]!=L2[i]:
            if L1[i]>L2[i]:return 1
            elif L1[i]<L2[i]:return 2
    return None
    
def getHandOrder(info):
    #return the order of hand
    handRank = ["High","Pair","DoublePair","ThreeOfKind","Straight","Flushing",
                "FullHouse","FourOfKind","StraightFlush","RoyalFlush"]
    hand = info[0]
    for i in range(len(handRank)):
        if handRank[i] == hand:
            return i
    return 0
    

def drawSimulation(canvas,data):
    #draw the simulation with probability
    p = data.p
    handRank = ["High","Pair","DoublePair","ThreeOfKind","Straight","Flushing",
                "FullHouse","FourOfKind","StraightFlush","RoyalFlush"]
    x = 100
    y = 520
    for i in range(len(handRank)):
        s = handRank[i]
        y = 470 if i<5 else 500  #relocate the text
        comp = i*130 if i<5 else(i-5)*130
        canvas.create_text(x+comp,y,text="%s: %0.2f" %(s,p[s]),fill="cyan")
    
    
def getMaxPossibleInput(data):
    #return the ceiling of input at each round
    if len(data.TXTableCards)==3:
        for c in data.TXTableCards:
            if c.faceUp:
                return 300
        return 600
    if len(data.TXTableCards)==4:
        return 900
    if len(data.TXTableCards)==5:
        return 1200



##### ONLY USED FOR PLAYER TIPS #####
##### Several function sets to test the hands of Texas Poker #####
def isFlushing(data):
    #return if the hand is flushing
    for suit in data.playerSuit:
        if data.playerSuit[suit] >=5:
            return True
    return False

def isRoyalFlushing(data):
    #return if the hand is royal flushing
    if not isFlushing(data):return False
    if not data.playerRank[1]>=1: return False
    for i in range(10,14):
        if not data.playerRank[i]>=1:return False
    return True

def isFourOfKind(data):
    #return if the hand is fourofkind
    for rank in data.playerRank:
        if data.playerRank[rank]>=4:
            return True
    return False

def isStraightFlushing(data):
    #return if the hand is straightflushing
    return isFlushing(data) and isStraight(data)


def isStraight(data):
    #return if the hand is straight
    #special case with A
    if hasConsecutiveCard(data,10,13) and data.playerRank[1]>=1:return True

    for i in range(1,9):
        if hasConsecutiveCard(data,i,i+4):
            return True
    return False
    
def hasConsecutiveCard(data,start,end):
    #helper function for testing is Straight
    for i in range(start,end+1):
        if not data.playerRank[i]>=1:
            return False
    return True

def isDoublePair(data):
    #return if the hand is double pair
    pairs = 0
    for rank in data.playerRank:
        if data.playerRank[rank]>=2:
            pairs+=1
    return pairs>=2

def isPair(data):
    #return if the hand is pair
    for rank in data.playerRank:
        if data.playerRank[rank]>=2:
            return True
    return False

def isTriple(data):
    #return if the hand is triple
    for rank in data.playerRank:
        if data.playerRank[rank]>=3:
            return True
    return False

def isFullHouse(data):
    #return if the hand is fullhouse
    if not isTriple(data):return False
    triple = None
    for rank in data.playerRank:
        if data.playerRank[rank]>=3:
            triple = rank
    double = None
    for rank in data.playerRank:
        if data.playerRank[rank]>=2 and rank!=triple:
            double = rank
    return (triple!=None and double!=None)
        

### SNAKE FOR EARN MONEY ###
### Code from my Carnegie Mellon 15-112 F15 homework7 question 5
def initSnake(data):
    #For Snakes
    data.cellSize = 50    
    data.rows = 8
    data.cols = 12
    data.board = getStartBoard(data)
    placeFood(data)
    data.headRow = data.rows//2
    data.headCol = data.cols//2
    data.pause = True
    data.gameover = False
    data.drow = 0
    data.dcol = 1
    data.foodEat = 0
    data.highestScore = 0


def getStartBoard(data):
#create the board
    rows = data.rows
    cols = data.cols
    board = [[0]*cols for i in range(rows)]
    board[rows//2][cols//2] = 1
    return board

def snakeMousePressed(event,data):
#pause control
    data.pause = False

def snakeKeyPressed(event,data):
#key operation
    if(event.keysym=="r"):
        resetSnake(data)
    if(event.keysym=="p"):data.pause=True;return
    if (event.keysym=="Escape"):
        data.mode="SplashScreen"
        data.timerDelay = 150    #reset timer
        resetSnake(data)
    if (data.pause or data.gameover):return
    (drow,dcol)=(0,0)
    if (event.keysym=="Up"):
        (drow,dcol)=(-1,0)
        moveSnake(data,drow,dcol)
    if (event.keysym=="Down"):
        (drow,dcol)=(1,0)
        moveSnake(data,drow,dcol)
    if(event.keysym=="Left"):
        (drow,dcol)=(0,-1)
        moveSnake(data,drow,dcol)
    if(event.keysym=="Right"):
        (drow,dcol)=(0,1)
        moveSnake(data,drow,dcol)
    (data.drow,data.dcol) = (drow,dcol)
    
    
def snakeTimerFired(data):
#time control
    if(data.pause == True or data.gameover == True):return
    moveSnake(data,data.drow,data.dcol)
    
def snakeRedrawAll(canvas,data):
#redraw all snake
    drawBoard(canvas,data)
    drawGameOver(canvas,data)
    drawScore(canvas,data)

def resetSnake(data):
#reset the snake to initial condition
    data.board = getStartBoard(data)
    data.headRow = data.rows//2
    data.headCol = data.cols//2
    data.pause = True
    data.gameover = False
    placeFood(data)
    data.foodEat = 0

def getCellBound(data,row,col):
#calculate the cell bound
    gridWidth = data.cellSize
    gridHeight = data.cellSize
    boardWidth = data.cellSize * data.cols
    boardHeight = data.cellSize * data.rows
    marginX = data.width/2 - boardWidth/2
    marginY = data.height/2 - boardHeight/2
    x0 = marginX + gridWidth*col
    x1 = marginX + gridWidth*(col+1)
    y0 = marginY + gridHeight*row
    y1 = marginY + gridHeight*(row+1)
    return (x0,y0,x1,y1)

def drawCell(canvas,data,row,col):
#draw cell
    (x0,y0,x1,y1) = getCellBound(data,row,col)
    canvas.create_rectangle(x0,y0,x1,y1,fill="white")
    if data.board[row][col]>0:
        canvas.create_oval(x0,y0,x1,y1,fill="blue")
    elif data.board[row][col] == -1:
        canvas.create_oval(x0,y0,x1,y1,fill="green")
    
def drawBoard(canvas,data):
#draw the board
    board = data.board
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas,data,row,col)
    canvas.create_text(data.width/2,data.height-30,text = """
press mouse to begin, press"r" for restart, press"p" for pause
     eat to grow, stay on board, don't run into yourself
         change rows and cols from init data function
""")

def moveSnake(data,drow,dcol):
#function to move the snake
    (newHeadRow,newHeadCol) = (0,0)
    headRow = data.headRow
    headCol = data.headCol
    (newHeadRow,newHeadCol) = (headRow+drow,headCol+dcol)
    board = data.board
    if (newHeadRow>=data.rows or newHeadCol>=data.cols or
    newHeadRow < 0 or newHeadCol <0):
        data.gameover = True
        data.playerBank += 20*data.foodEat
    elif(board[newHeadRow][newHeadCol]>0):
        data.gameover = True
        data.playerBank += 20*data.foodEat
    elif(board[newHeadRow][newHeadCol]==-1):
        data.board[newHeadRow][newHeadCol] = data.board[headRow][headCol]+1
        (data.headRow,data.headCol) = (newHeadRow,newHeadCol)
        placeFood(data)
        data.foodEat += 1
    else:
        data.board[newHeadRow][newHeadCol] = data.board[headRow][headCol]+1
        (data.headRow,data.headCol) = (newHeadRow,newHeadCol)
        for row in range (data.rows):
             for col in range(data.cols):
                 if data.board[row][col]>0:
                     data.board[row][col] -= 1

def drawScore(canvas,data):
#function to draw the score
    if data.foodEat > data.highestScore:
        data.highestScore = data.foodEat
    text = "Score: " + str(data.foodEat)
    canvas.create_text(data.width/2,15,text = text, font = "Arial 20 bold")
    #draw the score at desired position
    highScore = "High Score: " + str(data.highestScore)
    canvas.create_text(data.width/2,40,text = highScore, fill = "pink",
                       font = "Arial 20 bold")
    canvas.create_text(data.width/2,80,
                       text = "Your earn 20 dollars by each food eat",
                       fill = "purple",
                       font = "Arial 16 italic")
    #draw the highest score at desired position

def drawGameOver(canvas,data):
#if game over, draw the game over
    if (data.gameover):
        canvas.create_text(data.width/2,data.height/2,text="game over!!",
                           fill = "red", font = "Arial 26 bold italic")
    
def placeFood(data):
#place the food on the board ramdomly
    row0 = random.randint(0,data.rows-1)
    col0 = random.randint(0,data.cols-1)
    for drow in range(data.rows):   #find next empty position
        for dcol in range(data.cols):
            row = (row0 + drow)%data.rows
            col = (col0 + dcol)%data.cols
            if data.board[row][col] == 0:
                data.board[row][col] = -1   #place food
                return 


####################################
# Animation FrameWork from Carnegie Mellon University 15-112
# from Event Based Animation part 3 event-example0.py
# URL: http://www.cs.cmu.edu/~112/notes/notes-animations.html
# Includes run() function
####################################

def run(width=800, height=600):
    #Run function from Carnegie Mellon University 15-112
    #Event Based Animation part 3 event-example0.py
    #URL: http://www.cs.cmu.edu/~112/notes/events-example0.py
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Create root before calling init (so we can create images in init)
    root = Tk()
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 250 # milliseconds

    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    init(data)
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")




###############################################################################
#######################################TEST CASE###############################

############### TEST TEXAS POKER AI ################
class Struct(object):pass
def testTXPokerAI():
    #Try to test if the AI is able to know its highest hand

    print("Testing Texas Poker AI class...",end="")
    testStraightFlushing()
    testIsFourOfKind()
    testIsFullHouse()
    testIsStraight()
    testIsFlushing()
    testIsDoublePair()
    testIsTriple()
    testIsPair()
    testGoodHand()
    print("pass!!!")
    
def testStraightFlushing():
    data = Struct()
    data.TXTableCards = []
    data.TXTableCards.append(Poker(30))
    data.TXTableCards.append(Poker(31))
    data.TXTableCards.append(Poker(32))
    data.TXTableCards.append(Poker(33))
    data.TXTableCards.append(Poker(34))
    TX = TexasPokerAI()
    TX.cards.append(Poker(35))
    TX.cards.append(Poker(36))
    TX.fillDicts(data)
    assert(TX.isStraightFlushing()==True)
    assert(TX.getHighestHands()==['StraightFlush', [7]])


def testIsFourOfKind():
    data = Struct()
    data.TXTableCards = []
    data.TXTableCards.append(Poker(3))
    data.TXTableCards.append(Poker(16))
    data.TXTableCards.append(Poker(29))
    data.TXTableCards.append(Poker(43))
    data.TXTableCards.append(Poker(43))
    TX = TexasPokerAI()
    TX.cards.append(Poker(42))
    TX.cards.append(Poker(36))
    TX.fillDicts(data)
    assert(TX.isFourOfKind()==True)
    assert(TX.getHighestHands()==['FourOfKind', [13, 4, 11, 4, 4, 4, 5, 5]])

def testIsFullHouse():
    data = Struct()
    data.TXTableCards = []
    data.TXTableCards.append(Poker(3))
    data.TXTableCards.append(Poker(16))
    data.TXTableCards.append(Poker(29))
    data.TXTableCards.append(Poker(4))
    data.TXTableCards.append(Poker(43))
    TX = TexasPokerAI()
    TX.cards.append(Poker(17))
    TX.cards.append(Poker(36))
    TX.fillDicts(data)
    assert(TX.isFullHouse()==True)
    assert(TX.getHighestHands()==['FullHouse', [5, 4]])

def testIsStraight():
    data = Struct()
    data.TXTableCards = []
    data.TXTableCards.append(Poker(3))
    data.TXTableCards.append(Poker(5))
    data.TXTableCards.append(Poker(7))
    data.TXTableCards.append(Poker(43))
    data.TXTableCards.append(Poker(43))
    TX = TexasPokerAI()
    TX.cards.append(Poker(17))
    TX.cards.append(Poker(19))
    TX.fillDicts(data)
    assert(TX.isStraight()==True)
    assert(TX.getHighestHands()==['Straight', [4]])

def testIsFlushing():
    data = Struct()
    data.TXTableCards = []
    data.TXTableCards.append(Poker(3))
    data.TXTableCards.append(Poker(5))
    data.TXTableCards.append(Poker(7))
    data.TXTableCards.append(Poker(43))
    data.TXTableCards.append(Poker(43))
    TX = TexasPokerAI()
    TX.cards.append(Poker(1))
    TX.cards.append(Poker(9))
    TX.fillDicts(data)
    assert(TX.isFlushing()==True)
    assert(TX.getHighestHands()==['Flushing', [10]])

def testIsDoublePair():
    data = Struct()
    data.TXTableCards = []
    data.TXTableCards.append(Poker(3))
    data.TXTableCards.append(Poker(16))
    data.TXTableCards.append(Poker(7))
    data.TXTableCards.append(Poker(10))
    data.TXTableCards.append(Poker(51))
    TX = TexasPokerAI()
    TX.cards.append(Poker(20))
    TX.cards.append(Poker(19))
    TX.fillDicts(data)
    assert(TX.isDoublePair()==True)
    assert(TX.getHighestHands()==['DoublePair', [8, 4, 13]])

def testIsTriple():
    data = Struct()
    data.TXTableCards = []
    data.TXTableCards.append(Poker(3))
    data.TXTableCards.append(Poker(5))
    data.TXTableCards.append(Poker(7))
    data.TXTableCards.append(Poker(42))
    data.TXTableCards.append(Poker(49))
    TX = TexasPokerAI()
    TX.cards.append(Poker(16))
    TX.cards.append(Poker(21))
    TX.fillDicts(data)
    assert(TX.isTriple()==True)
    assert(TX.getHighestHands()==['ThreeOfKind', [4, 11, 9]])

def testIsPair():
    data = Struct()
    data.TXTableCards = []
    data.TXTableCards.append(Poker(3))
    data.TXTableCards.append(Poker(5))
    data.TXTableCards.append(Poker(7))
    data.TXTableCards.append(Poker(11))
    data.TXTableCards.append(Poker(49))
    TX = TexasPokerAI()
    TX.cards.append(Poker(16))
    TX.cards.append(Poker(19))
    TX.fillDicts(data)
    assert(TX.isPair()==True)
    assert(TX.getHighestHands()==['Pair', [4, 12, 11, 8]])

def testGoodHand():
    data = Struct()
    data.TXTableCards = []
    data.TXTableCards.append(Poker(0))
    data.TXTableCards.append(Poker(5))
    data.TXTableCards.append(Poker(7))
    data.TXTableCards.append(Poker(49))
    data.TXTableCards.append(Poker(43))
    TX = TexasPokerAI()
    TX.cards.append(Poker(12))
    TX.cards.append(Poker(19))
    TX.fillDicts(data)
    assert(TX.getHighestHands()==['High', [14, 13, 11, 8, 7]])


############### TEST BLACK JACK CLASS ################

def testBlackJack():
    #Test if Black Jack Dealer and Player classes is able to get correct sum
    print("Testing Black Jack class...",end="")
    BJD = BlackJackDealer()
    BJP = BlackJackPlayer()
    BJD.cards.append(Poker(0))
    BJD.cards.append(Poker(11))
    assert(BJD.getDealerSum()==21)
    BJD.cards.append(Poker(2))
    assert(BJD.getDealerSum()==14)
    BJP.cards.append(Poker(9))
    BJP.cards.append(Poker(3))
    assert(BJP.getPlayerSum()==14)
    BJP.cards.append(Poker(4))
    assert(BJP.getPlayerSum()==19)
    BJP.cards.clear()
    BJP.cards.append(Poker(0))
    BJP.cards.append(Poker(8))
    assert(BJP.getPlayerSum()==20)
    BJP.cards.append(Poker(5))
    assert(BJP.getPlayerSum()==16)
    print("pass!!")
    
def testAll():
    testBlackJack()
    testTXPokerAI()   
#testAll()





#############################################
###               RUN THE GAME            ###
#############################################
playCasino()
