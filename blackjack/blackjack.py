import random
import os
import time

class Blackjack:
    heart = "\u2665"
    spade = "\u2660"
    diamond = "\u2666"
    club = "\u2663"

    suits = {
        "diamond": diamond,
        "heart": heart,
        "spade": spade,
        "club": club
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
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
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
            result += f"{card['rank']}{suit}"

        return result.strip()
    
    def deal_card(self):
        card = self.deck.pop()
        if card["rank"] == "cut":
            self.cut_card = True
            card = self.deck.pop()
        
        return card

    def player_turn(self, player_stats, action):
        if action == "h":
            player_stats["hand"].append(self.deal_card())
            player_stats["hand_val"] = Blackjack.update_hand_val(player_stats["hand"])
            print(Blackjack.format_cards(player_stats["hand"]))

        # elif action == "sp":
        # elif action == "dd":

        else:
            print("Unknown move, try again")

    def dealer_turn(self):
        print(f"Dealer has {Blackjack.format_cards(self.dealer['hand'])}")

        while self.dealer["hand_val"] < 17: 
            self.dealer["hand"].append(self.deal_card())
            self.dealer["hand_val"] = Blackjack.update_hand_val(self.dealer["hand"])

            print("Dealer hits")
            print(f"Dealer:{Blackjack.format_cards(self.dealer['hand'])}, Hand Value: {self.dealer['hand_val']}")

    @staticmethod
    def update_hand_val(hand):
        value = 0
        aces = 0

        for card in hand:
            card_val = card["rank"]

            if card_val == "A":
                value += 11 
                aces += 1

            elif card_val in ["10", "J", "Q", "K"]:
                value += 10

            else:
                value += int(card_val)

        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value
            
    @staticmethod
    def place_bet(bet, player, player_stats):
        player_stats["cur_bet"] = bet
        player_stats["bal"] -= bet

    @staticmethod
    def hand_status(hand_val):
        if hand_val > 21:
            return True

        return False

    def game_results(self, player, player_stats):
        if Blackjack.hand_status(self.dealer["hand_val"]):
            print(f"Dealer busts, {player} wins ${2*player_stats['cur_bet']}")
            player_stats["bal"] += 2*player_stats["cur_bet"] 

        elif player_stats["hand_val"] > self.dealer["hand_val"]:
            print(f'{player} wins ${2*player_stats["cur_bet"]}')
            player_stats["bal"] += 2*player_stats["cur_bet"] 

        elif player_stats["hand_val"] == self.dealer["hand_val"]:
            print(f'{player} ties with dealer, player wins ${player_stats["cur_bet"]}')
            player_stats["bal"] += player_stats["cur_bet"] 

        else:
            print(f'{player} loses ${player_stats["cur_bet"]}')

    def reset_round(self):
        for player in self.players.values():
            player["hand"] = []
            player["cur_bet"] = 0
            player["hand_val"] = 0
            player["insurance"] = False

        self.dealer["hand"] = []
        self.dealer["hand_val"] = 0

    # def insurance(self, self.players):
    #     for player, player_stats in self.players:
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
    #             for player, player_stats in self.players:
    #                 if player_stats["insurance"] != True and player_stats["hand_val"] != 21:
    #                     player_stats["bal"] -= player_stats["cur_bet"]

    #             return True

    #         else:
    #             print("No 21, game continue")
    #             return False

    def main(self):
        exit = False       
        while not exit:
            cur_players = self.players.copy()
            
            if self.cut_card:
                self.shuffle_deck()

        
            for player_stats in self.players.values():
                print(player_stats)

            # ask players for bet amounts
            for player, player_stats in self.players.items():
                while True:
                    bet = int(input(f"{player}, how much do you want to bet (min $1): "))

                    if bet < 1:
                        print("Min bet not reached or invalid bet amount, try again")

                    else:
                        Blackjack.place_bet(bet, player, player_stats) 
                        break

            # give players and dealer their cards and sum hand value
            for i in range(2):
                for player_stats in self.players.values():
                    card = self.deal_card()
                    player_stats["hand"].append(card)
                    player_stats["hand_val"] = Blackjack.update_hand_val(player_stats["hand"])

                card = self.deal_card()
                self.dealer["hand"].append(card)
                self.dealer["hand_val"] = Blackjack.update_hand_val(self.dealer["hand"])

            # display players cards and dealer cards
            for player, player_stats in self.players.items():
                player_hand = Blackjack.format_cards(player_stats["hand"])
                print(f"{player}: {player_hand}")
            
            dealer_hand = Blackjack.format_cards([self.dealer["hand"][0]])
            print(f"Dealer: {dealer_hand}")   

            # do insurance
            # if dealer_hand[0]["rank"] == "Ace":
            #     if self.insurance(self.players):
            #         exit = True
            #         # add a way to end the game and reset everyones hands

            for player, player_stats in self.players.items():
                while True:
                    action = input(f"{player}, what's your move (s/h): ")

                    if action == "s":
                        break

                    if action == "h":
                        self.player_turn(player_stats, action)
                        
                        if Blackjack.hand_status(player_stats["hand_val"]):
                            print(f'{player} busts at {player_stats["hand_val"]}')
                            del cur_players[player]
                            break
                        
                        player_hand = Blackjack.format_cards(player_stats["hand"])
                        player_hand_val = player_stats["hand_val"]
                        print(f"{player}'s hand: {player_hand}, hand value: {player_hand_val}")

            if cur_players:
                self.dealer_turn()

                for player in cur_players:
                    self.game_results(player, self.players[player])
                    print(Blackjack.format_cards(self.players[player]["hand"]))

                print(f"Dealer:{Blackjack.format_cards(self.dealer['hand'])}, Hand Value: {self.dealer['hand_val']}")
            else:
                print("Everyone busts, round end")
            
            self.reset_round()

if __name__ == "__main__":
    # set up game settings
    os.system("cls")
    num_of_players = int(input("How many players?: "))
    num_of_decks = int(input("How many decks?: "))
    game = Blackjack(num_of_decks, num_of_players)
    game.main()