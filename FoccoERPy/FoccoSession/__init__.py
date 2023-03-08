from requests import Session
from urllib.parse import urljoin

class FoccoSession(Session):
    def __init__(self, server_url: str, token_acesso: str, id_empresa: int) -> None:
        super().__init__()

        self.SERVER_URL = server_url
        
        self.default_headers = {
            'Authorization': 'Bearer ' + token_acesso,
            'X-EMPR-ID': str(id_empresa)
        }
    
    def request(self, method, path, *args, **kwargs):

        complete_url = urljoin(str(self.SERVER_URL), path)

        headers = kwargs.get('headers', self.default_headers)

        kwargs.pop('headers', None)

        response = super().request(
            method  = method,
            url     = complete_url,
            headers = headers,
            *args,
            **kwargs
        )

        response.raise_for_status()

        return response