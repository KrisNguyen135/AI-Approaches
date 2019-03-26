import random
from tkinter import Tk, Canvas


class MainWindow:
    def __init__(self):
        self.grid_size = 600
        self.cell_size = 40
        self.half_cell = self.cell_size // 2
        self.tiles = self.grid_size // self.cell_size
        self.buffer_height = self.cell_size
        self.WIDTH = self.grid_size
        self.HEIGHT = self.grid_size + self.buffer_height
        self.button_dim = [self.cell_size * 3, self.cell_size // 2]
        self.master = Tk()
        self.canvas = Canvas(self.master, width=self.WIDTH, height=self.HEIGHT)
        self.count = 0
        self.canvas.bind("<Button-1>", callback_left)
        self.canvas.bind("<Button-3>", callback_right)

    def counter(self):
        """
        This function is called within the event timer. It updates the time counter, and draws it on the canvas.
        """
        if game.game_in_prog is False:
            pass
        else:
            self.count += 1

        self.canvas.create_rectangle(250, 0, 350, 40, fill="grey")
        self.canvas.create_text(300, 20, text=str(self.count))

    def event_timer(self):
        """
        This block of code executes once per second.
        """
        self.counter()
        self.canvas.after(1000, self.event_timer)

    def create_buttons(self):
        """
        Generates grid at the beginning of the game
        """
        self.canvas.create_rectangle(0, 0, self.button_dim[0], self.button_dim[1], fill="green")
        self.canvas.create_text(self.button_dim[0] // 2, self.button_dim[1] // 2, text="New game")

    def end_graphic(self, cell):
        """
        This code is executed when player selects mine. The locations of the mines are displayed to the player-
        with "X"'s in red boxes.
        """
        placement = cell.placement
        self.canvas.create_rectangle(placement[0] * self.cell_size,
                                     placement[1] * self.cell_size,
                                     placement[0] * self.cell_size + self.cell_size,
                                     placement[1] * self.cell_size + self.cell_size,
                                     fill="red")

        self.canvas.create_text(placement[0] * self.cell_size + self.half_cell,
                                placement[1] * self.cell_size + self.half_cell,
                                text="X", fill="black")

    def number_graphic(self, cell):
        placement = cell.placement
        mine_count = cell.mine_count
        self.canvas.create_text(placement[0] * self.cell_size + self.half_cell,
                                placement[1] * self.cell_size + self.half_cell,
                                text=mine_count, fill="black")

    def flag_graphic(self, cell):
        placement = cell.placement
        self.canvas.create_text(placement[0] * self.cell_size + self.half_cell,
                                placement[1] * self.cell_size + self.half_cell,
                                text="FLAG", fill="black")

    def grey_graphic(self, cell):
        placement = cell.placement
        self.canvas.create_rectangle(placement[0] * self.cell_size,
                                     placement[1] * self.cell_size,
                                     placement[0] * self.cell_size + self.cell_size,
                                     placement[1] * self.cell_size + self.cell_size,
                                     fill="grey")

    def green_graphic(self, cell):
        placement = cell.placement
        self.canvas.create_rectangle(placement[0] * self.cell_size,
                                     placement[1] * self.cell_size,
                                     placement[0] * self.cell_size + self.cell_size,
                                     placement[1] * self.cell_size + self.cell_size,
                                     fill="green")


class GameState:
    def __init__(self):
        self.mine_quantity = 35
        self.game_in_prog = True
        self.mines = []
        self.flags = []
        self.selected_tiles = []
        self.cells = []
        self.cell_dict = {}

    def create_mines(self):
        """
        Randomly generates mines at the beginning of the game.
        """
        for cell in self.cells:
            cell.mine_probability()

    def trip_mine(self):
        """
        Executes if player selects mine
        """
        self.game_in_prog = False
        self.show_mines()

    def show_mines(self):
        """
        This function is called at game over. It visually shows the player where the mines are located on the canvas
        """
        for mine in self.mines:
            window.end_graphic(mine)

    def new_game(self):
        """
        This function reinitializes game state
        """
        window.count = 0  # in-game counter
        self.game_in_prog = True
        self.flags = []
        self.selected_cells = []
        self.cells = []
        self.mines = []
        self.cell_dict = {}
        self.create_cells()
        self.start_cells()
        self.create_cell_dict()
        self.create_mines()
        self.find_all_mines()
        window.create_buttons()
        self.find_all_mines()

    def create_cells(self):
        for i in range(window.tiles):
            for j in range(window.tiles):
                placement = [i, j + 1]
                a_cell = Cell(placement)
                self.cells.append(a_cell)

    def create_cell_dict(self):
        for cell in self.cells:
            self.cell_dict[cell.name] = cell

    def start_cells(self):
        for cell in self.cells:
            cell.start()

    def find_all_mines(self):
        for cell in self.cells:
            if cell.is_mine:
                self.mines.append(cell)


class Cell:
    def __init__(self, placement):
        self.placement = placement
        self.name = ''
        self.mine_count = 0
        self.adjacent_cells = []
        self.is_mine = False
        self.letters = {
            0: 'A', 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H",
            8: "I", 9: "J", 10: "K", 11: "L", 12: "M", 13: "N", 14: "O", 15: "P"
        }

    def find_adjacent_cell(self):
        """
        Takes mouseclick cell as input, returns all adjacent cells to self .The a1 variable series (a1, a2, etc)-
        represents all adjacent cells.
        """
        self.adjacent_cells = []
        up = -1                                                           #_________________
        down = 1                                                          # a1 |  a2  | a3 |
        left = -1                                                         # a4 | self | a5 |
        right = 1                                                         # a6 |  a7  | a8 |
        same = 0                                                          #=================
        a1 = [self.placement[0] + left, self.placement[1] + up]           # upper left
        a2 = [self.placement[0] + same, self.placement[1] + up]           # upper
        a3 = [self.placement[0] + right, self.placement[1] + up]          # upper right
        a4 = [self.placement[0] + left, self.placement[1] + same]         # left
        a5 = [self.placement[0] + right, self.placement[1] + same]        # right
        a6 = [self.placement[0] + left, self.placement[1] + down]         # lower left
        a7 = [self.placement[0] + same, self.placement[1] + down]         # lower
        a8 = [self.placement[0] + right, self.placement[1] + down]        # lower right
        a_series = [a1, a2, a3, a4, a5, a6, a7, a8]
        for item in a_series:
            if 15 > item[0] >= 0 and 15 > item[1] >= 1:                   #screening out coord not in grid
                name = find_name(item)
                self.adjacent_cells.append(game.cell_dict[name])
        return self.adjacent_cells

    def mine_probability(self):
        a = random.randrange(5)
        if a == 0:
            self.is_mine = True

    def find_adjacent_mines(self):
        for adjacent_cell in self.adjacent_cells:
            if adjacent_cell in game.mines:
                self.mine_count += 1

    def create_name(self):
        a = self.letters[self.placement[0]]
        b = self.placement[1]
        self.name = a + str(b)

    def start(self):
        self.create_name()
        window.grey_graphic(self)

    def select_cell(self):
        self.find_adjacent_cell()
        self.find_adjacent_mines()
        game.selected_cells.append(self)
        window.number_graphic(self)
        if self.is_mine:
            game.trip_mine()


def find_name(placement):
    a = a_cell.letters[placement[0]]
    b = placement[1]
    name = a + str(b)
    return name

def detect_button(coordinates):
    """
    Determines if player hit "New Game" button, if so start new game
    """
    if coordinates[0] < window.button_dim[0] and coordinates[1] < window.button_dim[1]:
        game.new_game()

def find_placement(coordinates):
    """
    Converts input from mouse measured in pixels --> cell in canvas grid.
    """
    cell_conversion = [0, 0]
    cell_conversion[0] = coordinates[0] // window.cell_size
    cell_conversion[1] = coordinates[1] // window.cell_size
    return cell_conversion

def callback_left(event):
    """
    Handler for left mouseclick. This block of code executes everytime left-mouseclick event occurs.
    """
    coord = [event.x, event.y]
    detect_button(coord)
    if coord[1] < window.buffer_height:
        return None
    if game.game_in_prog is False:
        return None

    placement = find_placement(coord)
    name = find_name(placement)
    cell = game.cell_dict[name]
    if cell in game.selected_cells:
        return None

    cell.select_cell()

def callback_right(event):
    """
    Handler for right mouseclick. This block of code executes everytime left-mouseclick event occurs.
    """
    coord = [event.x, event.y]
    placement = find_placement(coord)
    name = find_name(placement)
    cell = game.cell_dict[name]

    if cell not in game.flags:
        window.flag_graphic(cell)
        game.flags.append(cell)
    else:
        window.grey_graphic(cell)
        game.flags.remove(cell)


# Objects
window = MainWindow()
game = GameState()
a_cell = Cell([1, 1])

# function calls
game.new_game()
window.event_timer()
window.canvas.pack()
window.master.mainloop()
