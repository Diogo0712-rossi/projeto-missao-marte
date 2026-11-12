from src.servico_telemetria import ServicoTelemetriaEspacial


class OxigenioInsuficienteError(Exception):
    pass


class AguaInsuficienteError(Exception):
    pass


class NivelEmergenciaInvalidoError(Exception):
    pass


class GerenciadorRecursosMarte:
    NIVEIS_EMERGENCIA = {
        "NORMAL": 1.0,
        "ALERTA": 0.8,
        "CRITICO": 0.5,
    }

    def __init__(
        self,
        oxigenio_kg: float,
        agua_litros: float,
        astronautas: int,
        telemetria: ServicoTelemetriaEspacial = None,
    ):
        if astronautas <= 0:
            raise ValueError("Número de astronautas deve ser maior que zero.")
        self.oxigenio_kg = float(oxigenio_kg)
        self.agua_litros = float(agua_litros)
        self.astronautas = int(astronautas)
        self.nivel_emergencia = "NORMAL"
        self.telemetria = telemetria or ServicoTelemetriaEspacial()

    def definir_nivel_emergencia(self, nivel: str):
        nivel_upper = nivel.upper()
        if nivel_upper not in self.NIVEIS_EMERGENCIA:
            raise NivelEmergenciaInvalidoError(f"Nível inválido: {nivel}")
        self.nivel_emergencia = nivel_upper
        if self.nivel_emergencia == "CRITICO":
            self.telemetria.disparar_alerta_crise(
                self.nivel_emergencia,
                f"Alerta de crise no habitat! Estoque O2: {self.oxigenio_kg}kg",
            )

    def calcular_consumo_diario(self, consumo_o2_por_pessoa: float = 0.84, consumo_agua_por_pessoa: float = 3.0) -> dict:
        fator_cota = self.NIVEIS_EMERGENCIA[self.nivel_emergencia]
        o2_diario = round(self.astronautas * consumo_o2_por_pessoa * fator_cota, 4)
        agua_diaria = round(self.astronautas * consumo_agua_por_pessoa * fator_cota, 4)
        return {"oxigenio_kg": o2_diario, "agua_litros": agua_diaria}

    def consumir_dia(self, consumo_o2_por_pessoa: float = 0.84, consumo_agua_por_pessoa: float = 3.0):
        consumo = self.calcular_consumo_diario(consumo_o2_por_pessoa, consumo_agua_por_pessoa)
        if self.oxigenio_kg < consumo["oxigenio_kg"]:
            raise OxigenioInsuficienteError("Estoque de oxigênio insuficiente para o ciclo diário.")
        if self.agua_litros < consumo["agua_litros"]:
            raise AguaInsuficienteError("Estoque de água insuficiente para o ciclo diário.")
        self.oxigenio_kg = round(self.oxigenio_kg - consumo["oxigenio_kg"], 4)
        self.agua_litros = round(self.agua_litros - consumo["agua_litros"], 4)

    def solicitar_cota_extra_oxigenio(self, quantidade_kg: float) -> float:
        if quantidade_kg <= 0:
            raise ValueError("Quantidade solicitada deve ser positiva.")
        if self.oxigenio_kg - quantidade_kg < 10.0:
            raise OxigenioInsuficienteError("Reserva mínima de segurança (10kg) não pode ser violada.")
        self.oxigenio_kg = round(self.oxigenio_kg - quantidade_kg, 4)
        self.telemetria.enviar_relatorio(
            {"evento": "COTA_EXTRA_O2", "quantidade": quantidade_kg, "restante": self.oxigenio_kg}
        )
        return self.oxigenio_kg
