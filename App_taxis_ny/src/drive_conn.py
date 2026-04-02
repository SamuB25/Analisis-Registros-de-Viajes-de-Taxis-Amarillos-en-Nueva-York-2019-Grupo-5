import os #Para agilizar el manejo de permisos y gestión de archivos/carpetas.
import gdown #Esto nos permitira descargar los archivos (parquet) de google drive.
import sys #para interactuar directamente con python y cerrar directamente procesos si es necesario.

def ob_datos_ny(file_id,nombre_archivo):
    #   Le otorgamos una especificación para buscar el archivo principalmente 
    # por la id que maneje dentro de drive la cual ira acompañada del nombre del arcchivo.

    #   Dado que ya creamos la carpeta llamada "data" la cual se encuentra dentro esta misma carpeta 
    # de la App nuestra prioridad es denominarla como nuestro directorio local a donde poder dirigir 
    # nuestros archivos parquet.

    directorio = "data"
    if not os.path.exists(directorio):
        os.makedirs(directorio)
        print(f"carpeta {directorio} creada con éxito")

        # Nos aseguramos de que en dado caso no exista la carpeta de data se cree para seguir sin problemas.

    ruta_completa = os.path.join(directorio, nombre_archivo)

    if os.path.exists(ruta_completa):
        print("el archivo ya se encuentra en la carpeta ´data´ local")
        return
            #  En este caso nos interesa ahorrar tiempo, si el archivo parquet ya se obtuvo por otros metodos nos
            # interesa que nuestra función pueda identificar ese archivo "x" y pasar directamente a aquellos que falten.

    url_final = f"https://drive.google.com/uc?id={file_id}"
            # Definimos la url_final con un f-string para así tener un codigo algo mas dinamico dado que 
            # son 6 archivos parquet dentro del drive y se debe ir adaptando a cada uno.

    try:
        gdown.download(url_final,ruta_completa, quiet=False)
                # quiet=false da permiso a gdown para activar la interfaz visual de descarga y así vizualizar la misma.

        if os.path.exists(ruta_completa):
            print(f"Se ha descargado exitosamente el archivo {nombre_archivo}")
    except Exception as e:
        print(f"no se pudo procesar el file_id {file_id}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Creamos un diccionario que contenga la (file_id, nombre del archivo) 
    print("__________ESTA VIVO___________")
    ar_parquets = {
        "1ASTSUYx9vd-3kkJwe9_v232iTseohzBR":"finanzas_viaje.parquet",
        "1RcW1H45PXIGl0OZjxMzfRJhBaBHo0cmg":"localizacion_viaje.parquet",
        "1uE8gNCKrOow_EX8HWzZKNto46OuDfi3F":"metodo_pago.parquet",
        "1u4F9VX9l-imFVndVCSxfWNDboq57nmRO":"plataformas_tpep.parquet",
        "1Q--m9CqqwTSlZQSQci-07uR5h4LVdeht":"registro_viaje.parquet",
        "1tYjnXuHOE08je0xxiLl8RHVGMetr7Fr9":"tarifas.parquet"
    }

    for f_id, nombre in ar_parquets.items():
        ob_datos_ny(f_id,nombre)