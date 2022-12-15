import requests
from urllib.parse import urljoin
from requests import Response

from FoccoERPy.handlers import handle_json

class Focco():
    def __init__(self, server_url: str, token_acesso: str, id_empresa: int) -> None:

        self.SERVER_URL   = server_url
        
        self.default_headers = {
            'Authorization': 'Bearer ' + token_acesso,
            'X-EMPR-ID': id_empresa
        }
    
    def request(self, method, path, params=None, body=None) -> Response:

        response = requests.request(
            method=method,
            url=urljoin(str(self.FOCCO_URL), path),
            headers=self.default_headers,
            params=params,
            json=body
        )

        response.raise_for_status()

        return response

    def consulta_ordem(self, id_ordem) -> dict:
        PATH = f'api/Entities/Manufatura.Producao.OrdemProducao/{id_ordem}'

        response = self.request('GET', PATH)

        return handle_json(response.json())

    def consulta_operacoes_ordem(self, id_roteiro: int) -> dict:
        
        PATH = 'api/Commands/Manufatura.Producao.Apontamento.GetApontamentosByOrdemRoteiroCommand'

        BODY = {
            'take': None,
            'skip': None,
            'ordemRoteiroID': id_roteiro
        }

        response = self.request('POST', PATH, body=BODY)

        return handle_json(response.json())
