import tkinter as tk
from tkinter import messagebox
from collections import deque

# --- Missionaries and Cannibals Solver (from previous response) ---

def solve_missionaries_cannibals():
    initial_state = (3, 3, 0)
    goal_state = (0, 0, 1)
    queue = deque([(initial_state, [initial_state])])
    visited = set()

    moves = [
        (1, 0), (0, 1), (2, 0), (0, 2), (1, 1)
    ]

    while queue:
        current_state, path = queue.popleft()

        if current_state == goal_state:
            return path

        if current_state in visited:
            continue

        visited.add(current_state)

        m_left, c_left, boat_pos = current_state

        for dm, dc in moves:
            if boat_pos == 0:  # Boat on left bank, moving to right
                new_m_left = m_left - dm
                new_c_left = c_left - dc
                new_boat_pos = 1
            else:  # Boat on right bank, moving to left
                new_m_left = m_left + dm
                new_c_left = c_left + dc
                new_boat_pos = 0

            new_state = (new_m_left, new_c_left, new_boat_pos)

            if is_valid(new_state):
                if new_state not in visited:
                    queue.append((new_state, path + [new_state]))
    return None

def is_valid(state):
    m_left, c_left, boat_pos = state
    m_right = 3 - m_left
    c_right = 3 - c_left

    if not (0 <= m_left <= 3 and 0 <= c_left <= 3 and
            0 <= m_right <= 3 and 0 <= c_right <= 3):
        return False

    if m_left > 0 and c_left > m_left:
        return False

    if m_right > 0 and c_right > m_right:
        return False
    return True

# --- GUI Implementation ---

class MC_GUI:
    def __init__(self, master):
        self.master = master
        master.title("Missionaries and Cannibals Solver")
        master.geometry("600x400")
        master.resizable(False, False)

        self.solution_path = solve_missionaries_cannibals()
        self.current_step_index = 0

        if not self.solution_path:
            messagebox.showerror("Error", "No solution found for the problem!")
            master.destroy()
            return

        self.create_widgets()
        self.display_current_state()

    def create_widgets(self):
        # Frame for displaying the banks
        self.display_frame = tk.Frame(self.master, bd=2, relief="groove", padx=10, pady=10)
        self.display_frame.pack(pady=20, padx=20, fill="x")

        # Left Bank Labels
        self.left_bank_label = tk.Label(self.display_frame, text="Left Bank", font=("Arial", 14, "bold"))
        self.left_bank_label.grid(row=0, column=0, padx=20)
        self.left_m_label = tk.Label(self.display_frame, text="M: 3", font=("Arial", 12))
        self.left_m_label.grid(row=1, column=0)
        self.left_c_label = tk.Label(self.display_frame, text="C: 3", font=("Arial", 12))
        self.left_c_label.grid(row=2, column=0)

        # River/Boat Labels
        self.river_label = tk.Label(self.display_frame, text="~ River ~", font=("Arial", 14, "italic"), width=15)
        self.river_label.grid(row=0, column=1)
        self.boat_label = tk.Label(self.display_frame, text="Boat: Left", font=("Arial", 12, "bold"))
        self.boat_label.grid(row=1, column=1)

        # Right Bank Labels
        self.right_bank_label = tk.Label(self.display_frame, text="Right Bank", font=("Arial", 14, "bold"))
        self.right_bank_label.grid(row=0, column=2, padx=20)
        self.right_m_label = tk.Label(self.display_frame, text="M: 0", font=("Arial", 12))
        self.right_m_label.grid(row=1, column=2)
        self.right_c_label = tk.Label(self.display_frame, text="C: 0", font=("Arial", 12))
        self.right_c_label.grid(row=2, column=2)

        # Step Counter
        self.step_label = tk.Label(self.master, text="Step 0 / 0", font=("Arial", 12))
        self.step_label.pack(pady=10)

        # Navigation Buttons
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(pady=10)

        self.prev_button = tk.Button(self.button_frame, text="Previous Step", command=self.prev_step, state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.button_frame, text="Next Step", command=self.next_step)
        self.next_button.pack(side=tk.RIGHT, padx=10)

    def display_current_state(self):
        if not self.solution_path:
            return

        current_state = self.solution_path[self.current_step_index]
        m_left, c_left, boat_pos = current_state
        m_right = 3 - m_left
        c_right = 3 - c_left

        self.left_m_label.config(text=f"M: {m_left}")
        self.left_c_label.config(text=f"C: {c_left}")
        self.right_m_label.config(text=f"M: {m_right}")
        self.right_c_label.config(text=f"C: {c_right}")

        boat_text = "Boat: Left" if boat_pos == 0 else "Boat: Right"
        self.boat_label.config(text=boat_text)

        self.step_label.config(text=f"Step {self.current_step_index} / {len(self.solution_path) - 1}")

        # Manage button states
        if self.current_step_index == 0:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)

        if self.current_step_index == len(self.solution_path) - 1:
            self.next_button.config(state=tk.DISABLED)
        else:
            self.next_button.config(state=tk.NORMAL)

    def next_step(self):
        if self.current_step_index < len(self.solution_path) - 1:
            self.current_step_index += 1
            self.display_current_state()

    def prev_step(self):
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.display_current_state()

if __name__ == "__main__":
    root = tk.Tk()
    gui = MC_GUI(root)
    root.mainloop()