from PIL import Image
import numpy as np

from Models.PaletteLoader import PaletteLoader
from Models.ColorMatcher import ColorMatcher
from Models.ImageProcessor import ImageProcessor

class PixelArtConverter:
    """Class to convert images to pixel art using a specified color palette."""

    def __init__(self, color_matcher: ColorMatcher) -> None:
        """
        Initialize the PixelArtConverter with a color matcher.

        Args:
            color_matcher (ColorMatcher): An object that has a method find_closest_color.
        """
        self.color_matcher = color_matcher
        self.image_processor = ImageProcessor


    def convert_to_pixel_art(self, image_path: str, palette_path: str, pixel_size: int, options:dict) -> Image:
        """
        Convert an image to pixel art using the specified palette and pixel size.

        Args:
            image_path (str): Path to the input image.
            palette_path (str): Path to the palette image.
            pixel_size (int): Size of the pixels in the output image.

        Returns:
            Image: Pixel art image.

        Raises:
            ValueError: If any error occurs during the conversion process.
        """
        try:
            # Load and convert the input image to RGB
            image = Image.open(image_path).convert("RGB")

            # Apply image preprocessing
            image = self.image_processor.adjust_brightness_contrast(image, options['brightness'], options['contrast'])
            if options['desaturate']:
                image = self.image_processor.desaturate_image(image)
            if options['dithering']:
                image = self.image_processor.apply_dithering(image)

            # Load the palette
            palette = PaletteLoader.load_palette(palette_path)

            # Resize the image to create a pixelated effect
            resized_image = self._resize_image(image, pixel_size)
            # Convert the image to a NumPy array for pixel manipulation
            image_array = np.array(resized_image)

            # Iterate over each pixel to find and assign the closest color from the palette
            for y in range(image_array.shape[0]):
                for x in range(image_array.shape[1]):
                    image_array[y, x, :3] = self.color_matcher.find_closest_color(image_array[y, x, :3], palette)

            # Convert the NumPy array back to an Image object
            pixel_art_image = Image.fromarray(image_array.astype('uint8'))
            return pixel_art_image
        except FileNotFoundError:
            raise ValueError(f"No such file or directory: {image_path}")
        except Exception as e:
            raise ValueError(f"An error occurred while converting to pixel art: {e}")


    def _resize_image(self, image: Image, pixel_size: int) -> Image:
        """
        Resize the image to the specified pixel size.

        Args:
            image (Image): The input image.
            pixel_size (int): Size of the pixels in the output image.

        Returns:
            Image: Resized image.
        """
        # Downscale the image
        image = image.resize((image.width // pixel_size, image.height // pixel_size), Image.NEAREST)
        # Upscale the image to the original size to achieve a pixelated effect
        return image.resize((image.width * pixel_size, image.height * pixel_size), Image.NEAREST)
