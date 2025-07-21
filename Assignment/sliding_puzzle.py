import tkinter as tk
import random
import heapq
import time

SIZE = 3

class SlidingPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Sliding Puzzle - 8 Puzzle")
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.tiles = []
        self.buttons = []

        self.move_count = 0
        self.move_label = tk.Label(self.root, text="Moves: 0", font=("Arial", 14))
        self.move_label.pack(pady=5)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=5)

        self.solve_button = tk.Button(self.control_frame, text="Solve", command=self.solve_puzzle)
        self.solve_button.pack()

        self.shuffle_board()
        self.create_ui()

    def shuffle_board(self):
        while True:
            nums = list(range(SIZE*SIZE))
            random.shuffle(nums)
            self.tiles = [nums[i*SIZE:(i+1)*SIZE] for i in range(SIZE)]
            if self.is_solvable(nums) and not self.is_solved():
                break
        self.move_count = 0
        self.update_move_label()

    def create_ui(self):
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                value = self.tiles[i][j]
                btn = tk.Button(self.frame, text=str(value) if value != 0 else "",
                                font=("Arial", 24), width=4, height=2,
                                command=lambda r=i, c=j: self.click_tile(r, c))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

    def update_ui(self):
        for i in range(SIZE):
            for j in range(SIZE):
                val = self.tiles[i][j]
                btn = self.buttons[i][j]
                btn.config(text=str(val) if val != 0 else "",
                           state="normal" if val != 0 else "disabled")

    def click_tile(self, row, col):
        empty_r, empty_c = self.find_empty()
        if (abs(empty_r - row) == 1 and empty_c == col) or (abs(empty_c - col) == 1 and empty_r == row):
            # Swap tiles
            self.tiles[empty_r][empty_c], self.tiles[row][col] = self.tiles[row][col], self.tiles[empty_r][empty_c]
            self.update_ui()
            self.move_count += 1
            self.update_move_label()
            if self.is_solved():
                self.show_victory()

    def find_empty(self, tiles=None):
        if tiles is None:
            tiles = self.tiles
        for i in range(SIZE):
            for j in range(SIZE):
                if tiles[i][j] == 0:
                    return i, j

    def is_solved(self, tiles=None):
        if tiles is None:
            tiles = self.tiles
        goal = list(range(1, SIZE*SIZE)) + [0]
        flat = [num for row in tiles for num in row]
        return flat == goal

    def is_solvable(self, flat):
        inv_count = 0
        for i in range(len(flat)):
            for j in range(i+1, len(flat)):
                if flat[i] and flat[j] and flat[i] > flat[j]:
                    inv_count += 1
        return inv_count % 2 == 0

    def show_victory(self):
        victory = tk.Toplevel(self.root)
        victory.title("You Win!")
        tk.Label(victory, text=f"🎉 Puzzle Solved in {self.move_count} moves!", font=("Arial", 18)).pack(padx=20, pady=20)
        tk.Button(victory, text="Play Again", command=lambda: [victory.destroy(), self.reset_game()]).pack()

    def reset_game(self):
        for row in self.buttons:
            for btn in row:
                btn.destroy()
        self.buttons.clear()
        self.shuffle_board()
        self.create_ui()

    def update_move_label(self):
        self.move_label.config(text=f"Moves: {self.move_count}")

    # --- A* Solver Section ---

    def solve_puzzle(self):
        self.solve_button.config(state="disabled")
        path = self.a_star_solver()
        if path is None:
            tk.messagebox.showinfo("No Solution", "No solution found!")
            self.solve_button.config(state="normal")
            return

        self.animate_solution(path)

    def a_star_solver(self):
        start = tuple(num for row in self.tiles for num in row)
        goal = tuple(list(range(1, SIZE*SIZE)) + [0])

        def get_neighbors(state):
            zero_pos = state.index(0)
            neighbors = []
            r, c = divmod(zero_pos, SIZE)
            directions = [(-1,0),(1,0),(0,-1),(0,1)]
            for dr, dc in directions:
                nr, nc = r+dr, c+dc
                if 0 <= nr < SIZE and 0 <= nc < SIZE:
                    new_pos = nr*SIZE + nc
                    new_state = list(state)
                    new_state[zero_pos], new_state[new_pos] = new_state[new_pos], new_state[zero_pos]
                    neighbors.append(tuple(new_state))
            return neighbors

        def manhattan(state):
            dist = 0
            for idx, val in enumerate(state):
                if val == 0:
                    continue
                target_r, target_c = divmod(val-1, SIZE)
                current_r, current_c = divmod(idx, SIZE)
                dist += abs(target_r - current_r) + abs(target_c - current_c)
            return dist

        open_set = []
        heapq.heappush(open_set, (manhattan(start), 0, start, []))
        closed_set = set()

        while open_set:
            f, g, current, path = heapq.heappop(open_set)
            if current == goal:
                return path

            if current in closed_set:
                continue
            closed_set.add(current)

            for neighbor in get_neighbors(current):
                if neighbor in closed_set:
                    continue
                new_g = g + 1
                new_f = new_g + manhattan(neighbor)
                heapq.heappush(open_set, (new_f, new_g, neighbor, path + [neighbor]))

        return None

    def animate_solution(self, path):
        # Disable all buttons during animation
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

        def step(index):
            if index >= len(path):
                self.solve_button.config(state="normal")
                # Update tiles to goal
                self.tiles = [list(path[-1][i*SIZE:(i+1)*SIZE]) for i in range(SIZE)]
                self.update_ui()
                self.move_count += len(path)
                self.update_move_label()
                self.show_victory()
                return

            state = path[index]
            self.tiles = [list(state[i*SIZE:(i+1)*SIZE]) for i in range(SIZE)]
            self.update_ui()
            self.root.after(300, step, index+1)

        step(0)


if __name__ == "__main__":
    root = tk.Tk()
    game = SlidingPuzzle(root)
    root.mainloop()
