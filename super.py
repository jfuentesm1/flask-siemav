import pandas as pd

def filtrar_registros(año,mes,dia):
    fecha = f'{año}-{mes:02d}-{dia:02d}'
    df1 = pd.read_excel(r"/home/pi/FlaskApp/inventario reparaciones/registro.xlsx")
    print(df1.loc[df1['fecha'] == fecha])
    df2 = pd.read_excel(r"/home/pi/FlaskApp/inventario reparaciones/componetes usados.xlsx")
    print(df2.loc[df2['fecha'] == fecha])


