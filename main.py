from random import shuffle
import random

class Card:
    suits = ["♠",
             "♥",
             "♦",
             "♣"]

    values = [None, None,"2", "3",
              "4", "5", "6", "7",
              "8", "9", "10",
              "J", "Q",
              "K", "A"]


    def __init__(self, v, s):
        """suit + value are ints"""
        self.value = v
        self.suit = s

    def __lt__(self, c2):
        if self.value < c2.value:
            return True
        if self.value == c2.value:
            if self.suit < c2.suit:
                return True
            else:
                return False
        return False

    def __gt__(self, c2):
        if self.value > c2.value:
            return True
        if self.value == c2.value:
            if self.suit > c2.suit:
                return True
            else:
                return False
        return False

    def __repr__(self):
        v = self.suits[self.suit]+""+self.values[self.value]
        return v

class Deck:
    def __init__(self):
        self.cards = []
        for i in range(2, 15):
            for j in range(4):
                self.cards\
                    .append(Card(i,
                                 j))
        shuffle(self.cards)

    def rm_card(self):
        if len(self.cards) == 0:
            return
        return self.cards.pop()

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = []
        self.AI_hand = []
        self.table = []
        self.player_toplanan = []
        self.AI_toplanan = []
        self.player_puan = 0
        self.AI_puan = 0
        self.AI_tracked_cards = []
        self.first_4 = []
        self.first_4_taken = 0

    def acilis_yap(self):
        for i in range(4):
            self.player_hand.append(self.deck.rm_card())

        for i in range(4):
            card = self.deck.rm_card()
            self.AI_hand.append(card)
            self.AI_tracked_cards.append(card)
            self.first_4.append(card)

        for i in range(4):
            self.table.append(self.deck.rm_card())

    def kart_dagit(self):
        for i in range(4):
            self.player_hand.append(self.deck.rm_card())

        for i in range(4):
            card = self.deck.rm_card()
            self.AI_hand.append(card)
            self.AI_tracked_cards.append(card)

    def oynancak_kart_no(self,simulation):
        play_card_no = 0
        if simulation:
            max = len(self.player_hand)
            return random.randint(0, max-1)

        while True:
            try:
                play_card_no = int(input("Enter a number between 1 and {}: ".format(len(self.player_hand))))
                assert 1 <= play_card_no <= len(
                    self.player_hand)

                break
            except (ValueError, AssertionError) as error:
                print("Input must be an integer between 1 and {}.".format(len(self.player_hand)))

        return play_card_no - 1

    def play_card(self,who_played,new_card,file): # who_played: 0 player - 1 AI
        last_played_card = Card(None,None)
        if len(self.table) > 0:
            last_played_card = self.table[-1]

        who = ""
        if who_played == 0:
            who = "You"
        else:
            who = "AI"

        if simulation == 0:
            print(who +" played: "+ str(new_card))
            file.write(who+" played: "+ str(new_card)+ "\n")
        self.table.append(new_card)

        if who_played == 0:
            self.AI_tracked_cards.append(new_card)

        new_card_suit = str(Card.suits[getattr(new_card,'suit')])
        new_card_value = str(Card.values[getattr(new_card,'value')])

        if last_played_card.value != None:
            last_card_played_suit = str(Card.suits[getattr(last_played_card,'suit')])
            last_card_played_value = str(Card.values[getattr(last_played_card,'value')])

        if last_played_card.value != None:
            if new_card_value == last_card_played_value:
                if len(self.table) == 2:
                    if simulation == 0:
                        print("PISTI!!!")
                        file.write("PISTI!!!\n")
                    if who_played == 0:
                        self.player_puan += 10
                    else:
                        self.AI_puan += 10

                ortadaki_kart_sayisi = len(self.table)
                for i in range(ortadaki_kart_sayisi):
                    if who_played == 0:
                        self.player_toplanan.append(self.table.pop())
                    else:
                        self.AI_toplanan.append(self.table.pop())

                if self.first_4_taken == 0:
                    if who_played == 0:
                        if simulation == 0:
                            print("First 3 cards:", end=" ")
                            file.write("First 3 cards: ")
                        for i in range(3):
                            if simulation == 0:
                                print(self.first_4[i], end=" ")
                                file.write(str(self.first_4[i])+" ")

                        if simulation == 0:
                            print()
                            file.write("\n")
                    else:
                        if simulation == 0:
                            file.write("AI saw the first 3 cards!\n")
                            print("AI saw the first 3 cards!")
                        for i in range(3):
                            self.AI_tracked_cards.append(self.first_4[i])
                self.first_4_taken = 1

        if new_card_value == "J" and len(self.table) > 1:
            ortadaki_kart_sayisi = len(self.table)
            for i in range(ortadaki_kart_sayisi):
                if who_played == 0:
                    self.player_toplanan.append(self.table.pop())
                else:
                    self.AI_toplanan.append(self.table.pop())

            if self.first_4_taken == 0:
                if who_played == 0:
                    if simulation == 0:
                        print("First 3 cards:", end=" ")
                        file.write("First 3 cards: ")
                    for i in range(3):
                        if simulation == 0:
                            print(self.first_4[i], end= " ")
                            file.write(str(self.first_4[i]) + " ")

                    if simulation == 0:
                        print()
                        file.write("\n")
                else:
                    if simulation == 0:
                        file.write("AI saw the first 3 cards!\n")
                        print("AI saw the first 3 cards!")
                    for i in range(3):
                        self.AI_tracked_cards.append(self.first_4[i])

            self.first_4_taken = 1

    def AI_algo(self):
        last_card_on_table = Card(None, None)
        if len(self.table) > 0:
            last_card_on_table = self.table[-1]

        if last_card_on_table.value == None:  # There is no card in middle -> play the most played value card
            count_values = []
            for i in range(len(self.AI_hand)):
                count_values.append(0)

            for i in range(len(self.AI_hand)):
                hand_card_value = str(Card.values[getattr(self.AI_hand[i], 'value')])
                for j in range(len(self.AI_tracked_cards)):
                    tracked_card_value = str(Card.values[getattr(self.AI_tracked_cards[j], 'value')])
                    if hand_card_value == tracked_card_value:
                        count_values[i] += 1

            return count_values.index(max(count_values))

        else:# play the same value card on the table if it exists in AI hand
            last_card_on_table = self.table[-1]
            last_card_value = str(Card.values[getattr(last_card_on_table, 'value')])

            for i in range(len(self.AI_hand)):
                hand_card_value = str(Card.values[getattr(self.AI_hand[i], 'value')])

                if last_card_value == hand_card_value:
                    return i

        for i in range(len(self.AI_hand)):
            hand_card_value = str(Card.values[getattr(self.AI_hand[i], 'value')])
            if hand_card_value == "J" and last_card_on_table.value != None:
                return i

        count_values = []
        for i in range(len(self.AI_hand)):
            count_values.append(0)

        for i in range(len(self.AI_hand)):
            hand_card_value = str(Card.values[getattr(self.AI_hand[i], 'value')])
            for j in range(len(self.AI_tracked_cards)):
                tracked_card_value = str(Card.values[getattr(self.AI_tracked_cards[j], 'value')])
                if hand_card_value == tracked_card_value:
                    count_values[i] += 1


        return count_values.index(max(count_values))

        return random.randint(1, len(self.AI_hand)) - 1

    def play_pisti(self,show_cards,simulation):
        cards = self.deck.cards

        self.player_hand = []
        self.AI_hand = []
        self.table = []

        self.acilis_yap()
        self.AI_tracked_cards.append(self.table[-1])
        self.draw_board(show_cards,simulation)

        for i in range(6):

            filename = f'tur{i}.txt'
            file = open(filename,"w")
            self.write_to_file(file,simulation)
            for i in range(4):
                card_no = self.oynancak_kart_no(simulation)
                card = self.player_hand[card_no]
                self.play_card(0, card, file)
                del self.player_hand[card_no]

                self.write_to_file(file,simulation)
                self.draw_board(show_cards,simulation)
                #print(self.AI_tracked_cards)

                card_no = self.AI_algo()
                card = self.AI_hand[card_no]
                self.play_card(1, card, file)
                del self.AI_hand[card_no]

                self.write_to_file(file,simulation)
                self.draw_board(show_cards,simulation)


            self.kart_dagit()
            self.draw_board(show_cards,simulation)
            file.close()

        self.puan_hesapla()

        if simulation == 0:
            print("Senin puanin: "+ str(self.player_puan))
            print("AI puani: "+str(self.AI_puan))
        if self.player_puan > self.AI_puan:
            return 0
        else:
            return 1

    def puan_hesapla(self):
        if len(self.AI_toplanan) > len(self.player_toplanan):
            self.AI_puan += 3
        else:
            self.player_puan += 3

        kart_sayisi = len(self.AI_toplanan)
        for i in range(kart_sayisi):
            card  = self.AI_toplanan.pop()
            card_suit = str(Card.suits[getattr(card, 'suit')])
            card_value = str(Card.values[getattr(card, 'value')])
            if card_suit == "♦" and card_value == "10":
                self.AI_puan += 3
            if card_suit == "♣" and card_value == "2":
                self.AI_puan += 2
            if card.value == "J":
                self.AI_puan += 1

        kart_sayisi = len(self.player_toplanan)
        for i in range(kart_sayisi):
            card = self.player_toplanan.pop()
            card_suit = str(Card.suits[getattr(card, 'suit')])
            card_value = str(Card.values[getattr(card, 'value')])
            if card_suit == "♦" and card_value == "10":
                self.player_puan += 3
            if card_suit == "♣" and card_value == "2":
                self.player_puan += 2
            if card.value == "J":
                self.player_puan += 1

    def draw_board(self,show_cards=1, simulation=0):
        if simulation:
            return

        if show_cards == 0:
            for i in range(len(self.AI_hand)):
                print("?", end=" ")
        else:
            for i in range(len(self.AI_hand)):
                print(self.AI_hand[i], end=" ")
        print()
        if len(self.table) > 0:
            print(self.table[-1], end=" ")
        else:
            print("X", end = " ")
        print()
        for i in range(len(self.player_hand)):
            print(self.player_hand[i], end=" ")
        print()
        print("------------------")

    def write_to_file(self,file, simulation):
        if simulation:
            return

        for i in range(len(self.AI_hand)):
            #print(self.AI_hand[i], end=" ")
            file.write(str(self.AI_hand[i]) + " ")
        file.write("\n")
        if len(self.table) > 0:
            file.write(str(self.table[-1]))
        else:
            file.write("X")
        file.write("\n")
        for i in range(len(self.player_hand)):
            file.write(str(self.player_hand[i]) + " ")
        file.write("\n")
        file.write("-----------------\n")



see_AI = 0 #0 off - 1 on  ---->   see AI hand
simulation = 0 #0 off - 1 on    ---->   AI plays against random card player
game_count = 1000 # how many games you want to simulate

if simulation:
    AI = 0
    player = 0
    for i in range(game_count):
        game = Game()
        who_won = game.play_pisti(see_AI, simulation)
        if who_won == 0:
            player += 1
        else:
            AI += 1

    print("AI: " + str(AI) + " times won")
    print("PLayer: " + str(player)  + " times won")
else:
    game = Game()
    who_won = game.play_pisti(see_AI, simulation)
    if who_won == 0:
        print("You won")
    else:
        print("AI won")


