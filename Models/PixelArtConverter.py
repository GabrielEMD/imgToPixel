
from PIL import Image
from multiprocessing import Pool, cpu_count
import numpy as np

from Models.PaletteLoader import PaletteLoader
from Models.ColorMatcher import ColorMatcher
from Models.ImageProcessor import ImageProcessor

class PixelArtConverter:
    """Class to convert images to pixel art using a specified color palette."""

    def __init__(self, color_matcher: ColorMatcher, palette_path: str) -> None:
        """
        Initialize the PixelArtConverter with a color matcher and a palette.

        Args:
            color_matcher (ColorMatcher): An object that has a method find_closest_color.
            alette_path (str): Path to the color palette image.
        """
        self.color_matcher = color_matcher
        self.image_processor = ImageProcessor

        self.palette = PaletteLoader.load_palette(palette_path)
        self.palette_grayscale = self._convert_palette_to_grayscale()
        self.palette_size = self._get_palette_size()


    def convert_to_pixel_art(self, image_path: str, pixel_size: int, options:dict) -> Image:
        """
        Convert an image to pixel art using the specified palette and pixel size.

        Args:
            image_path (str): Path to the input image.
            pixel_size (int): Size of the pixels in the output image.
            options (dict): Image parameters.

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
            if options['grayscale']:
                grayscale_image = image.convert("L")
                grayscale_image = self._resize_image(grayscale_image, pixel_size)
                grayscale_array = np.array(grayscale_image)

            # Resize the image to create a pixelated effect
            resized_image = self._resize_image(image, pixel_size)
            # Convert the image to a NumPy array for pixel manipulation
            image_array = np.array(resized_image)

            options['quantization_method'] = 'kmeans'
            options['quantization_method'] = 'median_cut'
            if 'quantization_method' in options and options['quantization_method']:
                image_array = ColorMatcher.quantize_image(image_array, options['quantization_method'], self.palette_size)

            image_array = self._parallel_color_matching(image_array)

            if options['grayscale']:
                image_array = self._map_to_palette_grayscale(image_array, grayscale_array)

            # Convert the NumPy array back to an Image object
            pixel_art_image = Image.fromarray(image_array.astype('uint8'))
            return pixel_art_image
        except FileNotFoundError:
            raise ValueError(f"No such file or directory: {image_path}")
        except Exception as e:
            raise ValueError(f"An error occurred while converting to pixel art: {e}")


    def _get_palette_size(self) -> int:
        """
        Determine the number of unique colors in the loaded palette.

        Returns:
            int: Number of unique colors in the palette.
        """
        return len(np.unique(self.palette, axis=0))


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


    def _parallel_color_matching(self, image_array: np.ndarray) -> np.ndarray:
        """
        Process pixel color matching in parallel.

        Args:
            image_array (np.ndarray): The input image as a NumPy array.

        Returns:
            np.ndarray: Image with matched colors.
        """
        height, width, _ = image_array.shape
        pixels = image_array.reshape(-1, 3)

        with Pool(cpu_count()) as pool:
            matched_pixels = pool.map(self._match_color_worker, pixels)

        return np.array(matched_pixels, dtype=np.uint8).reshape(height, width, 3)


    def _match_color_worker(self, color):
        """Helper function for multiprocessing color matching."""
        return self.color_matcher.find_closest_color(color, self.palette)


    def _convert_palette_to_grayscale(self) -> np.ndarray:
        """
        Convert the palette to grayscale values.

        Returns:
            np.ndarray: Grayscale values of the palette.
        """
        return np.array([np.dot(color[:3], [0.2989, 0.587, 0.114]) for color in self.palette])


    def _map_to_palette_grayscale(self, image_array: np.ndarray, grayscale_array: np.ndarray) -> np.ndarray:
        """
        Map image grayscale values to the closest grayscale values in the palette.

        Args:
            image_array (np.ndarray): The input image as a NumPy array.
            grayscale_array (np.ndarray): The grayscale representation of the image.

        Returns:
            np.ndarray: Image mapped to the closest grayscale values from the palette.
        """
        mapped_image = np.zeros_like(image_array)
        for y in range(image_array.shape[0]):
            for x in range(image_array.shape[1]):
                grayscale_value = grayscale_array[y, x]
                closest_index = np.argmin(np.abs(self.palette_grayscale - grayscale_value))
                mapped_image[y, x, :3] = self.palette[closest_index]
        return mapped_image
