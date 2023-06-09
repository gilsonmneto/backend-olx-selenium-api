from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys


class RulesOlx:
    '''Classe reponsável por raspar os dados da OLX e retornar os resultados em um JSON'''

    FORM_XPATH: str = '//*[@id="left-side-main-content"]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/form/'
    URL_PREFIX: str = 'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios'

    def __init__(self, params: dict):
        '''Carrega todos os valores recebidos nas respectivas variáveis e abre o webdriver na url correta'''
        self.fabricante: str = params["fabricante"]
        self.modelo: str = params['modelo']
        self.ano_inicio: str = params['ano_inicio']
        self.ano_fim: str = params['ano_fim']
        self.preco_minimo: str = params['preco_minimo']
        self.preco_maximo: str = params['preco_maximo']
        if not self.__is_params_correct():
            raise Exception("ERROR: Erro de Parâmetro")
        self.driver: object = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(f"{self.URL_PREFIX}/{self.fabricante}/{self.modelo}")
        self.driver.maximize_window()

    def __is_params_correct(self) -> bool:
        '''Verifica se todos os parâmetros de pesquisa estão presentes na requisição de raspagem'''
        if not self.fabricante or not self.modelo or not self.ano_inicio:
            return False
        if not self.ano_fim or not self.preco_minimo or not self.preco_maximo:
            return False
        return True

    def __digitar_ano_inicio(self) -> None:
        '''Digita o ano início no campo correto'''
        time.sleep(4)
        element: object = (Select(self.driver.find_element(
            By.XPATH, f'{self.FORM_XPATH}div[6]/div/div/div[1]/div/select')))
        element.select_by_visible_text(self.ano_inicio)

    def __digitar_ano_fim(self) -> None:
        '''Digita o ano fim no campo correto e clica'''
        element: object = Select(self.driver.find_element(
            By.XPATH, f'{self.FORM_XPATH}div[6]/div/div/div[2]/div/select'))
        element.select_by_visible_text(self.ano_fim)
        time.sleep(2)
        element = self.driver.find_element(
            By.XPATH, f'{self.FORM_XPATH}div[6]/div/div/div[3]/button')
        element.click()

    def __digitar_preco_minimo(self) -> None:
        '''Digita o preço mínimo no campo correto'''
        time.sleep(4)
        element: object = self.driver.find_element(
            By.XPATH, f'{self.FORM_XPATH}div[7]/div/div/div[1]/input')
        element.send_keys(self.preco_minimo)

    def __digitar_preco_maximo(self) -> None:
        '''Digita o preço máximo no campo correto e clica'''
        time.sleep(2)
        element: object = self.driver.find_element(
            By.XPATH, f'{self.FORM_XPATH}div[7]/div/div/div[2]/input')
        element.send_keys(self.preco_maximo)
        time.sleep(3)
        element = self.driver.find_element(
            By.XPATH, f'{self.FORM_XPATH}div[7]/div/div/div[3]/button')
        element.click()

    def __close_webdriver(self) -> None:
        '''Fecha o webdriver'''
        self.driver.quit()

    def __resultados(self) -> list[dict]:
        '''captura os resultados e monta a lista de dict [{}] de resposta'''
        time.sleep(2)
        carros: list = []
        itens: list = self.driver.find_elements(
            By.XPATH, "//*[@id='ad-list']/li")
        total_itens: int = len(itens) + 1
        time.sleep(2)

        for i in range(1, total_itens):
            try:
                marca: str = self.fabricante
                modelo: str = self.driver.find_element(
                    By.XPATH, f'//*[@id="ad-list"]/li[{i}]/div/a/div/div[2]/div[1]/div[1]/div[1]').text
                ano: str = self.driver.find_element(
                    By.XPATH, f'//*[@id="ad-list"]/li[{i}]/div/a/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/span').text
                preco: str = self.driver.find_element(
                    By.XPATH, f'//*[@id="ad-list"]/li[{i}]/div/a/div/div[2]/div[1]/div[1]/div[2]').text
                quilometragem: str = self.driver.find_element(
                    By.XPATH, f'//*[@id="ad-list"]/li[{i}]/div/a/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[1]/span').text
                carros.append({'id': str(i), 'fabricante': marca, 'modelo': modelo,
                              'ano': ano, 'valor': preco, 'quilometragem': quilometragem})
            except Exception as e:
                print(e)
                continue
        self.__close_webdriver()
        return carros

    def run(self) -> list[dict]:
        self.__digitar_ano_inicio()
        self.__digitar_ano_fim()
        self.__digitar_preco_minimo()
        self.__digitar_preco_maximo()
        result: list[dict] = self.__resultados()
        return result
