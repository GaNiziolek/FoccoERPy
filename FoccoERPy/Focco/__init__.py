from benedict import benedict
import numpy as np
from datetime import datetime
from requests.exceptions import HTTPError

import sys
sys.path.append("./")

from FoccoERPy import FoccoSession

from FoccoERPy.core import consulta_ordem
from FoccoERPy.core import consulta_operacoes_ordem
from FoccoERPy.core import apontamento_tempo_padrao

from FoccoERPy.exceptions import ErroFocco
from FoccoERPy.exceptions import OperacaoNaoEncontrada
from FoccoERPy.exceptions import SetorSemOperacoes
from FoccoERPy.exceptions import OrdemFinalizada
from FoccoERPy.exceptions import OrdemNaoEncontrada

class Focco():
    def __init__(self, server_url: str, token_acesso: str, id_empresa: int) -> None:

        self.Session = FoccoSession.FoccoSession(server_url, token_acesso, id_empresa)

    def apontamento_cego_por_setor(self, id_ordem: int, id_recurso: int, cod_centro_trabalho: str, quantidade: float) -> dict:
        """
            Antes de realizar o apontamento, é feito uma busca nas operações do roteiro deste centro de trabalho,
            e a operação a ser apontada é sempre a próxima operação com a menor quantidade apontada, por exemplo:
                Para uma peça com 4 operações, sendo a quantidade apontada de cada uma -> (1,1,0,0), o próxima
                operação que será escolhida para apontar será a 3.
        """

        finalizar_ordem = False

        # Busca informações da Ordem
        info_ordem = consulta_ordem(self.Session, id_ordem)

        if info_ordem.get('Finalizada'):
            raise OrdemFinalizada(id_ordem)

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

        if not operacoes_setor:
            raise SetorSemOperacoes(id_ordem, cod_centro_trabalho)

        # A proxima operacao a ser apontada é a subsequente a operacao que tiver a maior qtd_apontada
        index_op = np.argmin(lista_qtd)

        operacao_apontamento = operacoes_setor[index_op]

        if operacao_apontamento.get('ID') == ultima_operacao.get('ID') and qtd_apontada + quantidade == info_ordem.get('Quantidade') :
            # Se o ID for igual da última operação da ordem e
            # se a quantidade que ja foi apontada + a quantidade que está
            # sendo apontada agora é igual a quantidade total da ordem
            finalizar_ordem = True

        resposta_focco = apontamento_tempo_padrao(
                            self.Session,
                            id_ordem_roteiro = operacao_apontamento.get('ID'),
                            quantidade       = quantidade,
                            id_recurso       = id_recurso,
                            data             = datetime.now(),
                            finalizar        = finalizar_ordem
                        )
        id_apontamento = resposta_focco.get('Value')

        return {
            'id_apontamento': id_apontamento, 
            'finalizou_ordem': finalizar_ordem
        }

    def apontamento_por_sequencia(self, id_ordem: int, id_recurso: int, cod_centro_trabalho: str, quantidade: float, seq_operacao: int, pode_finalizar: bool = False) -> dict:
        """
        Realiza o apontamento da N esima operacão desse roteiro e centro de trabalho. 
        Se :pode_finalizar = True, e a operação requisitada for a última quantidade e operacão do centro de trabalho, entao finaliza a ordem

        Retorna o ID do apontamento
        """

        finalizar_ordem = False

        # Busca informações da Ordem
        info_ordem = consulta_ordem(self.Session, id_ordem)

        if info_ordem.get('Finalizada'):
            raise OrdemFinalizada(id_ordem)

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

        if not operacoes_setor:
            raise SetorSemOperacoes(id_ordem, cod_centro_trabalho)

        try:
            operacao_apontamento = operacoes_setor[seq_operacao - 1]
        except IndexError:
            raise OperacaoNaoEncontrada(id_ordem, seq_operacao, cod_centro_trabalho)

        if (
                operacao_apontamento.get('ID') == ultima_operacao.get('ID')   # Se o ID da ordem for igual ao ID da última ordem desse Centro de trabalho
                and qtd_apontada + quantidade == info_ordem.get('Quantidade') # se a qtd dessa operação que já está apontada + qtd a apontar agora for igual a qtd total da ordem
                and pode_finalizar
            ) :
            # Se o ID for igual da última operação da ordem e
            # se a quantidade que ja foi apontada + a quantidade que está
            # sendo apontada agora é igual a quantidade total da ordem
            finalizar_ordem = True

        resposta_focco = apontamento_tempo_padrao(
                            self.Session,
                            id_ordem_roteiro = operacao_apontamento.get('ID'),
                            quantidade       = quantidade,
                            id_recurso       = id_recurso,
                            data             = datetime.now(),
                            finalizar        = finalizar_ordem
                        )
        id_apontamento = resposta_focco.get('Value')

        return {
            'id_apontamento': id_apontamento, 
            'finalizou_ordem': finalizar_ordem
        }
     
if __name__ == '__main__':

    from dotenv import load_dotenv
    import os

    from FoccoERPy.core import impressao_etiqueta

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

    #print(focco.apontamento_por_sequencia(8792710, 229, '4', 1, 1))

    print(impressao_etiqueta(
                session=focco.Session,
                bearer='CfDJ8LKjHueZYEBBpHKrwAhYEE46auGpUjNxycS05P57ui3ADoFNv_LmuPWo0DI-PGx_bfD39U5GLYmw66PnpIry6SP_bZHlysdfog_40mVBU-bwX3oN9iT92zEnLlAPrNl4BBtCb1P-QK5pncunAr4WgB_p-FkgFC7ycIeyPKpfRKFZEZIvhLy5diIIPBXdXUyrm-6SMCXUu-eOwLk7EL7HC5I1pZAQ-EFscTHK1O4vSC-ibYF8HaTvW-QrUjqoWeJk-ZQAEuYnXLrJfMoRrixToNHxthaAJGGOcVL9nmEc9-Xn4AQKpKVVqE3U1U60goxuKtsatcQq4vcCVwpII9LZZoPNKOkx5UIqHvEX_roQFbiH3widephKAbrcXEFOZQhLVOkqLTeXL8E4JZuoTmXohMxxwiyZ2xgiSRXjaZjfsKsmIsfdeKejVQ5LkHvmCZRd8WHHoqVMTuMd750IYDcoUbXFrursCfayOmaCE7PwAPxepBWRH-C24M-unK0gp-MkaA',
                modelo_etiqueta='(203)-Etiqueta Produção - GERAL EMBALAGEM',
                id_empresa=2,
                id_apontamento=25130075, 
                qtd_copias=1,
                nome_impressora='ZebraTesteFocco',
                chave_servico_impressao='SERVER-INUSITTA'
        ))
