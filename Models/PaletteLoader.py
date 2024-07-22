from PIL import Image
import numpy as np

class PaletteLoader:
    """Class to load a color palette from an image."""

    @staticmethod
    def load_palette(palette_path: str) -> np.ndarray:
        """
        Load the color palette from an image.

        Args:
            palette_path (str): Path to the palette image.

        Returns:
            np.ndarray: Array of RGB colors.

        Raises:
            ValueError: If the palette format is invalid.
        """
        try:
            # Open the image file
            palette_image = Image.open(palette_path)
            # Convert the image to RGB format
            palette_image = palette_image.convert("RGB")
            # Convert the image to a NumPy array
            palette = np.array(palette_image)

            # Check the shape of the palette array and reshape if necessary
            if len(palette.shape) == 3:
                palette = palette.reshape(-1, 3)
            elif len(palette.shape) == 2:
                if palette.shape[1] != 3:
                    raise ValueError("The palette must have 3 channels (RGB)")
            else:
                raise ValueError("Invalid palette format")

            return palette
        except Exception as e:
            # Raise a ValueError with a descriptive message if any exception occurs
            raise ValueError(f"An error occurred while loading the palette: {e}")
