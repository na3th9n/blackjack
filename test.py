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
                                        "cur_bet" : [],
                                        "hand_val": [],
                                        "bust" : False,
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

    def player_turn(self, player_stats, action, hand_index):
        if action == "sp":
            sp_hands = [[player_stats["hand"][hand_index][0]], [player_stats["hand"][hand_index][1]]]

            for hand in sp_hands:
                card = self.deal_card()
                hand.append(card)
                
            # update current hand with split hand 1
            player_stats["hand"][hand_index] = sp_hands[0]
            player_stats["hand_val"][hand_index] = Blackjack.update_hand_val(player_stats["hand"][hand_index])

            # insert split hand 2 into hand array attribute
            player_stats["hand"].insert(hand_index+1, sp_hands[1])
            player_stats["hand_val"].insert(hand_index+1, Blackjack.update_hand_val(player_stats["hand"][hand_index+1]))

        if action == "dd":
            bet = player_stats["cur_bet"][hand_index]
            Blackjack.add_to_bet(bet, player_stats, hand_index)   

        player_stats["hand"][hand_index].append(self.deal_card())
        player_stats["hand_val"][hand_index] = Blackjack.update_hand_val(player_stats["hand"][hand_index])

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
    def place_bet(bet, player_stats):
        player_stats["cur_bet"].append(bet)
        player_stats["bal"] -= bet

    @staticmethod
    def add_to_bet(bet, player_stats, bet_index):
        player_stats["cur_bet"][bet_index] += bet
        player_stats["bal"] -= bet

    @staticmethod
    def hand_status(hand_val):
        if hand_val > 21:
            return True

        return False

    def game_results(self, player, player_stats):
        profit = sum(player_stats["cur_bet"])

        for i in range(len(player_stats["hand"])):
            cur_bet = player_stats["cur_bet"][i]
            hand_val = player_stats["hand_val"][i]
            dealer_hand_val = self.dealer["hand_val"]

            if Blackjack.hand_status(hand_val):
                print(f'{player} loses ${cur_bet} due to bust')
                profit -= cur_bet

            elif Blackjack.hand_status(dealer_hand_val):
                print(f"{player}'s hand wins due to dealer bust")
                player_stats["bal"] += 2*cur_bet 
                profit += cur_bet 

            elif hand_val > dealer_hand_val:
                print(f"{player} wins due to higher than dealer hand")
                player_stats["bal"] += 2*cur_bet
                profit += cur_bet

            elif hand_val == dealer_hand_val:
                print(f"{player} pushes")
                player_stats["bal"] += cur_bet

            else:
                print(f'{player} loses ${cur_bet} due to lower cards')
                profit -= cur_bet
        
        return profit

    def reset_round(self):
        for player in self.players.values():
            player["hand"] = []
            player["cur_bet"] = []
            player["hand_val"] = []
            player["insurance"] = False
            player["bust"] = False

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

            # ask players for how many hands they want to play and bet amounts
            for player, player_stats in self.players.items():
                    if player_stats["bal"] < 1:
                            print(f'{player} has insufficent funds, add more money to account to play')
                            del cur_players[player]
                            continue
                    
                    while True:
                        hands = int(input(f"{player}, how many hands do you want to play?: "))

                        if player_stats["bal"] < hands:
                            print("Insufficent funds to play that many hands, enter a lower amount")
                        
                        else:
                            break

                    for _ in range(hands):
                        player_stats["hand"].append([])
                        player_stats["hand_val"].append(-1)


                    for i in range(hands):
                        while True:
                            bet = int(input(f"{player}, how much do you want to bet for hand {i + 1} (min $1)?: "))

                            if bet < 1 or bet > player_stats["bal"]:
                                print("Insufficent funds or incorrect input, try again")

                            else:
                                Blackjack.place_bet(bet, player_stats) 
                                break
            
            

            # give players and dealer their cards and sum hand value
            for i in range(2):
                for player_stats in self.players.values():
                    for i in range(len(player_stats["hand"])):
                        card = self.deal_card()
                        player_stats["hand"][i].append(card)
                        player_stats["hand_val"][i] = Blackjack.update_hand_val(player_stats["hand"][i])

                card = self.deal_card()
                self.dealer["hand"].append(card)
                self.dealer["hand_val"] = Blackjack.update_hand_val(self.dealer["hand"])

            # display players cards and dealer cards
            for player, player_stats in self.players.items():
                for hand_index, hand in enumerate(player_stats["hand"]):
                    hand = Blackjack.format_cards(hand)
                    print(f"{player}, hand {hand_index + 1}: {hand}")
            
            dealer_hand = Blackjack.format_cards([self.dealer["hand"][0]])
            print(f"Dealer: {dealer_hand}")   

            # do insurance
            player_stats["hand_val"][hand_index] = Blackjack.update_hand_val(player_stats["hand"][hand_index])
            


            if dealer_hand["rank"] in ["10", "J", "Q", "K", "A"]:
                self.dealer["hand_val"] = Blackjack.update_hand_val(self.dealer["hand"])
                dealer_hand_val = self.dealer["hand_val"]

                if dealer_hand_val == 21:
                    if dealer_hand == "A":
                        pass
                        # insurance
                    
                    else:
                        print("Dealer Natural 21")

            for player, player_stats in self.players.items():
                num_of_busts = 0

                for hand_index, hand in enumerate(player_stats["hand"]):
                    cur_hand = Blackjack.format_cards(hand)
                    print(f"{player}, hand {hand_index + 1}: {cur_hand}")
                    
                    while True:
                        action = input(f"{player}, what's your move (s/h/dd/sp): ")
                        if action == "s":           
                            break

                        elif action == "h" or action == "dd":
                            if player_stats["bal"] < player_stats["cur_bet"][hand_index] * 2 and action == "dd":
                                print("Not enough money to double down")
                                continue
                            
                            self.player_turn(player_stats, action, hand_index)          

                        elif action == "sp" and player_stats["bal"] < (player_stats["cur_bet"][hand_index] * 2):
                            print("h2i")
                            if player_stats["hand"][0]["rank"] == player_stats["hand"][1]["rank"]:
                                self.player_turn(player_stats, action, hand_index)

                        else:
                            print("Invalid response, try again")
                            continue

                        if Blackjack.hand_status(player_stats["hand_val"][hand_index]):
                            print(f'{player} busts at {player_stats["hand_val"][hand_index]}')
                            num_of_busts += 1
                            break
                        
                        player_hand = Blackjack.format_cards(player_stats["hand"][hand_index])
                        player_hand_val = player_stats["hand_val"][hand_index]
                        print(f"{player}'s hand: {player_hand}, hand value: {player_hand_val}")

                        if action == "dd":
                            break
                    
                    if num_of_busts == len(player_stats["hand"]):
                        player_stats["bust"] = True

            all_bust = all(player.get("bust", False) for player in self.players.values())

            if all_bust:
                print("All players bust, round ends")

            else:
                self.dealer_turn()

            for player, player_stats in self.players.items():
                profit = self.game_results(player, player_stats)
                print(f"{player} wins ${profit}")
            
            print(f"Dealer:{Blackjack.format_cards(self.dealer['hand'])}, Hand Value: {self.dealer['hand_val']}")

            # check if players can still play
            for player, player_stats in self.players.items():
                if player_stats["bal"] <= 0:
                    print(f"{player} has no money. Kicked from table")
                    del player_stats[f"{player}"]
                    continue

                while True:
                    quit = input("Do you want to leave the table? (y/n): ")

                    if quit == "y":
                        print(f"{player} leaves the table")
                        del player_stats[f"{player}"]
                        continue

                    if quit == "n":
                        continue

                    else:
                        print("Invalid input")
 
            if not self.players:
                print("No more players, game end")
                exit = True

            self.reset_round()



if __name__ == "__main__":
    # set up game settings
    os.system("cls")
    num_of_players = int(input("How many players?: "))
    num_of_decks = int(input("How many decks?: "))
    game = Blackjack(num_of_decks, num_of_players)
    game.main()