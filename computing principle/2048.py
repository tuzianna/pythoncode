"""
    Clone of 2048 game.
    """

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
    DOWN: (-1, 0),
    LEFT: (0, 1),
    RIGHT: (0, -1)}

# get the none zero list to paire
def get_none_zero_list(line):
    """
        get all the none zero numbers
        """
    new_line = []
    for dummy_i in range(0,len(line)):
        if line[dummy_i] != 0:
            new_line.append(line[dummy_i])
    return new_line

#get the zero list without operation
def get_zero_list(line):
    """
        get a list with all zero
        """
    zero_list = []
    for dummy_i in range(0, len(line)):
        if line[dummy_i] == 0:
            zero_list.append(0)
    return zero_list


# get the slided list
def slide(line):
    """
        slide the list first
        """
    none_zero_list = get_none_zero_list(line)
    zero_list = get_zero_list(line)
    return none_zero_list + zero_list


# to find if there is a pair
def find_pair(line):
    """
        this is to save time
        """
    if len(line) >1:
        for dummy_i in range(0,len(line) - 1):
            if line[dummy_i] !=0 and line[dummy_i] == line[dummy_i+1]:
                return True
    return False


# to get the INDEX of first paired element in list
def get_index(line):
    """
        get the index of first paired
        """
    for dummy_i in range(0,len(line) - 1):
        if line[dummy_i] !=0 and line[dummy_i] == line[dummy_i+1]:
            return dummy_i


# get the list after the first paired tiles
def get_list_before_paired(line):
    """
        get the list after the first paired tiles
        """
    if find_pair(line):
        index = get_index(line)
        return line[ :index + 2]
    return []


def get_list_after_paired(line):
    """
        get the list after the first paired tiles
        """
    if find_pair(line):
        index = get_index(line)
        return line[index + 2: ]
    return []


# if there is a pair, merge the pair
# if no, return the original pair
def pair_list(line):
    """
        merge the pair
        """
    paired_line = []
    
    for dummy_i in range(0, len(line)-1):
        if line[dummy_i] !=0 and line[dummy_i] == line[dummy_i+1]:
            paired_line.append(2 * line[dummy_i])
            paired_line.append(0)
            break
        else:
            paired_line.append(line[dummy_i])
    return paired_line


# merge tiles
def merge(line):
    """
        Function that merges a single row or column in 2048.
        """
    # replace with your code
    none_zero_list = get_none_zero_list(line)
    zero_list = get_zero_list(line)
    if find_pair(none_zero_list):
        before_pair = get_list_before_paired(none_zero_list)
        after_pair = get_list_after_paired(none_zero_list)
        pair1 = pair_list(before_pair)
        while(find_pair(after_pair)):
            before_pair = get_list_before_paired(after_pair)
            after_pair = get_list_after_paired(after_pair)
            pair1 = pair1 + pair_list(before_pair)
        pair1 = pair1 + after_pair + zero_list
        return slide(pair1)
    else:
        return none_zero_list + zero_list


def adjust_grid(grid,direction):
    """
        to reverse the grid we get after move
        """
    height = len(grid)
    width = len(grid[0])
    if direction == RIGHT or direction == LEFT:
        new_grid = [[0 for dummy_i in range(width)] for dummy_j in range(height)]
        for row in range(height):
            for col in range(width):
                if direction == LEFT:
                    new_grid[row][col] = grid[row][col]
                else:
                    new_grid[row][col] = grid[row][width - 1 - col]
    else:
        new_grid = [[0 for dummy_i in range(height)] for dummy_j in range(width)]
        for row in range(width):
            for col in range(height):
                if direction == UP:
                    new_grid[row][col] = grid[col][row]
                else:
                    new_grid[row][col] = grid[col][width - 1 - row]
    return new_grid


