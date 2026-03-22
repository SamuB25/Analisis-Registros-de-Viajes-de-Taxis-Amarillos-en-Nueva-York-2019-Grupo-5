import sqlite3
import os 

#Importamos las librerias y nombramos cada base por su respectivo mes
base_oct = '2019-10.sqlite'
base_nov = '2019-11.sqlite'
base_dic = '2019-12.sqlite'

def unir_bases_datos():
    connex = None  #Evita errores de variables no definidas si la conexión inicial falla.
    try:
        # 1. Conectamos a la base de octubre para utilizarla como punto 
        # inicial para añadir los meses noviembre y diciembre
        connex = sqlite3.connect(base_oct)
        cursor = connex.cursor()

        # 2. Anexamos las base de noviembre y diciembre.
        # Attach nos permite conectar primero las bases antes de unirlas
        cursor.execute(f"ATTACH '{base_nov}' AS db_nov")
        cursor.execute(f"ATTACH '{base_dic}' AS db_dic")
        
        # 3. Insertamos los datos de Noviembre en la tabla 'tripdata' de Octubre
        cursor.execute("INSERT INTO tripdata SELECT * FROM db_nov.tripdata")
        
        # 4. Insertamos los datos de Diciembre de la misma forma
        cursor.execute("INSERT INTO tripdata SELECT * FROM db_dic.tripdata")
        
        # 5. Nos aseguramos de que los datos insertados se guarden 
        # permanentemente en la base de octubre
        connex.commit()
        
        # 6. Desconectamos las bases adjuntas
        cursor.execute("DETACH DATABASE db_nov")
        cursor.execute("DETACH DATABASE db_dic")
        
    except sqlite3.Error as e: 
        # Si la base de datos falla esta condicion va a imprimir la razon
        print(f"Error: {e}")
    finally:
        if connex:
            connex.close()

# Nos aseguramos de que se ralice la union solo si le damos conformación para realizarla
if __name__ == "__main__":
    unir_bases_datos()