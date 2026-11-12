import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from src.gerenciador_recursos import GerenciadorRecursosMarte, OxigenioInsuficienteError

scenarios("../features/solicitacao_oxigenio.feature")


@pytest.fixture
def contexto_bdd():
    return {"eclss": None, "erro": None}


@given(
    parsers.parse(
        "que o habitat possui {oxigenio:f} kg de oxigênio, {agua:f} litros de água e {astronautas:d} astronautas"
    )
)
def configurar_habitat(contexto_bdd, mock_telemetria, oxigenio, agua, astronautas):
    contexto_bdd["eclss"] = GerenciadorRecursosMarte(
        oxigenio_kg=oxigenio,
        agua_litros=agua,
        astronautas=astronautas,
        telemetria=mock_telemetria,
    )


@when(parsers.parse("um astronauta solicita uma cota extra de {quantidade:f} kg de oxigênio"))
def solicitar_cota(contexto_bdd, quantidade):
    try:
        contexto_bdd["eclss"].solicitar_cota_extra_oxigenio(quantidade)
    except OxigenioInsuficienteError as exc:
        contexto_bdd["erro"] = exc


@then(parsers.parse("o estoque restante de oxigênio deve ser {esperado:f} kg"))
def verificar_estoque_restante(contexto_bdd, esperado):
    assert contexto_bdd["erro"] is None
    assert contexto_bdd["eclss"].oxigenio_kg == esperado


@then("o relatório de telemetria deve ser enviado para a Terra")
def verificar_envio_telemetria(mock_telemetria):
    mock_telemetria.enviar_relatorio.assert_called_once()


@then("a solicitação deve ser bloqueada por oxigênio insuficiente")
def verificar_bloqueio_crise(contexto_bdd):
    assert isinstance(contexto_bdd["erro"], OxigenioInsuficienteError)


@then(parsers.parse("o estoque de oxigênio deve permanecer em {esperado:f} kg"))
def verificar_estoque_inalterado(contexto_bdd, esperado):
    assert contexto_bdd["eclss"].oxigenio_kg == esperado
