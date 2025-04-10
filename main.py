import tkinter as tk
from tkinter import ttk
import keyboard
#


class VerityOverlay:
    def __init__(self, root):
        self.root = root
        root.title("Verity Solver | Destiny 2")
        root.geometry("330x500+100+100")
        root.attributes("-topmost", True)
        root.configure(bg='#222222'),
        self.mode_var = tk.StringVar(value="Fast")

        # Initialize variables
        self.statue_var = tk.StringVar(value="Not Selected")
        self.held_shape_var = tk.StringVar(value="Not Selected")
        self.wall_shapes = []
        self.solution_var = tk.StringVar(value="")

        # Create UI
        self.create_widgets()
        self.setup_hotkeys()

    def create_widgets(self):

        # Toggle button in top-left
        mode_frame = tk.Frame(self.root, bg='#222222')
        mode_frame.pack(anchor='nw', padx=5, pady=5)

        self.mode_button = tk.Button(
            mode_frame,
            text="Mode: Fast",
            command=self.toggle_mode,
            bg="#444444",
            fg="white",
            font=("Arial", 10),
            relief="flat",
            padx=5,
            pady=2
        )
        self.mode_button.pack(side="left")

        # Custom Style
        style = ttk.Style()
        style.configure('TLabel', background='#222222', foreground='white', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 10, 'bold'), foreground='#222222', background='#222222')
        style.configure('Solution.TLabel', font=('Arial', 10, 'bold'), foreground='yellow')

        # Title
        tk.Label(self.root, text="Destiny 2 - Verity Helper", fg="#222222", bg="#222222",
                 font=('Arial', 10, 'bold')).pack(pady=(5, 10))

        # Frame (changed to tk.Frame for bg control)
        selection_frame = tk.Frame(self.root, bg="#222222")
        selection_frame.pack(pady=5)
        selection_frame.grid_columnconfigure(1, weight=1)

        # Statue Section
        tk.Label(selection_frame, text="My Statue:", fg="white", bg="#222222", font=('Arial', 10)).grid(row=0, column=0,
                                                                                                        sticky="w",
                                                                                                        padx=5)
        tk.Label(selection_frame, textvariable=self.statue_var, fg="#FF5555", bg="#222222", font=('Arial', 10)).grid(
            row=0, column=1, sticky="w")

        # Held Shape Section
        tk.Label(selection_frame, text="Held Shape:", fg="white", bg="#222222", font=('Arial', 10)).grid(row=1,
                                                                                                         column=0,
                                                                                                         sticky="w",
                                                                                                         padx=5)
        tk.Label(selection_frame, textvariable=self.held_shape_var, fg="#55FF55", bg="#222222",
                 font=('Arial', 10)).grid(row=1, column=1, sticky="w")

        # Wall Shapes Section
        tk.Label(selection_frame, text="Wall Shapes:", fg="white", bg="#222222", font=('Arial', 10)).grid(row=2,
                                                                                                          column=0,
                                                                                                          sticky="w",
                                                                                                          padx=5)
        self.wall_shapes_label = tk.Label(selection_frame, text="Not Selected", fg="#5555FF", bg="#222222",
                                          font=('Arial', 10))
        self.wall_shapes_label.grid(row=2, column=1, sticky="w")

        # Solution Section
        ttk.Label(self.root, text="Solution:", style='Title.TLabel').pack(pady=(15, 5))
        self.solution_label = ttk.Label(self.root, textvariable=self.solution_var, style='Solution.TLabel',
                                        wraplength=300)
        self.solution_label.pack()

        # Hotkey Legend
        ttk.Label(self.root, text="Hotkey Legend:", style='Title.TLabel').pack(pady=(10, 0))

        legend_text = (
            "        Statue Position\n"
            "7 = Left Statue   |   8 = Mid Statue   |   9 = Right Statue\n\n"
            "           Held Shape\n"
            "4 = Square        |   5 = Triangle     |   6 = Circle\n\n"
            "          Wall Shapes\n"
            "1 = Square        |   2 = Triangle     |   3 = Circle\n\n"
            "           0 = Reset"
        )

        # Clean out weird invisible characters just in case
        legend_text = legend_text.replace('\u00A0', ' ').replace('\u200B', ' ')

        legend_label = ttk.Label(
            self.root,
            text=legend_text,
            foreground="#AAAAAA",
            font=('Arial', 10),
            justify="center"
        )
        legend_label.pack(pady=(0, 10))

    def setup_hotkeys(self):
        # Statue Selection (Numpad 7-9)
        keyboard.add_hotkey("num 7", lambda: self.update_statue("Left"))
        keyboard.add_hotkey("num 8", lambda: self.update_statue("Mid"))
        keyboard.add_hotkey("num 9", lambda: self.update_statue("Right"))

        # Held Shape Selection (Numpad 4-6)
        keyboard.add_hotkey("num 4", lambda: self.update_held_shape("Square"))
        keyboard.add_hotkey("num 5", lambda: self.update_held_shape("Triangle"))
        keyboard.add_hotkey("num 6", lambda: self.update_held_shape("Circle"))

        # Wall Shapes Selection (Numpad 1-3)
        keyboard.add_hotkey("num 1", lambda: self.update_wall_shapes("Square"))
        keyboard.add_hotkey("num 2", lambda: self.update_wall_shapes("Triangle"))
        keyboard.add_hotkey("num 3", lambda: self.update_wall_shapes("Circle"))

        # Reset (Numpad 0)
        keyboard.add_hotkey("num 0", self.reset_all)

    def toggle_mode(self):
            current = self.mode_var.get()
            new_mode = "Double" if current == "Fast" else "Fast"
            self.mode_var.set(new_mode)
            self.mode_button.config(text=f"Mode: {new_mode}")
            self.calculate_solution()

    def update_statue(self, position):
        self.statue_var.set(position)
        self.calculate_solution()

    def update_held_shape(self, shape):
        self.held_shape_var.set(shape)
        self.calculate_solution()

    def update_wall_shapes(self, shape):
        if shape in self.wall_shapes:
            self.wall_shapes.remove(shape)
        else:
            if len(self.wall_shapes) < 2:
                self.wall_shapes.append(shape)

        if len(self.wall_shapes) == 0:
            self.wall_shapes_label.config(text="Not Selected")
        elif len(self.wall_shapes) == 1:
            self.wall_shapes_label.config(text=self.wall_shapes[0])
        else:
            self.wall_shapes_label.config(text=f"{self.wall_shapes[0]} + {self.wall_shapes[1]}")

        self.calculate_solution()

    def calculate_solution(self):
        if (self.held_shape_var.get() == "Not Selected" or
                len(self.wall_shapes) != 2 or
                self.statue_var.get() == "Not Selected"):
            self.solution_var.set("")
            return

        held = self.held_shape_var.get()
        wall1, wall2 = self.wall_shapes[0], self.wall_shapes[1]

        if self.mode_var.get() == "Double":
            if held == "Triangle":
                if "Triangle" in self.wall_shapes and "Circle" in self.wall_shapes:
                    self.solution_var.set(
                        "Deposit Circle on CIRCLE statue\n"
                        "You should now have 2 TRIANGLES on your wall\n"
                        "Give TRIANGLE to SQUARE statue and CIRCLE statue\n"
                        "Pick up both shapes and leave"
                    )
                elif "Triangle" in self.wall_shapes and "Square" in self.wall_shapes:
                    self.solution_var.set(
                        "Deposit Square on SQUARE statue\n"
                        "You should now have 2 TRIANGLES on your wall\n"
                        "Give TRIANGLE to SQUARE statue and CIRCLE statue\n"
                        "Pick up both shapes and leave"
                    )
            elif held == "Circle":
                if "Triangle" in self.wall_shapes and "Circle" in self.wall_shapes:
                    self.solution_var.set(
                        "Deposit Triangle on TRIANGLE statue\n"
                        "You should now have 2 CIRCLES on your wall\n"
                        "Give CIRCLE to SQUARE statue and TRIANGLE statue\n"
                        "Pick up both shapes and leave"
                    )
                elif "Square" in self.wall_shapes and "Circle" in self.wall_shapes:
                    self.solution_var.set(
                        "Deposit Square on SQUARE statue\n"
                        "You should now have 2 CIRCLES on your wall\n"
                        "Give CIRCLE to SQUARE statue and TRIANGLE statue\n"
                        "Pick up both shapes and leave"
                    )
            elif held == "Square":
                if "Square" in self.wall_shapes and "Circle" in self.wall_shapes:
                    self.solution_var.set(
                        "Deposit Circle on CIRCLE statue\n"
                        "You should now have 2 SQUARES on your wall\n"
                        "Give SQUARE to CIRCLE statue and TRIANGLE statue\n""Kill Ogres and Knights\n"
                        "Pick up both shapes and leave"
                    )
                elif "Square" in self.wall_shapes and "Triangle" in self.wall_shapes:
                    self.solution_var.set(
                        "Deposit Triangle on TRIANGLE statue\n"
                        "You should now have 2 SQUARES on your wall\n"
                        "Give SQUARE to CIRCLE statue and TRIANGLE statue\n"
                        "Pick up both shapes and leave"
                    )
            else:
                self.solution_var.set("Invalid combination - check your selections")
            return

        held = self.held_shape_var.get()
        wall1, wall2 = self.wall_shapes[0], self.wall_shapes[1]

        # Determine which key we're holding based on the rules
        if held == "Triangle" and "Triangle" in self.wall_shapes and "Circle" in self.wall_shapes:
            self.solution_var.set("You're holding the SQUARE key\nDeposit Triangle + Circle on SQUARE statue")
        elif held == "Triangle" and "Triangle" in self.wall_shapes and "Square" in self.wall_shapes:
            self.solution_var.set("You're holding the CIRCLE key\nDeposit Triangle + Square on CIRCLE statue")
        elif held == "Circle" and "Circle" in self.wall_shapes and "Triangle" in self.wall_shapes:
            self.solution_var.set("You're holding the SQUARE key\nDeposit Triangle + Circle on SQUARE statue")
        elif held == "Circle" and "Circle" in self.wall_shapes and "Square" in self.wall_shapes:
            self.solution_var.set("You're holding the TRIANGLE key\nDeposit Square + Circle on TRIANGLE statue")
        elif held == "Square" and "Square" in self.wall_shapes and "Circle" in self.wall_shapes:
            self.solution_var.set("You're holding the TRIANGLE key\nDeposit Circle + Square on TRIANGLE statue")
        elif held == "Square" and "Square" in self.wall_shapes and "Triangle" in self.wall_shapes:
            self.solution_var.set("You're holding the CIRCLE key\nDeposit Triangle + Square on CIRCLE statue")
        else:
            self.solution_var.set("Invalid combination - check your selections")

    def reset_all(self):
        self.statue_var.set("Not Selected")
        self.held_shape_var.set("Not Selected")
        self.wall_shapes = []
        self.wall_shapes_label.config(text="Not Selected")
        self.solution_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    overlay = VerityOverlay(root)
    root.mainloop()