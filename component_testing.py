#module references
import unittest
import blackjack

#needed to mock user inputs for certain tests
from unittest.mock import patch

#NOTE THAT UNITTEST RUNS TEST IN ALPHABETICAL ORDER WITHIN EACH CLASS BY DEFAULT
#THIS HAS IMPLICATIONS DUE TO THE GLOBAL ROUND COUNTER VARIABLE

class PlayPile_AddRemove_Test(unittest.TestCase):

	def test_playpile(self):
		playpile_instance = blackjack.Play_Pile("HUMAN")

		card_1 = blackjack.Card("Hearts", "Two")
		card_2 = blackjack.Card("Hearts", "Three")

		#this test checks that the first card in the pile is of rank two
		playpile_instance.add_card(card_1)
		playpile_instance.add_card(card_2)
		self.assertEqual(playpile_instance.pile_cards[0].rank, "Two")

		#this checks that, after removing the first card, the next card is of rank three
		playpile_instance.remove_card()
		self.assertEqual(playpile_instance.pile_cards[0].rank, "Three")

class PlayPile_Test(unittest.TestCase):
		playpile_instance = blackjack.Play_Pile("HUMAN")
		playpile_instance.pile_state = "DD"

		card_1 = blackjack.Card("Spades", "Ace")
		card_2 = blackjack.Card("Hearts", "Five")
		card_3 = blackjack.Card("Spades", "Five")

		playpile_instance.add_card(card_1)
		playpile_instance.add_card(card_2)
		playpile_instance.add_card(card_3)

		#REFACTOR NOTE
		#testing is currently only visual confirmation of the cards
		#would be nice to refactor this test so that it verifies the GUI display somehow
		print(playpile_instance)

		playpile_instance.pile_state = "NORM"

		print(playpile_instance)

		playpile_instance.pile_owner = "COMPY"

		print(playpile_instance)
		print("\n")

		#NOTE - NEED TO ADD TESTS FOR CARD SUMMATIONS AND ACE HANDLING
		# playpile_instance.remove_card()
		# self.assertEqual(playpile_instance.sum_ranks(), 10)

class BetValidator_Test(unittest.TestCase):
	def test_validator_logic(self):
		player_instance = blackjack.Player("test")

		bet_1 = 200
		bet_2 = 199
		bet_3 = 500
		bet_4 = 501
		bet_5 = "abc"

		self.assertEqual(blackjack.bet_validator(player_instance, bet_1), True)
		self.assertEqual(blackjack.bet_validator(player_instance, bet_2), False)
		self.assertEqual(blackjack.bet_validator(player_instance, bet_3), True)		
		self.assertEqual(blackjack.bet_validator(player_instance, bet_4), False)
		self.assertEqual(blackjack.bet_validator(player_instance, bet_5), False)

