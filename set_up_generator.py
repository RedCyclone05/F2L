import pandas as pd

# Leer el archivo CSV sin encabezados
df = pd.read_csv('DataBase.csv', header=None)

# Función para procesar el texto de la columna 6
def process_text(text):
    if text == "Main Algorithm":
        return "Set Up Algorithm"
    
    if text == "It's ready":
        return "It's ready"
    
    # Voltear el texto en orden inverso
    reversed_text = text[::-1]
    
    # Separar los elementos por espacio
    elements = reversed_text.split()
    
    # Procesar cada elemento
    processed_elements = []
    for element in elements:
        if "'" in element:
            # Eliminar apóstrofo si está presente
            processed_elements.append(element.replace("'", ""))
        else:
            # Agregar apóstrofo si no está presente
            processed_elements.append(element + "'")
    
    # Unir los elementos procesados con espacio
    processed_text = ' '.join(processed_elements)
    
    return processed_text

# Procesar cada fila en la columna 6 (índice 5) y escribir en la columna 10 (índice 9)
if len(df.columns) > 5:
    df[9] = df[5].apply(process_text)

    # Asignar "Set Up" al primer elemento de la columna 10
    if not df.empty:
        df.at[0, 9] = "Set Up"

    # Guardar el DataFrame modificado en el archivo CSV
    df.to_csv('DataBase.csv', index=False, header=False)

    print("Proceso completado. El archivo CSV ha sido actualizado.")
else:
    print("El archivo CSV no tiene suficientes columnas.")
