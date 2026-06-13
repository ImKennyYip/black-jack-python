import pygame
from sys import exit
import random

GAME_WIDTH = 600
GAME_HEIGHT = 600

CARD_WIDTH = 110
CARD_HEIGHT = 154
CARD_SPACING = 5

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.image = pygame.image.load(f"cards/{value}-{suit}.png")
        self.image = pygame.transform.smoothscale(self.image, (CARD_WIDTH, CARD_HEIGHT))

    def __str__(self):
        return f"{self.value}-{self.suit}"

    def get_value(self):
        if self.value == "A":
            return 11

        if self.value in ["J", "Q", "K"]:
            return 10

        return int(self.value)

class Player:
    def __init__(self):
        self.hand = []
        self.sum = 0
        self.ace_count = 0

    def add_card(self, card):
        self.hand.append(card)
        self.sum += card.get_value()

        if card.value == "A":
            self.ace_count += 1

    def get_total(self):
        total = self.sum
        aces = self.ace_count

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

def build_deck():
    values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ["C", "D", "H", "S"]
    return [Card(value, suit) for suit in suits for value in values]

def start_game():
    global deck, dealer, player, hidden_card, game_over, message

    deck = build_deck()
    random.shuffle(deck)

    dealer = Player()
    player = Player()

    game_over = False
    message = ""

    hidden_card = deck.pop()
    dealer.add_card(hidden_card)
    dealer.add_card(deck.pop())

    for i in range(2):
        player.add_card(deck.pop())

dealer = Player()
player = Player()
deck = []
hidden_card = None
game_over = False
message = ""

start_game()


pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Black Jack")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 30)
back_image = pygame.image.load("cards/BACK.png")
back_image = pygame.transform.smoothscale(back_image, (CARD_WIDTH, CARD_HEIGHT))

def hit():
    if game_over:
        return

    player.add_card(deck.pop())

    if player.get_total() > 21:
        stay()


def stay():
    global game_over, message

    if game_over:
        return

    while dealer.get_total() < 17:
        dealer.add_card(deck.pop())

    dealer_total = dealer.get_total()
    player_total = player.get_total()

    if player_total > 21:
        message = "You Lose!"
    elif dealer_total > 21 or player_total > dealer_total:
        message = "You Win!"
    elif player_total == dealer_total:
        message = "Tie!"
    else:
        message = "You Lose!"

    game_over = True


def draw():
    window.fill((53, 101, 77))

    if game_over:
        window.blit(hidden_card.image, (20, 20))
    else:
        window.blit(back_image, (20, 20))

    for i in range(1, len(dealer.hand)):
        card = dealer.hand[i]
        x = CARD_WIDTH + 25 + (CARD_WIDTH + CARD_SPACING) * (i - 1)
        window.blit(card.image, (x, 20))

    for i in range(len(player.hand)):
        card = player.hand[i]
        x = 20 + (CARD_WIDTH + CARD_SPACING) * i
        window.blit(card.image, (x, 320))

    controls = font.render("H = Hit   S = Stay   R = Restart", True, "white")
    window.blit(controls, (80, 560))

    if game_over:
        result_text = font.render(message, True, "white")
        window.blit(result_text, (220, 250))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                hit()
            elif event.key == pygame.K_s:
                stay()
            elif event.key == pygame.K_r:
                start_game()

    draw()
    pygame.display.update()
    clock.tick(60)