import tkinter as tk
from tkinter import messagebox
import random
import heapq
import time

SIZE = 3

# --- UI Constants ---
TILE_BG_COLOR = "#f0f0f0"  # Light gray
EMPTY_TILE_COLOR = "#e0e0e0" # Slightly darker gray for empty
HOVER_COLOR = "#d0e0ff"   # Light blue on hover
CLICK_COLOR = "#a0c0ff"   # Darker blue on click
SOLVED_COLOR = "#c3f0c3"  # Light green for solved state
FONT_FAMILY = "Arial"
FONT_SIZE_TILE = 24
FONT_SIZE_LABEL = 14
ANIMATION_DELAY_MS = 200 # Milliseconds for solution animation step

class SlidingPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Sliding Puzzle - 8 Puzzle")
        self.root.geometry("400x550") # Set initial window size
        self.root.resizable(False, False) # Disable resizing for simplicity

        self.tiles = []
        self.buttons = []
        self.move_count = 0
        self.min_moves = 0 # To store the optimal solution length

        # --- UI Elements ---
        self.main_frame = tk.Frame(self.root, bg="#f5f5f5", padx=10, pady=10) # Overall background
        self.main_frame.pack(expand=True, fill="both")

        # Puzzle grid frame
        self.puzzle_frame = tk.Frame(self.main_frame, bd=5, relief="ridge", bg="#cccccc")
        self.puzzle_frame.pack(pady=20)

        # Labels for game info
        self.move_label = tk.Label(self.main_frame, text="Moves: 0", font=(FONT_FAMILY, FONT_SIZE_LABEL))
        self.move_label.pack(pady=5)

        self.min_moves_label = tk.Label(self.main_frame, text="Optimal Moves: Calculating...", font=(FONT_FAMILY, FONT_SIZE_LABEL - 2), fg="gray")
        self.min_moves_label.pack(pady=2)

        self.status_label = tk.Label(self.main_frame, text="Click 'New Game' to start!", font=(FONT_FAMILY, FONT_SIZE_LABEL), fg="blue")
        self.status_label.pack(pady=5)

        # Control buttons frame
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(pady=10)

        self.new_game_button = tk.Button(self.control_frame, text="New Game", command=self.reset_game,
                                         font=(FONT_FAMILY, FONT_SIZE_LABEL - 2), bg="#4CAF50", fg="white", activebackground="#6BCF6B")
        self.new_game_button.pack(side=tk.LEFT, padx=10)

        self.solve_button = tk.Button(self.control_frame, text="Solve", command=self.solve_puzzle_gui_wrapper,
                                       font=(FONT_FAMILY, FONT_SIZE_LABEL - 2), bg="#2196F3", fg="white", activebackground="#51ADF6")
        self.solve_button.pack(side=tk.RIGHT, padx=10)

        # Initialize the game
        self.shuffle_board()
        self.create_ui()
        self.update_ui()
        self.calculate_min_moves_async() # Calculate optimal moves in background

    def shuffle_board(self):
        while True:
            nums = list(range(SIZE*SIZE))
            random.shuffle(nums)
            self.tiles = [nums[i*SIZE:(i+1)*SIZE] for i in range(SIZE)]
            # Check solvability after shuffling
            flat_tiles = [num for row in self.tiles for num in row]
            if self.is_solvable(flat_tiles) and not self.is_solved():
                break
        self.move_count = 0
        self.update_move_label()
        self.status_label.config(text="Ready to play!", fg="blue")
        # Reset solve button state
        self.solve_button.config(state="normal", text="Solve")
        # Clear min moves label until calculated
        self.min_moves_label.config(text="Optimal Moves: Calculating...", fg="gray")


    def create_ui(self):
        # Clear existing buttons
        for row_buttons in self.buttons:
            for btn in row_buttons:
                btn.destroy()
        self.buttons = []

        for i in range(SIZE):
            row_buttons = []
            for j in range(SIZE):
                value = self.tiles[i][j]
                btn = tk.Button(self.puzzle_frame, text=str(value) if value != 0 else "",
                                font=(FONT_FAMILY, FONT_SIZE_TILE, "bold"),
                                width=4, height=2,
                                command=lambda r=i, c=j: self.click_tile(r, c),
                                relief="raised", bd=3)
                btn.grid(row=i, column=j, padx=2, pady=2)
                
                # Bind hover events
                btn.bind("<Enter>", lambda e, button=btn: self.on_enter(button))
                btn.bind("<Leave>", lambda e, button=btn: self.on_leave(button))
                
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def update_ui(self, animating_move=None):
        for i in range(SIZE):
            for j in range(SIZE):
                val = self.tiles[i][j]
                btn = self.buttons[i][j]
                btn.config(text=str(val) if val != 0 else "")
                
                # Set colors based on tile value
                if val == 0:
                    btn.config(bg=EMPTY_TILE_COLOR, state="disabled")
                else:
                    btn.config(bg=TILE_BG_COLOR, state="normal")
                
                # Highlight the tile being animated
                if animating_move and (i, j) == animating_move:
                    btn.config(bg=CLICK_COLOR) # Briefly highlight the moving tile
                
                # If solved, change all non-empty tiles to a solved color
                if self.is_solved() and val != 0:
                    btn.config(bg=SOLVED_COLOR, fg="black") # Use a black foreground for solved tiles

    def on_enter(self, button):
        # Only highlight if the button is movable (not empty, and adjacent to empty)
        r, c = self.find_button_coords(button)
        if r is not None and c is not None:
            empty_r, empty_c = self.find_empty()
            if (abs(empty_r - r) == 1 and empty_c == c) or (abs(empty_c - c) == 1 and empty_r == r):
                button.config(bg=HOVER_COLOR)

    def on_leave(self, button):
        # Reset color when mouse leaves, unless it's the empty tile
        r, c = self.find_button_coords(button)
        if r is not None and c is not None:
            if self.tiles[r][c] != 0:
                button.config(bg=TILE_BG_COLOR)
            else:
                button.config(bg=EMPTY_TILE_COLOR)

    def find_button_coords(self, target_button):
        for r_idx, row in enumerate(self.buttons):
            for c_idx, button in enumerate(row):
                if button == target_button:
                    return r_idx, c_idx
        return None, None # Should not happen

    def click_tile(self, row, col):
        empty_r, empty_c = self.find_empty()
        
        # Check if the clicked tile is adjacent to the empty tile
        is_adjacent = (abs(empty_r - row) == 1 and empty_c == col) or \
                      (abs(empty_c - col) == 1 and empty_r == row)
        
        if is_adjacent:
            # Animate click feedback briefly
            self.buttons[row][col].config(bg=CLICK_COLOR)
            self.root.update_idletasks() # Force update
            time.sleep(0.05) # Small delay for visual effect

            # Swap tiles
            self.tiles[empty_r][empty_c], self.tiles[row][col] = self.tiles[row][col], self.tiles[empty_r][empty_c]
            self.update_ui()
            self.move_count += 1
            self.update_move_label()
            
            if self.is_solved():
                self.show_victory()
                self.status_label.config(text=f"Solved in {self.move_count} moves!", fg="green")
            else:
                self.status_label.config(text="Keep going!", fg="blue")


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
                if flat[i] != 0 and flat[j] != 0 and flat[i] > flat[j]:
                    inv_count += 1
        
        # For an N x N puzzle, solvability depends on N and inversion count
        # For N=3 (our 8-puzzle), it's solvable if inversion count is even.
        return inv_count % 2 == 0

    def show_victory(self):
        # Briefly flash solved tiles
        for i in range(SIZE):
            for j in range(SIZE):
                if self.tiles[i][j] != 0:
                    self.buttons[i][j].config(bg="#90ee90") # Lighter green
        self.root.update_idletasks()
        time.sleep(0.2)
        self.update_ui() # Reset to SOLVED_COLOR

        messagebox.showinfo("You Win!", f"🎉 Puzzle Solved in {self.move_count} moves!")
        # Disable user interaction after solving
        self.disable_buttons()

    def reset_game(self):
        self.shuffle_board()
        self.create_ui() # Re-create buttons to reset bindings and state
        self.update_ui()
        self.min_moves = 0 # Reset min moves display
        self.min_moves_label.config(text="Optimal Moves: Calculating...", fg="gray")
        self.calculate_min_moves_async() # Recalculate optimal moves for new board

    def update_move_label(self):
        self.move_label.config(text=f"Moves: {self.move_count}")

    def disable_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def enable_buttons(self):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.tiles[i][j] != 0:
                    self.buttons[i][j].config(state="normal")

    # --- A* Solver Section ---
    # This part runs in the background for calculating optimal moves,
    # and then for animating the solution.

    def calculate_min_moves_async(self):
        self.status_label.config(text="Calculating optimal moves...", fg="orange")
        self.root.update_idletasks() # Update GUI immediately

        # Use root.after to run heavy computation without freezing GUI
        # A more robust solution for very long computations would be threading
        self.root.after(100, self._calculate_min_moves_internal)

    def _calculate_min_moves_internal(self):
        start_time = time.time()
        initial_flat_state = tuple(num for row in self.tiles for num in row)
        
        # Run A* solver to find the path length
        path = self._a_star_solver_core(initial_flat_state, return_path_only_length=True)
        
        if path is not None:
            self.min_moves = len(path) - 1 # Exclude initial state
            self.min_moves_label.config(text=f"Optimal Moves: {self.min_moves}", fg="darkgreen")
        else:
            self.min_moves_label.config(text="Optimal Moves: Not solvable", fg="red")
            messagebox.showerror("Error", "The current puzzle state is not solvable. This shouldn't happen with the shuffling logic.")

        self.status_label.config(text="Ready to play!", fg="blue")
        print(f"Optimal moves calculation time: {time.time() - start_time:.2f} seconds")


    def solve_puzzle_gui_wrapper(self):
        if self.is_solved():
            messagebox.showinfo("Solved", "The puzzle is already solved!")
            return

        self.disable_buttons() # Disable user interaction
        self.solve_button.config(state="disabled", text="Solving...")
        self.new_game_button.config(state="disabled")
        self.status_label.config(text="Solving puzzle...", fg="red")
        self.root.update_idletasks() # Force GUI update

        initial_flat_state = tuple(num for row in self.tiles for num in row)
        
        # Using a slightly delayed call to allow GUI to update "Solving..."
        self.root.after(100, lambda: self._start_solving_animation(initial_flat_state))

    def _start_solving_animation(self, initial_flat_state):
        path = self._a_star_solver_core(initial_flat_state)
        
        if path is None:
            messagebox.showinfo("No Solution", "No solution found!")
            self.solve_button.config(state="normal", text="Solve")
            self.new_game_button.config(state="normal")
            self.enable_buttons() # Re-enable user buttons if no solution
            self.status_label.config(text="No solution found!", fg="red")
            return

        self.animate_solution(path)

    def _a_star_solver_core(self, start_state, return_path_only_length=False):
        goal = tuple(list(range(1, SIZE*SIZE)) + [0])

        def get_neighbors(state_tuple):
            zero_pos = state_tuple.index(0)
            neighbors = []
            r, c = divmod(zero_pos, SIZE)
            directions = [(-1,0),(1,0),(0,-1),(0,1)] # Up, Down, Left, Right
            for dr, dc in directions:
                nr, nc = r+dr, c+dc
                if 0 <= nr < SIZE and 0 <= nc < SIZE:
                    new_pos = nr*SIZE + nc
                    new_state_list = list(state_tuple)
                    new_state_list[zero_pos], new_state_list[new_pos] = new_state_list[new_pos], new_state_list[zero_pos]
                    neighbors.append(tuple(new_state_list))
            return neighbors

        def manhattan(state_tuple):
            dist = 0
            for idx, val in enumerate(state_tuple):
                if val == 0:
                    continue
                # Target row and column for value `val`
                target_r, target_c = divmod(val - 1, SIZE)
                # Current row and column of value `val`
                current_r, current_c = divmod(idx, SIZE)
                dist += abs(target_r - current_r) + abs(target_c - current_c)
            return dist

        open_set = [] # Min-heap of (f_score, g_score, state_tuple, path_list)
        # The path_list here stores the sequence of states to reach the current state
        # The g_score is the number of moves from the start
        heapq.heappush(open_set, (manhattan(start_state), 0, start_state, [start_state]))
        
        # closed_set stores states that have been fully evaluated
        closed_set = set() # Use a set for faster lookups

        # came_from (optional for reconstruction, but path is built directly here)
        
        # Optimization: if we only need length, we don't need to store full paths
        # This will save a lot of memory for long paths
        g_scores = {start_state: 0} # Stores the g_score (cost from start) for a state

        while open_set:
            f, g, current_state, current_path = heapq.heappop(open_set)

            if current_state == goal:
                if return_path_only_length:
                    return current_path # Return the path (list of states)
                return current_path # Return the full path for animation

            if current_state in closed_set:
                continue
            closed_set.add(current_state)

            for neighbor in get_neighbors(current_state):
                if neighbor in closed_set:
                    continue

                new_g = g + 1

                # If neighbor already in open_set but with higher g_score, update it
                if new_g < g_scores.get(neighbor, float('inf')):
                    g_scores[neighbor] = new_g
                    new_f = new_g + manhattan(neighbor)
                    heapq.heappush(open_set, (new_f, new_g, neighbor, current_path + [neighbor]))
        return None

    def animate_solution(self, path):
        # path includes the initial state, so actual moves = len(path) - 1
        self.move_count = 0
        self.update_move_label()
        
        def step(index):
            if index >= len(path):
                # Animation finished
                self.tiles = [list(path[-1][i*SIZE:(i+1)*SIZE]) for i in range(SIZE)]
                self.update_ui() # Final update
                self.show_victory() # Show victory message and handle game end
                self.solve_button.config(state="disabled", text="Solve") # Keep disabled if solved
                self.new_game_button.config(state="normal")
                self.status_label.config(text=f"Solved in {self.move_count} moves!", fg="green")
                return

            current_flat_state = path[index]
            prev_flat_state = path[index - 1] if index > 0 else None

            # Determine which tile moved
            moved_tile_pos = None
            if prev_flat_state:
                prev_empty_idx = prev_flat_state.index(0)
                current_empty_idx = current_flat_state.index(0)
                # The tile that moved is the one that's now in the empty tile's previous position
                moved_tile_value = current_flat_state[prev_empty_idx]
                # Find its new position for animation
                moved_tile_pos_flat = current_flat_state.index(moved_tile_value)
                moved_tile_pos = divmod(moved_tile_pos_flat, SIZE) # (row, col)

            self.tiles = [list(current_flat_state[i*SIZE:(i+1)*SIZE]) for i in range(SIZE)]
            self.update_ui(animating_move=moved_tile_pos)
            
            # Only increment move count for actual moves, not initial state
            if index > 0: 
                self.move_count = index 
                self.update_move_label()

            self.root.after(ANIMATION_DELAY_MS, step, index + 1)

        step(0) # Start animation from the first state in the path

if __name__ == "__main__":
    root = tk.Tk()
    game = SlidingPuzzle(root)
    root.mainloop()