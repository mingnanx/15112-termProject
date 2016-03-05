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
        self.v = random.randint(40,60)

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
        self.y -= self.v

    def moveDown(self):
        self.y += self.v

    def moveRight(self):
        self.x += self.v


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
    data.counter = 0
    data.TXTableCards = []  #for the table cards
    data.PlayerCards = []   #used to keep track of all the existing cards
    data.TXbackground = PhotoImage(file="BJ.gif")
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
    data.AIDifficulty = "Hard"
    data.dPause = True

def TXMousePressed(event,data):
    if data.TXgameover:
        if 100<event.x<180 and 400<event.y<450:
            initTX(data)
        return
    
    if data.addChip:
        if 50<event.x<100 and 100<event.y<150:
            data.playerChips.append(ChipOfTen())
            data.input+=10
        if 50<event.x<100 and 150<event.y<200:
            data.playerChips.append(ChipOfFifty())
            data.input+=50
        if 50<event.x<100 and 200<event.y<250:
            data.drawTip = False
            data.playerChips.append(ChipOfHundred())
    if 50<event.x<100 and 250<event.y<300:
        data.TXgameover = True
        data.winner = "AI"

    if 100<event.x<150 and 300<event.y<350:
        data.AI.makeDecision(data)
        if data.AI.decision=="FOLD":
            data.TXgameover = True
            data.winner = "PLAYER"

    if 50<event.x<100 and 300<event.y<350:
        data.initializePlayer = True


    
    if (150<event.x<200 and 300<event.y<350 and len(data.TXPlayer.cards)>1):
        if not valueMatch(data):
            print("Please Match")
            return
        
        if len(data.TXTableCards)<3:

            data.initializeGame = True
            data.addChip = True        

        elif len(data.TXTableCards)==3 and data.flip == False:
            data.flip = True
        else:
            if len(data.TXTableCards)<5:
                addTXCards(data)
                data.AI.fillDicts(data)
                data.TXPlayer.fillDicts(data)
                fillDicts(data)
                
            else:
                findWinner(data)
                data.TXgameover = True




        
    
def TXKeyPressed(event,data):
    if event.keysym=="Escape":data.mode = "SplashScreen"
    if event.keysym=="r":initTX(data)
    if event.keysym=="w":
        data.AI.getHighestHands()
        print(data.AI.hand)
    if event.keysym=="s":
        print(data.AI.simulateGame(data))
    if event.keysym=="p":
        print(valueMatch(data))
    
    
    if event.keysym=="q":
        for c in data.AI.allCards:
            c.faceUp = False
        
    return




def TXTimerFired(data):
    data.counter = data.counter+1 if data.counter<16 else 0
    
    if data.TXgameover==True:
        for c in data.playerChips:
            if data.winner=="PLAYER":
                c.moveDown()
            elif data.winner=="AI":
                c.moveUp()
            else:c.moveRight()
            if c.x<0 or c.x>800 or c.y<0 or c.y>600:
                data.playerChips.remove(c)
        for c in data.AIChips:
            if data.winner=="PLAYER":
                c.moveDown()
            elif data.winner=="AI":
                c.moveUp()
            else:c.moveRight()
            if c.x<0 or c.x>800 or c.y<0 or c.y>600:
                data.AIChips.remove(c)
        

        
    #case for the beginning stage
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
            data.addChip = True
        data.TXPlayer.fillDicts(data)
        data.AI.fillDicts(data)


    ##case for initializing game   
    if data.initializeGame and valueMatch(data):
        if data.counter == 2:
            initializeTXGame(data)
        if data.counter == 9:
            initializeTXGame(data)
        if len(data.TXTableCards)>=3:
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
    
     #case to move all the cards

    for c in data.TXTableCards:
        if c.x<200:
            c.x += 100

    for c in data.AI.cards:
        if c.x>600:
            c.x-=100
    if valueMatch(data):
        for c in data.TXPlayer.cards:
            if c.x<200:
                c.x+=100

    
def relocateChipsTX(data):
    start = 150
    for i in range(len(data.playerChips)):
        data.playerChips[i].x = start+i*20
        data.playerChips[i].y = 230

    for i in range(len(data.AIChips)):
        data.AIChips[i].x = 3*start+i*20
        data.AIChips[i].y = 260

def TXRedrawAll(canvas,data):
    canvas.create_image(0, 0,anchor=NW, image=data.TXbackground)
    drawTXButton(canvas,data)
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
        
    if data.winner!=None:
        canvas.create_text(400,250,text=data.winner+" WIN!!!",
                           font = "bold 30",fill="pink")

    
        


