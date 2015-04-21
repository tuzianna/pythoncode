"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._zombie_list = []
        self._human_list = []
        
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        if self._cells[row][col] != FULL:
            #self._cells[row][col] = ZOMBIE
            self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        if self.num_zombies() > 0:
            for zombie in self._zombie_list:
                yield zombie
            

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        if self._cells[row][col] != FULL:
            #self._cells[row][col] = HUMAN
            self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        if self.num_humans() > 0:
            for human in self._human_list:
                yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = [[EMPTY for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]
        distance_field = [[ self._grid_height * self._grid_width for dummy_i in range(self._grid_width)] for dummy_j in range(self._grid_height)]
        boundry = poc_queue.Queue()
        
        if entity_type == HUMAN:
            targets = list(self._human_list)

        if entity_type == ZOMBIE:
            targets = list(self._zombie_list)            
            
        for target in targets:
            boundry.enqueue(target)
            visited[target[0]][target[1]] = FULL
            distance_field[target[0]][target[1]] = 0
            
        while len(boundry) > 0:
            cell = boundry.dequeue()            
            neighbors = self.four_neighbors(cell[0], cell[1])
            for neighbor in neighbors:
                if visited[neighbor[0]][neighbor[1]] == EMPTY and self._cells[neighbor[0]][neighbor[1]] != FULL:
                    boundry.enqueue(neighbor)
                    visited[neighbor[0]][neighbor[1]] = FULL
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[cell[0]][cell[1]] + 1
        return distance_field


    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        
        if self.num_humans() > 0:
            distance = self.compute_distance_field(ZOMBIE)
            for idx in range(self.num_humans()):
                available_move = []
                neighbor_distances = []
                human = self._human_list[idx]
                available_move.append(human)
                neighbor_distances.append(distance[human[0]][human[1]])
                neighbors = self.eight_neighbors(human[0], human[1])
                for neighbor in neighbors:
                    if self._cells[neighbor[0]][neighbor[1]] != FULL:
                        neighbor_distances.append(distance[neighbor[0]][neighbor[1]])
                        available_move.append(neighbor)
                max_distance = max(neighbor_distances)
                best_moves = []
                for cell in available_move:
                    if distance[cell[0]][cell[1]] == max_distance:
                        best_moves.append(cell)
                random_best_move = best_moves[random.randrange(len(best_moves))]
                self._human_list[idx] = random_best_move
        
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        if self.num_zombies() > 0:
            distance = self.compute_distance_field(HUMAN)
            for idx in range(self.num_zombies()):
                available_move = []
                neighbor_distances = []
                zombie = self._zombie_list[idx]
                available_move.append(zombie)
                neighbor_distances.append(distance[zombie[0]][zombie[1]])
                neighbors = self.four_neighbors(zombie[0], zombie[1])
                for neighbor in neighbors:
                    if self._cells[neighbor[0]][neighbor[1]] != FULL:
                        neighbor_distances.append(distance[neighbor[0]][neighbor[1]])
                        available_move.append(neighbor)
                min_distance = min(neighbor_distances)
                best_moves = []
                for cell in available_move:
                    if distance[cell[0]][cell[1]] == min_distance:
                        best_moves.append(cell)
                random_best_move = best_moves[random.randrange(len(best_moves))]
                self._zombie_list[idx] = random_best_move

# Start up gui for simulation - You will need to write some code above
# before this will work without errors
poc_zombie_gui.run_gui(Zombie(30, 40))
