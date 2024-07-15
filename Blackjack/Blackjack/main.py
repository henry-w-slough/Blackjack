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


#defining screen
screen = pygame.display.set_mode((750, 750))

pygame.display.set_caption("Blackjack")
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)


handTextFont = pygame.font.Font("Blackjack/symtext/Symtext.ttf", 30)
switchTurnFont = pygame.font.Font("Blackjack/symtext/Symtext.ttf", 40)
winFont = pygame.font.Font("Blackjack/symtext/Symtext.ttf", 50)


#TEXTURES
background_image = pygame.transform.scale(pygame.image.load("Blackjack/img/background.png"), (750, 750))
mouse_texture = pygame.transform.scale(pygame.image.load("Blackjack/img/mouse.png"), (8, 8))
back_card_texture = pygame.transform.scale(pygame.image.load("Blackjack/img/back.png"), (96, 128))
ace_sign_texture = pygame.transform.scale(pygame.image.load("Blackjack/img/ace_sign.png"), (128, 128))

chip_textures = [
    pygame.transform.scale(pygame.image.load("Blackjack/img/chips/ten_chip1.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("Blackjack/img/chips/fifty_chip1.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("Blackjack/img/chips/hundred_chip1.png"), (80, 80))
]

chip_clicked_textures = [
    pygame.transform.scale(pygame.image.load("Blackjack/img/chips/ten_chip2.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("Blackjack/img/chips/fifty_chip2.png"), (80, 80)),
    pygame.transform.scale(pygame.image.load("Blackjack/img/chips/hundred_chip2.png"), (80, 80))

]

button_textures = [
    pygame.transform.scale(pygame.image.load("Blackjack/img/hit_button1.png"), (200, 75)),
    pygame.transform.scale(pygame.image.load("Blackjack/img/stand_button1.png"), (200, 75)),
    pygame.transform.scale(pygame.image.load("Blackjack/img/restart_button1.png"), (200, 75))
]

pressed_button_textures = [
    pygame.transform.scale(pygame.image.load("Blackjack/img/hit_button2.png"), (200, 75)),
    pygame.transform.scale(pygame.image.load("Blackjack/img/stand_button2.png"), (200, 75)),
    pygame.transform.scale(pygame.image.load("Blackjack/img/restart_button2.png"), (200, 75))
]

card_textures = []
card_iterate_count = 1
for img in os.listdir("Blackjack/img/cards"):
    if card_iterate_count == 11:
        break
    card_textures.append(pygame.transform.scale(pygame.image.load("Blackjack/img/cards/card_"+str(card_iterate_count)+".png"), (96, 128)))
    card_iterate_count += 1




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

        self.value = random.randrange(1, 10)

        self.image = card_textures[self.value]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.flipped = flipped

    def update(self):
        if self.flipped == False:
            self.image = back_card_texture
        if self.flipped == True:
            self.image = card_textures[self.value]




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
restartButton = Button(button_textures[2], pressed_button_textures[2], game_over_sprites, 270, 300)


starting_cards = [Card(280, 330, True), Card(350, 330, True), Card(280, 20, False), Card(350, 20, True)]

all_player_cards = 1
all_dealer_cards = 1


player_hand = starting_cards[0].value + starting_cards[1].value + 2
player_button_delay = 30
player_stand = False
player_hit = False


dealer_hand = starting_cards[2].value + starting_cards[3].value + 2
dealer_card_delay = 60



#MAIN FUNCTION
running = True
while running: 

    #resetting the hit button for repeated use and updating the holdback speed of the buttons
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

        if buttonClicked(hitButton, mouseCursor):
            hitButton.clicked = True
            player_hit = True

        if buttonClicked(standButton, mouseCursor):
            standButton.clicked = True
            player_stand = True


        if buttonClicked(restartButton, mouseCursor) and player_button_delay <= 0:
            player_button_delay = 30
            restartButton.clicked = True
            player_sprites.empty()
            dealer_sprites.empty()

            starting_cards = [Card(280, 330, True), Card(350, 330, True), Card(280, 20, False), Card(350, 20, True)]
            player_stand = False

            player_hand = starting_cards[0].value + starting_cards[1].value + 2
            dealer_hand = starting_cards[2].value + starting_cards[3].value + 2

            



    #PLAYERS TURN
    if player_hit == True and player_stand == False and player_button_delay <= 0:
        player_button_delay = 30

        #creating new card, adding its value to the player's hand, and including it in all_player_cards count
        newCard = Card(350+all_player_cards*50, 330, True)
        player_hand += newCard.value
        all_player_cards += 1

        #stopping player's turn if they bust
        if player_hand >= 21:
            player_stand = True



    #DEALERS TURN 
    if player_stand == True:
        starting_cards[2].flipped = True

        if player_hand <= 21:
            if dealer_hand <= player_hand:
                #delaying how fast the cards are created
                dealer_card_delay -= 1

                #if the delay is over, reset the delay, make a new card, add the card value to the dealers hand, and include card in all_dealer_cards
                if dealer_card_delay <= 0:
                    newCard = Card(350+all_dealer_cards*50, 20, True)
                    dealer_hand += newCard.value
                    dealer_card_delay = 60
                    all_dealer_cards += 1


        


            

    player_sprites.update()
    dealer_sprites.update()
    ui_sprites.update()

    cursor.update()

    screen.blit(background_image, (0, 0))


    if player_stand == True and player_hand > 21 or player_stand == True and dealer_hand > player_hand and dealer_hand <= 21:
        screen.blit(winFont.render("Dealer Wins", False, (255, 255, 255)), (180, 10))
        dealer_sprites.empty()
        
    if dealer_hand > 21:
        screen.blit(winFont.render("Player Wins", False, (255, 255, 255)), (200, 10))
        dealer_sprites.empty()
        
    if player_sprites.__len__() > 0 and dealer_sprites.__len__() > 0:
        screen.blit(handTextFont.render("Dealer Hand: "+str(dealer_hand), False, (255, 255, 255)), (230, 150))


    screen.blit(handTextFont.render("Hand: "+str(player_hand), False, (255, 255, 255)), (290, 460))



    player_sprites.draw(screen)
    dealer_sprites.draw(screen)
    ui_sprites.draw(screen)
    

    cursor.draw(screen)


    clock.tick(60)
    pygame.display.flip()
