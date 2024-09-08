# Proyecto F2L

## Descripción

Este proyecto está diseñado para procesar imágenes relacionadas con el método F2L (First Two Layers) del cubo Rubik y generar un documento PDF con las imágenes y detalles relevantes. El proceso incluye:

1. **Descarga de Imágenes**: Descarga imágenes desde enlaces generados a partir de un archivo CSV, llamado `DataBase.csv`.
2. **Procesamiento de Imágenes**: Aplica un filtro de relleno a las imágenes para resaltar áreas específicas.
3. **Generación de PDF**: Crea un documento PDF que incluye las imágenes procesadas, los algoritmos provenientes de un archivo CSV llamado `DataBase.csv`, con un formato estético y organizado.

## Estructura del Proyecto

El proyecto consta de tres scripts principales:

1. **Descargar Imágenes** (`download_images.py`): Este script descarga imágenes desde enlaces especificados en un archivo CSV y las guarda en una carpeta local.

2. **Procesar Imágenes** (`process_images.py`): Abre las imágenes descargadas, aplica un filtro de relleno y guarda las imágenes procesadas en una carpeta específica.

3. **Generar PDF** (`generate_pdf.py`): Lee un archivo CSV con información sobre las imágenes y genera un documento PDF que incluye las imágenes procesadas y detalles adicionales.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - `Pillow`
  - `matplotlib`
  - `numpy`
  - `reportlab`
  - `shutil`

## Instrucciones de Uso

1. **Preparar Imágenes**:
   - Asegúrate de tener las imágenes en la carpeta `preliminary_downloaded_images`.
   - El archivo CSV de entrada debe estar en el formato esperado por el script `process_images.py`.

2. **Ejecutar Scripts**:
   - **Descargar Imágenes**: Ejecuta `download_images.py` para descargar las imágenes necesarias.
   - **Procesar Imágenes**: Ejecuta `process_images.py` para procesar las imágenes descargadas.
   - **Generar PDF**: Ejecuta `generate_pdf.py` para generar el documento PDF final.

   ```bash
   python download_images.py
   python process_images.py
   python generate_pdf.py

## Resultados:

1. Las imágenes procesadas se guardarán en la carpeta `processed_downloaded_images`.

2. El documento PDF generado se guardará como `F2L_cases.pdf`.

