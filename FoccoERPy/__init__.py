import requests
from urllib.parse import urljoin
from requests import Response
from benedict import benedict
import numpy as np
from datetime import datetime

from FoccoSession import FoccoSession

from core import consulta_ordem
from core import consulta_operacoes_ordem
from core import apontamento_tempo_padrao

from exceptions import ErroFocco

class Focco():
    def __init__(self, server_url: str, token_acesso: str, id_empresa: int) -> None:

        self.Session = FoccoSession(server_url, token_acesso, id_empresa)

    def apontamento(self, id_ordem: int, id_recurso: int, cod_centro_trabalho: str, quantidade: float):

        def retorno(sucesso: bool, mensagem: str, id_apontamento: int = None):

            return {
                'sucesso': sucesso,
                'mensagem': mensagem,
                'finalizou_ordem': finalizar_ordem,
                'id_apontamento': id_apontamento
            }

        finalizar_ordem = False

        # Busca informações da Ordem
        info_ordem = consulta_ordem(self.Session, id_ordem)

        if info_ordem.get('Finalizada'):
            return retorno(False, 'A ordem informada já foi finalizada.')

        operacoes = info_ordem.get('RoteirosProducao.$values')

        ultima_operacao = operacoes[-1]

        lista_qtd = []

        operacoes_setor = []

        for op in operacoes:
            op = benedict(op)

            # Se a operacoes pertencer ao mesmo setor/centro de trabalho
            if cod_centro_trabalho == op.get('Operacao.CentroTrabalho.Codigo'):

                apontamentos_operacao = consulta_operacoes_ordem(self.Session, op.get('ID'))

                qtd_apontada = 0

                for apontamento in apontamentos_operacao:
                    qtd_apontada += apontamento.get('Quantidade')

                lista_qtd.append(qtd_apontada)
                operacoes_setor.append(op)

        # A proxima operacao a ser apontada é a subsequente a operacao que tiver a maior qtd_apontada

        index_op = np.argmin(lista_qtd)

        operacao_apontamento = operacoes_setor[index_op]

        if operacao_apontamento.get('ID') == ultima_operacao.get('ID') and qtd_apontada + quantidade == info_ordem.get('Quantidade') :
            # Se o ID for igual da última operação da ordem e
            # se a quantidade que ja foi apontada + a quantidade que está
            # sendo apontada agora é igual a quantidade total da ordem
            finalizar_ordem = True

        try:
            resposta_focco = apontamento_tempo_padrao(
                                self.Session,
                                id_ordem_roteiro = operacao_apontamento.get('ID'),
                                quantidade       = quantidade,
                                id_recurso       = id_recurso,
                                data             = datetime.now(),
                                finalizar        = finalizar_ordem
                            )
        except ErroFocco as e:
            return retorno(False, e)
        else:
            id_apontamento = resposta_focco.get('Value')
            return retorno(True, 'OK', id_apontamento)


if __name__ == '__main__':

    from dotenv import load_dotenv
    import os

    # Carrega as variaveis de ambiente
    load_dotenv()

    FOCCO_URL   = os.getenv('FOCCO_URL')
    if not FOCCO_URL:
        raise EnvironmentError("Não foi possível encontar o valor da variável de ambiente FOCCO_URL")

    FOCCO_TOKEN = os.getenv('FOCCO_TOKEN')
    if not FOCCO_TOKEN:
        raise EnvironmentError("Não foi possível encontar o valor da variável de ambiente FOCCO_TOKEN")

    FOCCO_EMPRESA = os.getenv('FOCCO_EMPRESA')
    if not FOCCO_EMPRESA:
        raise EnvironmentError("Não foi possível encontar o valor da variável de ambiente FOCCO_EMPRESA")

    focco = Focco(FOCCO_URL, FOCCO_TOKEN, FOCCO_EMPRESA)

    print(focco.apontamento(8421907, 234, '50', 1))
    