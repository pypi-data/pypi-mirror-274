import random
import tkinter as tk
from tkinter import messagebox
import time

class MazeGame:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.root = tk.Tk()
        self.root.title("Maze Game")
        self.canvas = tk.Canvas(self.root, width=width * cell_size, height=height * cell_size)
        self.canvas.pack()
        self.timer_label = tk.Label(self.root, text="Time: 0")
        self.timer_label.pack()
        self.start_time = None
        self.elapsed_time = 0
        self.timer_running = False
        self.level = 1  # Track current level

        self.start_game()

 
    def start_game(self):
        # Resize the canvas to fit the new maze dimensions
        self.canvas.config(width=self.width * self.cell_size, height=self.height * self.cell_size)

        self.maze = self.generate_maze(self.width, self.height)
        self.draw_maze()
        self.start_pos, self.end_pos = self.place_start_end()
        self.player_pos = self.start_pos
        self.player = self.canvas.create_rectangle(
            self.player_pos[0] * self.cell_size, self.player_pos[1] * self.cell_size,
            (self.player_pos[0] + 1) * self.cell_size, (self.player_pos[1] + 1) * self.cell_size,
            fill="blue"
        )

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.after(1000, self.update_timer)


    def generate_maze(self, width, height):
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        grid = [['#'] * width for _ in range(height)]

        def get_neighbors(x, y):
            neighbors = []
            if x > 1: neighbors.append((x - 2, y))
            if x < width - 2: neighbors.append((x + 2, y))
            if y > 1: neighbors.append((x, y - 2))
            if y < height - 2: neighbors.append((x, y + 2))
            return neighbors

        def is_valid_position(x, y):
            return 0 <= x < width and 0 <= y < height

        start_x, start_y = random.randint(1, width // 2) * 2 - 1, random.randint(1, height // 2) * 2 - 1
        grid[start_y][start_x] = ' '

        walls = []
        for nx, ny in get_neighbors(start_x, start_y):
            if is_valid_position(nx, ny):
                walls.append((nx, ny, start_x, start_y))

        while walls:
            wx, wy, px, py = walls.pop(random.randint(0, len(walls) - 1))

            if grid[wy][wx] == '#':
                if grid[(wy + py) // 2][(wx + px) // 2] == '#':
                    grid[wy][wx] = ' '
                    grid[(wy + py) // 2][(wx + px) // 2] = ' '
                    for nx, ny in get_neighbors(wx, wy):
                        if is_valid_position(nx, ny) and grid[ny][nx] == '#':
                            walls.append((nx, ny, wx, wy))

        return grid

    def draw_maze(self):
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                color = 'white' if cell == ' ' else 'black'
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color, outline=color
                )

    def place_start_end(self):
        empty_cells = [(x, y) for y in range(1, self.height, 2) for x in range(1, self.width, 2) if self.maze[y][x] == ' ']
        start_pos = random.choice(empty_cells)
        end_pos = random.choice(empty_cells)
        while end_pos == start_pos:
            end_pos = random.choice(empty_cells)

        self.canvas.create_rectangle(
            start_pos[0] * self.cell_size, start_pos[1] * self.cell_size,
            (start_pos[0] + 1) * self.cell_size, (start_pos[1] + 1) * self.cell_size,
            fill="green"
        )
        self.canvas.create_rectangle(
            end_pos[0] * self.cell_size, end_pos[1] * self.cell_size,
            (end_pos[0] + 1) * self.cell_size, (end_pos[1] + 1) * self.cell_size,
            fill="red"
        )

        return start_pos, end_pos

    def on_key_press(self, event):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True

        move_x, move_y = 0, 0
        if event.keysym == 'Up':
            move_y = -1
        elif event.keysym == 'Down':
            move_y = 1
        elif event.keysym == 'Left':
            move_x = -1
        elif event.keysym == 'Right':
            move_x = 1

        new_x = self.player_pos[0] + move_x
        new_y = self.player_pos[1] + move_y

        if 0 <= new_x < self.width and 0 <= new_y < self.height and self.maze[new_y][new_x] == ' ':
            self.canvas.move(self.player, move_x * self.cell_size, move_y * self.cell_size)
            self.player_pos = (new_x, new_y)

        if self.player_pos == self.end_pos:
            self.timer_running = False
            self.elapsed_time = int(time.time() - self.start_time)
            choice = messagebox.askyesno("Congratulations!", f"You reached the end! Time: {self.elapsed_time} seconds. Do you want to play the next level?")
            if choice:
                self.next_level()
            else:
                self.root.quit()

    def update_timer(self):
        if self.timer_running:
            current_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {current_time}")
        self.root.after(1000, self.update_timer)

    def next_level(self):
        self.level += 1
        self.width += 2  # Increase maze size for next level
        self.height += 2
        self.cell_size -= 1  # Adjust cell size for increased maze size
        self.start_game()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = MazeGame(width=21, height=21, cell_size=20)
    game.run()
