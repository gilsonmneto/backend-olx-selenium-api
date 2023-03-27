from lib2to3.pgen2 import driver
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from flask import Flask, request
from selenium.webdriver.common.keys import Keys


class RulesOlx:

    def get_inicio():
        
        global driver, parametros, fabricante
        # Instala o ChomeDriverManage biblioteca gerencia drivers automaticamente para diferentes navegadores
        driver = webdriver.Chrome(ChromeDriverManager().install())
        # Abre a página inicial da OLX
        driver.get('https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios')

        # Para maximizar o navegador
        driver.maximize_window()

        # Pega os parametros enviados na requisição
        parametros= request.get_json()
        fabricante = parametros["marca"]
    
        # Valida os parametros informados na requisição
        # Localiza o elemento na página e seleciona item conforme o parametro
        # Em caso de input localiza o elemento insere o valor e clika no botão de pesquisa

            
    def get_marca():
        try:    
            if ("marca" not in parametros):
                return{"status": 400, "mensagem": "O parametro marca é obrigatório"}
            else:
                marca = Select(driver.find_element(By.XPATH, '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/div[2]/div[1]/div/div/div/select'))
                marca = marca.select_by_visible_text(str.upper(parametros['marca']))
        except Exception as e: 
            print(e)
        return marca

    def get_modelo():
        try:       
            if ("modelo" not in parametros):
                return{"status": 400, "mensagem": "O parametro modelo é obrigatório"}
            else:
                time.sleep(4)
                modelo = Select(driver.find_element(By.XPATH, '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/div[2]/div[3]/div/div/div/select'))
                modelo.select_by_visible_text(str.upper(parametros['modelo']))
        except Exception as e: 
            print(e)
        return modelo

    def get_ano_inicio():
        try:        
            if ("ano_inicio" not in parametros):
                return{"status": 400, "mensagem": "O parametro ano inicio é obrigatório"}
            else:
                time.sleep(4)
                ano_inicio = (Select(driver.find_element(By.XPATH, '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/div[6]/div/div/div[1]/div/select')))
                ano_inicio = ano_inicio.select_by_visible_text(parametros['ano_inicio'])            
        except Exception as e: 
            print(e)
        return ano_inicio

    def get_ano_fim():
        try:
            if ("ano_fim" not in parametros):
                return{"status": 400, "mensagem": "O parametro ano inicio e ano_fim é obrigatório"}
            else:
                time.sleep(4) 
                ano_fim = Select(driver.find_element(By.XPATH, '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/div[6]/div/div/div[2]/div/select'))
                ano_fim = ano_fim.select_by_visible_text(parametros['ano_fim'])

                button_pesquisar_ano = driver.find_element(By.XPATH, '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/div[6]/div/div/div[3]/button')
                button_pesquisar_ano.click()
        except Exception as e: 
            print(e)
        return ano_fim

    def get_preco_minimo():
        try:
            if ("preco_minimo" not in parametros):
                return{"status": 400, "mensagem": "O parametro preço minimo é obrigatório"}
            else:
                time.sleep(4)
                preco_minimo = driver.find_element(By.XPATH, '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/div[7]/div/div/div[1]/input')
                preco_minimo = preco_minimo.send_keys(parametros['preco_minimo'])            
        except Exception as e: 
            print(e)
        return preco_minimo

    def get_preco_maximo():
        try:
            if ("preco_maximo" not in parametros):
                return{"status": 400, "mensagem": "O parametro preço maximo é obrigatório"}
            else:  
                preco_maximo = driver.find_element(By.XPATH, '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/div[7]/div/div/div[2]/input')
                preco_maximo = preco_maximo.send_keys(parametros['preco_maximo'])

                button_pesquisar_ano = driver.find_element(By.XPATH, '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/div[6]/div/div/div[3]/button')
                button_pesquisar_ano.click()            
        except Exception as e: 
            print(e)
        return preco_maximo                   
        
    def montar_json_resposta():
        
        # cria uma lista vazia para receber os registros encontrados
        carros = []

        # Extrai as informações da tabela de anúncios de carros encontrados na página de resultados - lu e li
        itens = driver.find_elements(By.XPATH, "//*[@id='ad-list']/li")
        total_itens = len(itens) + 1 

        for i in range(1, total_itens):

            try:
                marca = fabricante
                modelo = driver.find_element(
                    By.XPATH, f'//*[@id="ad-list"]/li[{i}]/div/a/div/div[2]/div[1]/div[1]/div[1]').text
                ano = driver.find_element(
                    By.XPATH, f'//*[@id="ad-list"]/li[{i}]/div/a/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/span').text
                preco = driver.find_element(
                    By.XPATH, f'//*[@id="ad-list"]/li[{i}]/div/a/div/div[2]/div[1]/div[1]/div[2]').text
                quilometragem = driver.find_element(
                    By.XPATH, f'//*[@id="ad-list"]/li[{i}]/div/a/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/span').text

                carros.append({'id': str(i), 'fabricante': marca, 'modelo': modelo, 'ano': ano, 'valor': preco, 'quilometragem': quilometragem})
                               
            except:
                continue
            
        return carros
        

    
