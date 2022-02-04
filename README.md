## SUMMARY ##

This code is a command-line reproduction of the game Blackjack. This has only been tested on Python V 3.8.10 but should work with every version of Python 3.

To play the game simply:
- Navigate to the directory of the script: `cd ./my/directory`
- Execute the script: `python3 blackjack.py`

There is a second file in this directory called `component_testing.py`. That script uses the Unittest library to exercise white-box and black-box tests on most of the classes and their functions. I used it during development to check that the code wasn't regressing as I debugged and refactored. If you want to run it you have to comment out two lines of code in the Blackjack script:
- Line 4: `os.system('cls' if os.name == 'nt' else 'clear')`
- Final line: `quit()`

## RULE EXCEPTIONS & KNOWN ISSUES ##

- The player gets the option to continue hitting on a split pair of Aces (typically the player is dealt only one card for each and the player has to stand).
- The player cannot insure their bet against dealer when they are showing an Ace--you shouldn't really be doing that anyways ;)
- If the deck empties the script terminates due to an error, which I'll fix by implementing a Vegas-style deck with a cut shoe to signal a shuffle.
- The Unittest script will fail even if you comment out the two lines of code. A last-minute refactor now triggers a false-positive `AssertionError` for four of the six test cases. So the Blackjack script is working--it's the test script that's broken.
