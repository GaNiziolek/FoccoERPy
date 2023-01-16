
class ErroFocco(Exception):
    def __init__(self, *args: object) -> None:
        """
            Erro utilizado quando houve algum erro no retorno da API
        """
        super().__init__(*args)

class OrdemNaoEncontrada(Exception):
    def __init__(self, *args: object) -> None:
        """
            Ordem não encontrada
        """
        super().__init__("Ordem não encontrada")
