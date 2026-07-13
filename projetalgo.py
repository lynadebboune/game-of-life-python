import random
import tkinter as tk
from tkinter import messagebox

class gameOfLife:
    def __init__(self, rows: int, cols: int, alive: int = 0):
        self.rows = rows
        self.cols = cols
        self.alive = alive
        self.grid = [["-" for _ in range(cols)] for _ in range(rows)]

    def insideGrid(self, x: int, y: int) -> bool:
        return 0 <= x < self.rows and 0 <= y < self.cols

    def setCell(self, x: int, y: int, alive: bool):
        if self.insideGrid(x, y):
            self.grid[x][y] = "*" if alive else "-"

    def countAdjacents(self, x: int, y: int) -> int:
        offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0), (1, 1)
        ]
        counter = 0
        for dx, dy in offsets:
            nx, ny = x + dx, y + dy
            if self.insideGrid(nx, ny) and self.grid[nx][ny] == "*":
                counter += 1
        return counter

    def distributeAlive(self):
        """Remplit aléatoirement la grille."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c] = "-"

        placed = 0
        while placed < self.alive:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.grid[r][c] == "-":
                self.grid[r][c] = "*"
                placed += 1

    def isEmpty(self) -> bool:
        return all(cell == "-" for row in self.grid for cell in row)

    def nextGeneration(self):
        """Calcule la génération suivante."""
        nextGen = [["-" for _ in range(self.cols)] for _ in range(self.rows)]

        for r in range(self.rows):
            for c in range(self.cols):
                adj = self.countAdjacents(r, c)
                if self.grid[r][c] == "*":
                    nextGen[r][c] = "*" if (adj == 2 or adj == 3) else "-"
                else:
                    nextGen[r][c] = "*" if adj == 3 else "-"

        self.grid = nextGen


class GameGUI:
    CELL_SIZE = 20
    SPEED = 120  

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Conway - Game of Life")

        self.running = False
        self.last_state = None
        self.game = None

        self.createUI()
        self.root.mainloop()

    def createUI(self):
        controls = tk.Frame(self.root)
        controls.pack(side="top")

        tk.Label(controls, text="Rows:").grid(row=0, column=0)
        tk.Label(controls, text="Cols:").grid(row=0, column=2)
        tk.Label(controls, text="Alive:").grid(row=0, column=4)

        self.rows_entry = tk.Entry(controls, width=5)
        self.cols_entry = tk.Entry(controls, width=5)
        self.alive_entry = tk.Entry(controls, width=5)

        self.rows_entry.grid(row=0, column=1)
        self.cols_entry.grid(row=0, column=3)
        self.alive_entry.grid(row=0, column=5)

        self.rows_entry.insert(0, "20")
        self.cols_entry.insert(0, "20")
        self.alive_entry.insert(0, "50")

        tk.Button(controls, text="Create Grid", command=self.createGrid).grid(row=0, column=6, padx=10)

        # Buttons
        tk.Button(controls, text="Start", command=self.start).grid(row=1, column=0)
        tk.Button(controls, text="Stop", command=self.stop).grid(row=1, column=1)
        tk.Button(controls, text="Clear", command=self.clear).grid(row=1, column=2)
        tk.Button(controls, text="Next Step", command=self.nextStep).grid(row=1, column=3)
        tk.Button(controls, text="Random", command=self.randomGrid).grid(row=1, column=4)

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.toggleCell)

    def createGrid(self):
        rows = int(self.rows_entry.get())
        cols = int(self.cols_entry.get())

        self.game = gameOfLife(rows, cols)
        self.canvas.config(width=cols * self.CELL_SIZE, height=rows * self.CELL_SIZE)
        self.drawGrid()

    def drawGrid(self):
        if self.game is None:
            return

        self.canvas.delete("all")

        for r in range(self.game.rows):
            for c in range(self.game.cols):
                x1 = c * self.CELL_SIZE
                y1 = r * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE

                color = "black" if self.game.grid[r][c] == "*" else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def toggleCell(self, event):
        if self.game is None:
            return

        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE

        if not self.game.insideGrid(row, col):
            return

        self.game.grid[row][col] = "-" if self.game.grid[row][col] == "*" else "*"
        self.drawGrid()

    def start(self):
        if self.game is None:
            return
        self.running = True
        self.last_state = None
        self.runStep()

    def stop(self):
        self.running = False

    def clear(self):
        if self.game is None:
            return
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                self.game.grid[r][c] = "-"
        self.drawGrid()

    def randomGrid(self):
        if self.game is None:
            return
        alive = int(self.alive_entry.get())
        self.game.alive = alive
        self.game.distributeAlive()
        self.drawGrid()

    def nextStep(self):
        if self.game is None:
            return
        old = [row[:] for row in self.game.grid]
        self.game.nextGeneration()
        self.drawGrid()

        if old == self.game.grid:
            messagebox.showinfo("Stable", "La configuration est stable.")

    def runStep(self):
        if not self.running:
            return

        old_state = [row[:] for row in self.game.grid]
        self.game.nextGeneration()
        self.drawGrid()

        if old_state == self.game.grid:
            self.running = False
            messagebox.showinfo("Stable!", "La structure est stable.")
            return

        if self.game.isEmpty():
            self.running = False
            messagebox.showinfo("Finished", "Toutes les cellules sont mortes.")
            return

        self.root.after(self.SPEED, self.runStep)


GameGUI()
