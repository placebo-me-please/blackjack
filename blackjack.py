# COMMENT THIS OUT BEFORE EXECUTING TESTS
# clear the terminal window for clean display
import os
os.system('cls' if os.name == 'nt' else 'clear')

#random number generator for the shuffle function
import random

#some important variables and their values
suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = (\
    'Two', 'Three', 'Four', 'Five', \
    'Six', 'Seven', 'Eight', 'Nine', 'Ten', \
    'Jack', 'Queen', 'King', 'Ace')

card_dict = {\
    'Two':2, 'Three':3, 'Four':4, 'Five':5, \
    'Six':6, 'Seven':7, 'Eight': 8, 'Nine': 9, 'Ten': 10, \
    'Jack': 10, 'Queen': 10, 'King':10, 'Ace': [1, 11]}

buy_in = 5
round_counter = 1

#----------#
#game objects
#----------#
class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        #calling the 'rank' variable without self declaration is legal inside the instantiation method
        self.value = card_dict[rank]

    #when the print function is called on a Card object, this __str__ method is utilized
    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    def __init__(self):
        
        #instantiate the deck as an empty list
        self.all_cards = []

        #step through the variable "suits"
        for suit in suits:
            #step through the variable "ranks"
            for rank in ranks:
                #instantiate the card object
                created_card = Card(suit, rank)
                #append the new card to the deck
                self.all_cards.append(created_card)

    def shuffle(self):
        #the shuffle method does not require variable assignment
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()

class Player:
    def __init__(self,input_name):
        self.input_name = input_name
        #the player will start with this amount of money
        self.player_cash = 500

    #this function subtracts the player's bet from their available cash
    #REFACTOR NOTE
    #validate whether the player has enough money to place a bet
    #build that check and also refactor the object testing script
    #consider how changes may affect the game logic too
    def place_bet(self, player_bet):
        self.player_cash = self.player_cash - player_bet

    #this function adds the settlement of the round to the player's available cash
    def add_settlement(self, round_settlement):
        self.player_cash = self.player_cash + round_settlement
    #ADD A PRINT STATEMENT THAT SHOWS THE PLAYER'S AVAILABLE CASH

class Play_Pile:

    #REFACT NOTE
    #consider integrating the output of the state_checker() function
    #it would serve as a replacement to the pile_state value that exists within this class
    #would need to also rebuild the PlayPile_Display_Test test case
    def __init__(self,pile_owner):
        self.pile_owner = pile_owner
        self.pile_cards = []
        #this state variable will change if the player can double-down and/or has pairs to split
        self.pile_state = "NORM"

    def add_card(self,new_card):
        self.pile_cards.append(new_card)

    #this function will only be used to remove a card from the pile if the player has pairs to split
    def remove_card(self):
        self.pile_cards.pop(0)

    #this function will show the player what cards are on the table whenever it is requested
    #cards are displayed in the order in which they were dealt by the Deck class
    def __str__(self):
        #if the play pile just belongs to a human, then show all the cards
        if self.pile_owner == "HUMAN":
            #note that this is needed because the return statement will immediately return a result
            #the string must be "accumulated" before it can be returned in whole
            card_display = ""
            for card in self.pile_cards:
                card_display += str(card) + "\n"
            return card_display
        #if the play pile belongs to the computer, then only display the first card
        elif self.pile_owner == "COMPY":
            return str(self.pile_cards[0])

#----------#
#game functions
#----------#
#REFACTOR NOTE
#consider how you might use decorators to deactivate error messages when executing unittests
def bet_validator(player_instance, bet_amount):
    
    #this function validates that a placed bet is valid
    #if the player has enough money the bet is valid (True)
    #if the player does not have enough money the best is invalid (False)
    #the function returns one of those booleans
    
    global buy_in
    global round_counter

    #the bet must be examined to determine if the player entered an integer
    try:
        bet_amount = int(bet_amount)
        if bet_amount >= buy_in:
            pass
        elif bet_amount < buy_in:
            print(f"Error: please enter a value greater than or equal to ${str(buy_in)}")
            return False
    except ValueError:
        print("Error: enter an integer value")
        return False

    #the player's remaining cash must be assessed regardless of the round number 
    try:
        if player_instance.player_cash >= bet_amount:
            return True
        elif player_instance.player_cash < bet_amount:
            return False
    except ValueError:
        print("Error: enter an integer value")
        return False

