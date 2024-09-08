from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Simulador de base de datos en memoria
comprobantes_db = []

def calcular_monto_convertido(monto_pesos, tipo_cambio):
    return monto_pesos * tipo_cambio

def calcular_comision(monto_convertido):
    return monto_convertido * 0.001

def calcular_monto_total(monto_convertido, comision):
    return monto_convertido - comision

def generar_comprobante(datos_emisor, datos_beneficiario, monto_convertido, comision, monto_total):
    comprobante = {
        "Datos del Emisor": datos_emisor,
        "Datos del Beneficiario": datos_beneficiario,
        "Monto Convertido": monto_convertido,
        "Comisión": comision,
        "Monto Total": monto_total,
        "Fecha y Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return comprobante

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        monto_pesos = float(request.form['monto_pesos'])
        tipo_cambio = float(request.form['tipo_cambio'])
        datos_emisor = request.form['datos_emisor']
        datos_beneficiario = request.form['datos_beneficiario']

        # Validación
        if monto_pesos <= 0 or tipo_cambio <= 0:
            return render_template('index.html', error="Monto o tipo de cambio inválidos.")

        monto_convertido = calcular_monto_convertido(monto_pesos, tipo_cambio)
        comision = calcular_comision(monto_convertido)
        monto_total = calcular_monto_total(monto_convertido, comision)

        comprobante = generar_comprobante(datos_emisor, datos_beneficiario, monto_convertido, comision, monto_total)
        comprobantes_db.append(comprobante)

        return render_template('comprobante.html', comprobante=comprobante)

    return render_template('index.html')

@app.route('/comprobantes')
def listar_comprobantes():
    return render_template('comprobantes.html', comprobantes=comprobantes_db)

if __name__ == '__main__':
    app.run(debug=True)
