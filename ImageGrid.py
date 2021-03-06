from Grid import Grid
from PIL import Image, ImageDraw, ImageFont
from additionalFunctions import number_to_abc
from copy import deepcopy


class ImageGrid(Grid):

    def __init__(self, *args, **kwargs):
        Grid.__init__(self, *args, **kwargs)

        # style
        self._size_palette = {"cell": 60, "border": 10, "marker": 40, "ruler": 30}
        self._color_palette = {"bg": "white", "obstacle": "black"}

        # other
        self._basic_image = None  # will be saved the first time generated
        self._rulers_image = None  # will be saved the first time generated
        self._ruler_font = ImageFont.truetype("arial.ttf", int(self._size_palette["ruler"] * 0.9))


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

            starting_x = self._size_palette["border"] + cell.get_position()[0] * (self._size_palette["cell"] + self._size_palette["border"])
            starting_y = self._size_palette["border"] + cell.get_position()[1] * (self._size_palette["cell"] + self._size_palette["border"])

            # drawing obstacle
            drawing.rectangle(
                (starting_x, starting_y, starting_x + self._size_palette["cell"], starting_y + self._size_palette["cell"]),
                fill=self._color_palette["obstacle"])
    

    # - - - GENERATE RULERS IMAGE - - - #

    def _create_empty_ruler(self, is_horizontal):

        if is_horizontal:
            base_image_len = self._generate_image_size()[0]
        else:
            base_image_len = self._generate_image_size()[1]

        ruler_size = (base_image_len + self._size_palette["ruler"], self._size_palette["ruler"])
        return Image.new("RGB", ruler_size, self._color_palette["obstacle"])


    def _get_horizontal_ruler(self):

        ruler_img = self._create_empty_ruler(is_horizontal=True)
        ruler_drawing = ImageDraw.Draw(ruler_img)

        for cur_cell in range(self._width):

            text = number_to_abc(cur_cell).upper()
            text_size = self._ruler_font.getsize(text)[0]

            cell_start_x = self._size_palette["ruler"] + self._size_palette["border"] + cur_cell * (self._size_palette["cell"] + self._size_palette["border"])            
            text_starting_x = int((self._size_palette["cell"] / 2) - (text_size / 2)) + cell_start_x

            ruler_drawing.text((text_starting_x, 0), text, fill=self._color_palette["bg"], font=self._ruler_font)
        
        return ruler_img
    

    def _get_vertical_ruler(self):
        
        ruler_img = self._create_empty_ruler(is_horizontal=False)
        ruler_drawing = ImageDraw.Draw(ruler_img)

        for cur_cell in range(self._height):

            text = str(cur_cell)
            text_size = self._ruler_font.getsize(text)[0]

            cell_end_x = self._generate_image_size(rulers=True)[1] - cur_cell * (self._size_palette["cell"] + self._size_palette["border"]) - self._size_palette["ruler"] - self._size_palette["border"]
            cell_start_x = cell_end_x - self._size_palette["cell"]
            text_starting_x = int((self._size_palette["cell"] / 2) - (text_size / 2)) + cell_start_x

            ruler_drawing.text((text_starting_x, 0), text, fill=self._color_palette["bg"], font=self._ruler_font)
        
        return ruler_img.rotate(90, expand=True)
    

    def _generate_ruler_image(self):
        
        img = Image.new("RGB", self._generate_image_size(rulers=True), self._color_palette["bg"])
        
        # paste rulers
        img.paste(self._get_horizontal_ruler())
        img.paste(self._get_vertical_ruler())

        # paste basic grid
        img.paste(self._basic_image, (self._size_palette["ruler"], self._size_palette["ruler"]))

        self._rulers_image = img
    

    # - - - GENETATE MARKER IMAGE - - - #

    def _get_marker_image(self):
        
        img = Image.new("RGBA", self._generate_image_size(rulers=False), color=(0, 0, 0, 0))  # grid transperent image
        drawing = ImageDraw.Draw(img)

        for row in self.get_array():
            for cell in row:
                self._draw_cell_marker(drawing, cell)

        return img

    
    def _draw_cell_marker(self, drawing, cell):

        if cell.get_marker_color() is not None:

            # calculate the position to start drawing the marker
            # in a way that the marker will be in the middle of the cell
            position_in_cell = int((self._size_palette["cell"] / 2) - (self._size_palette["marker"] / 2))

            starting_x = self._size_palette["border"] + cell.get_position()[0] * (self._size_palette["border"] + self._size_palette["cell"]) + position_in_cell
            starting_y = self._size_palette["border"] + cell.get_position()[1] * (self._size_palette["border"] + self._size_palette["cell"]) + position_in_cell
        
            drawing.rectangle((starting_x, starting_y, starting_x + self._size_palette["marker"], starting_y + self._size_palette["marker"]), fill=cell.get_marker_color())
    

    def _add_markers_to_image(self, base_img):

        marker_img = self._get_marker_image()

        # we want to stick the marker image to the
        # bottom right of the base_image.
        marker_width, marker_height = marker_img.size
        base_width, base_height = base_img.size

        pasting_x = base_width - marker_width
        pasting_y = base_height - marker_height

        base_img.paste(marker_img, (pasting_x, pasting_y), marker_img)


    # - - - GENERAL IMAGE METHODS - - - #

    def _get_image(self, rulers, markers):

        if self._basic_image is None:
            self._generate_basic_image()
        
        if rulers:
            if self._rulers_image is None:
                self._generate_ruler_image()
            
            img = deepcopy(self._rulers_image)
        else:
            img = deepcopy(self._basic_image)
        
        if markers:
            self._add_markers_to_image(img)
        
        return img


    def print_image(self, rulers=True, markers=True):
        self._get_image(rulers=rulers, markers=markers).show()

    
    def _generate_image_size(self, rulers=False):
        
        image_width = self._width * (self._size_palette["cell"] + self._size_palette["border"]) + self._size_palette["border"]
        image_height = self._height * (self._size_palette["cell"] + self._size_palette["border"]) + self._size_palette["border"]

        if rulers:
            image_width += self._size_palette["ruler"]
            image_height += self._size_palette["ruler"]

        return (image_width, image_height)
