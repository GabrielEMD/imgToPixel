import unittest
import numpy as np
from Models.ColorMatcher import ColorMatcher
from Models.PaletteLoader import PaletteLoader
from Models.PixelArtConverter import PixelArtConverter
from PIL import Image

class TestColorMatcher(unittest.TestCase):

    def test_lab_distance(self):
        # Ejemplo básico de prueba de distancia
        dist = ColorMatcher.lab_distance(0, 0)
        self.assertEqual(dist, 0)


    def test_find_closest_color(self):
        matcher = ColorMatcher()
        color = (255, 0, 0)  # Rojo
        palette = np.array([[0, 0, 255], [255, 0, 0]])  # Azul, Rojo
        closest_color = matcher.find_closest_color(color, palette)
        self.assertTrue(np.array_equal(closest_color, [255, 0, 0]))


class TestPaletteLoader(unittest.TestCase):

    def test_load_palette(self):
        palette_loader = PaletteLoader()
        palette = palette_loader.load_palette('Palette/16/na16.png')
        self.assertIsInstance(palette, np.ndarray)
        self.assertEqual(palette.shape[1], 3)  # Verifica que tenga 3 canales RGB


class TestPixelArtConverter(unittest.TestCase):

    def test_convert_to_pixel_art(self):
        converter = PixelArtConverter(ColorMatcher())
        pixel_art = converter.convert_to_pixel_art('Test/i2.jpeg', 'Palette/16/na16.png', 10)
        self.assertIsInstance(pixel_art, Image.Image)
        self.assertEqual(pixel_art.size, (730, 920))  # Suponiendo una imagen de entrada de 730x920 (como la imagen de entrada)


if __name__ == '__main__':
    unittest.main()
