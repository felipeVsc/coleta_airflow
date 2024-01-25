import requests
from cities.saveCityAsCSV import saveCityAsCSV

def req():
    API_URL = 'https://transporteservico.urbs.curitiba.pr.gov.br/getVeiculos.php?&c=e5b1c'
    response = requests.get(API_URL).json()
    return response
    
def process_response(response):
    veiculos = []

    tabela_de_veiculos = {
        '':'NAO ESPECIFICADO',
        '1':'COMUM',
        '2':'SEMI PADRON',
        '3':'PADRON',
        '4':'ARTICULADO',
        '5':'BIARTICULADO',
        '6':'MICRO',
        '7':'MICRO ESPECIAL',
        '8':'BIARTIC. BIO',
        '9':'ARTIC. BIO',
        '10':'HIBRIDO',
        '11':'HIBRIDO BIO',
        '12':'ELÉTRICO}',
    } 

    for cod in response:
        veiculo = dict()

        veiculo['id_onibus'] = cod
        veiculo['latitude'] = response[cod]['LAT']
        veiculo['longitude'] = response[cod]['LON']
        veiculo['tempo_captura'] = response[cod]['REFRESH'] # <-- DEVE SER AJUSTADO!!! NAO VEM COM A DATA!!!
        veiculo['tipo_veiculo'] = tabela_de_veiculos[response[cod]['TIPO_VEIC']]
        veiculo['linha'] = response[cod]['CODIGOLINHA']
        veiculo['situacao'] = response[cod]['SITUACAO']
        veiculo['situacao_2'] = response[cod]['SITUACAO2']
        veiculo['sentido'] = response[cod]['SENT']
        veiculo['tabela'] = response[cod]['TABELA']
        veiculo['adaptado'] = response[cod]['ADAPT']

        veiculos.append(veiculo)

    return veiculos

def curitiba():
    try:
        response = req()
        processed_response = process_response(response)
        saveCityAsCSV(city="cwb", data=processed_response)
    except Exception as e:
        print(f"curitiba - Error: {e}")
        raise ValueError('Erro em Cwb!')