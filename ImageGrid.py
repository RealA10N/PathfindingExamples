from Grid import Grid
from PIL import Image, ImageDraw


class ImageGrid(Grid):

    _border_size = 2
    _cell_size = 10
    
    _color_palette = ("white", "black")

    def print_image(self):
        
        img = Image.new("RGB", self._generate_image_size(), self._color_palette[0])

        drawing = ImageDraw.Draw(img)

        for row_i, row in enumerate(self.get_array()):
            for column_i, cell in enumerate(row):
                if cell.get_if_obstacle():  # current cell obstacle
                    self._draw_cell(drawing, (row_i, column_i), self._color_palette[1])

        img.show()
    
    def _generate_image_size(self):
        
        image_width = self._width * (self._cell_size + self._border_size) + self._border_size
        image_height = self._height * (self._cell_size + self._border_size) + self._border_size

        return (image_width, image_height)
    
    def _draw_cell(self, drawing, coords_tuple, color):
        
        starting_x = self._border_size + coords_tuple[0] * (self._cell_size + self._border_size)
        starting_y = self._border_size + coords_tuple[1] * (self._cell_size + self._border_size)
        
        drawing.rectangle(
            (starting_x, starting_y, starting_x + self._cell_size, starting_y + self._cell_size),
            fill=color)
        
