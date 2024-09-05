import subprocess
import csv
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os

# Registrar la fuente Montserrat y Montserrat-Medium
pdfmetrics.registerFont(TTFont('Montserrat', 'Montserrat-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Montserrat-Medium', 'Montserrat-Medium.ttf'))

# Crear un documento PDF
pdf_file = "F2L_casos.pdf"
document = SimpleDocTemplate(
    pdf_file, 
    pagesize=letter,
    rightMargin=85.05,  # Ajustar el margen derecho (en puntos, 1 inch = 72 puntos)
    leftMargin=85.05,   # Ajustar el margen izquierdo
    topMargin=70.875,    # Ajustar el margen superior
    bottomMargin=70.875  # Ajustar el margen inferior
)
width, height = letter  # Obtener las dimensiones de la página

# Definir estilos
styles = getSampleStyleSheet()

title_style = ParagraphStyle(name='Title', fontName='Montserrat-Medium', fontSize=20, alignment=1, spaceAfter=12)
subtitle_style = ParagraphStyle(name='Heading2', fontName='Montserrat-Medium', fontSize=16, alignment=1, spaceAfter=12)
subsub_style = ParagraphStyle(name='Heading3', fontName='Montserrat-Medium', fontSize=14, spaceAfter=12)
subsubsub_style = ParagraphStyle(name='Heading4', fontName='Montserrat-Medium', fontSize=12, spaceAfter=12)
author_style = ParagraphStyle(name='CenteredText', fontName='Montserrat', fontSize=10, alignment=1)
text_style = ParagraphStyle(name='CenteredText', fontName='Montserrat', fontSize=12, leading=16)
text_medium_style = ParagraphStyle(name='CenteredText', fontName='Montserrat-Medium', fontSize=12, leading=12)

# Función para crear una tabla de 2x1
def create_2x1_table(image_path, name_lines, text_lines):
    # Crear el párrafo para el nombre
    name_paragraph = Paragraph('<font name="Montserrat-Medium" size="12">{}</font>'.format('<br/>'.join(name_lines)), text_medium_style)
    
    # Crear una lista de párrafos para las líneas de texto
    text_paragraphs = [Paragraph('<font name="Montserrat" size="12">{}</font>'.format(line), text_style) for line in text_lines]
    
    # Combinar los párrafos del nombre, un Spacer, y las líneas de texto
    content = [name_paragraph, Spacer(1, 6)] + text_paragraphs  # Agregar un Spacer después del nombre
    
    data = [
        [Image(image_path, width=0.984*inch, height=0.984*inch),
         content]  # Insertar el contenido con Spacer en la tabla
    ]
    
    table = Table(data, colWidths=[1.37*inch, width - 1.37*inch - 2.5422*inch])  # Ajustar el ancho de la tabla
    table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    
    return table

# Leer el archivo CSV y generar tablas
content = []

# Título
title = Paragraph("F2L", title_style)
content.append(title)

# Nombre
author = Paragraph("RedCyclone05", author_style)
content.append(author)

# Saltar un espacio pequeño
content.append(Spacer(1, 12))

# Variables para almacenar el último subtema, subsubtema y subsubsubtema
last_subtema = ""
last_subsubtema = ""
last_subsubsubtema = ""


