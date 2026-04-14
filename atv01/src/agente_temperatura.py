class AgenteTemperatura:
    def __init__(self, temperatura_desejada=25):
        self.temperatura_desejada = temperatura_desejada
        self.estado = "desligado"
        self.historico_temperaturas = []
        self.historico_acoes = []
        self.margem = 0.5 

    def perceber(self, temperatura_atual):
        self.historico_temperaturas.append(temperatura_atual)

        if len(self.historico_temperaturas) >= 2:
            anterior = self.historico_temperaturas[-2]

            if temperatura_atual > anterior:
                tendencia = "aumentando"
            elif temperatura_atual < anterior:
                tendencia = "diminuindo"
            else:
                tendencia = "estavel"
        else:
            tendencia = "estavel"

        return {
            "temperatura_atual": temperatura_atual,
            "temperatura_desejada": self.temperatura_desejada,
            "estado": self.estado,
            "tendencia": tendencia
        }

    def decidir(self, percepcao):
        atual = percepcao["temperatura_atual"]
        desejada = percepcao["temperatura_desejada"]

        if atual < desejada - self.margem:
            acao = "ligar aquecedor"
            self.estado = "aquecendo"

        elif atual > desejada + self.margem:
            acao = "ligar resfriador"
            self.estado = "resfriando"

        else:
            acao = "manter"

        self.historico_acoes.append(acao)
        return acao

    def agir(self, temperatura_atual):
        percepcao = self.perceber(temperatura_atual)
        acao = self.decidir(percepcao)

        print(f"Temperatura: {temperatura_atual}°C")
        print(f"Tendência: {percepcao['tendencia']}")
        print(f"Ação: {acao}")
        print("-" * 30)


def testar_cenario(nome, temperaturas):
    print(f"\n{nome}")
    print("=" * 30)

    agente = AgenteTemperatura()

    for temp in temperaturas:
        agente.agir(temp)


cenario1 = [24.9, 25.1, 24.8, 25.2]
cenario2 = [30, 32, 35]
cenario3 = [28, 27, 26, 25, 24]

testar_cenario("CENÁRIO 1 - Oscilação", cenario1)
testar_cenario("CENÁRIO 2 - Calor Extremo", cenario2)
testar_cenario("CENÁRIO 3 - Resfriamento Gradual", cenario3)