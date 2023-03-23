from lib2to3.pgen2 import driver
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from flask import Flask, request
from selenium.webdriver.common.keys import Keys
from services.olxRules import RulesOlx, driver


app = Flask(__name__)

# Define a rota da API
@app.post("/dados")
def get_dados():
    
    RulesOlx.get_inicio()
    RulesOlx.get_marca()
    RulesOlx.get_modelo()
    RulesOlx.get_ano_inicio()
    RulesOlx.get_ano_fim()
    RulesOlx.get_preco_minimo()
    RulesOlx.get_preco_maximo()
          
    
    # ransforma os dados em um objeto JSON
    json_resultado = json.dumps(RulesOlx.montar_json_resposta())

    # Retorna os dados em formato JSON
    return json_resultado


if __name__ == "__main__":
    app.run()
