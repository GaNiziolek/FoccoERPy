from FoccoERPy.handlers import handle_json
from datetime import datetime
from requests.exceptions import HTTPError
from FoccoERPy.exceptions import ErroFocco
from FoccoERPy.exceptions import OrdemNaoEncontrada
from FoccoERPy.FoccoSession import FoccoSession

def consulta_ordem(session: FoccoSession, id_ordem: int) -> dict:
    PATH = f'api/Entities/Manufatura.Producao.OrdemProducao/{id_ordem}'

    try:
        response = session.request('GET', PATH)

        resposta_focco = handle_json(response.json())

        return resposta_focco
        
    except HTTPError as e:
        if e.response.status_code == 404:
            raise OrdemNaoEncontrada(id_ordem)
        else:
            raise e
    
    except Exception as e:
        raise ErroFocco(f"Não teve sucesso na busca da ordem: {str(e)}")
    
def consulta_operacoes_ordem(session: FoccoSession, id_roteiro: int) -> list:
    
    PATH = 'api/Commands/Manufatura.Producao.Apontamento.GetApontamentosByOrdemRoteiroCommand'

    BODY = {
        'take': None,
        'skip': None,
        'ordemRoteiroID': id_roteiro
    }

    response = session.request('POST', PATH, json=BODY)

    try:
        response.raise_for_status()
    except Exception as e:
        raise ErroFocco(f"Não teve sucesso na busca de operações: {resposta_focco.get('ErrorMessage')}")

    resposta_focco = handle_json(response.json()).get('$values')

    if not resposta_focco:
        return None
    
    return resposta_focco

def apontamento_tempo_padrao(session: FoccoSession, id_ordem_roteiro: int, quantidade: float, 
                             id_recurso: int, data: datetime, finalizar: bool):
    """
        Apontamento por tempo padrão
    """
    ID_TIPO_APONTAMENTO = 'TP'
    ID_FUNCIONARIO = 0
    ORIGEM_APONTAMENTO = 'API'
    USUARIO = 'Apontamento API GTRP'

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

    if not resposta_focco.get('Succeeded'):
        raise ErroFocco(f"Não teve sucesso no apontamento: {resposta_focco.get('ErrorMessage')}")
    
    return resposta_focco

def impressao_etiqueta(session: FoccoSession, 
        bearer: str,
        modelo_etiqueta: str,
        id_empresa: int,
        id_apontamento: int,
        qtd_copias: int,
        nome_impressora: str,
        chave_servico_impressao: str
    ):
    """
        Impressao de etiquetas
    """

    PATH = 'api/utilitarios/v1/ImpressaoEtiqueta'

    HEADERS = {
        'Authorization': 'Bearer ' + bearer
    }

    BODY = {
        'modeloEtiqueta':        modelo_etiqueta,
        'empresaId':             id_empresa,
        'apontamentoId':         id_apontamento,
        'numeroCopias':          qtd_copias,
        'nomeImpressora':        nome_impressora,
        'chaveServicoImpressao': chave_servico_impressao
    }

    response = session.request('POST', PATH, json=BODY, headers=HEADERS)

    resposta_focco = handle_json(response.json())

    if not resposta_focco.get('Succeeded'):
        raise ErroFocco(f"Não teve sucesso na impressão de etiquetas: {resposta_focco.get('ErrorMessage')}")
    
    return resposta_focco.get('Succeeded')


