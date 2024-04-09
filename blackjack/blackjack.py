import random
import os

class Blackjack:
    heart = "\u2665"
    spade = "\u2660"
    diamond = "\u2666"
    club = "\u2663"

    suits = {
        "diamonds": diamond,
        "hearts": heart,
        "spades": spade,
        "clubs": club
    }

    def __init__(self, num_decks = 1, num_players = 1, start_bal = 10):
        self.num_decks = num_decks
        self.deck = self.create_deck(self.num_decks)
        self.cut_card = False
        self.players = {f"Player{i+1}": {"bal": start_bal, 
                                        "hand" : [], 
                                        "cur_bet" : 0,
                                        "hand_val": 0,
                                        "insurance": False } for i in range(num_players)}
        self.dealer = {"hand" : [], "hand_val": 0}
        
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
        self.cut_card = False

        return deck
    
    def shuffle_deck(self):
        self.deck = self.create_deck(self.num_decks)

    def display_deck(self):
        for card in self.deck:
            print(f"{card['rank']} of {card['suit']}")

        print(self.deck)

    @staticmethod
    def format_cards(cards):
        result = ""
        for card in cards:
            suit = Blackjack.suits[card["suit"]]
            result += f"{card['number']}{suit} "

        return result.strip()
    
    def deal_card(self):
        card = self.deck.pop()
        if card["rank"] == "cut":
            self.cut_card = True
            card = self.deck.pop()

        return card

    def player_turn(self, player, action):
        if action == "h":
            self.player["hand"].append(self.deal_card())
            self.player["hand_val"] = self.update_hand_val(self.player["hand"])

        # elif action == "sp":

        # elif action == "dd":

        else:
            print("Unknown move, try again")

    def dealer_turn(self):
        dealer = self.dealer
        print(dealer["hand"])

        while dealer["hand_val"] < 17:
            print("Dealer hits")
            card = self.deck.pop()

            if card["rank"] == "cut":
                self.cut_card = True
                card = self.deck.pop()

            self.update_hand_val(dealer, card)
            dealer["hand"].append(card)
            print(dealer["hand"])

        if dealer["hand_val"] > 21:
            print("Dealer bust")
        else:
            print("Dealer stands")

        return

    @staticmethod
    def update_hand_val(self, hand):
        value = 0
        aces = 0

        for card in hand:
            card_val = card["rank"]

            if card_val == "Ace":
                value += 11 
                aces += 1

            elif card_val in ["10", "Jack", "Queen", "King"]:
                value += 10

            else:
                value += int(card_val)

        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    # def insurance(self, cur_players):
    #     for player, player_stats in cur_players:
    #         # ask for insurance
    #         while True:
    #             ans = input(f"{player}, do you want insurance (Y/N): ")
    #             if ans == "Y":
    #                 player_stats["cur_bet"] *= 1.5
    #                 player_stats["insurance"] = True

    #             elif ans == "N":
    #                 break

    #             else:
    #                 print("Invalid response, answer again")

    #         if self.dealer["hand_val"] == 21:
    #             for player, player_stats in cur_players:
    #                 if player_stats["insurance"] != True and player_stats["hand_val"] != 21:
    #                     player_stats["bal"] -= player_stats["cur_bet"]

    #             return True

    #         else:
    #             print("No 21, game continue")
    #             return False
            
    def reset_round(self):
        for player, player_stats in self.players.items():
            player_stats["hand"] = []
            player_stats["cur_bet"] = 0
            player_stats["hand_val"] = 0
            player_stats["insurance"] = False

        self.dealer["hand"] = []
        self.dealer["hand_val"] = 0

    def main(self):
        exit = False       
        while not exit:
            if self.cut_card:
                self.shuffle_deck()
            
            cur_players = self.players

            # ask players for bet amounts
            for player, player_stats in cur_players.items():
                while True:
                    bet = int(input(f"{player}, how much do you want to bet (min $1): "))

                    if bet < 1:
                        print("Min bet not reached or invalid bet amount, try again")

                    else:
                        print(f"{player} bets ${bet}")
                        player_stats["cur_bet"] = bet
                        player_stats["bal"] -= bet
                        break

            # give players and dealer their cards and sum hand value
            for i in range(2):
                for player_stats in cur_players.items():
                    card = self.deal_card()
                    player_stats["hand"].append(card)
                    player_stats["hand_val"] = Blackjack.update_hand_val(player_stats["hand"])

                card = self.deal_card
                self.dealer["hand"].append(card)
                self.dealer["hand_val"] = Blackjack.update_hand_val(self.dealer["hand"])

            # display players cards and dealer cards
            for player, player_stats in cur_players.items():
                player_hand = Blackjack.format_cards(player_stats["hand"])
                print(f"{player}: {player_hand}")
            
            dealer_hand = Blackjack.format_cards(self.deal_card["hand"][0])
            print(f"Dealer: {dealer_hand}, Unknown")   

            # do insurance
            # if dealer_hand[0]["rank"] == "Ace":
            #     if self.insurance(cur_players):
            #         exit = True
            #         # add a way to end the game and reset everyones hands

            cur_players_temp = cur_players.copy() # temp dictionary for modifying purposes
            for player, player_stats in cur_players_temp.items():
                while True:
                    action = input("What's your move (s/h): ")

                    if action == "s":
                        print("Stands")

                    if action == "h":
                        self.player_turn(player_stats, player_stats["hand"])
                        
                        if player_stats["hand_val"] > 21:
                            print(f'{player} busts at {player_stats["hand_val"]}')
                            del cur_players[player]
                            break
                        
                        player_hand = Blackjack.format_cards(player_stats["hand"])
                        player_hand_val = player_stats["hand_val"]
                        print("Hits")
                        print(f"{player}'s hand: {player_hand}, hand value: {player_hand_val}")

            self.dealer_turn()

            if cur_players:
                for player, player_stats in cur_players.items():
                    print(f"{player}, {player_stats}")
                    if self.dealer["hand_val"] > 21 or player_stats["hand_val"] > self.dealer["hand_val"]:
                        print(f'{player} wins')
                        player_stats["bal"] += 2*player_stats["cur_bet"] 

                    elif player_stats["hand_val"] == self.dealer["hand_val"]:
                        print(f'{player} ties with dealer, player wins ${player_stats["cur_bet"]}')

                    else:
                        print(f'{player} loses ${player_stats["cur_bet"]}')

                    print(f"{player}, {player_stats}")

            else:
                print("Everyone busts, round end")

            self.reset_round()

    def player_status(hand_val):
        if hand_val > 21:

            

if __name__ == "__main__":
    # set up game settings
    os.system("cls")
    num_of_players = int(input("How many players?: "))
    num_of_decks = int(input("How many decks?: "))
    game = Blackjack(num_of_decks, num_of_players)
    game.main()