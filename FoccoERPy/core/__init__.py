from typing import Optional
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
        raise ErroFocco("Não teve sucesso na busca de operações")

    resposta_focco = handle_json(response.json()).get('$values')

    if not resposta_focco:
        return None

    return resposta_focco

def apontamento_tempo_padrao(
        session: FoccoSession,
        id_ordem_roteiro: int,
        quantidade: float,
        data: Optional[datetime] = None,
        finalizar: bool = False,
        id_tipo_apontamento: str = 'TP',
        origem_apontamento: str = 'API',
        usuario: str = 'Apontamento API GTRP',
        id_funcionario: Optional[int] = None,
        id_recurso: Optional[int] = None,
    ):
    """
        Apontamento por tempo padrão
    """

    PATH = 'api/Entities/Manufatura.Producao.Apontamento.ApontamentoProducao'

    if data is None:
        data = datetime.now()

    BODY = {
        'OrdemRoteiro': {
            'ID': id_ordem_roteiro
        },
        'Quantidade': quantidade,
        'DataApontamento': data.isoformat(),
        'TipoApontamento': {
            'ID': id_tipo_apontamento
        },
        'Final': finalizar,
        'Usuario': usuario,
        'OrigemApontamento': origem_apontamento,
    }

    if id_funcionario is not None:
        BODY['Funcionario'] = {
            'ID': id_funcionario
        }

    if id_recurso is not None:
        BODY['ApontamentoMaquina'] = {
            'Maquina': {
                'ID': id_recurso
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