def selection_validator(player_selection, range_max):

    #this function validates the user's selection
    #if the player input something within the range 1-max_value the selection is valid (True)
    #if the player input is anything else the selection is invalid (False)

    #the function checks if the player entered an integer
    try:
        #range max is increased by 1 due to how Python handles the "in" aspect of the logic test
        if int(player_selection) in range(1, range_max + 1, 1):
            return True
        else:
            print(f"Error: enter a value 1-{range_max}")
            return False
    except ValueError:
        print("Error: enter an integer value")
        return False   

def opening_hand_options(player_hand_state, player_instance, bet_amount):

    #this function receives the state of a player's hand as an input
    #there are four possible states at this point in the game and three options the player can exercise
    #this function outputs the appropriate messages and ultimately returns the player's decision (the string, NOT the integer)
    
    #the player has one option by default: to play their hand (0x0)
    player_options = ["play your hand"]

    #special fives state
    if player_hand_state == "0x6":
        player_options.extend(["double down"])
        player_options.extend(["split pairs"])

    #double down state
    elif player_hand_state == "0x4":
        player_options.extend(["double down"])

    #split pairs state
    elif player_hand_state == "0x2":
        player_options.extend(["split pairs"])

    #the player is then presented with their possible options, which is validated before any action is taken
    validation_check = False
    while validation_check == False:
        
        i = 1
        print("Opening Hand")
        print("------------------------------")
        print("Do you...")

        for option in player_options:
            print(f"{option} ({i})")
            i += 1

        hand_decision = input(f"Enter a value 1-{len(player_options)}: ")
        validation_check = selection_validator(hand_decision, len(player_options))

        #if the validation passes then the decision is converted to an integer
        if validation_check == True:
            hand_decision = int(hand_decision)

        #the player should not be able to double-down or split pairs if they do not have the funds
        #i.e. the code should not allow them to have negative funds should the bet fail to succeed
        if hand_decision != 1 and validation_check == True:

            validation_check = False
            while validation_check == False:
                #if the player has sufficient funds then the choice is fully valid
                if bet_validator(player_instance, bet_amount) == True:
                    validation_check = True
                    return player_options[hand_decision - 1]
                #if the player has insufficient funds they must select another option
                else:
                    print(f"Selection not permitted: You only have ${str(player_instance.player_cash)}. Please select another option\n")
                    break

        #if the player chose to just play their hand then no bet validation is required
        elif hand_decision == 1 and validation_check == True:
            return player_options[hand_decision - 1]  

