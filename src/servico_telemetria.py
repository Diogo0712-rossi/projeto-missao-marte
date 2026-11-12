class ServicoTelemetriaEspacial:
    def enviar_relatorio(self, status: dict) -> bool:
        raise ConnectionError("Sem conexão com a estação terrestre em ambiente de teste.")

    def disparar_alerta_crise(self, nivel: str, mensagem: str) -> bool:
        raise ConnectionError("Sem conexão com a estação terrestre em ambiente de teste.")
