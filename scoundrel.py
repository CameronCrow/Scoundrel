from deck_of_cards import PlayingDeck
from deck_of_cards import DeckOfCards


class ScoundrelGame:
    def __init__(self):
        self.health = 20
        self.deck = PlayingDeck()
        self.deck.deck.ace_high()
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
        for card in to_discard:
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
        while self.room.size() > 0: # send room to bottom of deck
            self.deck.deck.add(self.room.discard(), "bottom")
                
        while self.room.size() < 4:
            self.room.add(self.deck.deck.draw("top"), "top")
    
    def refill_room(self):
        while self.room.size() < 4:
            self.room.add(self.deck.deck.draw("top"))
      
    def attack_enemy(self, room_index = -1, weapon = None):
        enemy_card = self.room.get_card(room_index)
        try:
            assert(enemy_card.suit == "Spades" or enemy_card.suit == "Clubs")
        except AssertionError:
            raise Exception("Enemy is not a spade or club!")
        enemy = self.room.discard(enemy_card, None, None)
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
        
    def take_damage(self, amount):
        self.health -= amount
    
    def heal_with(self, room_index):
        heal_card = self.room.get_card(room_index)
        try:
            assert(heal_card.suit == "Hearts")
        except AssertionError:
            raise Exception("Card is not a heart!")
        heal_card = self.room.discard(heal_card, None, None)
        heal_amount = heal_card.rank
        self.deck.discard.add(heal_card, "top")
        self.heal(heal_amount)
    
    def heal(self, heal_amount):
        self.health += heal_amount
        self.health = min(self.health, 20)
        
    # Equips given weapon and discards old weapon
    def equip_weapon(self, room_index):
        weapon_card = self.room.get_card(room_index)
        try:
            assert(weapon_card.suit == "Diamonds")
        except AssertionError:
            raise Exception("Card is not a diamond!")
        # Given weapon is valid, continue
        if self.weapon:
            self.deck.deck.discard(self.weapon.card, "top") # Add current weapon to discard
        weapon = self.room.discard(weapon_card, None, None)
        self.deck.discard.add(weapon, "top")
        self.weapon = self.Weapon(weapon, weapon.rank)
        
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
            damage_taken = 0
            if target.rank < self.max: # Weapon can attack this enemy
                self.max = target.rank
                barehanded = False
                if self.power < target.rank:
                    damage_taken = target.rank - self.power
                return barehanded, damage_taken
            else: # Weapon too weak, must barehand
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
        print("D. Display game status")
        print("R. Run from room")
        print("E. Equip weapon (select diamond from room)")
        print("A. Attack enemy (select spade/club from room)")
        print("H. Heal with heart")
        print("Q. Quit game")
        
        try:
            choice = str.lower(input("\nEnter your choice: ").strip())
            
            if choice == "d":
                print("\n" + game.status_str())
                
            elif choice == "r":
                if game.can_run:
                    game.run_from_room()
                    print("\nYou ran from the room!")
                else:
                    print("You cannot run right now!")
                    
            elif choice == "e":
                if game.room.size() == 0:
                    print("Room is empty!")
                    continue
                    
                print(game.room_status_str())
                
                try:
                    index = int(input("Select card index (0-3) to equip as weapon: "))
                    if 0 <= index < game.room.size():
                        try:
                            game.equip_weapon(index)
                        except Exception as e:
                            print(f"Error equipping weapon: {e}")
                            continue
                        print(f"Equipped weapon!")
                    else:
                        print("Invalid index!")
                except ValueError:
                    print("Please enter a valid number!")
                    
            elif choice == "a":
                if game.room.size() == 0:
                    print("Room is empty!")
                    continue
                    
                print(game.room_status_str())
                
                try:
                    index = int(input("Select enemy to attack: "))
                    enemy = game.room.get_card(index)
                    weapon_to_use = game.weapon
                    if game.can_use_weapon(enemy):
                        barehanded_in = None
                        barehanded_in = input("Attack barehanded or with a weapon? (y/n): ").strip()
                        barehanded = bool(str.lower(barehanded_in) == 'y')
                        if barehanded:
                            weapon_to_use = None
                    if 0 <= index < game.room.size():
                        try:
                            barehanded, damage = game.attack_enemy(index, weapon_to_use)
                        except Exception as e:
                            print(f"Error attacking enemy: {e}")
                            continue
                        if barehanded:
                            print(f"Attacked {enemy} with bare hands! Took {damage} damage.")
                        else:
                            print(f"Attacked {enemy} with {game.weapon.card}! Took {damage} damage.")
                        game.update_room()
                    else:
                        print("Invalid index!")
                except ValueError:
                    print("Please enter a valid number!")
                    
            elif choice == "h":
                if game.room.size() == 0:
                    print("Room is empty!")
                    continue
                    
                print(game.room_status_str())
                
                try:
                    index = int(input("Select heart card to heal with: "))
                    if 0 <= index < game.room.size():
                        try:
                            game.heal_with(index)
                        except Exception as e:
                            print(f"Error healing: {e}")
                            continue
                        print("Healed!")
                        game.update_room()
                    else:
                        print("Invalid index!")
                except ValueError:
                    print("Please enter a valid number!")
                    
            elif choice == "q":
                print("Thanks for playing!")
                break
                
            else:
                print("Invalid choice! Please try again.")
                
        except KeyboardInterrupt:
            print("\n\nGame interrupted. Thanks for playing!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            
    if game.health <= 0:
        print("\nGame Over! You died!")
    
    
if __name__ == "__main__":
    main()