# PixelArtConverter

PixelArtConverter es una herramienta para convertir imágenes a arte pixelado utilizando una paleta de colores especificada. El proyecto está diseñado para facilitar la conversión de imágenes a un estilo retro pixel art, ideal para videojuegos o proyectos gráficos.

## Contenidos del Proyecto

- **`main.py`**: El archivo principal para ejecutar la conversión de imágenes. Incluye el manejo de argumentos de línea de comandos y la lógica para procesar las imágenes.
- **`PaletteLoader.py`**: Carga paletas de colores desde imágenes.
- **`PixelArtConverter.py`**: Contiene la lógica para convertir imágenes a pixel art utilizando una paleta de colores.
- **`ImageProcessor.py`**: Proporciona funciones para ajustar el brillo, el contraste, la desaturación y aplicar dithering a las imágenes.
- **`ColorMatcher.py`**: Encuentra el color más cercano en una paleta utilizando el espacio de color LAB.

## Requisitos

- Python 3.x
- Pillow (PIL fork)
- numpy
- colormath

Puedes instalar las dependencias necesarias utilizando `pip`:

```bash
pip install pillow numpy colormath
```

## Uso

Para convertir una imagen a pixel art, usa el archivo `main.py` desde la línea de comandos. Aquí hay algunos ejemplos de cómo usarlo:

### Convertir una imagen a pixel art con una paleta específica

```bash
python main.py path/to/your/image.png -p Palette/64/aap-64.png -s 10 -o path/to/output/image.png
```

### Opciones disponibles

* `-p` o `--palette`: Ruta a la imagen de la paleta de colores (por defecto: `Palette/64/aap-64.png`).
* `-s` o `--size`: Tamaño del pixel para la imagen de salida (por defecto: 10).
* `-b` o `--brightness`: Factor de brillo (por defecto: 1.0).
* `-c` o `--contrast`: Factor de contraste (por defecto: 1.0).
* `-o` o `--output`: Ruta para guardar la imagen de pixel art resultante.
* `--desaturate`: Desaturar la imagen después del procesamiento.
* `--dithering`: Aplicar dithering Floyd-Steinberg a la imagen después del procesamiento.

### Listar paletas disponibles

Para listar todas las paletas disponibles en el directorio, usa el siguiente comando:

```bash
python main.py --list-palettes
```

### Estructura de Archivos

* `Palette/`: Directorio que contiene las imágenes de paletas de colores.
* * `Palette/16/`: Paletas con 16 colores.
* * `Palette/64/`: Paletas con 64 colores.
* * `Palette/4/`: Paletas con 4 colores.
* `Models/`: Directorio que contiene los módulos de procesamiento de imágenes y manejo de paletas.
