# from selenium.webdriver.support.ui import Select
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# import json
# from flask import Flask, request
# from selenium.webdriver.common.keys import Keys
from olxRulesNew import RulesOlx


# app = Flask(__name__)

# # Define a rota da API
# @app.post("/dados")
# def get_dados():

#     RulesOlx.get_inicio()
#     RulesOlx.get_marca()
#     RulesOlx.get_modelo()
#     RulesOlx.get_ano_inicio()
#     RulesOlx.get_ano_fim()
#     RulesOlx.get_preco_minimo()
#     RulesOlx.get_preco_maximo()


#     # ransforma os dados em um objeto JSON
#     json_resultado = json.dumps(RulesOlx.montar_json_resposta())

#     # Retorna os dados em formato JSON
#     return json_resultado


if __name__ == "__main__":
    param = {'fabricante': "fiat", 'modelo': "argo",
             'ano_inicio': "2022",
             'ano_fim': "2023",
             'preco_minimo': "50000",
             'preco_maximo': "95000"}
    olx_extract = RulesOlx(params=param)
    if not olx_extract.is_params_correct():
        pass  # return erro
    print(teste)
