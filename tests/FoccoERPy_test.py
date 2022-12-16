from dotenv import load_dotenv
import os

from ..FoccoERPy.Focco import Focco

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

def test_consulta_ordem():

    id_ordem = 1000000

    assert focco.consulta_ordem(id_ordem) is not None

def test_consulta_operacoes_ordem():

    id_roteiro = 10000000

    assert focco.consulta_operacoes_ordem(id_roteiro) is not None
