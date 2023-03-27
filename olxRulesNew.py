from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys


class RulesOlx:
    '''Classe reponsável por raspar os dados da OLX e retornar os resultados em um JSON'''

    FORM_XPATH = '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/'
    URL = 'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios'

    def __init__(self, params: dict):
        '''Carrega todos os valores recebidos nas respectivas variáveis e abre o webdriver'''
        self.fabricante = params["fabricante"]
        self.modelo = params['modelo']
        self.ano_inicio = params['ano_inicio']
        self.ano_fim = params['ano_fim']
        self.preco_minimo = params['preco_minimo']
        self.preco_maximo = params['preco_maximo']
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.URL)
        driver.maximize_window()

    def is_params_correct(self) -> bool:
        '''Verifica se todos os parâmetros de pesquisa estão presentes na requisição de raspagem'''
        if not self.fabricante or not self.modelo or not self.ano_inicio:
            return False
        if not self.ano_fim or not self.preco_minimo or not self.preco_maximo:
            return False
        return True

    def digitar_fabricante(self):
        '''Digita o fabricante no campo correto'''
        element = Select(self.driver.find_element(
            By.XPATH, f'{self.FORM_XPATH}div[2]/div[1]/div/div/div/select'))
        element.select_by_visible_text(
            str.upper(self.marca))

    def digitar_modelo(self):
        '''Digita o modelo no campo correto'''
        time.sleep(4)
        element = Select(self.driver.find_element(
            By.XPATH, f'{self.FORM_XPATH}div[2]/div[3]/div/div/div/select'))
        element.select_by_visible_text(str.upper(self.modelo))

    def digitar_ano_inicio(self):
        '''Digita o ano início no campo correto'''
        time.sleep(4)
        element = (Select(self.driver.find_element(
            By.XPATH, f'{self.FORM_XPATH}div[6]/div/div/div[1]/div/select')))
        element.select_by_visible_text(self.inicio)

    def digitar_ano_fim(self):
        '''Digita o ano fim no campo correto e clica'''
        element = Select(self.driver.find_element(
            By.XPATH, f'{self.FORM_XPATH}div[6]/div/div/div[2]/div/select'))
        element.select_by_visible_text(self.ano_fim)
        element = self.driver.find_element(
            By.XPATH, '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/div[6]/div/div/div[3]/button')
        element.click()

    def digitar_preco_minimo(self):
        '''Digita o preço mínimo no campo correto e clica'''
        time.sleep(4)
        element = self.driver.find_element(
            By.XPATH, '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/div[7]/div/div/div[1]/input')
        element.send_keys(self.preco_minimo)

    def digitar_preco_maximo(self):
        '''Digita o preço máximo no campo correto e clica'''
        element = self.driver.find_element(
            By.XPATH, '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/div[7]/div/div/div[2]/input')
        element.send_keys(self.preco_maximo)
        element = self.driver.find_element(
            By.XPATH, '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/div[6]/div/div/div[3]/button')
        element.click()

    def resultados(self) -> list:
        '''captura os resultados e monta o json de resposta'''
        carros = []
        itens = self.driver.find_elements(By.XPATH, "//*[@id='ad-list']/li")
        total_itens = len(itens) + 1

        for i in range(1, total_itens):
            try:
                marca = self.fabricante
                modelo = self.driver.find_element(
                    By.XPATH, f'//*[@id="ad-list"]/li[{i}]/div/a/div/div[2]/div[1]/div[1]/div[1]').text
                ano = self.driver.find_element(
                    By.XPATH, f'//*[@id="ad-list"]/li[{i}]/div/a/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/span').text
                preco = self.driver.find_element(
                    By.XPATH, f'//*[@id="ad-list"]/li[{i}]/div/a/div/div[2]/div[1]/div[1]/div[2]').text
                quilometragem = self.driver.find_element(
                    By.XPATH, f'//*[@id="ad-list"]/li[{i}]/div/a/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/span').text
                carros.append({'id': str(i), 'fabricante': marca, 'modelo': modelo,
                              'ano': ano, 'valor': preco, 'quilometragem': quilometragem})
            except Exception as e:
                print(e)
                continue

        return carros
