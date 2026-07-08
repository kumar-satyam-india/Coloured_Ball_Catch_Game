import tkinter as tk
import random
import base64

# Global variables
WIDTH = 700
HEIGHT = 500
SPAWN_DELAY = 500   # Change this to control ball appearing delay in milliseconds

class Game:
    def __init__(self, root):
        self.root = root
        ettl = "Q29sb3VyZWQgQmFsbCBDYXRjaCBHYW1lIChCeTogS3VtYXIgU2F0eWFtKQ=="
        self.root.title(base64.b64decode(ettl).decode("utf-8"))

        # Top UI
        top_frame = tk.Frame(root)
        top_frame.pack(pady=5)

        self.score_label = tk.Label(top_frame, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(side="left", padx=10)

        self.lives_label = tk.Label(top_frame, text="Lives: 3", font=("Arial", 14))
        self.lives_label.pack(side="left", padx=10)

        # Speed dropdown
        self.speed_var = tk.StringVar(value="Medium")
        self.speed_menu = tk.OptionMenu(
            top_frame,
            self.speed_var,
            "Very Slow", "Slow", "Medium", "Fast",
            command=self.change_speed
        )
        self.speed_menu.pack(side="left", padx=10)

        self.restart_btn = tk.Button(top_frame, text="Restart", command=self.restart_game)
        self.restart_btn.pack(side="left", padx=10)

        # Canvas
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        # Controls
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.canvas.bind("<Motion>", self.mouse_move)

        self.start_game()

    def start_game(self):
        self.canvas.delete("all")

        self.player = self.canvas.create_arc(
            WIDTH//2 - 30, HEIGHT - 80,
            WIDTH//2 + 30, HEIGHT - 20,
            start=30, extent=300,
            fill="yellow"
        )

        self.score = 0
        self.lives = 3
        self.objects = []
        self.running = True

        self.set_speed_from_dropdown()
        self.update_labels()

        self.spawn_object()
        self.update_game()

    def restart_game(self):
        self.running = False
        self.start_game()

    def update_labels(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.lives_label.config(text=f"Lives: {self.lives}")

    def set_speed_from_dropdown(self):
        speeds = {
            "Very Slow": 2,
            "Slow": 4,
            "Medium": 6,
            "Fast": 9
        }
        self.base_speed = speeds[self.speed_var.get()]

    def change_speed(self, value):
        self.set_speed_from_dropdown()

    def move_left(self, event):
        self.canvas.move(self.player, -30, 0)

    def move_right(self, event):
        self.canvas.move(self.player, 30, 0)

    def mouse_move(self, event):
        coords = self.canvas.coords(self.player)
        center_x = (coords[0] + coords[2]) / 2
        dx = event.x - center_x
        self.canvas.move(self.player, dx, 0)

    def spawn_object(self):
        if not self.running:
            return

        x = random.randint(50, WIDTH - 50)
        color = random.choice(["green", "red"])
        obj = self.canvas.create_oval(x, 0, x + 30, 30, fill=color)
        self.objects.append((obj, color))

        # Density controlled here
        self.root.after(SPAWN_DELAY, self.spawn_object)

    def update_game(self):
        if not self.running:
            return

        for obj, color in self.objects[:]:
            self.canvas.move(obj, 0, self.base_speed)
            coords = self.canvas.coords(obj)

            if self.check_collision(obj):
                if color == "green":
                    self.score += 1
                else:
                    self.lives -= 1

                self.canvas.delete(obj)
                self.objects.remove((obj, color))

            elif coords[3] > HEIGHT:
                self.canvas.delete(obj)
                self.objects.remove((obj, color))

        self.update_labels()

        if self.lives > 0:
            self.root.after(30, self.update_game)
        else:
            self.game_over()

    def check_collision(self, obj):
        p = self.canvas.coords(self.player)
        o = self.canvas.coords(obj)

        return not (
            p[2] < o[0] or
            p[0] > o[2] or
            p[3] < o[1] or
            p[1] > o[3]
        )

    def game_over(self):
        self.running = False
        self.canvas.create_text(
            WIDTH / 2, HEIGHT / 2,
            text="GAME OVER",
            fill="white",
            font=("Arial", 30)
        )


# Run game
root = tk.Tk()
game = Game(root)
root.mainloop()