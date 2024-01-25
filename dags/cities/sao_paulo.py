import requests
from cities.saveCityAsCSV import saveCityAsCSV
from os import getenv


def req() -> dict:
    # http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token=d1bb804b2deb44121c369766969557fac53d34fa4b595f884c13f81ca6de5245
    TOKEN = "d1bb804b2deb44121c369766969557fac53d34fa4b595f884c13f81ca6de5245" #felipe
    # TOKEN = getenv("SP_TOKEN")
    API_URL = "http://api.olhovivo.sptrans.com.br/v2.1"
    auth = requests.post(url=(API_URL + "/Login/Autenticar?token=" + TOKEN))
    print(auth.text)
    print(auth)
    if auth.text != 'true':
        raise "Houve um erro na autenticação"

    response = requests.get(API_URL + "/Posicao", cookies=auth.cookies)
    response = response.json()

    return response

def process_response(response: dict) -> list:
    lista_onibus = list()
    for linha in response['l']:
        for vs in linha['vs']:
            instancia_processada = {
                'latitude': vs['py'],
                'longitude': vs['px'],
                'tempo_captura': vs['ta'],
                'id_onibus': vs['p'],
                'c':linha['c'],
                'lt0':linha['lt0'],
                'lt1':linha['lt1'],
            }
            #enfim vamos adicionar a nova instância processada na lista
            lista_onibus.append(instancia_processada)
    
    return lista_onibus

def sao_paulo():
    try:
        response = req()
        processed_response = process_response(response)
        saveCityAsCSV(city="sp", data=processed_response)
    except Exception as e:
        print(f"sao_paulo - Error: {e}")
        raise ValueError('Erro em Sao Paulo!')
   