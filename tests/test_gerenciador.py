import pytest
from src.gerenciador_recursos import (
    GerenciadorRecursosMarte,
    OxigenioInsuficienteError,
    AguaInsuficienteError,
    NivelEmergenciaInvalidoError,
)


@pytest.mark.parametrize(
    "astronautas,nivel,consumo_o2,esperado_o2",
    [
        (4, "NORMAL", 0.84, 3.36),
        (4, "ALERTA", 0.84, 2.688),
        (4, "CRITICO", 0.84, 1.68),
        (6, "NORMAL", 1.0, 6.0),
        (2, "CRITICO", 1.0, 1.0),
    ],
)
def test_calculo_consumo_diario_parametrizado(
    mock_telemetria, astronautas, nivel, consumo_o2, esperado_o2
):
    eclss = GerenciadorRecursosMarte(
        oxigenio_kg=100.0,
        agua_litros=300.0,
        astronautas=astronautas,
        telemetria=mock_telemetria,
    )
    eclss.definir_nivel_emergencia(nivel)
    resultado = eclss.calcular_consumo_diario(consumo_o2_por_pessoa=consumo_o2)
    assert resultado["oxigenio_kg"] == esperado_o2


def test_disparo_alerta_crise_telemetria(gerenciador, mock_telemetria):
    gerenciador.definir_nivel_emergencia("CRITICO")
    mock_telemetria.disparar_alerta_crise.assert_called_once_with(
        "CRITICO",
        "Alerta de crise no habitat! Estoque O2: 120.0kg",
    )


def test_excecao_nivel_emergencia_invalido(gerenciador):
    with pytest.raises(NivelEmergenciaInvalidoError):
        gerenciador.definir_nivel_emergencia("APOCALIPSE")


def test_excecao_oxigenio_insuficiente_no_consumo(mock_telemetria):
    eclss = GerenciadorRecursosMarte(
        oxigenio_kg=1.0,
        agua_litros=100.0,
        astronautas=4,
        telemetria=mock_telemetria,
    )
    with pytest.raises(OxigenioInsuficienteError):
        eclss.consumir_dia()


def test_excecao_agua_insuficiente_no_consumo(mock_telemetria):
    eclss = GerenciadorRecursosMarte(
        oxigenio_kg=100.0,
        agua_litros=2.0,
        astronautas=4,
        telemetria=mock_telemetria,
    )
    with pytest.raises(AguaInsuficienteError):
        eclss.consumir_dia()


def test_solicitar_cota_extra_valida_e_envia_relatorio(gerenciador, mock_telemetria):
    restante = gerenciador.solicitar_cota_extra_oxigenio(20.0)
    assert restante == 100.0
    mock_telemetria.enviar_relatorio.assert_called_once_with(
        {"evento": "COTA_EXTRA_O2", "quantidade": 20.0, "restante": 100.0}
    )


def test_solicitar_cota_extra_viola_reserva_minima(gerenciador):
    with pytest.raises(OxigenioInsuficienteError):
        gerenciador.solicitar_cota_extra_oxigenio(115.0)
