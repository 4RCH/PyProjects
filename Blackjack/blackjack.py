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
        self.face_names = ["Ace", "Jack", "Queen", "King"]
        self.build()

    def build(self):
        """ Builds the deck as a list that includes value, suit and composes a label"""
        for suit in range(0, len(self.suits)):
            for value in range(1, 14):
                if value == 1:
                    label = (self.face_names[0] + " of " + self.suits[suit])
                elif value > 1 and value < 11:
                    label = (str(value) + " of " + self.suits[suit])
                elif value == 11:
                    label = (self.face_names[1] + " of " + self.suits[suit])
                    value = 10
                elif value == 12:
                    label = (self.face_names[2] + " of " + self.suits[suit])
                    value = 10
                elif value == 13:
                    label = (self.face_names[3] + " of " + self.suits[suit])
                    value = 10
                self.cards.append(Card(value, suit, label))

    def show(self):
        """Flags wether a card as facing down - may remove this"""
        for card in self.cards:
            card.show(False)
        print("\nHere's the deck, it is a standard deck and has {0} cards.\n".format(len(self.cards)))
        print (self.cards)

    def shuffle(self):
        """Shuffles a deck of cards"""
        for i in range(len(self.cards)-1, 0, -1):
            seed = random.randint(0, i)
            self.cards[i], self.cards[seed] = self.cards[seed], self.cards[i]

    def draw(self, numCards):
        """Draw x number of cards from the deck"""
        self.hand = []
        for i in range(numCards):
            card_drawn = self.cards.pop()
            card_drawn.shown = True
            self.hand.append(card_drawn)
        return self.hand

    def clean_up(self, p1, cpu):
        for player in [p1, cpu]:
            while player.hand:
                card_Returned = player.hand.pop()
                card_Returned.shown = False
                self.cards.append(card_Returned)
        return

    def __repr__(self):
        return ("Card Stack")

class Player(object):

    def __init__(self):
        self.name = ""
        self.hand = []
        self.hand_value = 0

    def draw_hand(self, deck, card_quantity):
        self.hand = (deck.draw(card_quantity))
        return self.hand
    
    def draw_x(self, deck, numCards):
        """Draw a card and add it to the player hand"""
        new_cards = deck.draw(numCards)
        self.hand.extend(new_cards)
        return self.hand

    def calculate_hand_value(self):
        """Update the value of the players hand"""
        x = 0
        ace_count = 0
        for card in self.hand:
            x += card.value
            if card.label.startswith("Ace"):
                ace_count += 1
        while x > 21 and ace_count:
            x -= 10
            ace_count -= 1
        self.hand_value = x
        print ("Hand value is: {}".format(self.hand_value))

    def show(self):
        """Show the hand and it's current value"""
        print(self.hand)
        self.calculate_hand_value()
        
    def player_name(self):
        self.name = input("What would you like to be known as?\n>>>")
        return self.name

class Game(object):
    """This is Blackjack"""
    def __init__(self):
        self.quit = False
        self.deck = Deck()
        self.deck.shuffle()
        self.cpu = Player()
        self.cpu.name = "The Dealer"
        self.draw_option = ["hit", "stand", "double down", "split", "surrender"]
    
    def run(self):
        self.p1 = Player()
        self.p1.player_name()
        while not self.quit:
            self.deck.shuffle()
            print ("\nHold on I'm shuffling...")
            time.sleep(0.5)
            self.deal_cards()
            self.validate()
            self.deck.clean_up(self.p1,self.cpu)
    
    def deal_cards(self):
        """Deal the initial hands to the player and the dealer"""
        print("OK {0} we're ready to go!\n".format(self.p1.name))        
        print("Here are your cards:")
        self.p1.draw_hand(self.deck,2)
        self.p1.show()
        self.cpu_draw()

    def cpu_draw(self):
        """CPU draws cards - Currently only the initial hand"""
        print ("\nThe dealer has:")
        self.cpu.draw_hand(self.deck,2)
        self.cpu.show()

    def draw_or_stay(self):
        """User decisions"""
    
        time.sleep(0.5)
        print("\nWhat would you like to do next?\n",
              "[1 - Hit]\t",
              "[2 - Stand]\t",
              "[3 - Double Down]\t",
              "[4 - Split]\t",
              "[5 - Surrender]")

        try:
            draw = int(input("Type the option >>>"))
            if draw == 1:
                self.p1.draw_x(self.deck,1)
                self.p1.show()
                return self.draw_option[0]
            elif draw == 2:
                print ("So you're feeling lucky huh?")
                return self.draw_option[1]
            elif draw == 3:
                print ("Doubling your bet huh? You won't be dealt anymore cards this game:")
                self.p1.draw_x(self.deck,1)
                self.p1.show()
                return self.draw_option[2]
            elif draw == 4:
                if len(self.p1.hand) == 2 and self.p1.hand[0].value == self.p1.hand[1].value:
                    print ("Splitting your hand...")
                    self.p1.draw_x(self.deck, 1)
                    self.p1.draw_x(self.deck, 1)
                    self.p1.show()
                    return self.draw_option[3]
                else:
                    print("You can't split this hand.")
                    return self.draw_option[3]
            elif draw == 5:
                print ("Quitting early, maybe next hand.")
                self.quit = True
            else:
                print ("WARNING: I didn't give you that option *eyeroll*")
                self.quit = True
        except ValueError:
            print ("WARNING: That wasn't an option, get out!!!")
            self.quit = True

    def dealerTurn(self):
        while self.cpu.hand_value < 17:
            self.cpu.draw_x(self.deck, 1)
            self.cpu.calculate_hand_value()
        print("\nDealer's final hand")
        self.cpu.show()

    def validate(self):
        """Check that the hand is higher than 2 and lower than 21"""
        while self.p1.hand_value >= 2 and self.p1.hand_value <= 20:
            action = self.draw_or_stay()
            if action == "stand":
                break
        else:
            if self.p1.hand_value == 21:
                print("You've won, take your money and get out of here!!!")
                return
            elif self.p1.hand_value > 21:
                print ("Game Over - You busted!!!")
                return

        self.dealerTurn()

        if self.cpu.hand_value > 21 or self.p1.hand_value >self.cpu.hand_value:
            print("you've won, take your money and get out of here!!!")
        elif self.p1.hand_value < self.cpu.hand_value:
            print("Game Over - Dealer wins!!!")
        else:
            print("it's a tie!")

def main():
    newgame = Game()
    newgame.run()
    pass

if __name__ == "__main__":
    main()
