"""Blackjack, by Al Sweigart al@inventwithpython.com
The classic card game also known as 21. (This version doesn't have
splitting or insurance.)
More info at: https://en.wikipedia.org/wiki/Blackjack
View this code at https://nostarch.com/big-book-small-python-projects
Tags: large, game, card game"""

import random, sys

# Set up the constants:
HEARTS = chr(9829) # Character 9829 is '♥'.
DIAMONDS = chr(9830) # Character 9830 is '♦'.
SPADES = chr(9824) # Character 9824 is '♠'.
CLUBS = chr(9827) # Character 9827 is '♣'.
 
# (A list of chr codes is at https://inventwithpython.com/charactermap)
BACKSIDE = 'backside'

def main():
    print('''Blackjack, by Al Sweigart al@inventwithpython.com

    Rules:
      Try to get as close to 21 without going over.
      Kings, Queens, and Jacks are worth 10 points.
      Aces are worth 1 or 11 points.
      Cards 2 through 10 are worth their face value.
      (H)it to take another card.
      (S)tand to stop taking cards.
      On your first play, you can (D)ouble down to increase your bet
      but must hit exactly one more time before standing.
      In case of a tie, the bet is returned to the player.
      The dealer stops hitting at 17.''')

    money = 5000
    # Main game loop.
    while True:#Setup loan option
        # Check if the player has run out of money:
        if money <= 0:#can add a topup option to improve game
            print("You're broke!")
            user_choice = input("Do you need a loan?!? Y/N")
            if user_choice == "Y" :
                while True:
                    user_amount = input("How much do you want?")
                    if int(user_amount)  <0:
                        print("invalid loan amount")
                    else:
                        break
                money += int(user_amount)
            else:
                print("Good thing you weren't playing with real money.")
                print('Thanks for playing!')
                sys.exit()

        # Let the player enter their bet for this round:
        print('Money:', money)
        bet = getBet(money)

        # Give the dealer and player two cards from the deck each:
        deck = getDeck()
        #dealerHand = [deck.pop(), deck.pop()] #Dealer gets one card, then player gets one card.
        #playerHand = [deck.pop(), deck.pop()]#Dealer gets second card, then player gets second card
        dealerHand=[]
        playerHand=[]
        dealerHand.append(deck.pop())
        playerHand.append(deck.pop())
        dealerHand.append(deck.pop())
        playerHand.append(deck.pop())
        # Handle player actions:
        print('Bet:', bet)
        # Keep looping until player stands or busts.
        while True:
            displayHands(playerHand, dealerHand, False)
            print()

            # Check if the player has bust:
            if getHandValue(playerHand) > 21:
                break

            # Get the player's move, either H, S, or D:
            move = getMove(playerHand, money - bet)

            # Handle the player actions:
            if move == 'D':
                # Player is doubling down, they can increase their bet:
                additionalBet = getBet(min(bet, (money - bet)))#HOMEWOrk, write down meaning of line
                bet += additionalBet
                print('Bet increased to {}.'.format(bet))
                print('Bet:', bet)

            if move in ('H', 'D'):
                # Hit/doubling down takes another card.
                newCard = deck.pop()
                rank, suit = newCard
                print('You drew a {} of {}.'.format(rank, suit))
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    # The player has busted:
                    continue

            if move in ('S', 'D'):
                # Stand/doubling down stops the player's turn.
                break

        # Handle the dealer's actions:
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                # The dealer hits:
                print('Dealer hits...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    # The dealer has busted.
                    break
                input('Press Enter to continue...')
                print('\n\n')

            # Show the final hands:
            displayHands(playerHand, dealerHand, True)

            playerValue = getHandValue(playerHand)
            dealerValue = getHandValue(dealerHand)
            # Handle whether the player won, lost, or tied:
            if dealerValue > 21:
                print('Dealer busts! You win ${}!'.format(bet))
                money += bet
            elif (playerValue > 21) or (playerValue < dealerValue):#HOMEWOrk, write down meaning of line
                print('You lost!')
                money -= bet
            elif playerValue > dealerValue:
                print('You won ${}!'.format(bet))
                money += bet
            elif playerValue == dealerValue:
                print('It\'s a tie, the bet is returned to you.')

            input('Press Enter to continue...')
            print('\n\n')
                
    

def getBet(maxBet):
    """Ask the player how much they want to bet for this round."""
    # Keep asking until they enter a valid amount.
    while True:
        print('How much do you bet? (1-{}, or QUIT)'.format(maxBet))
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('Thanks for playing!')
            sys.exit()

        if not bet.isdecimal():
            # If the player didn't enter a number, ask again.
            continue

        bet = int(bet)
        if 1 <= bet <= maxBet:
            # Player entered a valid bet.
            return bet
    

def getDeck():
    """Return a list of (rank, suit) tuples for all 52 cards."""
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            # Add the numbered cards.
            deck.append((str(rank), suit))
        for rank in ('J', 'Q', 'K', 'A'):
            # Add the face and ace cards.
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck

def displayHands(playerHand, dealerHand, showDealerHand):
    """Show the player's and dealer's cards. Hide the dealer's first
    card if showDealerHand is False."""
    print()
    if showDealerHand:
        print('DEALER:', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        # Hide the dealer's first card:
        displayCards([BACKSIDE] + dealerHand[1:])

    # Show the player's cards:
    print('PLAYER:', getHandValue(playerHand))
    displayCards(playerHand)

def getHandValue(cards):
    """Returns the value of the cards. Face cards are worth 10, aces are
    worth 11 or 1 (this function picks the most suitable ace value)."""
    value = 0
    numberOfAces = 0

    # Add the value for the non-ace cards:
    for card in cards:
        # card is a tuple like (rank, suit)
        rank = card[0]
        if rank == 'A':
            numberOfAces += 1
        # Face cards are worth 10 points.    
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            # Numbered cards are worth their number.
            value += int(rank)

    # Add the value for the aces:
    # Add 1 per ace.
    value += numberOfAces
    for i in range(numberOfAces):
        # If another 10 can be added with busting, do so:
        if value + 10 <= 21:
            value += 10

    return value

def displayCards(cards):
    """Display all the cards in the cards list."""
    # The text to display on each row.
    rows = ['', '', '', '', '']

    for i, card in enumerate(cards):
        # Print the top line of the card.
        rows[0] += ' ___  '
        if card == BACKSIDE:
            # Print a card's back:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            # Print the card's front:
            # The card is a tuple data structure.
            rank, suit = card
            rows[1] += '|{} | '.format(rank.ljust(2))#HOMEWOrk, write down meaning of line
            rows[2] += '| {} |'.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

    # Print each row on the screen:
    for row in rows:
        print(row)
        

def getMove(playerHand, money):
    """Asks the player for their move, and returns 'H' for hit, 'S' for
    stand, and 'D' for double down."""
    # Keep looping until the player enters a correct move.
    while True:
        # Determine what moves the player can make:
        moves = ['(H)it', '(S)tand']

        # The player can double down on their first move, which we can
        # tell because they'll have exactly two cards:
        if len(playerHand) == 2 and money > 0:
            moves.append('(D)ouble down')

        # Get the player's move:
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H', 'S'):
            # Player has entered a valid move.
            return move
        if move == 'D' and '(D)ouble down' in moves:
            # Player has entered a valid move.
            return move

# If the program is run (instead of imported), run the game:
if __name__ == '__main__':
    main()       