def drawTXButton(canvas,data):
    canvas.create_rectangle(100,300,150,350,fill="yellow")
    canvas.create_text(125,325,text = "READY")

    canvas.create_rectangle(100,450,180,500,fill="yellow")
    canvas.create_text(140,475,text="REMATCH")
    canvas.create_rectangle(150,300,200,350,fill="blue")
    canvas.create_text(175,325,text="NEXT")
    canvas.create_rectangle(50,100,100,150,fill="yellow")
    canvas.create_text(75,125,text = "+10")
    canvas.create_rectangle(50,150,100,200,fill="yellow")
    canvas.create_text(75,175,text = "+50")
    canvas.create_rectangle(50,200,100,250,fill="yellow")
    canvas.create_text(75,225,text = "+100")
    canvas.create_rectangle(50,250,100,300,fill="grey")
    canvas.create_text(75,275,text="FOLD")
    canvas.create_rectangle(50,300,100,350,fill = "cyan")
    canvas.create_text(75,325,text="START")

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



class TexasPokerAI(object):
    def __init__(self):
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
        if len(self.cards)<2:
            c = createNewValidCard(data)
            c.x = 800
            c.faceUp = True
            self.cards.append(c)

    def clearDict(self):
        for i in range(1,14):
            self.rank[i] = 0
        for s in "cdhs":
            self.suit[s] = 0
        
    def fillDicts(self,data):
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
        for suit in self.suit:
            if self.suit[suit]>=5:
                return True
        return False

    def getFlushingNum(self):
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
        return max(nums)

    def isRoyalFlushing(self):
        if not self.isFlushing():return False
        if not self.rank[1]>=1:return False
        for i in range(10,14):
            if not self.rank[i]>=1: return False
        return True

    def isFourOfKind(self):
        for rank in self.rank:
            if self.rank[rank]>=4:
                return True
        return False

    def getFourOfKindNum(self):
        four = None
        for r in self.rank:
            if self.r >=4:
                four = r
        result = []
        if four==1:four = 14
        result.append(four)
        for c in self.allCards:
            if c.rank!=four:
               result.append(c.rank)
        return result

    def isStraight(self):
        if self.hasConsecutiveCard(10,13) and self.rank[1]>=1:
            return True
        for i in range(1,9):
            if self.hasConsecutiveCard(i,i+4):
                return True
        return False

    def getStraightNum(self):
        if self.hasConsecutiveCard(10,13) and self.rank[1]>=1:
            return 10
        start = None
        for i in range(1,9):
            if self.hasConsecutiveCard(i,i+4):
                start = i
        return start


    def isStraightFlushing(self):
        return self.isFlushing() and self.isStraight()

    def isDoublePair(self):
        pairs = 0
        for rank in self.rank:
            if self.rank[rank]>=2:pairs+=1
        return pairs>=2

    def getDoublePairNum(self):
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
        return pairs+[max(nums)]
    
    def hasConsecutiveCard(self,start,end):
        #helper function for testing straight case
        for i in range(start,end+1):
            if not self.rank[i]>=1:
                return False
        return True

    def isPair(self):
        for rank in self.rank:
            if self.rank[rank]>=2:
                return True
        return False

    def getPairNum(self):
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
        for rank in self.rank:
            if self.rank[rank]>=3:
                return True
        return False

    def getTripleNum(self):
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
        print(self.isPair(),self.isTriple(),self.isDoublePair(),
              self.isStraight(), self.isFlushing(),self.isFullHouse())
    

    def getHighestHands(self):
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
        
    def makeDecisionEasy(self,data):
        info = self.getHighestHands()
        order = getHandOrder(info)
        if len(data.TXTableCards)<4:
            data.AIChips.append(ChipOfTen())
            return
        if order<1:
            
            self.decision = random.choice(["FOLD","RAISE"])
            if self.decision=="FOLD":return
            else:data.AIChips.append(ChipOfTen())
        else:
            self.decision = "RAISE"
            if order<2:
                data.AIChips.append(random.choice([ChipOfTen(),ChipOfFifty()]))
            elif order<4:
                data.AIChips.append(random.choice([ChipOfFifty()
                                                  ,ChipOfHundred()]))
            else:
                data.AIChips.append(ChipOFHundred())

    def makeDecision(self,data):
        if data.AIDifficulty=="Easy":
            self.makeDecisionEasy(data)
        if data.AIDifficulty=="Hard":
            self.makeDecisionHard(data)

    def makeDecisionHard(self,data):
        p = self.simulateGame(data)
        if p["RoyalFlush"]!=0:
            for i in range(5):
                data.AIChips.append(random.choice([ChipOfFifty()
                                                   ,ChipOfHundred()]))
        elif p["StraightFlush"]!=0:
            for i in range(4):
                data.AIChips.append(random.choice([ChipOfFifty(),
                                                   ChipOfHundred(),
                                                   ChipOfTen()]))

        elif p["FourOfKind"]>0.001:
            for i in range(3):
                data.AIChips.append(random.choice([ChipOfFifty(),
                                                   ChipOfHundred(),
                                                   ChipOfTen()]))

        elif p["Pair"]>0.4:
            for i in range(2):
                data.AIChips.append(random.choice([ChipOfFifty(),
                                                   ChipOfHundred(),
                                                   ChipOfTen()]))
        
        else:
            self.decision = random.choice(["FOLD","RAISE"])
            if self.decision=="FOLD":return
            else:
                data.AIChips.append(random.choice([ChipOfTen(),ChipOfFifty()]))
        
        
            

    


    #Series of Function to get largest possible at this time
    def simulateGame(self,data):
        result = dict()
        handRank = ["High","Pair","DoublePair","ThreeOfKind","Straight","Flushing",
                "FullHouse","FourOfKind","StraightFlush","RoyalFlush"]
        for s in handRank:
            result[s] = 0
        trial = 10000
        for i in range(trial):
            self.fillSimulationDicts(data)
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








