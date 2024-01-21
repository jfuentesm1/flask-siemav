import pandas as pd
import openpyxl
from datetime import datetime

def identificador(ip):
    lista_usuarios = {
        'jorge': '192.168.100.77',
        'frank': '192.168.100.78'
    }
    for usuario, identificador in lista_usuarios.items():
        if ip == identificador:
            return usuario
    return False

def escritura(numero: int, usuario: str, sheet_name: str):
    fecha = datetime.now().strftime("%Y-%m-%d")
    direccion = r'/home/pi/FlaskApp/registro.xlsx'

    # Intenta leer el archivo Excel; si no existe, se creará
    try:
        df = pd.read_excel(direccion, sheet_name=sheet_name, index_col='reparaciones')
    except FileNotFoundError:
        df = pd.DataFrame()

    # Actualiza o agrega datos en la hoja especificada
    df.at[usuario, fecha] = numero

    # Escribe en la hoja específica del archivo Excel
    with pd.ExcelWriter(direccion, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index_label='reparaciones')

    return f'{fecha}\tSe ha guardado correctamente {numero} tarjetas en la hoja {sheet_name}.'

# Ejemplo de uso
numero_tarjetas = 5
nombre_usuario = 'jorge'
nombre_hoja = 'Sheet1'

resultado = escritura(numero_tarjetas, nombre_usuario, nombre_hoja)
print(resultado)
