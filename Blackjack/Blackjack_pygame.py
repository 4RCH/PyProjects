import pygame
import sys
from blackjack import Game, Player

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack Game")

# Load card images (assuming you have images for each card)
CARD_WIDTH, CARD_HEIGHT = 100, 150
card_back = pygame.image.load('images/card_back.png')
card_back = pygame.transform.scale(card_back, (CARD_WIDTH, CARD_HEIGHT))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up fonts
font = pygame.font.SysFont(None, 36)

class BlackjackGUI:
    def __init__(self):
        self.game = Game()
        self.game.p1 = Player()
        self.game.p1.name = "Player"
        self.game.deck.shuffle()
        self.game.deal_cards()
        self.run_game()

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def draw_card(self, card, x, y):
        # Placeholder for drawing a card
        # You should load and draw the actual card image here
        pygame.draw.rect(win, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT))
        self.draw_text(card.label, font, BLACK, win, x + 5, y + 5)

    def draw_hand(self, hand, x, y):
        for i, card in enumerate(hand):
            self.draw_card(card, x + i * (CARD_WIDTH + 10), y)

    def run_game(self):
        running = True
        while running:
            win.fill(GREEN)

            # Draw dealer's hand
            self.draw_text("Dealer's Hand:", font, WHITE, win, 50, 50)
            self.draw_hand(self.game.cpu.hand, 50, 100)

            # Draw player's hand
            self.draw_text("Your Hand:", font, WHITE, win, 50, 300)
            self.draw_hand(self.game.p1.hand, 50, 350)

            # Draw buttons
            hit_button = pygame.Rect(600, 100, 150, 50)
            stand_button = pygame.Rect(600, 200, 150, 50)
            pygame.draw.rect(win, WHITE, hit_button)
            pygame.draw.rect(win, WHITE, stand_button)
            self.draw_text("Hit", font, BLACK, win, 625, 115)
            self.draw_text("Stand", font, BLACK, win, 625, 215)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hit_button.collidepoint(event.pos):
                        self.game.p1.draw_x(self.game.deck, 1)
                        if self.game.p1.hand_value > 21:
                            messagebox.showinfo("Game Over", "You busted!")
                            self.new_game()
                    if stand_button.collidepoint(event.pos):
                        self.game.dealerTurn()
                        if self.game.cpu.hand_value > 21 or self.game.p1.hand_value > self.game.cpu.hand_value:
                            messagebox.showinfo("Game Over", "You win!")
                        elif self.game.p1.hand_value < self.game.cpu.hand_value:
                            messagebox.showinfo("Game Over", "Dealer wins!")
                        else:
                            messagebox.showinfo("Game Over", "It's a tie!")
                        self.new_game()

            pygame.display.flip()
        pygame.quit()
        sys.exit()

    def new_game(self):
        self.game = Game()
        self.game.p1 = Player()
        self.game.p1.name = "Player"
        self.game.deck.shuffle()
        self.game.deal_cards()

if __name__ == "__main__":
    BlackjackGUI()