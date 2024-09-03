import csv
import requests
import os

# Ruta del archivo CSV
csv_file_path = 'DataBase.csv'

# Enlace base
base_url = "https://cube.rider.biz/visualcube.php?fmt=png&size=500&bg=t"

# Crear un directorio para guardar las imágenes si no existe
output_dir = 'imagenes_descargadas'
os.makedirs(output_dir, exist_ok=True)

# Diccionario para las variaciones de 'stage'
stage_variaciones = {
    "(BR Slot)": "f2l_2",
    "(FR Slot)": "f2l_3",
    "(FL Slot)": "f2l_1",
    "(BL Slot)": "f2l_2"
}

orientation_variaciones = {
    "Front Right": "y30x-30z0",
    "Front Left": "y-30x-30z0",
    "Back Left": "y-30x-30z0",
    "Back Right": "y30x-30z0"
}

# Abrir el archivo CSV y leer los datos
with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    
    # Omitir la primera fila (encabezado)
    next(reader)
    
    # Iterar sobre las filas del archivo CSV
    for row in reader:
        if len(row) >= 8:  # Verificar que al menos haya 8 columnas
            # Obtener los valores de las columnas necesarias
            columna_6_valor = row[5]  # algoritmo
            columna_5_nombre = row[4]  # Nombre
            columna_2_texto = row[1]  # Slot
            columna_1_condicion = row[0]  # Condición de Algoritmo (Basic, Advanced, etc.)
            columna_9_slot = row[8]  # Slot específico para variaciones
            
            # Modificar el valor según la primera condición del cubo
            if columna_1_condicion == "Basic Algorithm":
                # Mantener el stage como f2l para el algoritmo básico
                stage = "f2l"
            elif columna_1_condicion in ["Advanced Algorithms", "Advanced F2L", "Multislotting", "Pseudoslotting", "Useful Cases"]:
                # Revisar la columna 8 para cambiar el stage
                stage = stage_variaciones.get(columna_9_slot, "f2l")  # Si no está en el diccionario, usar f2l por defecto
            else:
                # Si no coincide con ninguna de las condiciones, usar f2l como predeterminado
                stage = "f2l"
            
            # Modificar la orientación de la imagen
            if columna_2_texto in ["Front Right", "Front Left", "Back Left", "Back Right"]:
                # Girar para que se vea bien el caso
                orientation = orientation_variaciones.get(columna_2_texto, "y30x-30z0")  # Valor por defecto
            else:
                orientation = "y30x-30z0"  # Valor por defecto si la columna 2 no contiene ninguna de las opciones

            # Verificar si la columna 6 contiene "Main Algorithm" o "It's ready"
            if "Main Algorithm" in columna_6_valor:
                columna_6_valor = "M2 E2 S2"  # Modificar el algoritmo a "U"
                stage = ""
            if "It's ready" in columna_6_valor:
                columna_6_valor = "U"  # Modificar el algoritmo a "U"
            
            # Modificar columna_6_valor si empieza con y o y'
            if columna_6_valor.startswith("y'"):
                columna_6_valor += " y"
            elif columna_6_valor.startswith("y"):
                columna_6_valor += " y'"
            elif columna_6_valor.startswith("y2"):
                columna_6_valor += " y2"

            # Modificar columna_6_valor si empieza con d o d'
            if columna_6_valor.startswith("d'"):
                columna_6_valor += " d"
            elif columna_6_valor.startswith("d"):
                columna_6_valor += " d'"
            elif columna_6_valor.startswith("d2"):
                columna_6_valor += " d2"
            
            # Generar el enlace con la variación de stage
            enlace = f"{base_url}&r={orientation}&stage={stage}&case={columna_6_valor}"
            
            # Depuración: imprimir el enlace generado
            print(f"Enlace generado: {enlace}")
            
            # Descargar la imagen
            response = requests.get(enlace)
            
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                # Definir la ruta del archivo
                archivo_nombre = f"{columna_5_nombre}_{columna_2_texto}.png"
                archivo_ruta = os.path.join(output_dir, archivo_nombre)
                
                # Guardar la imagen en el archivo
                with open(archivo_ruta, 'wb') as f:
                    f.write(response.content)
                
                print(f"Imagen descargada y guardada como {archivo_nombre}")
            else:
                print(f"Error al descargar la imagen desde {enlace} (Código de estado: {response.status_code})")
        else:
            print("Fila con menos de 8 columnas encontrada.")

print("Fin del Codigo")
