from Models.ColorMatcher import ColorMatcher
from Models.PixelArtConverter import PixelArtConverter

import argparse
import os

def output_file(output:str, image:str) -> str:
    """
    Generate an output filename that avoids overwriting existing files by appending a number.

    Args:
        output (str): The desired output file name.
        image (str): The original image file name.

    Returns:
        str: The final output file name that doesn't overwrite any existing files.
    """
    # Si no se proporciona una opción de salida, usa el nombre de la imagen
    if not output:
        output = image

    # Divide el nombre del archivo y su extensión
    base_name, extension = os.path.splitext(output)

    # Inicializa un contador para crear nombres únicos
    counter = 1

    # Mientras el archivo exista, agrega un número al final
    while os.path.exists(output):
        # Genera un nuevo nombre con el contador
        output = f"{base_name} ({counter}){extension}"
        counter += 1

    return output


def list_palettes(directory:str) -> None:
    """List all available palettes grouped by the number of colors."""
    try:
        # Recorrer recursivamente todas las subcarpetas dentro del directorio
        for root, _, files in os.walk(directory):
            if files:
                # Obtener el nombre de la subcarpeta actual (número de colores)
                color_count = os.path.basename(root)
                print(f"\nPalettes with {color_count} colors:")

                # Listar los archivos de imagen dentro de esta subcarpeta
                for file in files:
                    if file.endswith(('.png', '.jpg', '.jpeg')):
                        print(f"  - {directory}/{color_count}/{file}")
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
    except Exception as e:
        print(f"An error occurred while listing palettes: {e}")


def process_image(args):
    try:
        image_path = args.image
        palette_path = args.palette
        pixel_size = args.size
        options = {
            'brightness': args.brightness,
            'contrast': args.contrast,
            'desaturate': args.desaturate,
            'dithering': args.dithering
        }
        output = output_file(args.output, args.image)

        converter = PixelArtConverter(ColorMatcher())
        pixel_art_image = converter.convert_to_pixel_art(image_path, palette_path, pixel_size, options)
        pixel_art_image.save(output)
    except ValueError as e:
        print(e)


def main():
    # Crear el analizador de argumentos
    parser = argparse.ArgumentParser(description='Convert an image to pixel art using a specified color palette.')

    # Agregar un argumento posicional para la imagen
    parser.add_argument('image', nargs='?', help='Path to the input image.')

    # Añadir argumentos
    parser.add_argument('-p', '--palette', type=str, default='Palette/64/aap-64.png', help='Path to the palette image (default: Palette/64/aap-64.png).')
    parser.add_argument('-s', '--size', type=int, default=10, help='Pixel size for the output image (default: 10).')
    parser.add_argument('-b', '--brightness', type=float, default=1.0, help='Brightness factor (default: 1.0).')
    parser.add_argument('-c', '--contrast', type=float, default=1.0, help='Contrast factor (default: 1.0).')
    parser.add_argument('-o', '--output', type=str, default='', help='Path to save the output pixel art image.')
    parser.add_argument('--desaturate', type=bool, default=False, help='Desaturate the image after process.')
    parser.add_argument('--dithering', type=bool, default=False, help='Apply Floyd-Steinberg dithering to the image after process.')

    # Agregar el argumento para listar las paletas disponibles
    parser.add_argument("--list-palettes", action="store_true", help="List available palettes.")

    # Parsear los argumentos
    args = parser.parse_args()

    # Si se pasa --list-palettes, listar las paletas y salir
    if args.list_palettes:
        palettes_directory = "./Palette"  # Cambia esto al directorio donde guardas tus paletas
        list_palettes(palettes_directory)
        return

    # Verifica si la imagen fue proporcionada
    if not args.image:
        parser.error("The following argument is required: image")

    process_image(args)


if __name__ == '__main__':
    main()