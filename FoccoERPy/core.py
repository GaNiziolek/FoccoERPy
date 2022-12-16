from handlers import handle_json
from datetime import datetime

from exceptions import ErroFocco

def consulta_ordem(session, id_ordem) -> dict:
    PATH = f'api/Entities/Manufatura.Producao.OrdemProducao/{id_ordem}'

    response = session.request('GET', PATH)

    return handle_json(response.json())

def consulta_operacoes_ordem(session, id_roteiro: int) -> list:
    
    PATH = 'api/Commands/Manufatura.Producao.Apontamento.GetApontamentosByOrdemRoteiroCommand'

    BODY = {
        'take': None,
        'skip': None,
        'ordemRoteiroID': id_roteiro
    }

    response = session.request('POST', PATH, json=BODY)

    return handle_json(response.json()).get('$values')

def apontamento_tempo_padrao(session, id_ordem_roteiro: int, quantidade: float, 
                             id_recurso: int, data: datetime, finalizar: bool):
    """
        Apontamento por tempo padrão
    """
    ID_TIPO_APONTAMENTO = 'TP'
    ID_FUNCIONARIO = 0
    ORIGEM_APONTAMENTO = 'API'
    USUARIO = 'Apontamento API'

    PATH = 'api/Entities/Manufatura.Producao.Apontamento.ApontamentoProducao'

    BODY = {
        'OrdemRoteiro': {
            'ID': id_ordem_roteiro
        },
        'Quantidade': quantidade,
        'DataApontamento': data.isoformat(),
        'TipoApontamento': {
            'ID': ID_TIPO_APONTAMENTO
        },
        'Funcionario': {
            'ID': ID_FUNCIONARIO
        },
        'Final': finalizar,
        'Usuario': USUARIO,
        'OrigemApontamento': ORIGEM_APONTAMENTO,
        'ApontamentoMaquina': {
            'Maquina': {
                'ID': id_recurso
            }
        }
    }

    response = session.request('POST', PATH, json=BODY)

    resposta_focco = handle_json(response.json())

    if resposta_focco.get('Succeeded'):
        return handle_json(response.json())

    raise ErroFocco(resposta_focco.get('ErrorMessage'))
