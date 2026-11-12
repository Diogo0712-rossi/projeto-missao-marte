import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.gerenciador_recursos import GerenciadorRecursosMarte


@pytest.fixture(scope="module")
def parametros_iniciais_habitat():
    return {
        "oxigenio_kg": 120.0,
        "agua_litros": 400.0,
        "astronautas": 4,
    }


@pytest.fixture(scope="function")
def mock_telemetria(mocker):
    mock = mocker.MagicMock()
    mock.enviar_relatorio.return_value = True
    mock.disparar_alerta_crise.return_value = True
    return mock


@pytest.fixture(scope="function")
def gerenciador(parametros_iniciais_habitat, mock_telemetria):
    instancia = GerenciadorRecursosMarte(
        oxigenio_kg=parametros_iniciais_habitat["oxigenio_kg"],
        agua_litros=parametros_iniciais_habitat["agua_litros"],
        astronautas=parametros_iniciais_habitat["astronautas"],
        telemetria=mock_telemetria,
    )
    yield instancia
    # Limpeza após cada teste
    instancia.nivel_emergencia = "NORMAL"


@pytest.fixture(scope="function")
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,720")

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("browser")
        if driver:
            os.makedirs("evidencias", exist_ok=True)
            driver.save_screenshot(f"evidencias/falha_{item.name}.png")
