import pandas as pd
from datetime import datetime

def identificador(ip):
    #la ip llamada super_usuario tiene acceso a la lectura general
    lista_usuarios = {
        'jorge fuentes': '192.168.100.77',
        'super_usuario': '192.168.100.78'
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

def escritura_excel(numeroASP:int, numeroAMA:int, componetes,cantidad_componentes:int, usuario, direccion):

    fecha = datetime.now().strftime("%Y-%m-%d")
    try:
        df = pd.read_excel(direccion)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['reparaciones asp', 'reparaciones ama', 'fecha', 'usuario'])

    if direccion == r'/home/pi/FlaskApp/inventario reparaciones/registro.xlsx':   
        nueva_fila = {'reparaciones asp': int(numeroASP), 'reparaciones ama': int(numeroAMA), 'fecha': fecha, 'usuario': usuario}
        df = df.append(nueva_fila, ignore_index=True)

    elif direccion == r'/home/pi/FlaskApp/inventario reparaciones/componetes usados.xlsx':
        componente_necesario = listado_componetes(componetes)
        nueva_fila = {'componentes':componente_necesario,'cantidad':int(cantidad_componentes), 'fecha': fecha, 'usuario': usuario}
        df = df.append(nueva_fila, ignore_index=True)

    df.to_excel(direccion, index=False)
    print(df)
    return df

def filtrar_registros(año,mes,dia):
   fecha = f'{año}-{mes:02d}-{dia:02d}'

   df1 = pd.read_excel(r"/home/pi/FlaskApp/inventario reparaciones/registro.xlsx")
   
   df2 = pd.read_excel(r"/home/pi/FlaskApp/inventario reparaciones/componetes usados.xlsx")
   if 'fecha' not in df1.columns:# or 'fecha' not in df2.columns:
       data_registro = pd.DataFrame()
       data_componetes = df2.loc[df2['fecha'] == fecha]

       return data_registro, data_componetes
   elif 'fecha' not in df2.columns:
        data_componetes = pd.DataFrame()
        data_registro = df1.loc[df1['fecha'] == fecha]
        return data_registro , data_componetes
   
   else: 
       data_registro = df1.loc[df1['fecha'] == fecha]
       data_componetes = df2.loc[df2['fecha'] == fecha]
       return data_registro, data_componetes
       