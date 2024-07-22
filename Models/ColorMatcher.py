import numpy as np
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color

class ColorMatcher:
    """Class to find the closest color in a palette."""

    def __init__(self) -> None:
        """Initialize the ColorMatcher with a cache for color distances."""
        self.color_cache = {}


    @staticmethod
    def lab_distance(color_lab1: float, color_lab2: float) -> float:
        """
        Calculate the Euclidean distance in the LAB color space.

        Args:
            color_lab1 (LabColor): First color in LAB space.
            color_lab2 (LabColor): Second color in LAB space.

        Returns:
            float: Euclidean distance between the two colors.
        """
        return np.sqrt(np.sum((color_lab1 - color_lab2) ** 2))


    def find_closest_color(self, color: tuple[int, int, int], palette: np.ndarray) -> np.ndarray:
        """
        Find the closest color in the palette to the given color.

        Args:
            color (tuple): RGB color to match.
            palette (np.ndarray): Array of RGB colors.

        Returns:
            np.ndarray: Closest RGB color from the palette.
        """
        if tuple(color) in self.color_cache:
            # Return cached result if available
            return self.color_cache[tuple(color)]

        # Convert the input color to LAB color space
        color_lab = convert_color(sRGBColor(*color), LabColor)
        closest_color = None
        min_distance = float('inf')

        for palette_color in palette:
            # Convert the palette color to LAB color space
            palette_color_lab = convert_color(sRGBColor(*palette_color), LabColor)
            # Calculate the distance in LAB space
            distance = (
                self.lab_distance(color_lab.lab_l, palette_color_lab.lab_l) +
                self.lab_distance(color_lab.lab_a, palette_color_lab.lab_a) +
                self.lab_distance(color_lab.lab_b, palette_color_lab.lab_b)
            )

            # Update closest color if a smaller distance is found
            if distance < min_distance:
                min_distance = distance
                closest_color = palette_color

        # Cache the result
        self.color_cache[tuple(color)] = closest_color
        return closest_color