def state_checker(pile_instance, loop_counter):

    #this function checks the state of each play pile
    #there are two possible control flows: one for the player and one for the dealer
    #this function returns a hex value that corresponds to a specific state

    global buy_in

    #round 0 control flow
    #if the hand was just dealt then check for natural, splitable pairs, or a double-down opportunity
    if loop_counter == 0:

        #this control flow assumes that the play pile has only two cards
        card_1 = pile_instance.pile_cards[0]
        card_2 = pile_instance.pile_cards[1]

        #initialize the bit state as empty
        #the fourth bit is unused so it is initialized as zero
        bit_state = "0"

        #checks if the hand value sums to 9, 10 , or 11
        #this is checking for membership in the tuple set of valid values
        #error handling is added because an Ace rank is associated with two values
        try:
            if (card_1.value + card_2.value) in {9, 10, 11}:
                bit_state += "1"
            else:
                bit_state += "0"
        
        #this checks if either card is of a value that would add to 9-10-11 if the player wants the ace to be of value 1
        #note that a value of 10 is intentionally excluded because that would result in a natural (weird edge case)
        #code assumes that the player would take the natural instead of double-down
        except TypeError:
            try:
                if card_1.value in {8, 9}:
                    bit_state += "1"
            except TypeError:
                pass
            
            try:
                if card_2.value in {8, 9}:
                    bit_state += "1"
                else:
                    bit_state += "0"
            except TypeError:
                pass

        #checks if the hand consists of pairs (ranks identical, NOT values)
        if (card_1.rank == card_2.rank):
            bit_state += "1"
        else:
            bit_state += "0"

        #checks if the hand is natural
        if (card_1.rank == 'Ace' and card_2.value == 10) or (card_2.rank == 'Ace' and card_1.value == 10):
            bit_state += "1"
        else:
            bit_state += "0"

        #the second value in this returned list is empty because summation of cards doesn't matter at this stage
        return [hex(int("0b" + bit_state, 2)), ""]

    #round 1 and on control flow
    #this sets bits for three possible pile states: sum > 16, bust, and 21
    #sum >= 17 only matters to the dealer because it determines how it plays
    else:

        #this control flow does not assume the pile has only two cards
        #this control flow only checks the value of cards, so the summation is performed here
        summation = 0
        for card in pile_instance.pile_cards:
            #attempt to add the value of the card to the grand total
            try:
                summation += card.value
            
            #if the card iteration is an ace it will throw a TypeError
            #the player will be prompted decide if they want the value to be 1 or 11
            #the script asks how to assign the value after each card is dealt
            #the script will let the player bust if they choose to
            except TypeError:

                #the dealer has no decision power over their ace
                #if the sum of values were to be 17 or greater by playing the ace with a value of 11 then the ace defaults to that value
                #therefore the code simply assumes that the ace is valuated as 11
                if pile_instance.pile_owner == "COMPY":
                    summation += card.value[1]

                #the player does have decision power over their ace
                elif pile_instance.pile_owner == "HUMAN":
                    validation_check = False
                    while validation_check == False:
                        ace_selection = input(f"Enter 1 ({card.value[0]}) or 2 ({card.value[1]}) to select the value for your Ace: ")
                        if selection_validator(ace_selection, 2) == True:
                            validation_check = True
                            summation += card.value[int(ace_selection)-1]

        #initialize the bit state as empty
        #the fourth bit is unused so it is initialized as zero
        bit_state = "0"

        #checks if the hand is 21
        if summation == 21:
            bit_state += "1"
        else:
            bit_state += "0"

        #checks if the hand has busted
        if summation > 21:
            bit_state += "1"
        else:
            bit_state += "0" 

        #check if the sum of values is greater than 17
        if summation >= 17:
            bit_state += "1"
        else:
            bit_state += "0"

        #the method returns the state of the pile and its summation
        return [hex(int("0b" + bit_state, 2)), summation]

