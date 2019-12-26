import random

class Grid:

    def __init__(self, width, height, obstacle_percentage = 0.35, seed=random.random()):
        
        self._width = width
        self._height = height
        self._obstacle_percentage = obstacle_percentage

        self._array = self._generate_grid_array(seed)
    
    def _generate_grid_array(self, seed):
        
        random.seed(seed)
        array = []
        
        for i_row in range(self._height):
            
            cur_row = []
            for i_column in range(self._width):
                
                cur_if_obstacle = random.random() < self._obstacle_percentage
                cur_cell_position = (i_column, i_row)
                cur_row.append(BasicCell(cur_if_obstacle, cur_cell_position))
            
            array.append(cur_row)
        
        return array

    def print(self):

        for row in self.get_array():
            row_str = ""
            for cell in row:
                if cell.get_if_obstacle():
                    row_str += "X"
                else:
                    row_str += "-"
            print(row_str)
    
    def get_array(self):
        return self._array
    
    def get_cell(self, position):
        return self.get_array()[position[1]][position[0]]

class BasicCell:

    def __init__(self, if_obstacle, position, marker_color=None):
        self._if_obstacle = if_obstacle
        self._position = position
        self._marker_color = marker_color
    
    def get_if_obstacle(self):
        return self._if_obstacle
    
    def get_position(self):
        return self._position
    
    def get_marker_color(self):
        return self._marker_color

    def set_marker_color(self, color):
        self._marker_color = color
    
    def remove_marker(self):
        self._marker_color = None