class TexasPokerPlayer(TexasPokerAI):
    def initialize(self,data):
        if len(self.cards)<2:
            c = createNewValidCard(data)
            c.x = 100
            self.cards.append(c)
            
        


##Helper Functions for Texas Poker

def getAIChipsSum(data):
    total = 0
    for c in data.AIChips:
        total += c.value
    return total

def getPlayerChipsSum(data):
    total = 0
    for c in data.playerChips:
        total += c.value
    return total

def valueMatch(data):
    return getAIChipsSum(data)==getPlayerChipsSum(data)
        


def initDicts(data):
    data.playerSuit = dict()  #used to keep track of all public cards
    data.playerRank = dict()
    for i in range(1,14):
        data.playerRank[i] = 0
    for s in "cdhs":
        data.playerSuit[s] = 0

def addTXCards(data):
    if 2<len(data.TXTableCards)<5:
        c = createNewValidCard(data)
        data.TXTableCards.append(c)

def initializeTXGame(data):
    if len(data.TXTableCards)<3:
        c = createNewValidCard(data)
        c.faceUp = True
        data.TXTableCards.append(c)

def fillDicts(data):
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
    


#Method used to compare who is winner
def findWinner(data):
    playerInfo = data.TXPlayer.getHighestHands()
    print(playerInfo)
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
            
        
        if w==None:
            data.winner = "TIE"
        elif w==1:
            data.winner = "PLAYER"
        elif w==2:
            data.winner = "AI"
        else:
            data.winner = "NONE"

def getHighOrder(L1,L2):
    length = min(len(L1),len(L2))
    for i in range(length):
        if L1[i]==1:L1[i] = 14
        if L2[i]==1:L2[i] = 14
        if L1[i]!=L2[i]:
            if L1[i]>L2[i]:return 1
            elif L1[i]<L2[i]:return 2
    return None

def getPairOrder(L1,L2):
    length = min(len(L1),len(L2))
    for i in range(length):
        if L1[i]==1:L1[i] = 14
        if L2[i]==1:L2[i] = 14
        if L1[i]!=L2[i]:
            if L1[i]>L2[i]:return 1
            elif L1[i]<L2[i]:return 2
    return None

def getDoublePairOrder(L1,L2):
    length = min(len(L1),len(L2))
    for i in range(length):
        if L1[i]==1:L1[i] = 14
        if L2[i]==1:L2[i] = 14
        if L1[i]!=L2[i]:
            if L1[i]>L2[i]:return 1
            elif L1[i]<L2[i]:return 2
    return None

def getTripleOrder(L1,L2):
    length = min(len(L1),len(L2))
    for i in range(length):
        if L1[i]==1:L1[i] = 14
        if L2[i]==1:L2[i] = 14
        if L1[i]!=L2[i]:
            if L1[i]>L2[i]:return 1
            elif L1[i]<L2[i]:return 2
    return None

def getStraightOrder(L1,L2):
    if L1>L2:return 1
    elif L1<L2:return 2
    else:
        return None

def getFlushingOrder(L1,L2):
    if L1>L2: return 1
    elif L1<L2: return 2
    else:return None

def getFullHouseOrder(L1,L2):
    if L1[0]>L2[0]:return 1
    elif L1[0]<L2[0]:return 2
    else:
        if L1[1]>L2[1]:return 1
        elif L1[1]<L2[1]:return 2
        else: return None

def getFourOfKindOrder(L1,L2):
    length = min(len(L1),len(L2))
    for i in range(length):
        if L1[i]==1:L1[i] = 14
        if L2[i]==1:L2[i] = 14
        if L1[i]!=L2[i]:
            if L1[i]>L2[i]:return 1
            elif L1[i]<L2[i]:return 2
    return None
    
    

def getHandOrder(info):
    handRank = ["High","Pair","DoublePair","ThreeOfKind","Straight","Flushing",
                "FullHouse","FourOfKind","StraightFlush","RoyalFlush"]
    hand = info[0]
    for i in range(len(handRank)):
        if handRank[i] == hand:
            return i
    return 0
    






















#####ONLY USED FOR PLAYER TIPS
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
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@### SNAKE  #######
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@### Snake #######
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
