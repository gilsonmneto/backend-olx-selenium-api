import json
from flask import Flask, request
from olx_rules import RulesOlx


app = Flask(__name__)


@app.post("/dados")
def get_dados():
    '''sample request: {'fabricante': "fiat",'modelo': "argo",'ano_inicio': "2022",'ano_fim': "2023",'preco_minimo': "50000",'preco_maximo': "95000"}'''
    try:
        param = request.get_json()
        olx_extract = RulesOlx(params=param)
        json_resultado = json.dumps(olx_extract.run())
        return json_resultado, 200
    except:
        return 400


if __name__ == "__main__":
    app.run()
