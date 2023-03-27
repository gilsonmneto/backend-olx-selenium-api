# from selenium.webdriver.support.ui import Select
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# import time
import json
# from flask import Flask, request
# from selenium.webdriver.common.keys import Keys
from olxRulesNew import RulesOlx


# app = Flask(__name__)

# # Define a rota da API
# @app.post("/dados")
# def get_dados():


if __name__ == "__main__":
    param = {'fabricante': "fiat", 'modelo': "argo",
             'ano_inicio': "2022",
             'ano_fim': "2023",
             'preco_minimo': "50000",
             'preco_maximo': "95000"}
    olx_extract = RulesOlx(params=param)
    json_resultado = json.dumps(olx_extract.run())
    print(json_resultado)
