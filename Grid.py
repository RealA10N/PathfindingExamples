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
                    cur_row.append(1)  # current cell obstacle
                else:
                    cur_row.append(0)  # current cell empty
            
            array.append(cur_row)
        
        return array

    def print(self):

        for row in self.get_array():
            row_str = ""
            for cell in row:
                if cell == 1:
                    row_str += "X"
                else:
                    row_str += "-"
            print(row_str)
    
    def get_array(self):
        return self._array
