import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import shutil

# Configuración
carpeta_imagenes_preliminares = "preliminary_downloaded_images"
carpeta_imagenes_procesadas = "processed_downloaded_images"
color_reemplazo = (64, 64, 64, 255)  # Color de cubetazo en RGBA
color_borde = (0, 0, 0, 255)  # Color del borde que rodea al área a pintar
tolerancia_color = 151  # Tolerancia para considerar colores similares # Mayor a 151 el verde ya no se puede colorear

# Crear carpeta para imágenes procesadas si no existe
if not os.path.exists(carpeta_imagenes_procesadas):
    os.makedirs(carpeta_imagenes_procesadas)

def colores_similares(color1, color2, tolerancia):
    """Determina si dos colores son similares dentro de una tolerancia dada."""
    r1, g1, b1, a1 = color1
    r2, g2, b2, a2 = color2
    return (abs(r1 - r2) <= tolerancia and
            abs(g1 - g2) <= tolerancia and
            abs(b1 - b2) <= tolerancia and
            abs(a1 - a2) <= tolerancia)

def flood_fill(image, x, y, target_color, replacement_color, boundary_color, tolerancia):
    """Relleno por inundación mejorado con manejo de colores similares."""
    pixels = image.load()
    width, height = image.size

    if colores_similares(target_color, replacement_color, tolerancia) or colores_similares(target_color, boundary_color, tolerancia):
        return

    pixel_queue = [(x, y)]
    while pixel_queue:
        x, y = pixel_queue.pop(0)
        current_color = pixels[x, y]

        if colores_similares(current_color, target_color, tolerancia):
            pixels[x, y] = replacement_color
            if x > 0: pixel_queue.append((x - 1, y))
            if x < width - 1: pixel_queue.append((x + 1, y))
            if y > 0: pixel_queue.append((x, y - 1))
            if y < height - 1: pixel_queue.append((x, y + 1))

def seleccionar_punto(imagen, image_path, new_image_path):
    """Función para mostrar la imagen y seleccionar múltiples puntos con clics."""
    def onclick(event):
        if event.xdata is not None and event.ydata is not None:
            x, y = int(event.xdata), int(event.ydata)
            print(f"Aplicando cubetazo en coordenadas: ({x}, {y})")
            target_color = imagen.getpixel((x, y))
            flood_fill(imagen, x, y, target_color, color_reemplazo, color_borde, tolerancia_color)

            # Volvemos a mostrar la imagen editada para ver los cambios
            ax.imshow(np.array(imagen))
            fig.canvas.draw()

    imagen_array = np.array(imagen)
    
    # Mostramos la imagen y registramos los clics
    fig, ax = plt.subplots()
    ax.imshow(imagen_array)

    # Mostrar el nombre de la imagen en el título
    plt.title(f"Editando imagen: {os.path.basename(image_path)}")
    
    # Registrar clics para múltiples cubetazos
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    # Mantener ventana abierta para múltiples clics
    plt.show()

    # Guardar la imagen procesada
    imagen.save(new_image_path)
    print(f"Imagen guardada: {new_image_path}")

def procesar_imagenes():
    """Función para buscar y procesar las imágenes que cumplen con los criterios."""
    for archivo in os.listdir(carpeta_imagenes_preliminares):
        image_path = os.path.join(carpeta_imagenes_preliminares, archivo)
        new_image_path = os.path.join(carpeta_imagenes_procesadas, archivo)

        if any(keyword in archivo for keyword in ["AF2L", "UF2L"]) and \
           any(side in archivo for side in ["Back Left", "Back Right"]):
            imagen = Image.open(image_path).convert("RGBA")
            print(f"Abriendo imagen: {image_path}")
            seleccionar_punto(imagen, image_path, new_image_path)
        else:
            # Copiar las imágenes que no cumplen con los criterios
            shutil.copy2(image_path, new_image_path)
            print(f"Imagen no procesada copiada: {new_image_path}")

    print("Imagenes procesadas :)")


def editar_imagen_manual():
    """Permite al usuario buscar una imagen en la carpeta de procesadas para editar manualmente."""
    while True:
        buscar_imagen = input("Ingresa el nombre de la imagen a editar (o escribe 'salir' para finalizar), no olvides la extension: ")
        if buscar_imagen.lower() == 'salir':
            break

        # Verificar si la imagen existe en la carpeta de procesadas
        image_path = os.path.join(carpeta_imagenes_procesadas, buscar_imagen)
        if os.path.exists(image_path):
            imagen = Image.open(image_path).convert("RGBA")
            print(f"Abriendo imagen: {image_path}")
            seleccionar_punto(imagen, image_path, image_path)  # Reutilizar la misma función de edición
        else:
            print(f"La imagen '{buscar_imagen}' no se encontró en la carpeta de imágenes procesadas.")

# Agregamos la llamada a la nueva función al final del proceso
procesar_imagenes()
editar_imagen_manual()


