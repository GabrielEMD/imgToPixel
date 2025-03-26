from sklearn.cluster import KMeans
import numpy as np
from PIL import Image

class QuantizationMethod:
    """Class for different color quantization methods."""

    @staticmethod
    def apply_kmeans(image: np.ndarray, num_colors: int) -> np.ndarray:
        """
        Apply K-Means clustering for color quantization.

        Args:
            image (np.ndarray): Input image as a NumPy array.
            num_colors (int): Number of colors to reduce the image to.

        Returns:
            np.ndarray: Image with reduced color palette.
        """
        pixels = image.reshape(-1, 3)  # Flatten the image into a list of pixels
        kmeans = KMeans(n_clusters=num_colors, n_init=10)
        labels = kmeans.fit_predict(pixels)
        quantized_image = kmeans.cluster_centers_[labels].reshape(image.shape).astype(np.uint8)
        return quantized_image


    @staticmethod
    def apply_median_cut(image: Image, num_colors: int) -> Image:
        """
        Apply Median Cut algorithm for color quantization.

        Args:
            image (Image): Input image.

        Returns:
            Image: Quantized image with reduced color palette.
        """
        return image.convert('P', palette=Image.ADAPTIVE, colors=num_colors).convert("RGB")
