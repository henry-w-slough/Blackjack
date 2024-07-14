import time
import random


playerHand = random.randrange(1, 11)
playerHit = "y"

dealerHand = random.randrange(1, 11)

print("Your hand: "+str(playerHand))
time.sleep(1)


running = True
while running:

    #MAIN LOOP FOR PLAYER HAND
    while playerHand < 21 and playerHit == "y":

        playerHit = input("Hit? ")

        if playerHit == "y":
            playerHand += random.randrange(1, 11)
            time.sleep(1)
            print("Your hand: "+str(playerHand))

    if playerHand > 21:
        time.sleep(1)
        print("You bust!")
        running = False
    
    if playerHand <= 21:
        time.sleep(1)
        print("Dealers turn.")
        print("Dealers hand: "+str(dealerHand))

        if dealerHand < playerHand:
            while dealerHand < playerHand:
                time.sleep(1)
                dealerHand += random.randrange(1, 11)
                print("Dealers hand: "+str(dealerHand))
                
    if dealerHand > 21:
        print("Dealer bust! You win")
        running = False

    if dealerHand == 21 and playerHand == 21:
        print("Dealer 21! Another round...")
        time.sleep(1)
        playerHand = 0
        dealerHand = 0
        playerHit = "y"

    if dealerHand < 21 and dealerHand > playerHand:
        print("Dealer win!")
        running = False
    
        

                



