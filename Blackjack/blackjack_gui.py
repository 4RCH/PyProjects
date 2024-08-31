import tkinter as tk
from tkinter import messagebox
from blackjack import Game, Player

class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Game")
        self.game = Game()

        self.setup_ui()

    def setup_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.dealer_label = tk.Label(self.frame, text="Dealer's Hand")
        self.dealer_label.grid(row=0, column=0, padx=10, pady=10)

        self.dealer_hand = tk.Label(self.frame, text="")
        self.dealer_hand.grid(row=0, column=1, padx=10, pady=10)

        self.player_label = tk.Label(self.frame, text="Your Hand")
        self.player_label.grid(row=1, column=0, padx=10, pady=10)

        self.player_hand = tk.Label(self.frame, text="")
        self.player_hand.grid(row=1, column=1, padx=10, pady=10)

        self.hit_button = tk.Button(self.frame, text="Hit", command=self.hit)
        self.hit_button.grid(row=2, column=0, padx=10, pady=10)

        self.stand_button = tk.Button(self.frame, text="Stand", command=self.stand)
        self.stand_button.grid(row=2, column=1, padx=10, pady=10)

        self.new_game_button = tk.Button(self.frame, text="New Game", command=self.new_game)
        self.new_game_button.grid(row=3, column=0, padx=10, pady=10)

        self.new_game()

    def new_game(self):
        self.game = Game()
        self.game.p1 = Player()
        self.game.p1.name = "Player"
        self.game.deck.shuffle()
        self.game.deal_cards()
        self.update_ui()
    
    def hit(self):
        self.game.p1.draw_x(self.game.deck, 1)
        self.update_ui()
        if self.game.p1.hand_value > 21:
            messagebox.showinfo("Game Over", "You busted!")
            self.new_game()
        
    def stand(self):
        self.game.dealerTurn()
        self.update_ui()
        if self.game.cpu.hand_value > 21 or self.game.p1.hand_value > self.game.cpu.hand_value:
            messagebox.showinfo("Game Over", "You win!")
        elif self.game.p1.hand_value < self.game.cpu.hand_value:
            messagebox.showinfo("Game Over", "Dealer wins!")
        else:
            messagebox.showinfo("Game Over", "It's a tie!")
        self.new_game()
        
    def update_ui(self):
        self.dealer_hand.config(text=str(self.game.cpu.hand))
        self.player_hand.config(text=str(self.game.p1.hand))

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()