# Leer el archivo CSV
csv_file = 'DataBase.csv'
with open(csv_file, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Omitir la primera fila (encabezados)
    
    for row in reader:
        if row:
            subtema = row[0]
            subsubtema = row[1]
            subsubsubtema = row[2]
            image_filename = row[3]  # La cuarta columna contiene el nombre de la imagen
            name_lines = row[4:5]  # La quinta columna tiene el nombre
            text_lines = row[5:]  # Las celdas restantes se consideran líneas de texto

            # Construir la ruta completa de la imagen
            image_path = os.path.abspath(os.path.join('processed_downloaded_images', image_filename))
            # Depuración de la ruta de la imagen
            print(f"Buscando la imagen en: {image_path}")

            
            # Solo agregar un nuevo subtema si es diferente al último visto
            if subtema != last_subtema:
                content.append(Paragraph(subtema, subtitle_style))
                last_subtema = subtema
            
            # Solo agregar un nuevo subsubtema si es diferente al último visto
            if subsubtema != last_subsubtema:
                content.append(Paragraph(subsubtema, subsub_style))
                last_subsubtema = subsubtema
            
            # Solo agregar un nuevo subsubsubtema si es diferente al último visto
            if subsubsubtema != last_subsubsubtema:
                content.append(Paragraph(subsubsubtema, subsubsub_style))
                last_subsubsubtema = subsubsubtema

            # Crear y agregar la tabla de 2x1 para cada fila del CSV
            table = create_2x1_table(image_path, name_lines, text_lines)
            content.append(table)

            # Saltar un espacio pequeño
            content.append(Spacer(1, 12))

# Agregar sección de Referencias
content.append(Paragraph("Referencias", subtitle_style))

# Lista de referencias con solo el link cliqueable, en azul y subrayado
referencias = [
    'VisualCube: Generate custom Rubik\'s cube visualisations from your browser address bar: <a href="https://cube.rider.biz/visualcube.php" color="blue"><u>https://cube.rider.biz/visualcube.php</u></a>',
    'VisualCube: Cube image in each basic algorithm: <a href="https://cube.rider.biz/visualcube.php?fmt=png&size=500&stage=f2l&r=y30x-30z0&bg=t&case=U" color="blue"><u>https://cube.rider.biz/visualcube.php?fmt=png&size=500&stage=f2l&r=y30x-30z0&bg=t&case=U</u></a>',
    'VisualCube: Cube image in each advanced algorithm: <a href="https://cube.rider.biz/visualcube.php?fmt=png&size=500&stage=f2l_2&r=y30x-30z0&bg=t&case=U" color="blue"><u>https://cube.rider.biz/visualcube.php?fmt=png&size=500&stage=f2l_2&r=y30x-30z0&bg=t&case=U</u></a>',
    'SpeedCubeDB: F2L Algorithms: <a href="https://speedcubedb.com/a/3x3/F2L" color="blue"><u>https://speedcubedb.com/a/3x3/F2L</u></a>',
    'SpeedCubeDB: F2L Advanced Algorithms: <a href="https://speedcubedb.com/a/3x3/AdvancedF2L" color="blue"><u>https://speedcubedb.com/a/3x3/AdvancedF2L</u></a>',
    'CubeSkills: F2L Useful Cases: <a href="https://www.cubeskills.com/tutorials/useful-f2l-algorithms" color="blue"><u>https://www.cubeskills.com/tutorials/useful-f2l-algorithms</u></a>',
    'Eddievak: Rubik\'s Cube: Pro Fingertricks: <a href="https://www.youtube.com/watch?v=5uqpcifk5ro" color="blue"><u>https://www.youtube.com/watch?v=5uqpcifk5ro</u></a>',
    'EddieVak: Example solve, using Keyhole: <a href="https://www.youtube.com/shorts/d7co6HdEbf4" color="blue"><u>https://www.youtube.com/shorts/d7co6HdEbf4</u></a>',
    'Eddievak: F2L Advanced Cases: <a href="https://www.youtube.com/shorts/VgaYZEh3LZE" color="blue"><u>https://www.youtube.com/shorts/VgaYZEh3LZE</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/pcWonR6TRsU" color="blue"><u>https://www.youtube.com/shorts/pcWonR6TRsU</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/B_qMmK77vuM" color="blue"><u>https://www.youtube.com/shorts/B_qMmK77vuM</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/NpC1Is_0gKQ" color="blue"><u>https://www.youtube.com/shorts/NpC1Is_0gKQ</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/vBEG0WnALz4" color="blue"><u>https://www.youtube.com/shorts/vBEG0WnALz4</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/gWuaVQY4oVw" color="blue"><u>https://www.youtube.com/shorts/gWuaVQY4oVw</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/5fb6GV9CDAA" color="blue"><u>https://www.youtube.com/shorts/5fb6GV9CDAA</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/YHASEHHPoOE" color="blue"><u>https://www.youtube.com/shorts/YHASEHHPoOE</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/aZPmz5SNE_E" color="blue"><u>https://www.youtube.com/shorts/aZPmz5SNE_E</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/VAHjYclnUfo" color="blue"><u>https://www.youtube.com/shorts/VAHjYclnUfo</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/tatbSlNBAuw" color="blue"><u>https://www.youtube.com/shorts/tatbSlNBAuw</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/pKBFk0Tuqrc" color="blue"><u>https://www.youtube.com/shorts/pKBFk0Tuqrc</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/W0Af7wzzyas" color="blue"><u>https://www.youtube.com/shorts/W0Af7wzzyas</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/3PvyLNVwEf4" color="blue"><u>https://www.youtube.com/shorts/3PvyLNVwEf4</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/_WOC0ZCxKEs" color="blue"><u>https://www.youtube.com/shorts/_WOC0ZCxKEs</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/X_PYfqJNFIc" color="blue"><u>https://www.youtube.com/shorts/X_PYfqJNFIc</u></a>',
    'Eddievak: <a href="https://www.youtube.com/shorts/DF_o8ejApAw" color="blue"><u>https://www.youtube.com/shorts/DF_o8ejApAw</u></a>',
    'GitHub: Repositorio con el que se crearon las imagenes y este Documento: <a href="https://github.com/RedCyclone05/F2L" color="blue"><u>https://github.com/RedCyclone05/F2L</u></a>'
]

# Agregar cada referencia como un bullet con enlace cliqueable
for referencia in referencias:
    bullet = Paragraph(f"• {referencia}", text_style)
    content.append(bullet)

# Saltar un espacio pequeño
content.append(Spacer(1, 12))

# Construir el PDF
document.build(content)

# Abrir el PDF
if subprocess.run(['start', pdf_file], shell=True).returncode != 0:
    print(f"No se pudo abrir el PDF '{pdf_file}'.")
else:
    print(f"PDF '{pdf_file}' creado y abierto con éxito.")
