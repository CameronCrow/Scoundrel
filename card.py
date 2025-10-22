import pprint

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.face_name = self.get_face_name()
        try:
            assert(type(rank) == int)
            assert(type(suit) == str)
        except AssertionError:
            print("Type error when creating Card:\n")
            print(f"\ttype(rank) = {type(rank)}")
            print(f"\ttype(suit) = {type(suit)}")
        
    def __repr__(self):
        return f"{self.face_name} of {self.suit}"
        
    def to_string_debug(self): # add more object info here if necessary
        return f"{self.face_name} of {self.suit}"
        
    def get_face_name(self):
        match self.rank:
            case 1:
                return "Ace"
            case 11:
                return "Jack"
            case 12: 
                return "Queen"
            case 13:
                return "King"
            case _: # face name is the number if 2-10
                return self.rank
    
    def equals(self, other) -> bool:
        if other == None:
            return False
        if (self.rank == other.rank and self.face_name == other.face_name and self.suit == other.suit):
            return True
        else:
            return False
        
    def __eq__(self, other):
        return self.equals(other)