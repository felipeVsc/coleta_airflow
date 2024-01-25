import requests
from cities.saveCityAsCSV import saveCityAsCSV
# from utils.convertResponseToDict import convertResponseToDict
from datetime import datetime, timedelta
import time
import pandas as pd
import os

# def saveCityAsCSV(city, data):
#     timestamp = str(time.time())
#     try:
#         print("Aqui é o RIo")
#         df = pd.DataFrame(data)
#         dataset_dir = '/home/felipe/airflow/dags/dags_ind/60seg'
#         output_dir = f"{dataset_dir}/{city}2"

#         if not os.path.exists(f"{dataset_dir}/{city}"):
#             os.makedirs(f"{dataset_dir}/{city}")

#         print(f"Called | {timestamp} | {city}")
#         df.to_csv(f"{output_dir}/{timestamp}.csv")

#         print(f"SAVING FILE {city}")
#     except Exception as e:
#         print(f"{city} - Error on save as CSV {timestamp}: {e}")


# https://dados.mobilidade.rio/gps/sppo?dataInicial=2024-01-08+11:50:00&dataFinal=2024-01-08+11:51:00
def req() -> dict:
    # API_URL = "https://jeap.rio.rj.gov.br/dadosAbertosAPI/v2/transporte/veiculos/onibus2"
    # API_URL = "https://dados.mobilidade.rio/gps/sppo"
    datetime_atual = datetime.now()
    mes = '0'+str(datetime_atual.month)
    dia = '0'+str(datetime_atual.day) if len(str(datetime_atual.day))==1 else str(datetime_atual.day)
    hora = '0'+str(datetime_atual.hour) if len(str(datetime_atual.hour))==1 else str(datetime_atual.hour)
    minutos = '0'+str(datetime_atual.minute) if len(str(datetime_atual.minute))==1 else str(datetime_atual.minute)
    segundos = '0'+str(datetime_atual.second) if len(str(datetime_atual.second))==1 else str(datetime_atual.second)

    datetime_passado = datetime_atual-timedelta(minutes=1)
    mes_passado = '0'+str(datetime_passado.month)
    dia_passado = '0'+str(datetime_passado.day) if len(str(datetime_passado.day))==1 else str(datetime_passado.day)
    hora_passado = '0'+str(datetime_passado.hour) if len(str(datetime_passado.hour))==1 else str(datetime_passado.hour)
    minutos_passado = '0'+str(datetime_passado.minute) if len(str(datetime_passado.minute))==1 else str(datetime_passado.minute)
    segundos_passado = '0'+str(datetime_passado.second) if len(str(datetime_passado.second))==1 else str(datetime_passado.second)

    API_URL = f"https://dados.mobilidade.rio/gps/sppo?dataInicial={2024}-{mes_passado}-{dia_passado}+{hora_passado}:{minutos_passado}:{segundos_passado}&dataFinal={2024}-{mes}-{dia}+{hora}:{minutos}:{segundos}"

    
    response = requests.get(API_URL).json()
    return response 

def process_response(response: dict) -> list:
    # onibus = convertResponseToDict(response, latitude_key='latitude', longitude_key='longitude', tempo_captura_key='dataHora', id_key='ordem')
    # return onibus
    lista_onibus = list()
    for vs in response:
        instancia_processada = {
            'latitude' : vs['latitude'],
            'longitude' : vs['longitude'],
            'tempo_captura' : vs['datahora'],
            'id_onibus' : vs['ordem'],
            'velocidade': vs['velocidade'],
            'linha':vs['linha']
        }
        lista_onibus.append(instancia_processada)
    return lista_onibus


def rio():
    response = req()
    processed_response = process_response(response)
    saveCityAsCSV(city="rj", data=processed_response)

