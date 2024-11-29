#  mazevisualizer, generator is not my code
#  just made the bfs search and path maker
#  see_maze is just so it's not ugly
Maze = list[list[int]]
Path = list[tuple[int]]
Result = tuple[Path, Path]

class MazeVisualizer:

    def __init__(self, master, maze, cell_size=10):
        import tkinter as tk
        self.master = master
        self.maze = maze
        self.cell_size = cell_size
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.canvas = tk.Canvas(master, width=self.cols * cell_size, height=self.rows * cell_size)
        self.canvas.pack()
        self.draw_maze()

    def draw_maze(self):
        """Draws the maze grid."""
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if self.maze[row][col] == 1:  # Wall
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray10")
                else:  # Open path
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")

    def draw_start_and_end(self, start, end):
        row, col = end
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="gray")

    def animate_path(self, path, delay=100, on_complete=None):
        def draw_step(index):
            if index < len(path):
                row, col = path[index]
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="RoyalBlue1", outline="gray")
                self.master.after(delay, draw_step, index + 1)
            else:
                if on_complete:
                    on_complete()

        draw_step(0)

    def animate_solution(self, path, delay=100):
        def draw_solution_step(index):
            if index < len(path):
                row, col = path[index]
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="lawn green", outline="gray")
                self.master.after(delay, draw_solution_step, index + 1)
        draw_solution_step(0)
def generate_maze(height, width):
    import random
    maze = [[1 for _ in range(width)] for _ in range(height)]

    def is_valid_cell(r, c):
        return 0 <= r < height and 0 <= c < width and maze[r][c] == 1

    def neighbors(r, c):
        steps = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # Two steps in all four directions
        result = []
        for dr, dc in steps:
            nr, nc = r + dr, c + dc
            if is_valid_cell(nr, nc):
                result.append((nr, nc))
        return result

    def carve_path(r, c):
        maze[r][c] = 0  # Mark the current cell as a path
        random.shuffle(neighbor_list := neighbors(r, c))  # Randomize neighbors
        for nr, nc in neighbor_list:
            # Find the wall between the current cell and the neighbor
            wall_r, wall_c = (r + nr) // 2, (c + nc) // 2
            if maze[nr][nc] == 1:  # If the neighbor is a wall, carve through
                maze[wall_r][wall_c] = 0
                carve_path(nr, nc)

    # Start carving the maze from the top-left corner
    carve_path(0, 0)

    # Ensure the start (0, 0) and end (height-1, width-1) are open
    maze[0][0] = 0
    maze[height-1][width-1] = 0

    return maze
def bfs(maze: Maze, start, end, empty= 0, wall= 1) -> Result | bool:

    if len(maze[0]) < 1 or maze[0][0] != 0 or maze[end[0]][end[1]] != empty:
        return False

    columns_count = len(maze)
    values_in_col_count = len(maze[0])
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    waiting_line = [start]
    path_used = {start: None}

    used = [start]

    while len(waiting_line) > 0:

        working_pos = waiting_line.pop(0)
        working_col, working_row = working_pos[0], working_pos[1]


        if working_pos == end:
                path: Path  = []
                while working_pos:
                    path.append(working_pos)
                    working_pos = path_used[working_pos]
                path.reverse()

                if used is not None and path is not None:
                    return used, path

        for changer in moves:
            next_move = (working_col - changer[0] , working_row - changer[1] )
            next_col, next_row = next_move

            if 0 <= next_col < columns_count and 0 <= next_row < values_in_col_count:
                if maze[next_col][next_row] != wall and next_move not in used and next_move:
                    waiting_line.append(next_move)
                    used.append(next_move)
                    path_used[next_move] = working_pos

    return False
def see_maze(height, width, square_size = 20):
    import tkinter as tk
    maze = generate_maze(height, width)
    start = (0, 0)
    end = (len(maze) - 1, len(maze[0]) - 1)

    path_checked, path_solution = bfs(maze, start, end)  # moj algoritmus
    root = tk.Tk()
    root.title("Maze Visualizer")
    visualizer = MazeVisualizer(root, maze, square_size)
    visualizer.draw_start_and_end(start, end)

    visualizer.animate_path(path_checked, delay=1,
                            on_complete=lambda: visualizer.animate_solution(path_solution, delay=1))

    root.mainloop()


see_maze(37, 71, 20)

