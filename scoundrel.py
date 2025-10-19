from deck_of_cards import PlayingDeck
from deck_of_cards import DeckOfCards


class ScoundrelGame:
    def __init__(self):
        self.health = 20
        self.deck = PlayingDeck()
        self.deck.deck.shuffle()
        self.weapon = None
        self.room = DeckOfCards([], True)
        self.can_run = True
        self.discard_face_reds()
        
        
    def discard_face_reds(self):
        to_discard = []
        for card in self.deck.deck.deck:
            if (card.suit == "Hearts" or card.suit == "Diamonds") and (card.rank > 10 or card.rank == 1):
                to_discard.append(card)
                print(f"Discard {card}")
        for card in to_discard:
            print(f"Discarding {card}")
            self.deck.deck.discard(card)
            
    
    def update_room(self):
        if self.room.size() <= 1:
            self.refill_room()
    
    def run_from_room(self):
        if self.can_run:
            self.reset_room()
            self.can_run = False
        else:
            Exception("Can not run!")
            
    def move_rooms(self):
        self.can_run = True
        self.refill_room()
        
    def reset_room(self):
        print("Sending room to bottom of deck")
        while self.room.size() > 0: # send room to bottom of deck
            print(f"Room size: {self.room.size()}")
            self.deck.deck.add(self.room.discard(), "bottom")
                
        print("drawing into a new room")
        while self.room.size() < 4:
            self.room.add(self.deck.deck.draw("top"), "top")
    
    def refill_room(self):
        while self.room.size() < 4:
            self.room.add(self.deck.deck.draw("top"))
    
    def take_damage(self, amount):
        self.health -= amount
    
    def heal(self, amount):
        self.health += amount
        
    def attack_enemy(self, room_index = -1, weapon = None):
        enemy = self.room.discard(None, None, room_index)
        try:
            assert(enemy.suit == "Spades" or enemy.suit == "Clubs")
        except AssertionError:
            print("Enemy is not a spade or club!")
        damage_taken = 0
        self.deck.discard.add(enemy)
        barehanded = True
        if weapon:
            barehanded, damage_taken = weapon.use(enemy)
            self.take_damage(damage_taken)
        else:
            barehanded = True
            damage_taken = enemy.rank
            self.take_damage(damage_taken)
        self.deck.discard.add(enemy)
        return barehanded, damage_taken
    
    def equip_weapon(self, room_index):
        card = self.room.discard(None, None, room_index)
        try:
            assert(card.suit == "Diamonds")
        except AssertionError:
            print("Card is not a diamond!")
            return
        if self.weapon:
            self.deck.discard.add(self.weapon.card, "top")
        self.weapon = self.Weapon(card, card.rank)
    
    def heal_with(self, room_index):
        heal_card = self.room.discard(None, None, room_index)
        try:
            assert(heal_card.suit == "Hearts")
        except AssertionError:
            print("Card is not a heart!")
        heal_amount = heal_card.rank
        self.deck.discard.add(heal_card, "top")
        self.heal(heal_amount)
    
    def heal(self, heal_amount):
        self.health += heal_amount
        self.health = min(self.health, 20)
        
    def status_str(self) -> str:
        status_str = f"Health: {self.health}\n"
        status_str += f"Cards left in deck: {self.deck.deck.size()}\n"
        if self.weapon:
            status_str += f"Weapon: {self.weapon.card}\n"
            status_str += f"  Power = {self.weapon.power}\n"
            status_str += f"  Max = {self.weapon.max}\n"
        else:
            status_str += "Weapon: None\n"
        status_str += "Room:\n"
        status_str += self.room.to_string()
        return status_str
    
    def room_status_str(self) -> str:
        room_status_str = "Room:\n"
        room_status_str += f"{self.room.to_string()}\n"
        return room_status_str
    
    def can_use_weapon(self, enemy) -> bool:
        if self.weapon != None:
            if self.weapon.max >= enemy.rank:
                return True
        return False
        
    class Weapon:
        def __init__(self, card, max = 14):
            self.card = card
            self.max = 14
            self.power = card.rank
            
        def use(self, target):
            barehanded = True
            if target.rank < self.max:
                self.max = target.rank
                barehanded = False
                return barehanded, target.rank - self.power
            else:
                return barehanded, target.rank
        
        def __repr__(self):
            return f"Weapon: {self.card} (Power: {self.power}, Max: {self.max})"
        

def main():
    game = ScoundrelGame()
    print("\n\nWelcome to Scoundrel - CLI Edition\n\n")
    game.move_rooms()
    
    while game.health > 0:
        print("=" * 50)
        print(game.status_str())
        print("=" * 50)
        
        # Show available actions
        print("\nAvailable Actions:")
        print("1. Display game status")
        print("2. Run from room")
        print("3. Equip weapon (select diamond from room)")
        print("4. Attack enemy (select spade/club from room)")
        print("5. Heal with heart")
        print("6. Quit game")
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                print("\n" + game.status_str())
                
            elif choice == "2":
                if game.can_run:
                    game.run_from_room()
                    print("You ran from the room!")
                else:
                    print("You cannot run right now!")
                    
            elif choice == "3":
                if game.room.size() == 0:
                    print("Room is empty!")
                    continue
                    
                print(game.room_status_str())
                
                try:
                    index = int(input("Select card index (0-3) to equip as weapon: "))
                    if 0 <= index < game.room.size():
                        game.equip_weapon(index)
                        print(f"Equipped weapon!")
                    else:
                        print("Invalid index!")
                except ValueError:
                    print("Please enter a valid number!")
                    
            elif choice == "4":
                if game.room.size() == 0:
                    print("Room is empty!")
                    continue
                    
                print(game.room_status_str())
                
                try:
                    index = int(input("Select enemy to attack: "))
                    enemy = game.deck.deck.get_card(index)
                    weapon_to_use = game.weapon
                    if game.can_use_weapon(enemy):
                        barehanded_in = None
                        barehanded_in = input("Attack barehanded or with a weapon? (y/n)").strip()
                        barehanded = bool(str.lower(barehanded_in) == 'y')
                        if barehanded:
                            weapon_to_use = None
                    if 0 <= index < game.room.size():
                        barehanded, damage = game.attack_enemy(index, weapon_to_use)
                        if barehanded:
                            print(f"Attacked {enemy} with bare hands! Took {damage} damage.")
                        else:
                            print(f"Attacked {enemy} with {game.weapon.card}! Took {damage} damage.")
                        game.update_room()
                    else:
                        print("Invalid index!")
                except ValueError:
                    print("Please enter a valid number!")
                    
            elif choice == "5":
                if game.room.size() == 0:
                    print("Room is empty!")
                    continue
                    
                print(game.room_status_str())
                
                try:
                    index = int(input("Select heart card to heal with: "))
                    if 0 <= index < game.room.size():
                        game.heal_with(index)
                        print("Healed!")
                        game.update_room()
                    else:
                        print("Invalid index!")
                except ValueError:
                    print("Please enter a valid number!")
                    
            elif choice == "6":
                print("Thanks for playing!")
                break
                
            else:
                print("Invalid choice! Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n\nGame interrupted. Thanks for playing!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            
    if game.health <= 0:
        print("\nGame Over! You died!")
    
    
if __name__ == "__main__":
    main()