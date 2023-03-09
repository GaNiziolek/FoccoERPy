
class ErroFocco(Exception):
    def __init__(self, *args: object) -> None:
        """
            Erro utilizado quando houve algum erro no retorno da API
        """
        super().__init__(*args)

class OrdemNaoEncontrada(Exception):
    def __init__(self, id_ordem: int):
        """
            Ordem não encontrada
        """
        self.id_ordem = id_ordem

        self.msg   = 'Ordem "{id_ordem}" não encontrada'
        super().__init__(self.msg)

class OperacaoNaoEncontrada(Exception):
    def __init__(self, id_ordem: int, seq_operacao: int, cod_centro_trabalho: int):
        """
            Operação não encontrada
        """
        self.id_ordem = id_ordem
        self.seq_operacao = seq_operacao,
        self.cod_centro_trabalho = cod_centro_trabalho

        self.msg = f"Não é possível encontrar a operação número {seq_operacao} na ordem '{id_ordem}' e setor {cod_centro_trabalho}"
        super().__init__(self.msg)

class SetorSemOperacoes(Exception):
    def __init__(self, id_ordem: int, cod_centro_trabalho: int):
        """
            Operação não encontrada
        """
        self.id_ordem = id_ordem
        self.cod_centro_trabalho = cod_centro_trabalho

        self.msg = f"A ordem '{id_ordem}' não possui nenhuma operação no setor {cod_centro_trabalho}."
        super().__init__(self.msg)

class OrdemFinalizada(Exception):
    def __init__(self, id_ordem: int):
        """
            Ordem está finalizada
        """
        self.id_ordem = id_ordem

        self.msg = f"A ordem '{id_ordem}' está finalizada."
        super().__init__(self.msg)
