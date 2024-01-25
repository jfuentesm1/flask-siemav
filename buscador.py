import pandas as pd
from datetime import datetime

def identificador(ip):
    #la ip llamada super_usuario tiene acceso a la lectura general
    lista_usuarios = {
        'JORGE FUENTES': '192.168.100.77',
        'super_usuario': '192.168.100.78'
        }
    
    for usuario, identificador in lista_usuarios.items():
        if ip == identificador:
            return usuario 
    return False

def listado_componetes(reparacion):
    lista_usuarios = {
        'Q11 AMA': 'c1818',
        'diodos': 'c1919',
        'reguladores':'c1212'
        }
    
    for usuario, identificador in lista_usuarios.items():
        if reparacion == usuario:
            return identificador
    return False

excel_registro = r'/home/pi/FlaskApp/inventario reparaciones/registro.xlsx'
excel_componentes = r'/home/pi/FlaskApp/inventario reparaciones/componetes usados.xlsx'

def escritura_excel(sector:str, clase:str ,recibidas:int, reparadas:int, descartadas:int, componetes,cantidad_componentes:int, usuario, direccion):

    fecha = datetime.now().strftime("%Y-%m-%d")

    try:
        df = pd.read_excel(direccion)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['fecha','camaronera','clase','recibidas','reparadas','descartadas','responsable'])

    if direccion == excel_registro:   
        nueva_fila = {'fecha' :fecha, 'camaronera': sector, 'clase':clase, 'recibidas': recibidas, 'reparadas': reparadas, 'descartadas':descartadas,'responsable': usuario}
        df = df.append(nueva_fila, ignore_index=True)

    elif direccion == excel_componentes:
        componente_necesario = listado_componetes(componetes)
        nueva_fila = {'fecha': fecha,'componentes':componente_necesario,'cantidad':int(cantidad_componentes), 'responsable': usuario}
        df = df.append(nueva_fila, ignore_index=True)

    df.to_excel(direccion, index=False)
    #print(df)
    return df

def filtrar_registros(año,mes,dia):

    fecha = f'{año}-{mes:02d}-{dia:02d}'

    try:
        df1 = pd.read_excel(excel_registro)
        df1 = df1[df1['fecha'] == fecha]
    except KeyError:
        df1 = pd.DataFrame()

    try:
        df2 = pd.read_excel(excel_componentes)
        df2 = df2[df2['fecha'] == fecha]
    except KeyError:
        df2 = pd.DataFrame()

    return df1, df2

