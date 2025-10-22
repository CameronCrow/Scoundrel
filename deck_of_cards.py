from card import Card
from collections import deque
import random

# Used for plyaing games, contains 3 decks to move cards between:
# (deck, discard, and hand)
class PlayingDeck:
    def __init__(self, card_dict = None):
        self.deck = DeckOfCards(card_dict)
        self.discard = DeckOfCards(None, True)
        self.hand = DeckOfCards(None, True)


class DeckOfCards:
    def __init__(self, card_dict = None, empty_deck = False):
        self.deck = self.deck_builder(card_dict, empty_deck)
        
    def deck_builder(self, card_dict = None, empty_deck = False):
        # scenarios
        # 1: Given full card info, count -> just duplicate count times
        # 2: Given rank, count -> make even amount for each suit
        # 3: dict is empty, just make default 52 card deck
        
        # TODO: implement 1 and 2
        deck = deque()
        if empty_deck:
            return deck
        
        if card_dict:
            for card, count in card_dict.items():
                for _ in range(count):
                    new_card = Card(card.rank, card.suit)
                    deck.append(new_card)
        
        # 3: default deck
        else:
            suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
            for suit in suits:
                for rank in range(1, 14):
                    deck.append(Card(rank, suit))   
        
        return deck
    
    # default 52 card deck init uses ace low
    def ace_high(self):
        for card in self.deck:
            if card.rank == 1:
                card.rank = 14
    
    def to_string(self) -> str:
        rep = ""
        for card in self.deck:
            rep += (f"{card}\n")
        return rep
    
    def size(self):
        return len(self.deck)
    
    def shuffle(self):
        temp_list = list(self.deck)
        random.shuffle(temp_list)
        self.deck = deque(temp_list)
    
    def draw(self, location = "top", index = None) -> Card:
        if location != None:
            location = str.lower(location)
        match location:
            case "top":
                return self.draw_top()
            case "bottom":
                return self.draw_bottom()
            case "random":
                return self.draw_random()
            case _:
                try: 
                    assert(index != None)
                    return self.draw_index(index)
                except AssertionError:
                    print("No location or index provided for "
                            "DeckOfCards.add().")
                    
    def get_card(self, index):
        if self.size() == 0:
            return None
        return self.deck[index]

    # problem with this function
    def discard(self, card_to_discard = None, location = "top", index = None) -> Card:
        card = None
        if card_to_discard != None:
            card = self.discard_card(card_to_discard)
        else:
            card = self.draw(location, index)
        return card
    
    def discard_card(self, card) -> Card:
        i = 0
        for curr_card in self.deck:
            if curr_card == card:
                return self.draw_index(i)
            i += 1
        return None

    def draw_top(self) -> Card:
        if self.size() == 0:
            return None
        return self.deck.popleft()
        
    def draw_bottom(self) -> Card:
        if self.size() == 0:
            return None
        return self.deck.pop()
    
    def draw_index(self, index) -> Card:
        if self.size() == 0:
            return None
        card = self.deck[index]
        del self.deck[index]
        return card
    
    def draw_random(self) -> Card:
        if self.size() == 0:
            return None
        rand_index = random.randrange(len(self.deck))
        rand_card = self.deck[rand_index]
        del self.deck[rand_index]
        return rand_card
    
    def add(self, card, location = "top", index = None):
        if location:
            location = str.lower(location)
        match location:
            case "top":
                self.deck.insert(0, card)
            case "bottom":
                self.deck.append(card)
            case _:
                try: 
                    assert(index != None)
                    self.deck.insert(index, card)
                except AssertionError:
                    print("No location or index provided for "
                          "DeckOfCards.add().")
                
    