def bet_settler(human_pile_state, human_pile, computer_pile_state):
    
    #this function acts at the bet settler at the end of each round
    #the function does not return anything: it simply processes the outcome
    
    #if neither the player or dealer busted then the sum of the ranks is calculated and an outcome is determined
    #this excludes the possibility that both the player and dealer have twenty-one, which is handled differently
    if human_pile_state[0] != "0x3" and computer_pile_state[0] != "0x3":

        #if the player wins the round then they take the bet pool and win the bet amount
        #this does not apply to a double down pile
        if human_pile_state[1] > computer_pile_state[1] and human_pile.pile_state != "DD":
            human_player.add_settlement(bet_pool + bet_amount)
            print(f"{human_player.input_name} wins the round and has ${human_player.player_cash} remaining.")

        elif human_pile_state[1] > computer_pile_state[1] and human_pile.pile_state == "DD":
            human_player.add_settlement(bet_pool + bet_amount * 2)
            print(f"{human_player.input_name} wins the round and has ${human_player.player_cash} remaining.")

        #if the computer wins the round then no action is taken because the bet has already been deducted
        elif human_pile_state[1] < computer_pile_state[1]:
            print(f"{human_player.input_name} loses the round and has ${human_player.player_cash} remaining.")

        #if neither wins then bet pool is returned to the player
        elif human_pile_state[1] == computer_pile_state[1]:
            human_player.add_settlement(bet_pool)
            print(f"The round is a tie and the bet is returned. {human_player.input_name} has ${human_player.player_cash} remaining.")

    #if the player and dealer both have twenty-one then the bet(s) is/are returned
    elif human_pile_state[0] == "0x5" and computer_pile_state[0] == "0x5":
        human_player.add_settlement(bet_pool)
        print(f"The round is a tie and the bet is returned. {human_player.input_name} has ${human_player.player_cash} remaining.")

    #if the the player busted they lose their bet (this is true regardless of the dealer's state)
    elif human_pile_state[0] == "0x3" and computer_pile_state[0] != "0x3":
        print(f"{human_player.input_name} loses the round and has ${human_player.player_cash} remaining.")

    #if the dealer busted and the player did not bust then they win the bet
    elif human_pile_state[0] != "0x3" and computer_pile_state[0] == "0x3":
        human_player.add_settlement(bet_pool + bet_amount)
        print(f"{human_player.input_name} wins the round and has ${human_player.player_cash} remaining.")

def round_incrementer():

    #this function increments the round counter
    global round_counter
    round_counter += 1

