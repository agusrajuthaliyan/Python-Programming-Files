import tkinter as tk
from tkinter import messagebox, ttk # ttk for themed widgets like Combobox
import random
import heapq
import time
from collections import deque

# --- Game Constants ---
SIZE = 3 # For 3x3 puzzle (8-puzzle)

# --- UI Colors & Styles ---
BG_COLOR = "#f5f5f5"
PUZZLE_FRAME_COLOR = "#cccccc"
TILE_BG_COLOR = "#f0f0f0"
EMPTY_TILE_COLOR = "#e0e0e0"
HOVER_COLOR = "#d0e0ff"   # Light blue for hover
CLICK_COLOR = "#a0c0ff"   # Darker blue for click feedback
HINT_HIGHLIGHT_COLOR = "#ffcc00" # Orange for hint
SOLVED_COLOR = "#c3f0c3"  # Light green for solved state
BUTTON_BG_NORMAL = "#4CAF50" # Green for New Game
BUTTON_FG_NORMAL = "white"
BUTTON_BG_SOLVE = "#2196F3" # Blue for Solve
BUTTON_BG_UNDO_REDO = "#607D8B" # Gray-blue for Undo/Redo

FONT_FAMILY = "Arial"
FONT_SIZE_TILE = 28 # Slightly larger
FONT_SIZE_LABEL = 14
FONT_SIZE_BUTTON = 12
ANIMATION_DELAY_MS = 150 # Faster animation
HINT_FLASH_DELAY_MS = 400 # How long hint tile flashes

class SlidingPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Sliding Puzzle - 8 Puzzle")
        self.root.geometry("420x650") # Adjust size for new elements
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        self.tiles = []
        self.buttons = []
        self.move_count = 0
        self.min_moves = 0 # To store the optimal solution length
        
        # --- History for Undo/Redo ---
        self.history = deque() # Stores (flat_state_tuple, move_count_at_state)
        self.future = deque()  # Stores (flat_state_tuple, move_count_at_state)

        # --- UI Elements ---
        self.main_frame = tk.Frame(self.root, bg=BG_COLOR, padx=10, pady=10)
        self.main_frame.pack(expand=True, fill="both")

        # Puzzle grid frame
        self.puzzle_frame = tk.Frame(self.main_frame, bd=5, relief="ridge", bg=PUZZLE_FRAME_COLOR)
        self.puzzle_frame.pack(pady=15)

        # Labels for game info
        self.move_label = tk.Label(self.main_frame, text="Moves: 0", font=(FONT_FAMILY, FONT_SIZE_LABEL))
        self.move_label.pack(pady=2)

        self.min_moves_label = tk.Label(self.main_frame, text="Optimal Moves: Calculating...", font=(FONT_FAMILY, FONT_SIZE_LABEL - 2), fg="gray")
        self.min_moves_label.pack(pady=2)
        
        self.status_label = tk.Label(self.main_frame, text="Click 'New Game' to start!", font=(FONT_FAMILY, FONT_SIZE_LABEL), fg="blue")
        self.status_label.pack(pady=5)

        # --- Solver Options and Stats Frame ---
        self.solver_options_frame = tk.LabelFrame(self.main_frame, text="Solver Options & Stats", font=(FONT_FAMILY, FONT_SIZE_BUTTON, "bold"), bg=BG_COLOR, padx=10, pady=5)
        self.solver_options_frame.pack(pady=10, fill="x")

        # Algorithm Selection
        tk.Label(self.solver_options_frame, text="Algorithm:", font=(FONT_FAMILY, FONT_SIZE_BUTTON), bg=BG_COLOR).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.solver_algorithm = tk.StringVar(self.root)
        self.solver_algorithm.set("A* Search") # default value
        self.algo_options = ["A* Search", "BFS", "DFS"]
        self.algo_menu = ttk.Combobox(self.solver_options_frame, textvariable=self.solver_algorithm, values=self.algo_options, state="readonly", font=(FONT_FAMILY, FONT_SIZE_BUTTON))
        self.algo_menu.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.algo_menu.bind("<<ComboboxSelected>>", self.on_algo_select) # Event when selection changes

        # Solver Stats
        self.solver_time_label = tk.Label(self.solver_options_frame, text="Time: N/A", font=(FONT_FAMILY, FONT_SIZE_BUTTON - 2), bg=BG_COLOR)
        self.solver_time_label.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky="w")

        self.solver_nodes_label = tk.Label(self.solver_options_frame, text="Nodes: N/A", font=(FONT_FAMILY, FONT_SIZE_BUTTON - 2), bg=BG_COLOR)
        self.solver_nodes_label.grid(row=2, column=0, columnspan=2, padx=5, pady=2, sticky="w")
        
        self.solver_options_frame.grid_columnconfigure(1, weight=1) # Allow combobox to expand

        # --- Control buttons frame ---
        self.control_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.control_frame.pack(pady=10)

        self.new_game_button = tk.Button(self.control_frame, text="New Game", command=self.reset_game,
                                         font=(FONT_FAMILY, FONT_SIZE_BUTTON), bg=BUTTON_BG_NORMAL, fg=BUTTON_FG_NORMAL, activebackground="#6BCF6B",
                                         relief="raised", bd=3)
        self.new_game_button.grid(row=0, column=0, padx=5, pady=5)

        self.hint_button = tk.Button(self.control_frame, text="Hint", command=self.give_hint,
                                      font=(FONT_FAMILY, FONT_SIZE_BUTTON), bg=BUTTON_BG_SOLVE, fg=BUTTON_FG_NORMAL, activebackground="#51ADF6",
                                      relief="raised", bd=3)
        self.hint_button.grid(row=0, column=1, padx=5, pady=5)

        self.solve_button = tk.Button(self.control_frame, text="Solve", command=self.solve_puzzle_gui_wrapper,
                                       font=(FONT_FAMILY, FONT_SIZE_BUTTON), bg=BUTTON_BG_SOLVE, fg=BUTTON_FG_NORMAL, activebackground="#51ADF6",
                                       relief="raised", bd=3)
        self.solve_button.grid(row=0, column=2, padx=5, pady=5)
        
        # --- Undo/Redo Buttons ---
        self.undo_redo_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        self.undo_redo_frame.pack(pady=5)

        self.undo_button = tk.Button(self.undo_redo_frame, text="Undo", command=self.undo_move,
                                     font=(FONT_FAMILY, FONT_SIZE_BUTTON), bg=BUTTON_BG_UNDO_REDO, fg=BUTTON_FG_NORMAL, activebackground="#7E9AAB",
                                     relief="raised", bd=3, state=tk.DISABLED)
        self.undo_button.pack(side=tk.LEFT, padx=10)

        self.redo_button = tk.Button(self.undo_redo_frame, text="Redo", command=self.redo_move,
                                     font=(FONT_FAMILY, FONT_SIZE_BUTTON), bg=BUTTON_BG_UNDO_REDO, fg=BUTTON_FG_NORMAL, activebackground="#7E9AAB",
                                     relief="raised", bd=3, state=tk.DISABLED)
        self.redo_button.pack(side=tk.RIGHT, padx=10)

        # Initialize the game
        self.shuffle_board()
        self.create_ui()
        self.update_ui()
        self.calculate_min_moves_async() # Calculate optimal moves in background

    def on_algo_select(self, event=None):
        # When algorithm changes, clear previous solver stats
        self.solver_time_label.config(text="Time: N/A", fg="black")
        self.solver_nodes_label.config(text="Nodes: N/A", fg="black")

    def get_current_flat_state(self):
        return tuple(num for row in self.tiles for num in row)

    def store_current_state_for_undo(self):
        # Store the state BEFORE the move
        self.history.append((self.get_current_flat_state(), self.move_count))
        # Clear redo history when a new move is made
        self.future.clear()
        self.update_undo_redo_buttons()

    def update_undo_redo_buttons(self):
        self.undo_button.config(state=tk.NORMAL if self.history else tk.DISABLED)
        self.redo_button.config(state=tk.NORMAL if self.future else tk.DISABLED)

    def undo_move(self):
        if not self.history:
            return
        
        # Move current state to future stack
        self.future.appendleft((self.get_current_flat_state(), self.move_count))
        
        # Pop previous state from history
        prev_state_flat, prev_move_count = self.history.pop()
        self.tiles = [list(prev_state_flat[i*SIZE:(i+1)*SIZE]) for i in range(SIZE)]
        self.move_count = prev_move_count
        self.update_move_label()
        self.update_ui()
        self.status_label.config(text="Undo!", fg="purple")
        self.update_undo_redo_buttons()
        # Re-enable interactive play buttons if they were disabled by a solve/win
        self.enable_buttons() 
        self.solve_button.config(state="normal", text="Solve")
        self.new_game_button.config(state="normal")


    def redo_move(self):
        if not self.future:
            return
        
        # Move current state to history stack
        self.history.append((self.get_current_flat_state(), self.move_count))
        
        # Pop next state from future
        next_state_flat, next_move_count = self.future.popleft()
        self.tiles = [list(next_state_flat[i*SIZE:(i+1)*SIZE]) for i in range(SIZE)]
        self.move_count = next_move_count
        self.update_move_label()
        self.update_ui()
        self.status_label.config(text="Redo!", fg="purple")
        self.update_undo_redo_buttons()
        # Re-enable interactive play buttons if they were disabled by a solve/win
        self.enable_buttons() 
        self.solve_button.config(state="normal", text="Solve")
        self.new_game_button.config(state="normal")


    def shuffle_board(self):
        while True:
            nums = list(range(SIZE*SIZE))
            random.shuffle(nums)
            self.tiles = [nums[i*SIZE:(i+1)*SIZE] for i in range(SIZE)]
            
            flat_tiles = [num for row in self.tiles for num in row]
            if self.is_solvable(flat_tiles) and not self.is_solved():
                break
        
        self.move_count = 0
        self.update_move_label()
        self.status_label.config(text="Ready to play!", fg="blue")
        
        # Reset solver stats
        self.solver_time_label.config(text="Time: N/A", fg="black")
        self.solver_nodes_label.config(text="Nodes: N/A", fg="black")

        # Reset undo/redo history
        self.history.clear()
        self.future.clear()
        self.update_undo_redo_buttons()
        
        # Reset solve button state
        self.solve_button.config(state="normal", text="Solve")
        self.new_game_button.config(state="normal")
        self.hint_button.config(state="normal")

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
                                width=3, height=1, # Adjust size to fit 420px width for 3x3
                                command=lambda r=i, c=j: self.click_tile(r, c),
                                relief="raised", bd=3)
                btn.grid(row=i, column=j, padx=2, pady=2, ipadx=5, ipady=5) # Internal padding
                
                # Bind hover events
                btn.bind("<Enter>", lambda e, button=btn: self.on_enter(button))
                btn.bind("<Leave>", lambda e, button=btn: self.on_leave(button))
                
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def update_ui(self, animating_move=None, hint_tile_coords=None):
        for i in range(SIZE):
            for j in range(SIZE):
                val = self.tiles[i][j]
                btn = self.buttons[i][j]
                btn.config(text=str(val) if val != 0 else "")
                
                # Set base colors
                if val == 0:
                    btn.config(bg=EMPTY_TILE_COLOR, state="disabled", fg="black")
                else:
                    btn.config(bg=TILE_BG_COLOR, state="normal", fg="black") # Default foreground for numbers
                
                # Highlight the tile being animated
                if animating_move and (i, j) == animating_move:
                    btn.config(bg=CLICK_COLOR) # Briefly highlight the moving tile
                
                # Highlight hint tile
                if hint_tile_coords and (i, j) == hint_tile_coords:
                    btn.config(bg=HINT_HIGHLIGHT_COLOR, fg="black") # Make sure number is visible

                # If solved, change all non-empty tiles to a solved color
                if self.is_solved() and val != 0:
                    btn.config(bg=SOLVED_COLOR, fg="black")

    def on_enter(self, button):
        # Only highlight if the button is movable (not empty, and adjacent to empty)
        r, c = self.find_button_coords(button)
        if r is not None and c is not None:
            empty_r, empty_c = self.find_empty()
            if self.tiles[r][c] != 0 and \
               ((abs(empty_r - r) == 1 and empty_c == c) or \
                (abs(empty_c - c) == 1 and empty_r == r)):
                button.config(bg=HOVER_COLOR)

    def on_leave(self, button):
        # Reset color when mouse leaves, unless it's the empty tile
        r, c = self.find_button_coords(button)
        if r is not None and c is not None:
            if not self.is_solved() or self.tiles[r][c] == 0: # If not solved or it's the empty tile
                if self.tiles[r][c] != 0:
                    button.config(bg=TILE_BG_COLOR)
                else:
                    button.config(bg=EMPTY_TILE_COLOR)
            else: # If solved and it's a number tile
                button.config(bg=SOLVED_COLOR)

    def find_button_coords(self, target_button):
        for r_idx, row in enumerate(self.buttons):
            for c_idx, button in enumerate(row):
                if button == target_button:
                    return r_idx, c_idx
        return None, None

    def click_tile(self, row, col):
        if self.solve_button["state"] == "disabled" and self.solve_button["text"] == "Solving...":
            # Prevent user interaction during automated solving
            return

        empty_r, empty_c = self.find_empty()
        
        is_adjacent = (abs(empty_r - row) == 1 and empty_c == col) or \
                      (abs(empty_c - col) == 1 and empty_r == row)
        
        if is_adjacent:
            self.store_current_state_for_undo() # Store state BEFORE making the move

            # Animate click feedback briefly
            self.buttons[row][col].config(bg=CLICK_COLOR)
            self.root.update_idletasks() # Force update
            time.sleep(0.05) # Small delay for visual effect

            # Perform the swap
            self.tiles[empty_r][empty_c], self.tiles[row][col] = self.tiles[row][col], self.tiles[empty_r][empty_c]
            self.update_ui()
            self.move_count += 1
            self.update_move_label()
            
            if self.is_solved():
                self.show_victory()
                self.status_label.config(text=f"Solved in {self.move_count} moves!", fg="green")
                self.disable_buttons() # Disable interactive tiles after solving
                self.hint_button.config(state="disabled")
            else:
                self.status_label.config(text="Keep going!", fg="blue")
                self.enable_buttons() # Ensure buttons are enabled after a move if not solved

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
        # For an N x N puzzle, solvability depends on N and inversion count
        # For N=3 (our 8-puzzle), it's solvable if inversion count is even.
        inv_count = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                # Count inversions only for non-zero numbers
                if flat[i] != 0 and flat[j] != 0 and flat[i] > flat[j]:
                    inv_count += 1
        
        # For an N x N puzzle:
        # If N is odd, puzzle is solvable if inversion count is even.
        # If N is even:
        #   - If empty tile is on an even row counting from bottom (0,2,4..), solvable if inv_count is odd.
        #   - If empty tile is on an odd row counting from bottom (1,3,5..), solvable if inv_count is even.
        # For 8-puzzle (N=3, odd):
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
        self.new_game_button.config(state="disabled")
        self.solve_button.config(state="disabled")
        self.hint_button.config(state="disabled")
        self.undo_button.config(state="disabled")
        self.redo_button.config(state="disabled")

    def enable_buttons(self):
        # Re-enable puzzle tiles if they are not the empty one
        for i in range(SIZE):
            for j in range(SIZE):
                if self.tiles[i][j] != 0:
                    self.buttons[i][j].config(state="normal")
                else:
                    self.buttons[i][j].config(state="disabled") # Empty tile stays disabled
        self.new_game_button.config(state="normal")
        self.solve_button.config(state="normal")
        self.hint_button.config(state="normal")
        self.update_undo_redo_buttons() # Update state based on history/future

    # --- Hint System ---
    def give_hint(self):
        if self.is_solved():
            self.status_label.config(text="Puzzle already solved!", fg="green")
            return
        
        self.status_label.config(text="Getting hint...", fg="orange")
        self.disable_buttons() # Disable during hint calculation

        # Calculate the next optimal move using A*
        current_state_flat = self.get_current_flat_state()
        hint_path = self._a_star_solver_core(current_state_flat)

        if hint_path and len(hint_path) > 1:
            next_state_flat = hint_path[1] # The state after the first optimal move
            
            # Find which tile moved to reach next_state_flat
            current_empty_pos = current_state_flat.index(0)
            next_empty_pos = next_state_flat.index(0)
            
            # The tile that moved is the one currently at next_empty_pos
            # but was previously at current_empty_pos
            moved_tile_value = current_state_flat[next_empty_pos]
            moved_tile_coords = divmod(next_empty_pos, SIZE) # Row, Col of the tile to click

            # Temporarily highlight the hint tile
            self.update_ui(hint_tile_coords=moved_tile_coords)
            self.root.after(HINT_FLASH_DELAY_MS, self.reset_hint_highlight)
            self.status_label.config(text="Here's a hint!", fg="darkgreen")
        else:
            self.status_label.config(text="No hint found (puzzle might be solved or error).", fg="red")

        self.root.after(HINT_FLASH_DELAY_MS + 100, self.enable_buttons) # Re-enable after flash

    def reset_hint_highlight(self):
        self.update_ui() # Revert colors to normal

    # --- Algorithm Solvers ---

    def calculate_min_moves_async(self):
        self.status_label.config(text="Calculating optimal moves...", fg="orange")
        self.root.update_idletasks() # Update GUI immediately

        # Run A* solver to find the path length
        # This will run in the main thread but with a slight delay
        self.root.after(100, self._calculate_min_moves_internal)

    def _calculate_min_moves_internal(self):
        start_time = time.time()
        initial_flat_state = self.get_current_flat_state()
        
        # Use A* for minimal moves calculation
        path = self._a_star_solver_core(initial_flat_state, return_path_only_length=True)
        
        if path is not None:
            self.min_moves = len(path) - 1 # Exclude initial state
            self.min_moves_label.config(text=f"Optimal Moves: {self.min_moves}", fg="darkgreen")
        else:
            self.min_moves_label.config(text="Optimal Moves: Not solvable", fg="red")
            messagebox.showerror("Error", "The current puzzle state is not solvable. This shouldn't happen with the shuffling logic.")

        self.status_label.config(text="Ready to play!", fg="blue")
        # print(f"Optimal moves calculation time: {time.time() - start_time:.2f} seconds")

    def solve_puzzle_gui_wrapper(self):
        if self.is_solved():
            messagebox.showinfo("Solved", "The puzzle is already solved!")
            return

        self.disable_buttons() # Disable user interaction
        self.solve_button.config(state="disabled", text="Solving...")
        self.new_game_button.config(state="disabled")
        self.hint_button.config(state="disabled")
        self.undo_button.config(state="disabled")
        self.redo_button.config(state="disabled")
        
        self.status_label.config(text=f"Solving using {self.solver_algorithm.get()}...", fg="red")
        self.solver_time_label.config(text="Time: Calculating...", fg="orange")
        self.solver_nodes_label.config(text="Nodes: Calculating...", fg="orange")
        self.root.update_idletasks() # Force GUI update

        initial_flat_state = self.get_current_flat_state()
        
        # Using a slightly delayed call to allow GUI to update "Solving..."
        self.root.after(100, lambda: self._start_solving_animation(initial_flat_state))

    def _start_solving_animation(self, initial_flat_state):
        selected_algo = self.solver_algorithm.get()
        path = None
        nodes_explored = 0
        start_time = time.time()

        if selected_algo == "A* Search":
            path, nodes_explored = self._a_star_solver_core(initial_flat_state, return_nodes_explored=True)
        elif selected_algo == "BFS":
            path, nodes_explored = self._bfs_solver_core(initial_flat_state)
        elif selected_algo == "DFS":
            path, nodes_explored = self._dfs_solver_core(initial_flat_state)
        
        end_time = time.time()
        elapsed_time = end_time - start_time

        self.solver_time_label.config(text=f"Time: {elapsed_time:.3f}s", fg="black")
        self.solver_nodes_label.config(text=f"Nodes: {nodes_explored}", fg="black")


        if path is None:
            messagebox.showinfo("No Solution", "No solution found!")
            self.solve_button.config(state="normal", text="Solve")
            self.new_game_button.config(state="normal")
            self.hint_button.config(state="normal")
            self.enable_buttons() # Re-enable user buttons if no solution
            self.status_label.config(text="No solution found!", fg="red")
            return

        # Clear undo/redo history before animating a solution
        self.history.clear()
        self.future.clear()
        self.update_undo_redo_buttons()

        self.animate_solution(path)

    # --- Core A* Solver ---
    def _a_star_solver_core(self, start_state, return_path_only_length=False, return_nodes_explored=False):
        goal = tuple(list(range(1, SIZE*SIZE)) + [0])
        
        def manhattan(state_tuple):
            dist = 0
            for idx, val in enumerate(state_tuple):
                if val == 0: continue
                target_r, target_c = divmod(val - 1, SIZE)
                current_r, current_c = divmod(idx, SIZE)
                dist += abs(target_r - current_r) + abs(target_c - current_c)
            return dist

        open_set = [] # Min-heap of (f_score, g_score, state_tuple, path_list)
        heapq.heappush(open_set, (manhattan(start_state), 0, start_state, [start_state]))
        
        closed_set = set() # Use a set for faster lookups
        g_scores = {start_state: 0} # Stores the g_score (cost from start) for a state
        nodes_explored = 0

        while open_set:
            f, g, current_state, current_path = heapq.heappop(open_set)
            nodes_explored += 1

            if current_state == goal:
                if return_path_only_length: return current_path # Return the path (list of states)
                if return_nodes_explored: return current_path, nodes_explored
                return current_path

            if current_state in closed_set:
                continue
            closed_set.add(current_state)

            for neighbor in self._get_neighbors(current_state):
                if neighbor in closed_set:
                    continue

                new_g = g + 1

                if new_g < g_scores.get(neighbor, float('inf')):
                    g_scores[neighbor] = new_g
                    new_f = new_g + manhattan(neighbor)
                    heapq.heappush(open_set, (new_f, new_g, neighbor, current_path + [neighbor]))
        
        if return_nodes_explored: return None, nodes_explored
        return None

    # --- Core BFS Solver ---
    def _bfs_solver_core(self, start_state):
        goal = tuple(list(range(1, SIZE*SIZE)) + [0])
        queue = deque([(start_state, [start_state])]) # (state, path)
        visited = {start_state}
        nodes_explored = 0

        while queue:
            current_state, path = queue.popleft()
            nodes_explored += 1

            if current_state == goal:
                return path, nodes_explored

            for neighbor in self._get_neighbors(current_state):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None, nodes_explored

    # --- Core DFS Solver ---
    def _dfs_solver_core(self, start_state, max_depth=50): # Add a max_depth to prevent infinite recursion/long runs
        goal = tuple(list(range(1, SIZE*SIZE)) + [0])
        stack = [(start_state, [start_state], 0)] # (state, path, depth)
        visited = set() # To track visited states in the current path to avoid cycles
        
        # We need to manage visited states carefully for DFS to find *any* path without loops.
        # For finding a solution and not getting stuck, it's often better to re-initialize visited
        # for each branch, or use iterative deepening DFS for optimal path.
        # For simplicity, this visited set prevents re-exploring states if found during search.
        nodes_explored = 0

        while stack:
            current_state, path, depth = stack.pop()
            nodes_explored += 1

            if current_state == goal:
                return path, nodes_explored
            
            if current_state in visited:
                continue
            visited.add(current_state) # Mark as visited for this DFS run

            if depth < max_depth: # Depth limit to prevent extremely long runs/recursion errors
                # Get neighbors and push them onto the stack (in reverse order for natural LIFO)
                for neighbor in reversed(self._get_neighbors(current_state)):
                    if neighbor not in visited: # Only explore if not already visited in this path
                        stack.append((neighbor, path + [neighbor], depth + 1))
        
        return None, nodes_explored

    def _get_neighbors(self, state_tuple):
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
                
                # Re-enable main game buttons, but solve button stays disabled if solved
                self.solve_button.config(state="disabled", text="Solve") 
                self.new_game_button.config(state="normal")
                self.hint_button.config(state="disabled") # No hints after solved
                self.update_undo_redo_buttons() # Re-enable undo/redo if applicable
                
                self.status_label.config(text=f"Solved in {self.move_count} moves!", fg="green")
                return

            current_flat_state = path[index]
            prev_flat_state = path[index - 1] if index > 0 else None

            # Determine which tile moved for visual highlight
            moved_tile_coords = None
            if prev_flat_state:
                prev_empty_idx = prev_flat_state.index(0)
                current_empty_idx = current_flat_state.index(0)
                # The tile that moved is the one that's now in the empty tile's previous position
                # Its value is current_flat_state[prev_empty_idx]
                # Its coordinates in the new state are determined by prev_empty_idx
                moved_tile_coords = divmod(prev_empty_idx, SIZE) # (row, col)

            self.tiles = [list(current_flat_state[i*SIZE:(i+1)*SIZE]) for i in range(SIZE)]
            self.update_ui(animating_move=moved_tile_coords)
            
            # Only increment move count for actual moves, not initial state
            if index > 0: 
                self.move_count = index 
                self.update_move_label()

            self.root.after(ANIMATION_DELAY_MS, step, index + 1)

if __name__ == "__main__":
    root = tk.Tk()
    game = SlidingPuzzle(root)
    root.mainloop()