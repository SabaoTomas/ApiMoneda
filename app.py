from datetime import date
from datetime import timedelta
from flask import Flask, jsonify
from flask_cors import  CORS
import requests

app = Flask(__name__)

CORS(app)

delta = timedelta(days=1)
fecha_ayer = str(date.today()-delta)
fecha_ayer = fecha_ayer.split('-')
anio = fecha_ayer[0]
mes = fecha_ayer[1]
dia = fecha_ayer[2]

#api para billete
api_url = 'https://www.bna.com.ar/Cotizador/DescargarPorFecha?fechaDesde=' + dia + '%2F' + mes + '%2F' + anio + '&fechaHasta=' + dia + '%2F' + mes + '%2F' + anio + '&id=billetes'

#api para divisas
api_url_divisa = 'https://www.bna.com.ar/Cotizador/MonedasHistorico'

#url para valor de ethereum a usdt
api_url_ethereum = 'https://api.binance.com/api/v3/avgPrice?symbol=ETHUSDT'

flagDivisaCargada = False
datosDivisa = ''


def fetch_data_billete(target_url):
    # Make a GET request to the external API
    response = requests.get(target_url)
    # Check if the request was successful
    if response.status_code == 200:
        print(response.text)
        # Return the JSON data received from the API)
        valor = response.text.split('\n')[1].split(';')[2]
        return jsonify(valor), 200
    else:
        # If the request failed, return an error message
        return jsonify({'error': 'Failed to fetch data from external API'}), response.status_code

@app.route('/fetch-data/DolarBillete', methods=['GET'])
def fetch_data_dolar_billete():
    # External API URL
    target_url = api_url + '&filtroDolarDescarga=1'
    return fetch_data_billete(target_url)

@app.route('/fetch-data/EuroBillete', methods=['GET'])
def fetch_data_euro_billete():
    # External API URL
    target_url = api_url + '&filtroEuroDescarga=1'
    return fetch_data_billete(target_url)

def fetch_divisa(string_divisa,datosDivisa):
    separador =  '<td>'  + string_divisa + '</td>'
    valor = datosDivisa.split(separador)[1].split('</td>')[1].split('>')[1]
    return valor


@app.route('/fetch-data/Dolar', methods=['GET'])
def fetch_data_dolar():
    response = requests.get(api_url_divisa)
    datosDivisa = response.text
    return jsonify(fetch_divisa('Dolar U.S.A',datosDivisa)), 200

@app.route('/fetch-data/Euro', methods=['GET'])
def fetch_data_euro():
    response = requests.get(api_url_divisa)
    datosDivisa = response.text
    return jsonify(fetch_divisa('Euro',datosDivisa)), 200

@app.route('/fetch-data/LibraEsterlina', methods=['GET'])
def fetch_data_libra():
    response = requests.get(api_url_divisa)
    datosDivisa = response.text
    return jsonify(fetch_divisa('Libra Esterlina',datosDivisa)), 200

@app.route('/fetch-data/FrancoSuizo', methods=['GET'])
def fetch_data_franco_suizo():
    response = requests.get(api_url_divisa)
    datosDivisa = response.text
    return jsonify(fetch_divisa('Franco Suizos (*)',datosDivisa)), 200

@app.route('/fetch-data/Yen', methods=['GET'])
def fetch_data_yenes():
    response = requests.get(api_url_divisa)
    datosDivisa = response.text
    return jsonify(fetch_divisa('YENES (*)',datosDivisa)), 200

@app.route('/fetch-data/Yuan', methods=['GET'])
def fetch_data_yuanes():
    response = requests.get(api_url_divisa)
    datosDivisa = response.text
    return jsonify(fetch_divisa('Yuan (*)',datosDivisa)), 200

@app.route('/fetch-data/DolarAustraliano', methods=['GET'])
def fetch_data_dolar_australiano():
    response = requests.get(api_url_divisa)
    datosDivisa = response.text
    return jsonify(fetch_divisa('Dolar Australiano',datosDivisa)), 200

@app.route('/fetch-data/Ethereum', methods=['GET'])
def fetch_data_cotizacion_ethereum():
    response = requests.get(api_url_ethereum)

    return jsonify(response.text), 200




if __name__ == '__main__':
    #Ruta debug
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
