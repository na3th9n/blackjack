import random

class Blackjack:
    # each suit has a style
    suits = ["diamond", "heart", "spade", "club"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    suits = {
        "diamond" : suits[0],
        "heart" : suits[1],
        "spade" : suits[2],
        "club" : suits[3]
    }

    def __init__(self, num_decks = 1, num_players = 1, start_bal = 10):
        # initialize deck
        self.deck = self.create_deck(num_decks)
        self.cut_card = False
        
        # init players and dealer 
        self.players = {f"Player{i+1}": {"bal": start_bal, 
                                          "hand" : [], 
                                          "cur_bet" : 0, } for i in range(num_players)}
        self.dealer = {"hand" : []}
        


    def create_deck(self, num_decks):
        # create a new deck if the game just started or if the cut card was hit
        suits = ["diamond", "heart", "spade", "club"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        deck = [{"rank":rank, "suit":suit} for _ in range(num_decks) for rank in ranks for suit in suits]
        random.shuffle(deck)

        # find random index for cut card
        last_quarter_index = (len(deck) // 4)
        insert_index = random.randint(last_quarter_index, len(deck) - 10)

        # insert cut card at random index
        deck.insert(insert_index, {"rank": "cut", "suit": None})

        return deck
    
    def shuffle_deck(self, num_decks):
        self.deck = self.create_deck(num_decks)

    def display_deck(self):
        for card in self.deck:
            print(f"{card['rank']} of {card['suit']}")

        print(self.deck)

    def player_turn(self):
        pass

    def dealer_turn(self):
        pass

    def insurance(self):
        # dealer_hand = self.dealer["hand"]
        pass

    def main(self):
        # self.display_deck()
        # initialize deck
        exit = False

        num_decks = 2
        turns = 2

        self.create_deck(num_decks)        
        # deal cards, pop cards and send to player and then dealer
        
        while not exit:
            if self.cut_card:
                self.shuffle_deck(num_decks)
            
            dealer_hand = self.dealer["hand"]
            # give all players and dealer their cards
            for i in range(turns):
                for i, player in enumerate(self.players):
                    # draw a card and check if it is cut
                    card = self.deck.pop()
                    if card["rank"] == "cut":
                        self.cut_card = True
                        card = self.deck.pop()
                    
                    player_hand = self.players[f"Player{i+1}"]["hand"]
                    player_hand.append(card)
                
                dealer_hand.append(self.deck.pop())

            # display players cards and dealer cards
            for player, player_stats in self.players.items():
                player_hand = player_stats["hand"] 
                print(f"{player}: {player_hand}")

            print(f"Dealer: {dealer_hand[0]}, Unknown")   
            print(len(self.deck))

            exit = True 

            # if self.dealer_hands[0]["rank"] == "Ace":
            #     # ask player for insurance
            #     answered = False
            #     while not answered:
            #     ans = input("Do you want insurance?(Y/N)": )

            #     if ans == "Y":

        # player turn
        # dealer turn 


if __name__ == "__main__":
    game = Blackjack(2, 4)
    game.main()