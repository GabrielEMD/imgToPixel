from PIL import Image, ImageEnhance

class ImageProcessor:
    """Class to handle image preprocessing tasks like brightness, contrast, desaturation, and dithering."""

    @staticmethod
    def adjust_brightness_contrast(image: Image, brightness_factor: float = 1.0, contrast_factor: float = 1.0) -> Image:
        """
        Adjust the brightness and contrast of an image.

        Args:
            image (Image): The input image to be adjusted.
            brightness_factor (float): Factor by which to adjust the brightness (default is 1.0).
            contrast_factor (float): Factor by which to adjust the contrast (default is 1.0).

        Returns:
            Image: The adjusted image with modified brightness and contrast.
        """
        # Enhance the brightness of the image
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness_factor)

        # Enhance the contrast of the image
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast_factor)

        return image


    @staticmethod
    def apply_dithering(image: Image) -> Image:
        """
        Apply Floyd-Steinberg dithering to the image to reduce color depth.

        Args:
            image (Image): The input image to be dithered.

        Returns:
            Image: The dithered image with reduced color depth.
        """
        # Convert the image to 'P' mode with adaptive palette and apply Floyd-Steinberg dithering
        return image.convert('RGB').convert('P', palette=Image.ADAPTIVE, dither=Image.FLOYDSTEINBERG).convert('RGB')


    @staticmethod
    def desaturate_image(image: Image) -> Image:
        """
        Desaturate the image, converting it to grayscale and then back to RGB.

        Args:
            image (Image): The input image to be desaturated.

        Returns:
            Image: The desaturated image in grayscale, converted back to RGB.
        """
        # Convert the image to grayscale ('L' mode) and then back to RGB
        return image.convert("L").convert("RGB")
