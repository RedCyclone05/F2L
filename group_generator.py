import pandas as pd
import os
import shutil

# Leer el archivo CSV
input_file = 'DataBase.csv'
df = pd.read_csv(input_file)

# Crear una carpeta para los nuevos archivos CSV
output_dir = 'Divided_CSV'
os.makedirs(output_dir, exist_ok=True)

# Obtener la primera columna (grupos) y eliminar duplicados
groups = df.iloc[:, 0].unique()

# Dividir el CSV en archivos por grupo
for group in groups:
    # Filtrar los datos del grupo
    group_df = df[df.iloc[:, 0] == group]
    
    # Guardar el archivo CSV para el grupo
    output_file = os.path.join(output_dir, f'{group}.csv')
    group_df.to_csv(output_file, index=False)

print("Archivos CSV divididos y guardados exitosamente.")

# Copiar el archivo DataBase.csv a la carpeta Divided_CSV
shutil.copy(input_file, os.path.join(output_dir, 'DataBase.csv'))

print("Copia de DataBase.csv creada en la carpeta Divided_CSV.")

print("Fin :)")