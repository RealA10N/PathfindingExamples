from random import random

class Grid:

    def __init__(self, width, height, obstacle_percentage = 0.25):
        
        self._width = width
        self._height = height
        self._obstacle_percentage = obstacle_percentage

        self._array = self._generate_grid_array()
    
    def _generate_grid_array(self):
        
        array = []
        
        for i_row in range(self._width):
            
            cur_row = []
            for i_column in range(self._height):
                
                if random() < self._obstacle_percentage:
                    cur_if_obstacle = True
                else:
                    cur_if_obstacle = False
                
                cur_row.append(BasicCell(cur_if_obstacle))
            
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

class BasicCell:

    def __init__(self, if_obstacle):
        self.set_if_obstacle(if_obstacle)

    def set_if_obstacle(self, if_obstacle):
        self._if_obstacle = if_obstacle
    
    def get_if_obstacle(self):
        return self._if_obstacle