from Models.ColorMatcher import ColorMatcher
from Models.PixelArtConverter import PixelArtConverter

if __name__ == "__main__":
    image_path = 'input_image.ext'
    palette_path = 'Palette/x/palette.png'
    pixel_size = 10

    converter = PixelArtConverter(ColorMatcher())
    pixel_art_image = converter.convert_to_pixel_art(image_path, palette_path, pixel_size)
    pixel_art_image.save('output_image.png')
