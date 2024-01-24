from flask import Flask, render_template, request, jsonify
import buscador as bus
app = Flask(__name__)

def usuarios():
    ip_user = request.remote_addr
    usuario = bus.identificador(ip_user)
    return usuario

def escritura_excel():
    conectados = usuarios()
    if 'numeros_y_sector' in request.form:
        recibidas = request.form.get('recibidas')
        reparadas = request.form.get('reparadas')
        descartadas = request.form.get('descartadas')
        sector = request.form.get('sector')
        clase = request.form.get('clase')

        if recibidas is not None and reparadas is not None and descartadas is not None and sector is not None and clase is not None:
            # Verificar si los campos no son cadenas vacías
            if recibidas.strip() and reparadas.strip() and descartadas.strip() and descartadas.strip() and sector.strip() and clase.strip():
                try:
                    recibidas = int(recibidas)
                    reparadas = int(reparadas)
                    descartadas = int(descartadas)
                    clase = str(clase)
                    sector = sector.upper().strip()
                except ValueError:
                    return False
                
                componetes = None
                cantidad = None
                excel_registro = bus.escritura_excel(sector, clase, recibidas, reparadas, descartadas, componetes, cantidad, conectados, direccion=r'/home/pi/FlaskApp/inventario reparaciones/registro.xlsx')              
                return excel_registro

    # verificar si 'componentes_usados' está presente en el formulario
    elif 'componentes_usados' in request.form:
        # verificar si existen y tienen valores los campos requeridos
        componentes = request.form.get('opcion')
        cantidad = request.form.get('cantidad')

        if componentes is not None and cantidad is not None:
            # verificar si los campos no son cadenas vacías
            if componentes.strip() and cantidad.strip():
                #procesar segundo excel y escribir
                recibidas =  None
                reparadas = None
                descartadas = None
                clase = None
                sector = None

                excel_componentes = bus.escritura_excel(sector, clase ,recibidas, reparadas,descartadas, componentes, cantidad, conectados, direccion=r'/home/pi/FlaskApp/inventario reparaciones/componetes usados.xlsx')              
                return excel_componentes

    # si no se cumple ninguna de las condiciones, retornar False
    return False
    
def lectura_excel():
    año = int(request.form['year'])
    mes = int(request.form['month'])
    dia = int(request.form['day'])
    df_registro, df_componetes = bus.filtrar_registros(año,mes,dia) 
    if 'revisar_tarjetas' in request.form:

        return df_registro
    elif 'revisar_componentes' in request.form:
 
        return df_componetes
    elif df_registro or df_componetes == False:
        return False


@app.route('/', methods=['GET', 'POST'])
def index():
    titulo = usuarios()

    if titulo == 'super_usuario':
        return render_template('super_index.html')
    elif titulo is False:
        return render_template('exit.html')
    else:
        return render_template('index.html', titulo=titulo)


@app.route('/reporte', methods=['POST'])
def reporte_diario():
    titulo = usuarios()
    registro = escritura_excel()
    if registro is False:
        return render_template('error.html')
    else:
        return render_template('final.html', titulo=titulo) 
    
@app.route('/lecturas', methods=['POST'])
def lectura():
    df = lectura_excel()
    return render_template('dataframe.html', table= df.to_html(classes='table table-striped'))

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
