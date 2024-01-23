from flask import Flask, render_template, request, jsonify
import buscador as bus
app = Flask(__name__)

def usuarios():
    ip_cliente = request.remote_addr
    usuario = bus.identificador(ip_cliente)
    return usuario

def excel_registro():
    conectados = usuarios()
    
    if 'numeros_y_sector' in request.form:
        # Procesar los números ASP y AMA
        componetes= None
        cantidad= None
        numeroASP = int(request.form['numeroASP'])
        numeroAMA = int(request.form['numeroAMA'])
        sector = request.form['sector'].upper()
        excel1 = bus.escritura_excel(numeroASP,numeroAMA, sector,componetes,cantidad,conectados,direccion=r'/home/pi/FlaskApp/inventario reparaciones/registro.xlsx')              
        return excel1
    
    elif 'componentes_usados' in request.form:
        #  Procesar segundo excel y escribir
        numeroASP = None
        numeroAMA = None
        componentes_electronicos = request.form['opcion']
        cantidad = request.form['cantidad']
        excel2 = bus.escritura_excel(numeroASP,numeroAMA,componentes_electronicos,cantidad,conectados ,direccion=r'/home/pi/FlaskApp/inventario reparaciones/componetes usados.xlsx')              
        
        return excel2  
def lectura_excel():

    año = int(request.form['year'])
    mes = int(request.form['month'])
    dia = int(request.form['day'])
    dato1, dato2 = bus.filtrar_registros(año,mes,dia) 
    if 'revisar_tarjetas' in request.form:
        #print(dato1)
        return dato1
    elif 'revisar_componentes' in request.form:
        #print(dato2)
        return dato2
    elif dato1 or dato2 == False:
        return False


@app.route('/', methods=['GET', 'POST'])
def index():
    titulo = usuarios()

    if titulo == 'super_usuario':
        return render_template('super_index.html')
    elif titulo == False:
        return render_template('exit.html')
    else:
        return render_template('index.html', titulo=titulo)


@app.route('/reporte', methods=['POST'])
def reporte_diario():
    try:
        registro_diario = excel_registro()
        return registro_diario
    finally:
        return render_template('final.html') 
    
@app.route('/lecturas', methods=['POST'])
def lectura():
    df = lectura_excel()
    return render_template('dataframe.html', table=df.to_html(classes='table table-striped'))

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
