from card import Card
from collections import deque
import random

# Used for plyaing games, contains 3 decks to move cards between:
# (deck, discard, and hand)
class PlayingDeck:
    def __init__(self, card_dict = None):
        self.deck = DeckOfCards(card_dict)
        self.discard = DeckOfCards(True)
        self.hand = DeckOfCards(True)


class DeckOfCards:
    def __init__(self, card_dict = None, empty_deck = False):
        self.deck = self.deck_builder(card_dict, empty_deck)
        self.size = 0
        
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
                    self.size += 1
        
        # 3: default deck
        else:
            suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
            for suit in suits:
                for rank in range(1, 14):
                    deck.append(Card(rank, suit))   
                    
        return deck
    
    def to_string(self) -> str:
        rep = ""
        for card in self.deck.items():
            rep += (f"{card}\n")
        return rep
    
    def shuffle(self):
        temp_list = list(self.deck)
        random.shuffle(temp_list)
        self.deck = deque(temp_list)
    
    def draw(self, location = "top", index = None) -> Card:
        location = str.lower(location)
        match location:
            case "top":
                self.size -= 1
                return self.draw_top()
            case "bottom":
                self.size -= 1
                return self.draw_bottom()
            case "random":
                self.size -= 1
                return self.draw_random()
            case _:
                try: 
                    assert(index != None)
                    self.size -= 1
                    return self.draw_index(index)
                except AssertionError:
                    print("No location or index provided for "
                            "DeckOfCards.add().")

    def discard(self, location = "top", index = None) -> Card:
        card = None
        try:
            card = self.draw(location, index)
        except AssertionError:
            print("No location or index provided for "
                  " DeckOfCards.dicard().")
        return card

    def draw_top(self) -> Card:
        if self.size == 0:
            return None
        return self.deck.popleft()
        
    def draw_bottom(self) -> Card:
        if self.size == 0:
            return None
        return self.deck.pop()
    
    def draw_index(self, index) -> Card:
        if self.size == 0:
            return None
        card = self.deck[index]
        del self.deck[index]
        return card
    
    def draw_random(self) -> Card:
        if len(self.deck) == 0:
            return None
        rand_index = random.randrange(len(self.deck))
        rand_card = self.deck[rand_index]
        del self.deck[rand_index]
        return rand_card
    
    def add(self, card, location = "top", index = None):
        location = str.lower(location)
        match location:
            case "top":
                self.size += 1
                self.deck.append(card)
            case "bottom":
                self.size += 1
                self.deck.insert(0, card)
            case _:
                try: 
                    assert(index != None)
                    self.size += 1
                    self.deck.insert(index, card)
                except AssertionError:
                    print("No location or index provided for "
                          "DeckOfCards.add().")

        
        
    