#CS112  Term Project

from tkinter import *
import random
import copy


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
        #return the corresponding card
        return data.cardImages[self.cardRank]

    def drawPoker(self,data,canvas,position):
        if self.faceUp==False:
            image = self.getPlayingCardImage(data)
            (left,top) = position
            canvas.create_image(left, top, anchor=NW, image=image)
        else:
            image = data.cardImages[52]
            (left,top) = position
            canvas.create_image(left, top, anchor=NW, image=image)
            

    def __eq__(self,other):
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
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
        if len(self.cards)<2:          
            card1 = createNewValidCard(data)
            (card1.x,card1.y)=(0,100)
            if len(self.cards)>0:
                card1.faceUp = True
            self.cards.append(card1)


    def drawDealer(self,canvas,data):
        if data.runDealer == True:
            canvas.create_text (550,65,text = str(self.getDealerSum()),
                                fill = "white",font = "bold 28")
        p = 60
        for card in self.cards:
            position = (p+card.x,card.y)
            card.drawPoker(data,canvas,position)
            p += 80

    def getDealerSum(self):
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
                    currSum+=11
        return currSum

    def runDealer(self,data):
        if(self.getDealerSum()<17):
            newCard = createNewValidCard(data)
            newCard.y = 100
            self.cards.append(newCard)
        
        

def findSumOfA(currSum,numOfA):
    for i in range(numOfA,-1,-1):
        if currSum+i*11+(numOfA-i)*1<22:
            return i*11+(numOfA-i)*1
    return numOfA*1
     

class BlackJackPlayer(object):
    def __init__(self):
        self.cards = []

    def initializeBJPlayer(self,data):
        if len(self.cards)<2:
            card1 = createNewValidCard(data)
            (card1.x,card1.y)=(0,400)
            self.cards.append(card1)

    def drawPlayer(self,canvas,data):
        canvas.create_text (550,355,text = str(self.getPlayerSum()),
                                fill = "white",font = "bold 28")
        p = 60
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
        Asum = findSumOfA(currSum,numOfA)
        return currSum+Asum

    def addCard(self,data):
        if self.getPlayerSum()<21 and len(self.cards)>=2:
            card1 = createNewValidCard(data)
            (card1.x,card1.y) = (0,400)
            self.cards.append(card1)
            
        

class Chip(object):
    def __init__(self):
        self.x = 400
        self.y = 300

    def draw(self,canvas):
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
        self.y -= 50

    def moveDown(self):
        self.y += 50

    def moveRight(self):
        self.x += 50


class ChipOfTen(Chip):
    def __init__(self):
        super().__init__()
        self.value = 10


class ChipOfFifty(Chip):
    def __init__(self):
        super().__init__()
        self.value = 50

    def draw(self,canvas):
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
    def __init__(self):
        super().__init__()
        self.value = 100

    def draw(self,canvas):
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

        
        

    

    
        
        

        
        









#### FROM LECTURE NOTES ####
def init(data):
    data.mode = "SplashScreen"
    data.timerDelay = 500
    data.backgroundImage = PhotoImage(file="Casino-1.gif")
    loadPlayingCardImages(data) # always load images in init!
    data.playerBank = 500
    initSnake(data)
    initBJ(data)
    initTX(data)

