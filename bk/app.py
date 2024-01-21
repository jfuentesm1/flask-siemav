from flask import Flask, render_template, request
import buscador as bus
app = Flask(__name__)

def usuarios():
    ip_cliente = request.remote_addr
    usuario = bus.identificador(ip_cliente)
    return usuario

def excel_registro():
    conectados = usuarios()
    
    if 'enviar_numeros' in request.form:
        # Procesar los números ASP y AMA
        componetes= None
        cantidad= None
        numeroASP = request.form['numeroASP']
        numeroAMA = request.form['numeroAMA']
        excel1 = bus.escritura_excel(numeroASP,numeroAMA,componetes,cantidad,conectados,direccion=r'/home/pi/FlaskApp/inventario reparaciones/registro.xlsx')              
        return excel1
    
    elif 'enviar_opcion' in request.form:
        #  Procesar segundo excel y escribir
        numeroASP = None
        numeroAMA = None
        componentes_electronicos = request.form['opcion']
        cantidad = request.form['cantidad']
        excel2 = bus.escritura_excel(numeroASP,numeroAMA,componentes_electronicos,cantidad,conectados ,direccion=r'/home/pi/FlaskApp/inventario reparaciones/componetes usados.xlsx')              
        
        return excel2  

@app.route('/')
def index():
    titulo = usuarios()
    if titulo == False:
        return render_template('exit.html')
    else:
        return render_template('index.html', titulo = titulo)

@app.route('/reporte', methods=['POST'])

def asp_ama():
    

    registro_diario = excel_registro()
    return registro_diario 
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
