import cv2
import pygame
from numba import njit
import numpy as np

@njit(fastmath=True)
def accelerate_conversion(image, width, height, color_coeff, step, char_indices, chars):
    values = []
    color_indices = image // color_coeff
    for x in range(0, width, step):
        for y in range(0, height, step):
            char_index = char_indices[x, y]
            if char_index:
                char = chars[char_index]
        color = tuple(color_indices[x, y])
        values.append([char, color, (x, y)])
    return values

class ArtConverter:
    def __init__(self, path="lagtrain.mp4", font_size=10, color_lvl=16):
        self.cv2_image = None
        pygame.init()
        self.COLOR_LVL = color_lvl
        self.capture = cv2.VideoCapture(path)
        self.path = path
        self.image, self.gray_image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pygame.display.set_mode(self.RES)
        self.clock = pygame.time.Clock()

        self.ASCII_CHARS = ' ixzao*#MW&8%B@$'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS)-1)

        self.font = pygame.font.SysFont('Arial', font_size, bold=True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.PALETTE, self.COLOR_COEFF = self.create_palette()

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = dict.fromkeys(self.ASCII_CHARS, None)
        color_coeff = int(color_coeff)
        for char in palette:
            char_palette = {}
            for color in color_palette:
                color_key = tuple(color // color_coeff)
                char_palette[color_key] = self.font.render(char, False, tuple(color))
            palette[char] = char_palette
        return palette, color_coeff


    def get_image(self):
        ret, self.cv2_image = self.capture.read()
        if not ret:
            exit()
        transposed_image = cv2.transpose(self.cv2_image)
        gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2RGB)
        return image, gray_image

    def draw_converted_image(self):
        self.surface.fill("black")
        self.image, self.gray_image = self.get_image()
        char_indices = self.gray_image // self.ASCII_COEFF
        #values = accelerate_conversion(self.image, self.WIDTH, self.HEIGHT, self.COLOR_COEFF, self.CHAR_STEP, char_indices, self.ASCII_CHARS)
        color_indices = self.image // self.COLOR_COEFF
        for x in range(0, self.WIDTH, self.CHAR_STEP):
            for y in range(0, self.HEIGHT, self.CHAR_STEP):
                char_index = char_indices[x, y]
                if char_index:
                    char = self.ASCII_CHARS[char_index]
                    color = tuple(color_indices[x, y])
                    self.surface.blit(self.PALETTE[char][color], (x, y))

    def draw(self):
        self.surface.fill("black")
        pygame.surfarray.blit_array(self.surface, self.image)

    def run(self):
        while True:
            for i in pygame.event.get():
                if (i.type == pygame.QUIT):
                    exit()
                if (i.type == pygame.KEYUP):
                    exit()
            self.draw_converted_image()
            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.flip()
            self.clock.tick()


if __name__ == '__main__':
    app = ArtConverter()
    app.run()
