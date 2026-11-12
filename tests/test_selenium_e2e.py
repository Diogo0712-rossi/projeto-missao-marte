from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _get_painel_url() -> str:
    caminho_html = Path(__file__).resolve().parent.parent / "web" / "painel.html"
    return caminho_html.as_uri()


def test_solicitacao_cota_oxigenio_sucesso_e2e(browser):
    browser.get(_get_painel_url())

    campo_cota = browser.find_element(By.ID, "input-cota")
    botao = browser.find_element(By.ID, "btn-solicitar")

    campo_cota.clear()
    campo_cota.send_keys("15.0")
    botao.click()

    wait = WebDriverWait(browser, 5)
    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "mensagem-status"), "Solicitação aprovada com sucesso!"
        )
    )
    wait.until(
        EC.text_to_be_present_in_element((By.ID, "nivel-oxigenio"), "85.0")
    )

    assert browser.find_element(By.ID, "nivel-oxigenio").text == "85.0"


def test_solicitacao_cota_oxigenio_bloqueada_reserva_minima_e2e(browser):
    browser.get(_get_painel_url())

    campo_cota = browser.find_element(By.ID, "input-cota")
    botao = browser.find_element(By.ID, "btn-solicitar")

    campo_cota.clear()
    campo_cota.send_keys("95.0")
    botao.click()

    wait = WebDriverWait(browser, 5)
    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "mensagem-status"), "Erro: Reserva mínima de segurança atingida."
        )
    )
    wait.until(
        EC.text_to_be_present_in_element((By.ID, "status-sistema"), "ALERTA")
    )

    assert browser.find_element(By.ID, "nivel-oxigenio").text == "100.0"
