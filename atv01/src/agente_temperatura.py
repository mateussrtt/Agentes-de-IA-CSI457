import math
import time


class AgenteTemperatura:
    def __init__(self, temperatura_desejada=20, alpha=1, beta=1, sigma=0.5):
        self.Td = temperatura_desejada
        self.alpha = alpha
        self.beta = beta
        self.sigma = sigma

        self.sistema_ligado = False
        self.modo = None

        self.memoria_temperaturas = []
        self.historico = []

    def perceber(self, temperatura):
        return temperatura

    def armazenar(self, temperatura):
        self.memoria_temperaturas.append(temperatura)

    def custo(self, Ta):
        ligado = 1 if self.sistema_ligado else 0
        return self.alpha * abs(Ta - self.Td) + self.beta * ligado

    def limite_superior(self):
        return self.Td + 3 * self.sigma

    def limite_inferior(self):
        return self.Td - 3 * self.sigma

    def decidir(self, Ta):
        Ls = self.limite_superior()
        Li = self.limite_inferior()

        if Ta > Ls:
            self.sistema_ligado = True
            self.modo = "resfriando"
            acao = "ligar resfriador"

        elif Ta < Li:
            self.sistema_ligado = True
            self.modo = "aquecendo"
            acao = "ligar aquecedor"

        elif self.sistema_ligado and Li <= Ta <= Ls:
            self.sistema_ligado = False
            self.modo = None
            acao = "desligar sistema"

        else:
            acao = "manter"

        self.historico.append(acao)
        return acao

    def atualizar_temperatura(self, Ta):
        if self.sistema_ligado:

            if self.modo == "resfriando":
                Ta -= 2

            elif self.modo == "aquecendo":
                Ta += 2

        else:
            if Ta > 25:
                Ta -= 0.5
            elif Ta < 25:
                Ta += 0.5

        return round(Ta, 1)
    
    def mostrar_status(self, ciclo, Ta, acao):
        print("\n" + "=" * 55)
        print(f"⏱ CICLO {ciclo}")
        print("=" * 55)
        print(f"🌡 Temperatura atual : {Ta}°C")
        print(f"🎯 Temperatura alvo  : {self.Td}°C")
        print(f"📈 Limite superior  : {self.limite_superior():.1f}°C")
        print(f"📉 Limite inferior  : {self.limite_inferior():.1f}°C")
        print(f"⚡ Ação escolhida   : {acao}")
        print(f"🔌 Sistema ligado   : {self.sistema_ligado}")
        print(f"💰 Custo atual      : {self.custo(Ta):.2f}")
        print("=" * 55)

    def simular(self, temperatura_inicial, max_ciclos=20):
        Ta = temperatura_inicial

        for ciclo in range(1, max_ciclos + 1):
            self.armazenar(Ta)

            leitura = self.perceber(Ta)
            acao = self.decidir(leitura)

            self.mostrar_status(ciclo, Ta, acao)

            if (
                not self.sistema_ligado
                and self.limite_inferior() <= Ta <= self.limite_superior()
            ):
                print("\n✅ Temperatura estabilizada com sucesso.")
                break

            Ta = self.atualizar_temperatura(Ta)
            time.sleep(1)

    def mostrar_historico(self):
        print("\n📜 Histórico de ações:")
        for i, acao in enumerate(self.historico, 1):
            print(f"{i}. {acao}")


def menu():
    while True:
        print("\n===== AGENTE INTELIGENTE DE TEMPERATURA =====")
        print("1 - Simular ambiente quente")
        print("2 - Simular ambiente frio")
        print("3 - Simulação personalizada")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            agente = AgenteTemperatura(25)
            agente.simular(35)
            agente.mostrar_historico()

        elif opcao == "2":
            agente = AgenteTemperatura(25)
            agente.simular(18)
            agente.mostrar_historico()

        elif opcao == "3":
            try:
                atual = float(input("Temperatura atual: "))
                desejada = float(input("Temperatura desejada: "))

                agente = AgenteTemperatura(desejada)
                agente.simular(atual)
                agente.mostrar_historico()

            except:
                print("❌ Valor inválido.")

        elif opcao == "0":
            print("Encerrando...")
            break

        else:
            print("❌ Opção inválida.")


if __name__ == "__main__":
    menu()