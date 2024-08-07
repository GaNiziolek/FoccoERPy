
def test_consulta_ordem(focco_session):
    from FoccoERPy import consulta_ordem

    id_ordem = 1000000

    ordem = consulta_ordem(focco_session, id_ordem)

    assert ordem is not None

def test_consulta_operacoes_ordem(focco_session):
    from FoccoERPy import  consulta_operacoes_ordem

    id_roteiro = 10000000

    operacoes = consulta_operacoes_ordem(focco_session, id_roteiro)

    assert operacoes is not None
