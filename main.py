import pygame
import random
import os

pygame.init()
clock = pygame.time.Clock()

cursor = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
dealer_sprites = pygame.sprite.Group()
ui_sprites = pygame.sprite.Group()
game_over_sprites = pygame.sprite.Group()
chips = pygame.sprite.Group()


#defining screen
screen = pygame.display.set_mode((750, 750))

pygame.display.set_caption("Blackjack")
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)


thirty_font = pygame.font.Font("symtext/Symtext.ttf", 30)
forty_font = pygame.font.Font("symtext/Symtext.ttf", 40)
fifty_font = pygame.font.Font("symtext/Symtext.ttf", 50)


#TEXTURES
background_image = pygame.transform.scale(pygame.image.load("img/background.png"), (750, 750))
mouse_texture = pygame.transform.scale(pygame.image.load("img/mouse.png"), (8, 8))
back_card_texture = pygame.transform.scale(pygame.image.load("img/back.png"), (96, 128))
ace_sign_texture = pygame.transform.scale(pygame.image.load("img/ace_sign.png"), (128, 128))


chip_textures = [
    pygame.transform.scale(pygame.image.load("img/chips/ten_chip1.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("img/chips/fifty_chip1.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("img/chips/hundred_chip1.png"), (80, 80))
]

chip_clicked_textures = [
    pygame.transform.scale(pygame.image.load("img/chips/ten_chip2.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("img/chips/fifty_chip2.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("img/chips/hundred_chip2.png"), (80, 80))

]

button_textures = [
    pygame.transform.scale(pygame.image.load("img/hit_button1.png"), (200, 75)),
    pygame.transform.scale(pygame.image.load("img/stand_button1.png"), (200, 75)),
    pygame.transform.scale(pygame.image.load("img/restart_button1.png"), (275, 125))
]

pressed_button_textures = [
    pygame.transform.scale(pygame.image.load("img/hit_button2.png"), (200, 75)),
    pygame.transform.scale(pygame.image.load("img/stand_button2.png"), (200, 75)),
    pygame.transform.scale(pygame.image.load("img/restart_button2.png"), (275, 125))
]

card_textures = [
    pygame.transform.scale(pygame.image.load("img/cards/card_1.png"), (96, 128)),
    pygame.transform.scale(pygame.image.load("img/cards/card_2.png"), (96, 128)),
    pygame.transform.scale(pygame.image.load("img/cards/card_3.png"), (96, 128)),
    pygame.transform.scale(pygame.image.load("img/cards/card_4.png"), (96, 128)),
    pygame.transform.scale(pygame.image.load("img/cards/card_5.png"), (96, 128)),
    pygame.transform.scale(pygame.image.load("img/cards/card_6.png"), (96, 128)),
    pygame.transform.scale(pygame.image.load("img/cards/card_7.png"), (96, 128)),
    pygame.transform.scale(pygame.image.load("img/cards/card_8.png"), (96, 128)),
    pygame.transform.scale(pygame.image.load("img/cards/card_9.png"), (96, 128)),
    pygame.transform.scale(pygame.image.load("img/cards/card_10.png"), (96, 128)),
]







class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        cursor.add(self)

        self.image = mouse_texture
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x, self.rect.y = pygame.mouse.get_pos()




class Card(pygame.sprite.Sprite):
    def __init__(self, x, y, flipped, group):
        super().__init__()

        group.add(self)

        self.value = random.randrange(0, 10) + 1

        self.card_value = self.value - 1

        self.image = card_textures[self.card_value]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.flipped = flipped

    def update(self):
        if self.flipped == False:
            self.image = back_card_texture
        if self.flipped == True:
            self.image = card_textures[self.card_value]




class Button(pygame.sprite.Sprite):
    def __init__(self, img, pressed_img, group, x, y):
        super().__init__()

        group.add(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y  

        self.pressed_img = pressed_img
        self.img = img

        self.clicked = False
        self.animation_frames = 0

    def update(self):
        if self.clicked == True:
            self.animation_frames += 1
            self.image = self.pressed_img

            if self.animation_frames == 25:
                self.image = self.img
                self.clicked = False
                self.animation_frames = 0



def buttonClicked(button, mouse):
    if pygame.sprite.collide_mask(button, mouse):
        button.clicked = True
        return True
    else:
        return False




mouseCursor = Cursor()


hitButton = Button(button_textures[0], pressed_button_textures[0], ui_sprites, 150, 560)
standButton = Button(button_textures[1], pressed_button_textures[1], ui_sprites, 380, 560)
restartButton = Button(button_textures[2], pressed_button_textures[2], game_over_sprites, 240, 275)


fiveChip = Button(chip_textures[0], chip_clicked_textures[0], chips, 10, 530)
twentyFiveChip= Button(chip_textures[1], chip_clicked_textures[1], chips, 10, 440)  
fiftyChip = Button(chip_textures[2], chip_clicked_textures[2], chips, 10, 350)


aceSign_one = Button


starting_cards = [Card(280, 380, True, player_sprites), Card(350, 380, True, player_sprites), Card(280, 20, False, dealer_sprites), Card(350, 20, True, dealer_sprites)]


all_player_cards = 1
all_dealer_cards = 1


player_hand = starting_cards[0].value + starting_cards[1].value


player_bet = 0
player_money = 100
player_can_bet = True
player_has_bet = False

player_stand = False
player_hit = False

dealer_hand = starting_cards[3].value 



player_win = False
dealer_win = False



player_button_delay = 30
dealer_card_delay = 60
end_game_delay = 120


dealer_second_card_added = False




#MAIN FUNCTION
running = True
while running: 

    #resetting the hit button for repeated use and updating the delay speed of the buttons
    player_hit = False
    player_button_delay -= 1   
    


    #quitting via ESCAPE button
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    #quitting via EXIT button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False





    #CHECKING FOR MOUSE INPUT
    if pygame.mouse.get_pressed()[0]:



        if player_can_bet == True:
            if buttonClicked(fiveChip, mouseCursor) and player_money >= 5 and player_button_delay <= 0:
                player_bet += 5
                player_money -= 5
                player_button_delay = 30
                player_has_bet = True
            if buttonClicked(twentyFiveChip, mouseCursor) and player_money >= 25 and player_button_delay <= 0:
                player_button_delay = 30
                player_money -= 25
                player_bet += 25
                player_has_bet = True
            if buttonClicked(fiftyChip, mouseCursor) and player_money >= 50 and player_button_delay <= 0:
                player_button_delay = 30
                player_money -= 50
                player_bet += 50
                player_has_bet = True


        if player_has_bet == True:
            if buttonClicked(hitButton, mouseCursor):
                hitButton.clicked = True
                player_can_bet = False
                player_hit = True

            if buttonClicked(standButton, mouseCursor):
                standButton.clicked = True
                player_can_bet = False
                player_stand = True


        if buttonClicked(restartButton, mouseCursor) and player_win == True or buttonClicked(restartButton, mouseCursor) and dealer_win == True:

            starting_cards = [Card(280, 330, True, player_sprites), Card(350, 330, True, player_sprites), Card(280, 20, False, dealer_sprites), Card(350, 20, True, dealer_sprites)]

            player_hand = starting_cards[0].value + starting_cards[1].value
            dealer_hand = starting_cards[3].value

            player_stand = False
            player_win = False
            dealer_win = False

            player_bet = 0

            player_can_bet = True
            player_has_bet = False

            end_game_delay = 60
            player_button_delay = 30

            all_player_cards = 1
            all_dealer_cards = 1

            dealer_second_card_added = False

            



    #PLAYERS TURN
    if player_hit == True and player_stand == False and player_win == False and dealer_win == False and player_button_delay <= 0:

        player_button_delay = 30

        #creating new card, adding its value to the player's hand, and including it in all_player_cards count
        newCard = Card(350+all_player_cards*50, 330, True, player_sprites)
        player_hand += newCard.value
        all_player_cards += 1

        if player_hand > 21:
            dealer_win = True






    #DEALERS TURN 
    if player_stand == True or dealer_win == True:

        if dealer_second_card_added == False:

            starting_cards[2].flipped = True
            dealer_hand += starting_cards[2].value
            dealer_second_card_added = True
        




        if player_hand <= 21:

            if dealer_hand <= player_hand:
                dealer_card_delay -= 1

                #if the delay is over, reset the delay, make a new card, add the card value to the dealers hand, and include card in all_dealer_cards
                if dealer_card_delay <= 0:
                    newCard = Card(350+all_dealer_cards*50, 20, True, dealer_sprites)
                    dealer_hand += newCard.value
                    dealer_card_delay = 60
                    all_dealer_cards += 1






        if dealer_hand > 21:
            player_win = True

        if dealer_hand > player_hand and dealer_hand <= 21:
            dealer_win = True







    #Delaying the reset screen only one time
    if player_win == True or dealer_win == True:
        end_game_delay -= 1

    #One time finishing aspects
    if end_game_delay == 0:
        if player_win == True:
            player_money += round(player_bet * 1.5)

        if player_money == 0:
            player_money = 100




    screen.blit(background_image, (0, 0))


    #END OF GAME DISPLAYTING
    if end_game_delay <= 0:
        game_over_sprites.update()
        game_over_sprites.draw(screen)

        if player_win == True:
            dealer_sprites.empty()
            player_sprites.empty()
            screen.blit(forty_font.render("Player Wins", False, (255, 255, 255)), (190, 150))


        if dealer_win == True:
            dealer_sprites.empty()
            player_sprites.empty()
            screen.blit(forty_font.render("Dealer Wins", False, (255, 255, 255)), (190, 150))




    #DURING GAME DISPLAYING
    else: 
        player_sprites.update()
        dealer_sprites.update()
        ui_sprites.update()
        chips.update()

        if player_can_bet == True:
            screen.blit(fifty_font.render("Place Bet", False, (255, 255, 255)), (240, 200))


        screen.blit(thirty_font.render("Dealer Hand: "+str(dealer_hand), False, (255, 255, 255)), (230, 150))
        screen.blit(thirty_font.render("Hand: "+str(player_hand), False, (255, 255, 255)), (290, 510))

        screen.blit(thirty_font.render("Bet: "+str(player_bet), False, (255, 255, 255)), (10, 650))
        screen.blit(thirty_font.render("Money:  "+str(player_money), False, (255, 255, 255)), (10, 690))


        chips.draw(screen)
        ui_sprites.draw(screen)




    cursor.update()

    dealer_sprites.draw(screen)
    player_sprites.draw(screen)
    cursor.draw(screen)


    clock.tick(60)
    pygame.display.flip()



