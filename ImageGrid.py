from Grid import Grid
from PIL import Image, ImageDraw, ImageFont
from additionalFunctions import number_to_abc


class ImageGrid(Grid):

    def __init__(self, *args, **kwargs):
        Grid.__init__(self, *args, **kwargs)

        # style
        self._border_size = 10
        self._cell_size = 60
        self._ruler_size = 30    
        self._color_palette = {"bg": "white", "obstacle": "black"}

        # other
        self._basic_image = None  # will be saved the first time generated
        self._rulers_image = None  # will be saved the first time generated
        self._ruler_font = ImageFont.truetype("arial.ttf", int(self._ruler_size * 0.9))

    # - - - GENERATE BASIC IMAGE - - - #

    def _generate_basic_image(self):

        img = Image.new("RGB", self._generate_image_size(), self._color_palette["bg"])
        drawing = ImageDraw.Draw(img)

        for row in self.get_array():
            for cell in row:
                self._draw_cell(drawing, cell)
        
        self._basic_image = img
    

    def _draw_cell(self, drawing, cell):
        
        if cell.get_if_obstacle():

            starting_x = self._border_size + cell.get_position()[0] * (self._cell_size + self._border_size)
            starting_y = self._border_size + cell.get_position()[1] * (self._cell_size + self._border_size)

            # drawing obstacle
            drawing.rectangle(
                (starting_x, starting_y, starting_x + self._cell_size, starting_y + self._cell_size),
                fill=self._color_palette["obstacle"])
    
    # - - - GENERATE RULERS IMAGE - - - #

    def _create_empty_ruler(self, is_horizontal):

        if is_horizontal:
            base_image_len = self._generate_image_size()[0]
        else:
            base_image_len = self._generate_image_size()[1]

        ruler_size = (base_image_len + self._ruler_size, self._ruler_size)
        return Image.new("RGB", ruler_size, self._color_palette["obstacle"])


    def _get_horizontal_ruler(self):

        ruler_img = self._create_empty_ruler(is_horizontal=True)
        ruler_drawing = ImageDraw.Draw(ruler_img)

        for cur_cell in range(self._width):

            text = number_to_abc(cur_cell).upper()
            text_size = self._ruler_font.getsize(text)[0]

            cell_start_x = self._ruler_size + self._border_size + cur_cell * (self._cell_size + self._border_size)            
            text_starting_x = (self._cell_size / 2) - (text_size / 2) + cell_start_x

            ruler_drawing.text((text_starting_x, 0), text, fill=self._color_palette["bg"], font=self._ruler_font)
        
        return ruler_img
    

    def _get_vertical_ruler(self):
        
        ruler_img = self._create_empty_ruler(is_horizontal=False)
        ruler_drawing = ImageDraw.Draw(ruler_img)

        for cur_cell in range(self._height):

            text = str(cur_cell)
            text_size = self._ruler_font.getsize(text)[0]

            cell_end_x = self._generate_image_size(rulers=True)[1] - cur_cell * (self._cell_size + self._border_size) - self._ruler_size - self._border_size
            cell_start_x = cell_end_x - self._cell_size
            text_starting_x = (self._cell_size / 2) - (text_size / 2) + cell_start_x

            ruler_drawing.text((text_starting_x, 0), text, fill=self._color_palette["bg"], font=self._ruler_font)
        
        return ruler_img.rotate(90, expand=True)
    

    def _generate_ruler_image(self):
        
        img = Image.new("RGB", self._generate_image_size(rulers=True), self._color_palette["bg"])
        
        # paste rulers
        img.paste(self._get_horizontal_ruler())
        img.paste(self._get_vertical_ruler())

        # paste basic grid
        img.paste(self._basic_image, (self._ruler_size, self._ruler_size))

        self._rulers_image = img
    
    # - - - GENERAL IMAGE METHODS - - - #

    def _get_image(self, rulers):

        if self._basic_image is None:
            self._generate_basic_image()
        
        if rulers:
            if self._rulers_image is None:
                self._generate_ruler_image()
            
            return self._rulers_image
        else:
            return self._basic_image


    def print_image(self, rulers=True):
        self._get_image(rulers=rulers).show()

    
    def _generate_image_size(self, rulers=False):
        
        image_width = self._width * (self._cell_size + self._border_size) + self._border_size
        image_height = self._height * (self._cell_size + self._border_size) + self._border_size

        if rulers:
            image_width += self._ruler_size
            image_height += self._ruler_size

        return (image_width, image_height)
    

    