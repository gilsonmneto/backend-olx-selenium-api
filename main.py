from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Configura o Selenium WebDriver para controlar o Google Chrome
# driver = webdriver.Chrome()

driver = webdriver.Chrome(ChromeDriverManager().install())
# Abre a página inicial da OLX
driver.get('https://www.olx.com.br/')

# Para maximizar o navegador
driver.maximize_window()

# Localiza e clika no botão Autos e pecas

botao_Autos_e_pecas = driver.find_element(
    By.XPATH, '//*[@id="gatsby-focus-wrapper"]/div[2]/div[1]/div/div[2]/div/div/ul/li[4]/a/span')
botao_Autos_e_pecas.click()

# Localiza os elementos HTML da página de pesquisa
modelo_input = driver.find_element(By.XPATH, '//*[@id="searchtext-input"]')
ano_inicio_input = driver.find_element(
    By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div/div[4]/div/div[1]/span/input')
ano_fim_input = driver.find_element(
    By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div/div[4]/div/div[2]/span/input')

# Insere as informações de pesquisa nos campos correspondentes
modelo_input.send_keys('Fiesta')
ano_inicio_input.send_keys('2010')
ano_fim_input.send_keys('2021')

# Clica no botão "Pesquisar"
pesquisar_button = driver.find_element(
    By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[2]/div/a')
pesquisar_button.click()

# Aguarda até que a página de resultados seja carregada
time.sleep(3)

# Extrai as informações dos anúncios de carros encontrados na página de resultados
resultados = driver.find_elements(By.XPATH, '//*[@id="ad-list"]/li')

# cria uma lista vazia para receber os registros encontrados
carros = []

print('\n')

time.sleep(3)

# ERRO: ESTÁ TRAZENDO APENAS O PRIMEIRO VEÍCULO DA RELAÇÃO
for resultado in resultados:

    modelo = resultado.find_element(
        By.XPATH, '//*[@id="ad-list"]/li[1]/div/a/div/div[2]/div[1]/div[1]/div[1]/div/h2').text
    ano = resultado.find_element(
        By.XPATH, '//*[@id="ad-list"]/li[1]/div/a/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]').text
    valor = resultado.find_element(
        By.XPATH, '//*[@id="ad-list"]/li[1]/div/a/div/div[2]/div[1]/div[1]/div[2]/div/div/div/span').text
    quilometragem = resultado.find_element(
        By.XPATH, '//*[@id="ad-list"]/li[1]/div/a/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/span').text

    carros.append({'modelo': modelo, 'ano': ano, 'valor': valor,
                  'quilometragem': quilometragem})

    print('Modelo: ', modelo, '| Ano: ', ano, '| Valor: ',
          valor, '| Quilometragem: ', quilometragem)


print('\n')

qtdDeItens = len(carros)
print('Foram encontrados ', qtdDeItens, ' carros a venda')
# Fecha o navegador
driver.quit()
