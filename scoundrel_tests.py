from scoundrel import ScoundrelGame
from deck_of_cards import PlayingDeck, DeckOfCards

# Test game initialization
def test_init():
    healthh = 20
    deck = PlayingDeck()
    print("Playing deck info:")
    print("\n\nDeck:")
    print(deck.deck.to_string())
    print("\n\nDiscard:")
    print(deck.discard.to_string())
    print("\n\nHand:")
    print(deck.hand.to_string())
    
    deck.deck.shuffle()
    print("\n\nShuffled deck:")
    print(deck.deck.to_string())
    
    room = DeckOfCards([], True)
    print("\n\nRoom:")
    print(room.to_string())
    
    can_run = True
    
    to_discard = []
    for card in deck.deck.deck:
        if (card.suit == "Hearts" or card.suit == "Diamonds") and (card.rank > 10 or card.rank == 1):
            to_discard.append(card)
    for card in to_discard:
        deck.deck.discard(card)
    print("Deck after deleting face reds:")
    print(deck.deck.to_string())
    
    print(f"Deck size: {deck.deck.size()}")

def test_drawing():
    deck = DeckOfCards([])
    print("\nNew deck:")
    print(deck.to_string())
    
    print("Drawing card from bottom:")
    card = deck.draw_bottom()
    print(card.to_string_debug())
    print("Deck:")
    print(deck.to_string())
    
    print("Drawing card from top:")
    card = deck.draw_top()
    print(card.to_string_debug())
    
    print("Drawing card from index = 4:")
    card = deck.draw_index(4)
    print(card.to_string_debug())
    
    print("Drawing using generalized draw(), index = 2:")
    card = deck.draw(None, 2)
    print(card.to_string_debug())
    
    

def main():
    test_init()
    test_drawing()

if __name__ == "__main__":
    main()