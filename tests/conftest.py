
import os
from dotenv import load_dotenv
import pytest
from FoccoERPy import FoccoSession


@pytest.fixture(scope="session")
def focco_session():
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

    FOCCO_EMPRESA = int(FOCCO_EMPRESA)

    return FoccoSession(FOCCO_URL, FOCCO_TOKEN, FOCCO_EMPRESA)
