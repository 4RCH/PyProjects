import random, time

class Card(object):
    """ A card object storing the card value, suit and an accompanying label"""
    def __init__(self, value, suit, label):
        self.value = value
        self.suit = suit
        self.label = label
        self.shown = False

    def show(self,toggle):
        if toggle == True:	
            print(self.label)
        else:
            print("?", end="")


    def __repr__(self):
        return self.label


class Deck(list):
    """Creates and handles a standard deck of cards"""

    def __init__(self):
        self.cards = []
        self.suits = ["Spades", "Diamonds", "Hearts", "Clubs"]
        self.faceNames = ["Ace", "Jack", "Queen", "King"]
        self.build()

    def build(self):
        """ Builds the deck as a list that includes value, suit and composes a label"""
        for suit in range(0, len(self.suits)):
            for value in range(1, 14):
                if value == 1:
                    label = (self.faceNames[0] + " of " + self.suits[suit])
                elif value > 1 and value < 11:
                    label = (str(value) + " " + self.suits[suit])
                elif value == 11:
                    label = (self.faceNames[1] + " of " + self.suits[suit])
                    value = 10
                elif value == 12:
                    label = (self.faceNames[2] + " of " + self.suits[suit])
                    value = 10
                elif value == 13:
                    label = (self.faceNames[3] + " of " + self.suits[suit])
                    value = 10
                self.cards.append(Card(value, suit, label))

    def show(self):
        """Flags wether a card as facing down - may remove this"""
        for card in self.cards:
            card.show(False)
        #print("\nHere's the deck, it is a standard deck and has {0} cards.\n".format(len(self.cards)))
        #print (self.cards)

    def shuffle(self):
        """Shuffles a deck of cards"""
        for i in range(len(self.cards)-1, 0, -1):
            seed = random.randint(0, i)
            self.cards[i], self.cards[seed] = self.cards[seed], self.cards[i]

    def draw(self, numCards):
        """Draw x number of cards from the deck"""
        self.hand = []
        for i in range(numCards):
            cardDrawn = self.cards.pop()
            cardDrawn.shown = True
            self.hand.append(cardDrawn)
        return self.hand

    def cleanUp(self, p1, cpu):
        for i in range(0,len(p1.hand)):
            cardReturned = p1.hand.pop()
            cardReturned.shown = False
            self.cards.append(cardReturned)
        for i in range(0,len(cpu.hand)):
            cardReturned = cpu.hand.pop()
            cardReturned.shown = False
            self.cards.append(cardReturned)
        
        #try:
            #if len(self.cards) == 52:
                #print("things are all good, another game?")
        #except:
            #print("something went wrong")
        return


    def __repr__():
        return ("Card Stack")


class Player(object):

    def __init__(self):
        self.name = ""
        self.hand = []
        self.handVal = 0

    def drawHand(self, deck, numCards):
        self.hand = (deck.draw(numCards))
        return self.hand
    
    def drawX(self, deck, numCards):
        """Draw a card and add it to the player hand"""
        x = deck.draw(numCards)
        self.hand.append(x.pop())
        return self.hand

    def handValue(self):
        """Update the value of the players hand"""
        handTotal = 0
        for i in range(len(self.hand)):
            handTotal += self.hand[i].value
        print ("Hand value is: {}".format(handTotal))
        self.handVal = handTotal

    def show(self):
        """Show the hand and it's current value"""
        print(self.hand)
        self.handValue()
        
    def playerName(self):
        self.name = input("What would you like to be known as?\n>>>")
        return self.name


class game(object):
    """This is Blackjack"""
    def __init__(self):
        self.quit = False
        self.deck = Deck()
        self.deck.shuffle()
        self.cpu = Player()
        self.cpu.playerName = "The Dealer"
        self.drawOpt = ["hit", "stand", "double down", "split", "surrender"]
    
    def run(self):
        self.p1 = Player()
        self.p1.playerName()
        while not self.quit:
            self.deck.shuffle()
            print ("\nHold on I'm shuffling...")
            time.sleep(0.5)
            self.dealCards()
            self.validate()
            self.deck.cleanUp(self.p1,self.cpu)
    
    def dealCards(self):
        """Deal the initial hands to the player and the dealer"""
        print("OK {0} we're ready to go!\n".format(self.p1.name))        
        print("Here are your cards:")
        self.p1.drawHand(self.deck,2)
        self.p1.show()
        self.cpuDraw()
        
    
    def cpuDraw(self):
        """CPU draws cards - Currently only the initial hand"""
        print ("\nThe dealer has:")
        self.cpu.drawHand(self.deck,2)
        self.cpu.show()
    
    def drawOrStay(self):
        """User decisions"""
        self.playDes = 0
        time.sleep(0.5)
        print("\nWhat would you like to do next?\n",
              "[1 - Hit]\t",
              "[2 - Stand]\t",
              "[3 - Double Down]\t",
              "[4 - Split]\t",
              "[5 - Surrender]")

        draw = int(input("Type the option >>>"))
        try:
            userOpt = isinstance(draw, int)
            if userOpt and draw >= 1 and draw <= 5:
                if draw == 1:
                    self.p1.drawX(self.deck,1)
                    self.p1.show()
                    return self.drawOpt[0]
                elif draw == 2:
                    print ("So you're feeling lucky huh?")
                    return self.drawOpt[1]
                elif draw == 3:
                    print ("Doubling your bet huh? You won't be dealt anymore cards this game:")
                    self.p1.drawX(self.deck,1)
                    self.p1.show()
                    return self.drawOpt[2]
                elif draw == 4:
                    print ("Ooops, I still need to write the logic for this")
                    return self.drawOpt[3]
                elif draw == 5:
                    print ("Quitting early, maybe next hand.")
                    self.quit = True
            elif userOpt:
                print ("WARNING: I didn't give you that option *eyeroll*")
                self.quit = True
        except:
            print ("WARNING: That wasn't an option, get out!!!")
            self.quit = True
    
    def validate(self):
        """Check that the hand is higher than 2 and lower than 21"""
        while self.p1.handVal >= 2 and self.p1.handVal <= 20:
            self.drawOrStay()
        else:
            if self.p1.handVal == 21:
                print("You've won, take your money and get out of here!!!")
            else:
                print ("Game Over - Give me your money sucka!!!\n")
            


def main():
    newgame = game()
    newgame.run()
    pass


if __name__ == "__main__":
    main()