class SpecialConditions_Test(unittest.TestCase):
	
	#round 0 pile states
	#------------------------------------------------------------------
	def test_round_0(self):

		#player instance
		playpile_instance = blackjack.Play_Pile("HUMAN")

		#cards for validating the natural state
		card_1 = blackjack.Card("Spades", "Ten")
		card_2 = blackjack.Card("Spades", "Ace")
		playpile_instance.add_card(card_1)
		playpile_instance.add_card(card_2)
		self.assertEqual(blackjack.state_checker(playpile_instance, 0), "0x1")
		playpile_instance.remove_card()
		playpile_instance.remove_card()

		#cards for validating special fives
		card_1 = blackjack.Card("Spades", "Five")
		card_2 = blackjack.Card("Hearts", "Five")
		playpile_instance.add_card(card_1)
		playpile_instance.add_card(card_2)
		self.assertEqual(blackjack.state_checker(playpile_instance, 0), "0x6")
		playpile_instance.remove_card()
		playpile_instance.remove_card()

		#cards for validating pairs
		card_1 = blackjack.Card("Spades", "Queen")
		card_2 = blackjack.Card("Hearts", "Queen")
		playpile_instance.add_card(card_1)
		playpile_instance.add_card(card_2)
		self.assertEqual(blackjack.state_checker(playpile_instance, 0), "0x2")
		playpile_instance.remove_card()
		playpile_instance.remove_card()

		#cards for validating summation (part 1)
		card_1 = blackjack.Card("Spades", "Four")
		card_2 = blackjack.Card("Hearts", "Five")
		playpile_instance.add_card(card_1)
		playpile_instance.add_card(card_2)
		self.assertEqual(blackjack.state_checker(playpile_instance, 0), "0x4")
		playpile_instance.remove_card()
		playpile_instance.remove_card()
		
		#cards for validating summation (part 2)
		card_1 = blackjack.Card("Spades", "Six")
		card_2 = blackjack.Card("Hearts", "Five")
		playpile_instance.add_card(card_1)
		playpile_instance.add_card(card_2)
		self.assertEqual(blackjack.state_checker(playpile_instance, 0), "0x4")
		playpile_instance.remove_card()
		playpile_instance.remove_card()

	#round 1 and on (1+) pile states
	#------------------------------------------------------------------
	def test_round_1plus(self):

		#increment the round counter via the incrementer function
		blackjack.round_incrementer()

		#player instance
		playpile_instance = blackjack.Play_Pile("HUMAN")

		#cards for validating sum > 16
		#three cards are added to the play pile to simulate round 1+ play
		card_1 = blackjack.Card("Spades", "Ten")
		card_2 = blackjack.Card("Hearts", "Five")
		card_3 = blackjack.Card("Clubs", "Two")
		playpile_instance.add_card(card_1)
		playpile_instance.add_card(card_2)
		playpile_instance.add_card(card_3)
		self.assertEqual(blackjack.state_checker(playpile_instance, 1), "0x1")
		playpile_instance.remove_card()
		playpile_instance.remove_card()
		playpile_instance.remove_card()

		#cards for validating if the sum == 21
		card_1 = blackjack.Card("Spades", "Ten")
		card_2 = blackjack.Card("Hearts", "Five")
		card_3 = blackjack.Card("Clubs", "Six")
		playpile_instance.add_card(card_1)
		playpile_instance.add_card(card_2)
		playpile_instance.add_card(card_3)
		self.assertEqual(blackjack.state_checker(playpile_instance, 1), "0x5")
		playpile_instance.remove_card()
		playpile_instance.remove_card()
		playpile_instance.remove_card()


	#inputs need to be mocked for this test because the user has to choose the value of their ace	
	#this is accomplished via the "patch" package within the unittest.mock module
	@patch('builtins.input', lambda *args: "1")
	def test_round_1plus_acelow(self):
		
		# print(blackjack.round_counter)

		#player instance
		playpile_instance = blackjack.Play_Pile("HUMAN")

		#same test as previous function EXCEPT an ace is introduced to exercise handling
		card_1 = blackjack.Card("Spades", "Ten")
		card_2 = blackjack.Card("Hearts", "Six")
		card_3 = blackjack.Card("Clubs", "Ace")
		playpile_instance.add_card(card_1)
		playpile_instance.add_card(card_2)
		playpile_instance.add_card(card_3)
		self.assertEqual(blackjack.state_checker(playpile_instance, 1), "0x1")

	#new function needs to be called to patch in a new input
	@patch('builtins.input', lambda *args: "2")
	def test_round_1plus_acehigh(self):
		#player instance
		playpile_instance = blackjack.Play_Pile("HUMAN")

		#same test as previous function EXCEPT an ace is introduced to exercise handling
		card_1 = blackjack.Card("Spades", "Ten")
		card_2 = blackjack.Card("Hearts", "Six")
		card_3 = blackjack.Card("Clubs", "Ace")
		playpile_instance.add_card(card_1)
		playpile_instance.add_card(card_2)
		playpile_instance.add_card(card_3)
		self.assertEqual(blackjack.state_checker(playpile_instance, 1), "0x3")

if __name__ == '__main__':
	unittest.main(verbosity = 2)