import pandas as pd
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

def listado_componetes(reparacion):
    lista_usuarios = {
        'mosfet': 'c1818',
        'diodos': 'c1919',
        'reguladores':'c1212'
        }
    
    for usuario, identificador in lista_usuarios.items():
        if reparacion == usuario:
            return identificador
    return False


def escritura_excel(numeroASP, numeroAMA, componetes,cantidad_componentes, usuario, direccion):

    fecha = datetime.now().strftime("%Y-%m-%d")
    try:
        df = pd.read_excel(direccion)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['reparaciones asp', 'reparaciones ama', 'fecha', 'usuario'])

    if direccion == r'/home/pi/FlaskApp/inventario reparaciones/registro.xlsx':   
        nueva_fila = {'reparaciones asp': numeroASP, 'reparaciones ama': numeroAMA, 'fecha': fecha, 'usuario': usuario}
        df = df.append(nueva_fila, ignore_index=True)

    elif direccion == r'/home/pi/FlaskApp/inventario reparaciones/componetes usados.xlsx':
        componente_necesario = listado_componetes(componetes)
        nueva_fila = {'componentes':componente_necesario,'cantidad':cantidad_componentes, 'fecha': fecha, 'usuario': usuario}
        df = df.append(nueva_fila, ignore_index=True)

    df.to_excel(direccion, index=False)
    print(df)
    return f'{fecha}\tse han guardado correctamente'

