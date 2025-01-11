import tkinter as tk
import random


class MemoryMatchGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Ganesh Mulage Game")
        self.theme = None  # No default theme
        self.difficulty = None
        self.cards = []
        self.buttons = []
        self.first_card = None
        self.second_card = None
        self.locked = False
        self.matches_found = 0
        self.level = 1
        self.grid_size = 2
        self.create_theme_selection_screen()

    def apply_theme(self):
        """Applies the current theme to the window."""
        bg_color = "white" if self.theme == "Light" else "#2e2e2e"
        fg_color = "black" if self.theme == "Light" else "white"
        self.root.configure(bg=bg_color)
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=bg_color, fg=fg_color)
            elif isinstance(widget, tk.Button):
                widget.config(bg=bg_color, fg=fg_color, activebackground=fg_color, activeforeground=bg_color)

    def toggle_theme(self):
        """Toggles between light and dark themes."""
        self.theme = "Dark" if self.theme == "Light" else "Light"
        self.apply_theme()

    def create_theme_selection_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Select Theme", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Light Theme", command=lambda: self.set_theme("Light"), width=15, height=2).pack(pady=10)
        tk.Button(self.root, text="Dark Theme", command=lambda: self.set_theme("Dark"), width=15, height=2).pack(pady=10)

    def set_theme(self, theme):
        self.theme = theme
        self.apply_theme()
        self.create_difficulty_screen()

    def create_difficulty_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Select Level", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Easy", command=lambda: self.set_level(1), width=15, height=2).pack(pady=10)
        tk.Button(self.root, text="Medium", command=lambda: self.set_level(2), width=15, height=2).pack(pady=10)
        tk.Button(self.root, text="Hard", command=lambda: self.set_level(3), width=15, height=2).pack(pady=10)

    def set_level(self, level):
        self.level = level
        self.start_game()

    def start_game(self):
        self.clear_screen()
        self.cards = list(range(1, 9)) * 2
        if self.level == 2:
            self.cards += list(range(9, 13)) * 2
        elif self.level == 3:
            self.cards += list(range(9, 17)) * 2
        random.shuffle(self.cards)
        self.buttons = []
        self.first_card = None
        self.second_card = None
        self.locked = False
        self.matches_found = 0
        self.create_game_screen()

    def create_game_screen(self):
        rows = 4 if self.level == 1 else 5 if self.level == 2 else 6
        cols = 4
        for i, card in enumerate(self.cards):
            btn = tk.Button(self.root, text="?", width=10, height=5,
                            command=lambda c=card, b=i: self.reveal_card(c, b))
            btn.grid(row=i // cols, column=i % cols)
            self.buttons.append(btn)
        self.level_label = tk.Label(self.root, text=f"Level: {self.level}", font=("Arial", 14))
        self.level_label.grid(row=rows, column=0, columnspan=cols, pady=10)

    def reveal_card(self, card, index):
        if self.locked or self.buttons[index]["state"] == "disabled":
            return
        self.buttons[index].config(text=str(card), state="disabled")
        if not self.first_card:
            self.first_card = (self.buttons[index], card)
        elif not self.second_card:
            self.second_card = (self.buttons[index], card)
            self.check_match()

    def check_match(self):
        if self.first_card[1] == self.second_card[1]:
            self.matches_found += 1
            self.reset_cards(disable=True)
            if self.matches_found == len(self.cards) // 2:
                self.level_up()
        else:
            self.locked = True
            self.root.after(1000, self.reset_cards)

    def reset_cards(self, disable=False):
        for btn, _ in [self.first_card, self.second_card]:
            if not disable:
                btn.config(text="?", state="normal")
            else:
                btn.config(state="disabled")
        self.first_card = None
        self.second_card = None
        self.locked = False

    def level_up(self):
        if self.level < 3:
            self.level += 1
            self.grid_size += 1
            self.matches_found = 0
            self.create_game_screen()
        else:
            self.display_victory_message()

    def display_victory_message(self):
        self.clear_screen()
        tk.Label(self.root, text="Congratulations! You've completed all levels!", font=("Arial", 16), fg="green").pack(pady=20)
        tk.Button(self.root, text="Play Again", command=self.create_theme_selection_screen, width=15, height=2).pack(pady=10)
        self.apply_theme()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryMatchGame(root)
    root.mainloop()
