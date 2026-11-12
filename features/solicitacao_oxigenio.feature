# language: pt
Funcionalidade: Solicitação de cota extra de oxigênio no Habitat Marte
  Como um astronauta da Missão Marte
  Quero solicitar cotas extras de oxigênio pelo sistema ECLSS
  Para realizar atividades extraveiculares com segurança sem comprometer a reserva vital

  Cenário: Solicitação de cota extra em condições normais
    Dado que o habitat possui 100.0 kg de oxigênio, 300.0 litros de água e 4 astronautas
    Quando um astronauta solicita uma cota extra de 20.0 kg de oxigênio
    Então o estoque restante de oxigênio deve ser 80.0 kg
    E o relatório de telemetria deve ser enviado para a Terra

  Cenário: Solicitação negada por atingir reserva mínima de segurança em crise
    Dado que o habitat possui 25.0 kg de oxigênio, 300.0 litros de água e 4 astronautas
    Quando um astronauta solicita uma cota extra de 20.0 kg de oxigênio
    Então a solicitação deve ser bloqueada por oxigênio insuficiente
    E o estoque de oxigênio deve permanecer em 25.0 kg