def loadPlayingCardImages(data):
#Pre-Load all card image from default file
    cards = 55 # cards 1-52, back, joker1, joker2
    data.cardImages = [ ]
    for card in range(cards):
        rank = (card%13)+1
        suit = "cdhsx"[card//13]
        filename = "playing-card-gifs/%s%d.gif" % (suit, rank)
        data.cardImages.append(PhotoImage(file=filename))

def mousePressed(event, data):
#mouse control
    if data.mode =="Snake":
        snakeMousePressed(event,data)
    if data.mode =="BJ":
        blackJackMousePressed(event, data)
    if data.mode=="TX":
        TXMousePressed(event,data)
        

def keyPressed(event, data):
    if data.mode == "SplashScreen":
        splashScreenKeyPressed(event,data)
    if data.mode =="Snake":
        snakeKeyPressed(event,data)
    if data.mode=="BJ":
        blackJackKeyPressed(event, data)
    if data.mode=="TX":
        TXKeyPressed(event,data)

def timerFired(data):
#time control
    if data.mode =="Snake":
        snakeTimerFired(data)
    if data.mode=="BJ":
        blackJackTimerFired(data)
    if data.mode=="TX":
        TXTimerFired(data)
    
def redrawAll(canvas, data):
#redraw based on the mode
    if data.mode == "SplashScreen":splashScreenRedrawAll(canvas,data)
    if data.mode == "BJ":blackJackRedrawAll(canvas, data)
    if data.mode == "Snake":snakeRedrawAll(canvas,data)
    if data.mode=="TX":TXRedrawAll(canvas,data)

#####################################################        
### Splash Screen ###
def splashScreenMousePressed(event,data):pass  #no mouse action
def splashScreenKeyPressed(event,data):
    if (event.keysym=="1"):
        data.mode = "TX"
        data.timerDelay = 100
        initTX(data)
    if (event.keysym=="2"):
        data.mode = "BJ"
        initBJ(data)
        data.timerDelay = 100
    if (event.keysym=="3"):
        data.mode = "Snake"
        data.timerDelay = 500
    if (event.keysym=="Escape"):data.mode = "SplashScreen"
def splashScreenTimerFired(data):pass
def splashScreenRedrawAll(canvas,data):
    canvas.create_image(0, 0,anchor=NW, image=data.backgroundImage)
    canvas.create_text(data.width/2,340,text="CASINO",fill="white",
                       font = "Cambria 28 bold")
    canvas.create_text(data.width/2,data.height-90,
                       text="""
1 -> Texas Poker
2 -> Black Jack
3 -> Snake
4 -> Instruction""", fill = "white", font = "Cambria 15 italic")


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@### BLACK JACK  #######
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@### BLACK JACK  #######
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@### BLACK JACK  #######
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@### BLACK JACK  #######

def initBJ(data):    
    data.step = 0
    data.addChip = True
    data.initialize = False
    data.runDealer = False
    data.countMoney = True
    data.counter = 0
    data.PlayerCards = []
    data.BJDealer = BlackJackDealer()
    data.BJPlayer = BlackJackPlayer()
    data.BJbackground = PhotoImage(file="B-J.gif")
    data.BJgameover = False
    data.winner = None
    data.chips = []
    data.input = 0
    data.drawTip = False
    data.split = False
    data.doSplit = False

def doubleChips(data):
    exist = copy.deepcopy(data.chips)
    for c in exist:
        data.chips.append(c)

    
def blackJackMousePressed(event, data):
    #click on start
    if 50<event.x<100 and 450<event.y<500 and len(data.chips)==0:
        data.drawTip = True
        
    if 50<event.x<100 and 450<event.y<500 and len(data.chips)>0:
        data.initialize = True
        data.addChip = False

    if 100<event.x<150 and 450<event.y<500 and data.BJgameover:
        initBJ(data)
        
    #click on adding chips
    if data.addChip:
        if 50<event.x<100 and 100<event.y<150:
            data.drawTip = False
            data.chips.append(ChipOfTen())
            data.input+=10
        if 50<event.x<100 and 150<event.y<200:
            data.chips.append(ChipOfFifty())
            data.input+=50
            data.drawTip = False
        if 50<event.x<100 and 200<event.y<250:
            data.drawTip = False
            data.chips.append(ChipOfHundred())
            data.input+=100

    if 50<event.x<120 and 300<event.y<350 and len(data.BJDealer.cards)==2:
        #when ready to go for game
        data.runDealer = True
        data.BJDealer.cards[1].faceUp=False

    if 50<event.x<120 and 350<event.y<400:
        #add new card by player
        data.BJPlayer.addCard(data)
        if data.BJPlayer.getPlayerSum()>21:
            data.BJgameover = True
            data.winner = "DEALER"
            data.counter = 20

    if (120<event.x<190 and 300<event.y<350
        and len(data.BJDealer.cards)==2 and len(data.BJPlayer.cards)==2):
        doubleChips(data)
        data.BJPlayer.addCard(data)
        if data.BJPlayer.getPlayerSum()>21:
            data.BJgameover = True
            data.winner = "DEALER"
        data.BJDealer.cards[1].faceUp = False
        data.runDealer = True

    #case for split
    

        
    

def blackJackKeyPressed(event, data):
    if event.keysym=="Escape":
        data.mode = "SplashScreen"
        data.timerDelay = 500
    if event.keysym=="r":initBJ(data)
    if data.BJgameover: return
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



def blackJackTimerFired(data):
    #case when gameover
    if data.BJgameover==True and data.counter>18:
        for c in data.chips:
            if data.winner=="DEALER":
                c.moveUp()
                if data.countMoney:
                    data.playerBank-=data.input;data.countMoney=False
            elif data.winner=="PLAYER":
                c.moveDown()
                if data.countMoney:
                    data.playerBank+=data.input;data.countMoney=False
            else:
                c.moveRight()
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
            data.initialize=False
            if data.BJPlayer.cards[0].rank == data.BJPlayer.cards[1].rank:
                data.split = True
                
    for card in data.BJDealer.cards:
        if card.x<200:
            card.x+=100
    for card in data.BJPlayer.cards:
        if card.x<200:card.x+=100

    #case when dealer is running
    if data.runDealer==True:
        data.counter +=1
        if data.counter%8==0:
            data.BJDealer.runDealer(data)
        if data.BJDealer.getDealerSum()>=17:
            data.BJgameover = True
            dscore = data.BJDealer.getDealerSum()
            pscore = data.BJPlayer.getPlayerSum()
            if dscore>21 or (dscore<pscore and pscore<=21):
                data.winner = "PLAYER"
            elif (pscore<dscore and dscore<=21) or pscore>21:
                data.winner = "DEALER"
            else:
                data.winner = "TIE"
        
            
            
def relocateChips(data):
    start = 250
    for i in range(len(data.chips)):
        data.chips[i].x = start+i*50
    

def blackJackRedrawAll(canvas, data):
    
    canvas.create_image(0, 0,anchor=NW, image=data.BJbackground)
    #draw the player score
    canvas.create_rectangle(720,0,800,40,fill="green")
    canvas.create_text(760,20,text = "$"+str(data.playerBank))
    drawBJButton(canvas,data)
    data.BJDealer.drawDealer(canvas,data)
    data.BJPlayer.drawPlayer(canvas,data)
    if len(data.chips)>0 and data.winner!="TIE":
        relocateChips(data)
    for c in data.chips:
        c.draw(canvas)
    if data.drawTip == True:
        canvas.create_text(data.width/2,data.height/2,text="Please Bet Before Start", fill="yellow")
    if data.BJgameover == True:
        canvas.create_text(data.width/2,data.height/2
                           ,text = "%s WIN!!!" %(data.winner)
                           ,fill = "red"
                           ,font = "bold 28")


def drawBJButton(canvas,data):
    canvas.create_rectangle(50,450,100,500,fill = "yellow")
    canvas.create_text(75,475,text = "START")

    canvas.create_rectangle(100,450,150,500,fill="yellow")
    canvas.create_text(125,475,text=
"""
NEW
GAME
""")
    
    canvas.create_rectangle(50,100,100,150,fill="yellow")
    canvas.create_text(75,125,text = "+10")
    canvas.create_rectangle(50,150,100,200,fill="yellow")
    canvas.create_text(75,175,text = "+50")
    canvas.create_rectangle(50,200,100,250,fill="yellow")
    canvas.create_text(75,225,text = "+100")

    canvas.create_rectangle(50,300,120,350,fill="pink")
    canvas.create_text(85,325,text="STAND")
    canvas.create_rectangle(50,350,120,400,fill="pink")
    canvas.create_text(85,375,text="ADD")

    canvas.create_rectangle(120,300,190,350,fill="pink")
    canvas.create_text(155,325,text="DOUBLE")

    if data.split:
        canvas.create_rectangle(120,350,190,400,fill="pink")
        canvas.create_text(155,375,text="SPLIT")
    
    
    








#@@@@@@@@@@TEXAS POKER@@@@@@@@@@@@@@@@@@
    #WWWWWWWWWWWW

def initTX(data):
    data.TXPlayerCards = []
    data.PlayerCards = []   #used to keep track of all the existing cards
    data.fillDict = True
    data.TXbackground = PhotoImage(file="BJ.gif")


    #add cards for testing
    data.TXPlayerCards.append(Poker(2))
    data.TXPlayerCards.append(Poker(15))
    data.TXPlayerCards.append(Poker(28))
    data.TXPlayerCards.append(Poker(12))
    data.TXPlayerCards.append(Poker(29))
    data.TXPlayerCards.append(Poker(50))
    data.TXPlayerCards.append(Poker(49))

    initDicts(data)

def TXMousePressed(event,data):
    if 100<event.x<150 and 300<event.y<350:
        if data.fillDict == True:
            fillDicts(data)
            data.fillDict = False
    if 100<event.x<180 and 450<event.y<500:
        data.fillDict = True
        initDicts(data)
        data.TXPlayerCards.clear()
        data.PlayerCards.clear()
        for i in range(7):
            data.TXPlayerCards.append(createNewValidCard(data))
    
def TXKeyPressed(event,data):
    if event.keysym=="Escape":data.mode = "SplashScreen"
    if event.keysym=="r":initTX(data)
    if event.keysym=="p":
        print(data.playerSuit)
        print(data.playerRank)


def TXTimerFired(data):pass
def TXRedrawAll(canvas,data):
    canvas.create_image(0, 0,anchor=NW, image=data.TXbackground)
    drawTXButton(canvas,data)
    drawTXTexts(canvas,data)
    x = 200
    y = 100
    for c in data.TXPlayerCards:
        position = (x,y)
        c.drawPoker(data,canvas,position)
        x+=80
        if x>520:
            y = 200
            x = 300

def drawTXButton(canvas,data):
    canvas.create_rectangle(100,300,150,350,fill="yellow")
    canvas.create_text(125,325,text = "READY")

    canvas.create_rectangle(100,450,180,500,fill="yellow")
    canvas.create_text(140,475,text="RANDOM")

def drawTXTexts(canvas,data):
    canvas.create_text(400,500,text = "TEXAS POKER",fill = "white",font = "bold 28")
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



##Helper Functions for Texas Poker
def initDicts(data):
    data.playerSuit = dict()
    data.playerRank = dict()
    for i in range(1,14):
        data.playerRank[i] = 0
    for s in "cdhs":
        data.playerSuit[s] = 0

def fillDicts(data):
    for c in data.TXPlayerCards:
        rank = c.rank
        suit = c.suit
        data.playerRank[rank] += 1
        data.playerSuit[suit] += 1

def isFlushing(data):
    for suit in data.playerSuit:
        if data.playerSuit[suit] >=5:
            return True
    return False

def isRoyalFlushing(data):
    if not isFlushing(data):return False
    if not data.playerRank[1]>=1: return False
    for i in range(10,14):
        if not data.playerRank[i]>=1:return False
    return True

def isFourOfKind(data):
    for rank in data.playerRank:
        if data.playerRank[rank]>=4:
            return True
    return False

def isStraightFlushing(data):
    return isFlushing(data) and isStraight(data)


def isStraight(data):
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
    pairs = 0
    for rank in data.playerRank:
        if data.playerRank[rank]>=2:
            pairs+=1
    return pairs>=2

def isPair(data):
    for rank in data.playerRank:
        if data.playerRank[rank]>=2:
            return True
    return False

def isTriple(data):
    for rank in data.playerRank:
        if data.playerRank[rank]>=3:
            return True
    return False

def isFullHouse(data):
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
        






























###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@### BLACK JACK  #######
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@### BLACK JACK  #######
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@### BLACK JACK  #######
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@### BLACK JACK  #######
### SNAKE ###
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
        data.timerDelay = 500    #reset timer
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
        data.playerBank += 10*data.foodEat
    elif(board[newHeadRow][newHeadCol]>0):
        data.gameover = True
        data.playerBank += 10*data.foodEat
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
# use the run function as-is
####################################

def run(width=800, height=600):
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
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 600)