#----------#
#game logic
#----------#
if __name__ == '__main__':
    
    #------------------------------#
    #player initilization
    #------------------------------#
    game_on = True
    
    #REFACTOR NOTES: 
        #consider building a vegas-style deck (three decks combined into one) with a cut "shoe"
        #need to consider how to handle situations in which the deck has been emptied

    #instantiate the deck and shuffle it
    game_deck = Deck()
    game_deck.shuffle()

    #instantiate the player
    human_player = Player(input("Enter your name: "))
    print(f"{human_player.input_name}, you have ${str(human_player.player_cash)}\n")

    #main game logic loop
    while game_on == True:
        
        #------------------------------#
        #bet and deal logic (round zero)
        #------------------------------#

        #initialize the bet and the pool as zero
        bet_amount = 0
        bet_pool = 0

        #ask for input and validate that it meets the criterion
        validation_check = False
        while validation_check == False:

            bet_amount = input(f"Minimum buy-in of ${str(buy_in)} is required. Place your bet: $")

            if bet_validator(human_player, bet_amount) == True:
                validation_check = True
                bet_amount = int(bet_amount)
                human_player.place_bet(bet_amount)
                bet_pool += int(bet_amount)
                print(f"Okay bet. You now have ${str(human_player.player_cash)} remaining")
        
        #instantiate the play piles and set the loop counter equal to zero
        human_pile = Play_Pile("HUMAN")
        computer_pile = Play_Pile("COMPY")
        table_piles = [human_pile, computer_pile]
        loop_counter = 0

        #deal the two cards, starting with the human player
        i = 0
        while i < 2:
            for active_play_pile in table_piles:
                active_play_pile.add_card(game_deck.deal_one())
            i += 1

        #-------------------------------------------------------------------  
        #GAME LOGIC INJECTIONS - TO BE USED FOR TESTING ONLY
        #to test the logic of a hand simply remove the comment marks associated with it

        # #PLAYER CARDS
        # #------------
        # #special fives condition (0x6)
        # human_pile.remove_card()
        # human_pile.remove_card()
        # human_pile.add_card(Card("Hearts", "Five"))
        # human_pile.add_card(Card("Spades", "Five"))
        # print(state_checker(human_pile, loop_counter))

        # #split pairs condition (0x2)
        # human_pile.remove_card()
        # human_pile.remove_card()
        # human_pile.add_card(Card("Hearts", "Four"))
        # human_pile.add_card(Card("Spades", "Four"))
        # print(state_checker(human_pile, loop_counter))

        # #split pairs condition with Aces (0x2)
        # human_pile.remove_card()
        # human_pile.remove_card()
        # human_pile.add_card(Card("Hearts", "Ace"))
        # human_pile.add_card(Card("Spades", "Ace"))
        # print(state_checker(human_pile, loop_counter))

        # #double down condition (0x4)
        # human_pile.remove_card()
        # human_pile.remove_card()
        # human_pile.add_card(Card("Hearts", "Four"))
        # human_pile.add_card(Card("Spades", "Six"))
        # print(state_checker(human_pile, loop_counter))

        # #no special condition (0x0)
        # human_pile.remove_card()
        # human_pile.remove_card()
        # human_pile.add_card(Card("Hearts", "Four"))
        # human_pile.add_card(Card("Spades", "Eight"))

        # #DEALER CARDS
        # #------------
        # #no special condition but at the limit of hit/stand decision (0x0)
        # computer_pile.remove_card()
        # computer_pile.remove_card()
        # computer_pile.add_card(Card("Hearts", "Ace"))
        # computer_pile.add_card(Card("Hearts", "Five"))

        # #just over the limit of hit/stand decision (0x1)
        # computer_pile.remove_card()
        # computer_pile.remove_card()
        # computer_pile.add_card(Card("Hearts", "Ace"))
        # computer_pile.add_card(Card("Hearts", "Six"))
        #-------------------------------------------------------------------

        #display the dealt cards to the player
        print(f"\n{human_player.input_name} is showing:")
        print("------------------------------")
        print(human_pile)
        print("The dealer is showing:")
        print("------------------------------")
        print(computer_pile)
        print("")

        #check the initial play pile states before proceeding with play
        table_states = [state_checker(human_pile, loop_counter), state_checker(computer_pile, loop_counter)]
        
        # #STATE CHECKING PRINTOUT FOR DEBUG PURPOSES
        # #------------------------------------------------------------------
        # print(f"The player's initial state is: {table_states[0][0]}")
        # print(f"The player's initial sum is: {table_states[0][1]}")
        # #------------------------------------------------------------------

        #the following control flows check the determined states and react appropriately
        #these three control flows check the possible natural states
        #if both hands are natural then the player's bet is returned and the next round begins
        if table_states[0][0] == "0x1" and table_states[1][0] == "0x1":
            human_player.add_settlement(bet_pool)
            print(f"Both hands were natural so the bet is returned to the player. {human_player.input_name} has ${human_player.player_cash} remaining.")
            round_incrementer()
            continue

        #if the player's hand is natural and the dealer's is not the the player receives 1.5x their bet
        elif table_states[0][0] == "0x1" and table_states[1][0] != "0x1":
            human_player.add_settlement(bet_pool + bet_amount * 1.5)
            print(f"The player's hand is natural so they win their bet (and then some). {human_player.input_name} has ${human_player.player_cash} remaining.")
            round_incrementer()
            continue

        #if the dealer's hand is natural and the player's is not the player loses their bet
        #this code does not allow the player to insure their bet if the dealer's face up card is an ace
        elif table_states[0][0] != "0x1" and table_states[1][0] == "0x1":
            print(f"The dealer's hand is natural so {human_player.input_name} loses their bet. They have ${human_player.player_cash} remaining.")
            round_incrementer()
            continue

        #the player is given decision options if they can double down and/or split pairs
        if table_states[0][0] != "0x0":
            hand_decision = opening_hand_options(table_states[0][0], human_player, bet_amount)

        #otherwise they have no decision to make and code proceeds
        elif table_states[0][0] == "0x0":
            hand_decision = "no choice"

        #then the following control flows occur after the player has made their decisions (if any were required to be made)
        #double-down option
        if hand_decision == "double down":
            #assuming the validation passed, the initial bet is deducted a second time and added to the pool
            human_player.place_bet(int(bet_amount))
            bet_pool += bet_amount

            #the player is notified that the bet was allowed and the new balance is reported
            print(f"Selection permitted. You now have ${str(human_player.player_cash)} remaining")

            #the state of the play pile is changed to reflect doubling-down so that only the first two cards are printed
            human_pile.pile_state = "DD"

            #finally the player is dealt an additional card that will be revealed after the computer's turn is over
            human_pile.add_card(game_deck.deal_one())

        #split pairs option
        elif hand_decision == "split pairs":
            #assuming the validation passed, the initial bet is deducted a second time and added to the pool
            #each pile represents one half the total pool for that player
            #i.e. if one pile wins the player collects half the pool
            human_player.place_bet(int(bet_amount))
            bet_pool += bet_amount

            #the player is notified that the bet was allowed and the new balance is reported
            print(f"Selection permitted. You now have ${str(human_player.player_cash)} remaining")

            #then instantiate two new play piles that each consist of one card from the initial pile
            split_pile_1 = Play_Pile("HUMAN")
            split_pile_1.add_card(human_pile.pile_cards[0])
            split_pile_2 = Play_Pile("HUMAN")
            split_pile_2.add_card(human_pile.pile_cards[1])

            #finally the initial pile is re-instantiated as an empty list that will contain the two new piles
            #NOTE TO SELF: plan on writing code such that an error is intentiontally triggered, which results in exception handling for split pairs
            human_pile = [split_pile_1, split_pile_2]

        #------------------------------#
        #player logic (round one+)
        #------------------------------#

        #the round advances from round zero to round one, thus changing the control flow of the state checker
        #the counter never advances past one (no need for it to)
        loop_counter += 1

        #if the player doubled down then the play advances to the dealer
        if hand_decision == "double down":
            human_pile_state = state_checker(human_pile, loop_counter)

            print(f"\n{human_player.input_name}'s final pile is:")
            print("------------------------------")
            print(human_pile)

        elif hand_decision == "split pairs":

            #initialize the pile states as unknown for both piles
            human_pile_state = []
            i = 0

            #the player must play each of their piles out
            #each pile is treated separate from the other
            for active_pile in human_pile:

                if i == 0:
                    print(f"\n{human_player.input_name} now has two piles in play:\n")
                    print("Pile 1")
                    print(human_pile[0])
                    print("Pile 2")
                    print(human_pile[1])

                if i == 1:
                    print("First pile done. Moving play to second pile.\n")

                #as long as the player has not busted or decided to stay they may continue to play
                end_pile_play = False
                while end_pile_play == False:

                    #one of the two piles is dealt a card, then the state of the pile is checked
                    #NOTE: NEED TO ADD SPECIAL HANDLING FOR ACES (ONLY DEAL ONE CARD BY DEFAULT)
                    active_pile.add_card(game_deck.deal_one())
                    print(f"Currently playing pile {i + 1}")
                    print("------------------------------")
                    print(active_pile)
                    active_pile_state = state_checker(active_pile, loop_counter)

                    #if the player has not busted then they can decide to continue play
                    if active_pile_state[0] == "0x0" or active_pile_state[0] == "0x1":

                        #the player must choose whether or not to continue playing
                        validation_check = False
                        while validation_check == False:
                            play_decision = input("Do you hit (1) or stay (2)? ")
                            validation_check = selection_validator(play_decision, 2)

                            if validation_check == True:
                                play_decision = int(play_decision)

                        #if the player wants to hit then the control flow advances to the next iteration for the pile
                        if play_decision == 1:
                            print("\nTaking a hit.")

                        #if the player wants to stay then the end pile play variable switches to True and the next pile selected
                        elif play_decision == 2:
                            end_pile_play = True
                            i += 1
                            human_pile_state.extend([active_pile_state])
                            print("\nStaying here.")

                    #if the player has reached twenty-one then that pile is finished and the play advances
                    elif active_pile_state[0] == "0x5":
                        end_pile_play = True
                        i += 1
                        human_pile_state.extend([active_pile_state])
                        print("Twenty-one!")

                    #if the player has busted then that pile is finished and the play advances
                    elif active_pile_state[0] == "0x3":
                        end_pile_play = True
                        i += 1
                        human_pile_state.extend([active_pile_state])
                        print("This pile busted.")

            print(f"\n{human_player.input_name}'s final piles are:")
            print("------------------------------")
            for active_pile in human_pile:
                print(active_pile)                    

        #the logic here is essentially identical to the split pairs control flow, so comments are omitted
        elif hand_decision == "no choice" or hand_decision == "play your hand":

                print("\nCurrently playing this pile")
                print("------------------------------")
                print(human_pile)
                end_pile_play = False
                while end_pile_play == False:

                    human_pile_state = state_checker(human_pile, loop_counter)

                    if human_pile_state[0] == "0x0" or human_pile_state[0] == "0x1":

                        validation_check = False
                        while validation_check == False:
                            play_decision = input("Do you hit (1) or stay (2)? ")
                            validation_check = selection_validator(play_decision, 2)

                            if validation_check == True:
                                play_decision = int(play_decision)

                        if play_decision == 1:
                            human_pile.add_card(game_deck.deal_one())
                            print(f"\nTaking a hit. {human_player.input_name} is now showing:")
                            print("------------------------------")
                            print(human_pile)

                        elif play_decision == 2:
                            end_pile_play = True
                            i += 1
                            print("\nStaying here.")

                    elif human_pile_state[0] == "0x5":
                        end_pile_play = True
                        i += 1
                        print("Twenty-one!")

                    elif human_pile_state[0] == "0x3":
                        end_pile_play = True
                        i += 1
                        print("This pile busted.")

                print(f"\n{human_player.input_name}'s final pile is:")
                print("------------------------------")
                print(human_pile)

        #------------------------------#
        #dealer logic (round one+)
        #------------------------------#

        #the dealer logic is simpler because the dealer does not have decision making power
        end_pile_play = False
        while end_pile_play == False:

            computer_pile_state = state_checker(computer_pile, loop_counter)

            #if the sum of the dealer's cards is greater then 16 or they busted then they cannot hit and their turn is over
            if computer_pile_state[0] == "0x1" or computer_pile_state == "0x3":
                end_pile_play = True

            #if the sum is 16 or less then they have to hit
            elif computer_pile_state[0] == "0x0":
                computer_pile.add_card(game_deck.deal_one())

        #this is needed because the Play_Pile class won't show all of the dealer's cards
        print("The dealer's final pile is:")
        print("------------------------------")
        final_dealer_cards = ""
        for card in computer_pile.pile_cards:
                final_dealer_cards += str(card) + "\n"
        print(final_dealer_cards)

        #------------------------------#
        #bet settlement
        #------------------------------#

        #now that the player and computer have completed play the bet(s) is/are settled using the bet_settler function
        #if the piles were split then a control flow is needed to iterate through the pile states
        print("Round Settlement")
        print("------------------------------")
        if hand_decision == "split pairs":
            i = 1
            for split_pile_state in human_pile_state:
                print(f"Pile {i} outcome is:")
                bet_settler(split_pile_state, human_pile, computer_pile_state)
                print("")
                i += 1

        #otherwise the single pile is processed
        else:
            bet_settler(human_pile_state, human_pile, computer_pile_state)

        #------------------------------#
        #round end
        #------------------------------#

        if human_player.player_cash <= 0:
            game_on = False
            print("You're out of money! Game over.")

        elif human_player.player_cash < buy_in:
            game_on = False
            print("You do not meet the buy-in requirement! Game over.")

        else:
            validation_check = False 
            while validation_check == False:
                play_decision = input("Do you continue play (1) or leave the table (2)? ")
                validation_check = selection_validator(play_decision, 2)

                if validation_check == True:
                    play_decision = int(play_decision)

                if play_decision == 1:
                    round_incrementer()
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"Playing Round {round_counter}")
                    print("------------------------------")
                    print(f"You have ${human_player.player_cash} to bet this round")

                elif play_decision == 2:
                    game_on = False
                    print(f"You left the table with ${human_player.player_cash}.")

#COMMENT THIS OUT BEFORE EXECUTING TESTS
quit()