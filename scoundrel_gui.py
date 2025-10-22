import tkinter as tk
from tkinter import messagebox, ttk
from scoundrel import ScoundrelGame


class ScoundrelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Scoundrel - GUI Edition")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        self.game = ScoundrelGame()
        self.game.move_rooms()
        
        self.selecting_card_mode = None  # None, "attack", "equip", "heal"
        
        self.setup_ui()
        self.update_display()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="SCOUNDREL", 
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        title_label.pack(pady=(0, 20))
        
        # Status Frame
        status_frame = tk.Frame(main_frame, bg="#34495e", relief=tk.RAISED, borderwidth=2)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.health_label = tk.Label(
            status_frame,
            text="Health: 20",
            font=("Arial", 16, "bold"),
            bg="#34495e",
            fg="#e74c3c"
        )
        self.health_label.pack(pady=5)
        
        self.deck_label = tk.Label(
            status_frame,
            text="Cards in deck: 0",
            font=("Arial", 12),
            bg="#34495e",
            fg="#ecf0f1"
        )
        self.deck_label.pack(pady=5)
        
        self.weapon_label = tk.Label(
            status_frame,
            text="Weapon: None",
            font=("Arial", 12),
            bg="#34495e",
            fg="#ecf0f1"
        )
        self.weapon_label.pack(pady=5)
        
        # Room Frame
        room_frame = tk.Frame(main_frame, bg="#2c3e50")
        room_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        room_title = tk.Label(
            room_frame,
            text="ROOM",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        room_title.pack(pady=(0, 10))
        
        self.room_buttons_frame = tk.Frame(room_frame, bg="#2c3e50")
        self.room_buttons_frame.pack()
        
        self.room_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.room_buttons_frame,
                text="",
                font=("Arial", 12),
                width=15,
                height=4,
                bg="#ecf0f1",
                fg="#2c3e50",
                relief=tk.RAISED,
                borderwidth=3,
                command=lambda idx=i: self.card_button_clicked(idx)
            )
            btn.grid(row=0, column=i, padx=5)
            self.room_buttons.append(btn)
        
        # Message Label
        self.message_label = tk.Label(
            main_frame,
            text="Choose an action",
            font=("Arial", 12, "italic"),
            bg="#2c3e50",
            fg="#f39c12",
            wraplength=700
        )
        self.message_label.pack(pady=(0, 10))
        
        # Action Buttons Frame
        action_frame = tk.Frame(main_frame, bg="#2c3e50")
        action_frame.pack()
        
        button_style = {
            "font": ("Arial", 11, "bold"),
            "width": 12,
            "height": 2,
            "relief": tk.RAISED,
            "borderwidth": 2
        }
        
        self.attack_btn = tk.Button(
            action_frame,
            text="ATTACK",
            bg="#e74c3c",
            fg="white",
            command=self.attack_action,
            **button_style
        )
        self.attack_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.equip_btn = tk.Button(
            action_frame,
            text="EQUIP",
            bg="#3498db",
            fg="white",
            command=self.equip_action,
            **button_style
        )
        self.equip_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.heal_btn = tk.Button(
            action_frame,
            text="HEAL",
            bg="#27ae60",
            fg="white",
            command=self.heal_action,
            **button_style
        )
        self.heal_btn.grid(row=0, column=2, padx=5, pady=5)
        
        self.run_btn = tk.Button(
            action_frame,
            text="RUN",
            bg="#f39c12",
            fg="white",
            command=self.run_action,
            **button_style
        )
        self.run_btn.grid(row=0, column=3, padx=5, pady=5)
        
    def update_display(self):
        # Update status labels
        self.health_label.config(text=f"Health: {self.game.health}")
        self.deck_label.config(text=f"Cards in deck: {self.game.deck.deck.size()}")
        
        if self.game.weapon:
            weapon_text = f"Weapon: {self.game.weapon.card} (Power: {self.game.weapon.power}, Max: {self.game.weapon.max})"
        else:
            weapon_text = "Weapon: None"
        self.weapon_label.config(text=weapon_text)
        
        # Update room buttons
        for i in range(4):
            if i < self.game.room.size():
                card = self.game.room.get_card(i)
                card_text = str(card)
                
                # Color code by suit
                if card.suit == "Hearts":
                    bg_color = "#ffb3ba"  # Light red
                    fg_color = "#c0392b"
                elif card.suit == "Diamonds":
                    bg_color = "#bae1ff"  # Light blue
                    fg_color = "#2980b9"
                elif card.suit == "Spades":
                    bg_color = "#555555"  # Dark gray
                    fg_color = "white"
                elif card.suit == "Clubs":
                    bg_color = "#333333"  # Darker gray
                    fg_color = "white"
                else:
                    bg_color = "#ecf0f1"
                    fg_color = "#2c3e50"
                
                self.room_buttons[i].config(
                    text=card_text,
                    bg=bg_color,
                    fg=fg_color,
                    state=tk.NORMAL
                )
            else:
                self.room_buttons[i].config(
                    text="",
                    bg="#95a5a6",
                    fg="#2c3e50",
                    state=tk.DISABLED
                )
        
        # Check game over
        if self.game.health <= 0:
            messagebox.showinfo("Game Over", "You died! Game Over.")
            self.root.quit()
        
        # Check if deck is empty
        if self.game.deck.deck.size() == 0:
            messagebox.showinfo("Victory!", "You've cleared the deck! You win!")
            self.root.quit()
    
    def card_button_clicked(self, room_index):
        if self.selecting_card_mode == "attack":
            self.execute_attack(room_index)
        elif self.selecting_card_mode == "equip":
            self.execute_equip(room_index)
        elif self.selecting_card_mode == "heal":
            self.execute_heal(room_index)
        else:
            self.set_message("Please select an action first (Attack, Equip, or Heal)")
    
    def attack_action(self):
        if self.game.room.size() == 0:
            self.set_message("Room is empty!")
            return
        self.selecting_card_mode = "attack"
        self.set_message("Select an enemy (Spade or Club) to attack")
    
    def execute_attack(self, room_index):
        if room_index >= self.game.room.size():
            self.set_message("Invalid card selection!")
            return
        
        try:
            enemy = self.game.room.get_card(room_index)
            weapon_to_use = self.game.weapon
            
            # Check if we can use weapon
            if self.game.can_use_weapon(enemy):
                # Ask if player wants to use weapon
                use_weapon = messagebox.askyesno(
                    "Use Weapon?",
                    f"Attack {enemy} with your weapon?\n\n"
                    f"Yes = Use weapon\n"
                    f"No = Attack barehanded"
                )
                if not use_weapon:
                    weapon_to_use = None
            else:
                weapon_to_use = None
            
            barehanded, damage = self.game.attack_enemy(room_index, weapon_to_use)
            
            if barehanded:
                self.set_message(f"Attacked {enemy} with bare hands! Took {damage} damage.")
            else:
                self.set_message(f"Attacked {enemy} with {self.game.weapon.card}! Took {damage} damage.")
            
            self.game.update_room()
            self.selecting_card_mode = None
            self.update_display()
            
        except Exception as e:
            self.set_message(f"Error: {e}")
            self.selecting_card_mode = None
    
    def equip_action(self):
        if self.game.room.size() == 0:
            self.set_message("Room is empty!")
            return
        self.selecting_card_mode = "equip"
        self.set_message("Select a Diamond card to equip as weapon")
    
    def execute_equip(self, room_index):
        if room_index >= self.game.room.size():
            self.set_message("Invalid card selection!")
            return
        
        try:
            weapon_card = self.game.room.get_card(room_index)
            self.game.equip_weapon(room_index)
            self.set_message(f"Equipped {weapon_card} as weapon!")
            self.selecting_card_mode = None
            self.update_display()
        except Exception as e:
            self.set_message(f"Error: {e}")
            self.selecting_card_mode = None
    
    def heal_action(self):
        if self.game.room.size() == 0:
            self.set_message("Room is empty!")
            return
        self.selecting_card_mode = "heal"
        self.set_message("Select a Heart card to heal")
    
    def execute_heal(self, room_index):
        if room_index >= self.game.room.size():
            self.set_message("Invalid card selection!")
            return
        
        try:
            heal_card = self.game.room.get_card(room_index)
            self.game.heal_with(room_index)
            self.set_message(f"Healed with {heal_card}!")
            self.game.update_room()
            self.selecting_card_mode = None
            self.update_display()
        except Exception as e:
            self.set_message(f"Error: {e}")
            self.selecting_card_mode = None
    
    def run_action(self):
        try:
            if self.game.can_run:
                self.game.run_from_room()
                self.set_message("You ran from the room!")
                self.update_display()
            else:
                self.set_message("You cannot run right now!")
        except Exception as e:
            self.set_message(f"Error: {e}")
    
    def set_message(self, message):
        self.message_label.config(text=message)


def main():
    root = tk.Tk()
    app = ScoundrelGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

