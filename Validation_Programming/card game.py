import random
from random import shuffle

class Card:
    suits = ["hearts", "diamonds", "clubs", "spades"]
    #dictionary to map card ranks to their numerical values
    rank_values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 11, "Queen": 12, "King": 13, "Ace": 14}

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __lt__(self, other):
        #compare card ranks using the rank_values dictionary
        return Card.rank_values[self.rank] < Card.rank_values[other.rank] or (Card.rank_values[self.rank] == Card.rank_values[other.rank] and self.suit < other.suit)

    def __gt__(self, other):
        #compare card ranks using the rank_values dictionary
        return Card.rank_values[self.rank] > Card.rank_values[other.rank] or (Card.rank_values[self.rank] == Card.rank_values[other.rank] and self.suit > other.suit)

    def __str__(self): 
        #return string representation of the card
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.rank_values.keys()]
        shuffle(self.cards)
    
    def draw_card(self):
        return self.cards.pop() if self.cards else None

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = None  #initialize hand as None
        self.wins = 0  #initialize wins as 0

class Game:
    def __init__(self, player1_name, player2_name):
        self.deck = Deck()
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)
    
    def round_winner(self, winner):
        print(f"{winner} wins this round.")

    def draw(self, player1, player1_card, player2, player2_card):
        print(f"{player1} drew {player1_card}, while {player2} drew {player2_card}.")

    def start(self):
        print("Starting the game...")
        while len(self.deck.cards) >= 2:
            response = input("Press q to QUIT or Any key to PLAY: ")

            if response == "q":
                break

            player1_card = self.deck.draw_card()
            player2_card = self.deck.draw_card()
            self.draw(self.player1.name, player1_card, self.player2.name, player2_card)

            if player1_card > player2_card:
                self.player1.wins += 1
                self.round_winner(self.player1.name)
            else:
                self.player2.wins += 1
                self.round_winner(self.player2.name)

        if self.player1.wins != self.player2.wins:
            print(f"Game over, and the winner is: {self.game_winner()}")
        else:
            print("Game over, it is a Tie!")

    def game_winner(self):
        if self.player1.wins > self.player2.wins:
            return self.player1.name
        elif self.player2.wins > self.player1.wins:
            return self.player2.name

if __name__ == '__main__':
    player1_name = input("Enter the FIRST player's name: ")
    player2_name = input("Enter the SECOND player's name: ")
    game = Game(player1_name, player2_name)
    game.start()