class TwentyFortyEight:
    """
        Class to run the game logic.
        """
    
    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._grid_height = grid_height
        self._grid_width = grid_width
        
        #initiate all tiles' value to 0
        self._grid_2048 = [[0 for col in range(self._grid_width)] for row in range(self._grid_height)]
        
        self.reset()
        
        # get list of indices of all directions
        self._grid_indices = {
        UP: [(0, col) for col in range(self._grid_width)],
        DOWN: [(self._grid_height - 1, col) for col in range(self._grid_width)],
        LEFT: [(row, 0) for row in range(self._grid_height)],
        RIGHT: [(row, self._grid_width -1 ) for row in range(self._grid_height)]
    }
    
    
    def reset(self):
        """
            Reset the game so the grid is empty except for two
            initial tiles.
            """
        
        #initiate all tiles' value to 0
        self._grid_2048 = [[0 for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]
        
        # two new tiles
        self.new_tile()
        self.new_tile()
    
    
    def __str__(self):
        """
            Return a string representation of the grid for debugging.
            """
        # replace with your code
        grid = '['
        for row in range(0,self._grid_height):
            grid += '['
            for col in range(0,self._grid_width):
                if col == self._grid_width - 1:
                    grid += str(self.get_tile(row, col))
                else:
                    grid += str(self.get_tile(row, col)) + ', '
            if row == self._grid_height - 1:
                grid += ']'
            else:
                grid += '], '
        
        grid += ']'
        return grid
    
    
    def get_grid_height(self):
        """
            Get the height of the board.
            """
        # replace with your code
        return self._grid_height
    
    def get_grid_width(self):
        """
            Get the width of the board.
            """
        # replace with your code
        return self._grid_width
    
    def move(self, direction):
        """
            Move all tiles in the given direction and add
            a new tile if any tiles moved.
            """
        new_grid = []
        # get the indices of specific direction
        new_indices = self._grid_indices[direction]
        for cell in new_indices:
            lst = self.traversed_list(cell, direction)
            merged_list = merge(lst)
            new_grid.append(merged_list)
        
        adjusted_grid = adjust_grid(new_grid,direction)
        if self.is_changed(adjusted_grid):
            self.update_grid(adjusted_grid)
            self.new_tile()
    
    
    def update_grid(self,grid):
        """
            update grid
            """
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                self.set_tile(row, col, grid[row][col])
    
    
    def new_tile(self):
        """
            Create a new tile in a randomly selected empty
            square.  The tile should be 2 90% of the time and
            4 10% of the time.
            """
        
        # get random corordinates for new tile
        row = random.randint(0,self._grid_width)
        col = random.randint(0,self._grid_height)
        #  keeps generating random tile corordinates for non-empty tile
        while self.get_tile(row,col) != 0:
            row = random.randint(0,self._grid_width)
            col = random.randint(0,self._grid_height)
        
        # get random index of new tile value
        freq = random.randint(0,9)
        if freq == 9:
            self.set_tile(row, col, 4)
        else:
            self.set_tile(row, col, 2)
    
    
    
    def set_tile(self, row, col, value):
        """
            Set the tile at position row, col to have the given value.
            """
        # replace with your code
        self._grid_2048[row][col] = value
    
    def get_tile(self, row, col):
        """
            Return the value of the tile at position row, col.
            """
        # replace with your code
        if row < self._grid_height and col < self._grid_width:
            return self._grid_2048[row][col]
    
    # get the list in one direction
    def traversed_list(self, start_cell, direction):
        """
            Function that iterates through the cells in a grid
            in a linear direction
            
            Both start_cell is a tuple(row, col) denoting the
            starting cell
            
            direction is a tuple that contains difference between
            consecutive cells in the traversal
            """
        lst = []
        if direction == UP or direction == DOWN:
            for step in range(self._grid_height):
                row = start_cell[0] + step * OFFSETS[direction][0]
                col = start_cell[1] + step * OFFSETS[direction][1]
                lst.append(self.get_tile(row, col))
        else:
            for step in range(self._grid_width):
                row = start_cell[0] + step * OFFSETS[direction][0]
                col = start_cell[1] + step * OFFSETS[direction][1]
                lst.append(self.get_tile(row, col))
        return lst
    
    
    def is_changed(self, new_grid):
        """
            to determine if any tile is moved
            """
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self.get_tile(row,col) != new_grid[row][col]:
                    return True
        return False



poc_2048_gui.run_gui(TwentyFortyEight(4, 5))
