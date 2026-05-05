from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set, Tuple

Estado = Tuple[int, int]


@dataclass
class No:
    estado: Estado
    pai: Optional["No"] = None
    acao: Optional[str] = None
    g: float = 0.0


@dataclass
class ResultadoBusca:
    algoritmo: str
    encontrado: bool
    caminho: List[Estado]
    acoes: List[str]
    nos_explorados: int
    nos_expandidos: int
    estados_explorados: Set[Estado]

    @property
    def tamanho_caminho(self) -> Optional[int]:
        return len(self.acoes) if self.encontrado else None


class LabirintoBusca:
    def __init__(self, arquivo_labirinto: str) -> None:
        caminho = Path(arquivo_labirinto)
        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo nao encontrado: {arquivo_labirinto}")

        linhas = caminho.read_text(encoding="utf-8").splitlines()
        if not linhas:
            raise ValueError("Labirinto vazio.")

        self.altura = len(linhas)
        self.largura = max(len(linha) for linha in linhas)
        self.inicio: Optional[Estado] = None
        self.objetivo: Optional[Estado] = None
        self.paredes: Set[Estado] = set()

        for i, linha in enumerate(linhas):
            linha_completa = linha.ljust(self.largura, " ")
            for j, ch in enumerate(linha_completa):
                pos = (i, j)
                if ch == "A":
                    if self.inicio is not None:
                        raise ValueError("Labirinto deve ter apenas um inicio (A).")
                    self.inicio = pos
                elif ch == "B":
                    if self.objetivo is not None:
                        raise ValueError("Labirinto deve ter apenas um objetivo (B).")
                    self.objetivo = pos
                elif ch == " ":
                    continue
                else:
                    self.paredes.add(pos)

        if self.inicio is None or self.objetivo is None:
            raise ValueError("Labirinto deve conter inicio (A) e objetivo (B).")

    def h(self, estado: Estado) -> float:
        return abs(estado[0] - self.objetivo[0]) + abs(estado[1] - self.objetivo[1])

    def vizinhos(self, estado: Estado) -> List[Tuple[str, Estado, float]]:
        movimentos = [
            ("up", (-1, 0)),
            ("down", (1, 0)),
            ("left", (0, -1)),
            ("right", (0, 1)),
        ]
        saida: List[Tuple[str, Estado, float]] = []
        for acao, (di, dj) in movimentos:
            ni, nj = estado[0] + di, estado[1] + dj
            if 0 <= ni < self.altura and 0 <= nj < self.largura and (ni, nj) not in self.paredes:
                saida.append((acao, (ni, nj), 1.0))
        return saida

    @staticmethod
    def reconstruir(no_final: No) -> Tuple[List[Estado], List[str]]:
        caminho: List[Estado] = []
        acoes: List[str] = []
        atual: Optional[No] = no_final
        while atual is not None:
            caminho.append(atual.estado)
            if atual.acao is not None:
                acoes.append(atual.acao)
            atual = atual.pai
        caminho.reverse()
        acoes.reverse()
        return caminho, acoes

    def busca_largura(self) -> ResultadoBusca:
        fronteira = deque([No(self.inicio)])
        visitados = {self.inicio}
        estados_explorados: Set[Estado] = set()
        nos_expandidos = 0

        while fronteira:
            atual = fronteira.popleft()
            estados_explorados.add(atual.estado)
            if atual.estado == self.objetivo:
                caminho, acoes = self.reconstruir(atual)
                return ResultadoBusca("BFS", True, caminho, acoes, len(estados_explorados), nos_expandidos, estados_explorados)

            nos_expandidos += 1
            for acao, viz, custo in self.vizinhos(atual.estado):
                if viz not in visitados:
                    visitados.add(viz)
                    fronteira.append(No(viz, atual, acao, atual.g + custo))

        return ResultadoBusca("BFS", False, [], [], len(estados_explorados), nos_expandidos, estados_explorados)

    def busca_profundidade(self) -> ResultadoBusca:
        fronteira = [No(self.inicio)]
        visitados = {self.inicio}
        estados_explorados: Set[Estado] = set()
        nos_expandidos = 0

        while fronteira:
            atual = fronteira.pop()
            estados_explorados.add(atual.estado)
            if atual.estado == self.objetivo:
                caminho, acoes = self.reconstruir(atual)
                return ResultadoBusca("DFS", True, caminho, acoes, len(estados_explorados), nos_expandidos, estados_explorados)

            nos_expandidos += 1
            for acao, viz, custo in reversed(self.vizinhos(atual.estado)):
                if viz not in visitados:
                    visitados.add(viz)
                    fronteira.append(No(viz, atual, acao, atual.g + custo))

        return ResultadoBusca("DFS", False, [], [], len(estados_explorados), nos_expandidos, estados_explorados)

    def busca_prioridade(self, nome: str, prioridade: Callable[[No], float]) -> ResultadoBusca:
        fila: List[Tuple[float, int, No]] = []
        contador = count()
        no_inicial = No(self.inicio)
        heappush(fila, (prioridade(no_inicial), next(contador), no_inicial))

        melhor_g: Dict[Estado, float] = {self.inicio: 0.0}
        estados_explorados: Set[Estado] = set()
        nos_expandidos = 0

        while fila:
            _, _, atual = heappop(fila)
            if atual.g > melhor_g.get(atual.estado, float("inf")):
                continue

            estados_explorados.add(atual.estado)
            if atual.estado == self.objetivo:
                caminho, acoes = self.reconstruir(atual)
                return ResultadoBusca(nome, True, caminho, acoes, len(estados_explorados), nos_expandidos, estados_explorados)

            nos_expandidos += 1
            for acao, viz, custo in self.vizinhos(atual.estado):
                novo_g = atual.g + custo
                if novo_g < melhor_g.get(viz, float("inf")):
                    melhor_g[viz] = novo_g
                    novo_no = No(viz, atual, acao, novo_g)
                    heappush(fila, (prioridade(novo_no), next(contador), novo_no))

        return ResultadoBusca(nome, False, [], [], len(estados_explorados), nos_expandidos, estados_explorados)

    def busca_custo_uniforme(self) -> ResultadoBusca:
        return self.busca_prioridade("UCS", lambda no: no.g)

    def busca_gulosa(self) -> ResultadoBusca:
        return self.busca_prioridade("Gulosa", lambda no: self.h(no.estado))

    def busca_weighted_astar(self, peso: float = 2.0) -> ResultadoBusca:
        return self.busca_prioridade("Weighted A*", lambda no: no.g + peso * self.h(no.estado))

    def busca_idastar(self, max_iteracoes: int = 10_000) -> ResultadoBusca:
        limite = self.h(self.inicio)
        estados_explorados: Set[Estado] = set()
        nos_expandidos = 0
        iteracoes = 0

        while iteracoes < max_iteracoes:
            caminho_atual = [self.inicio]

            def dfs_limitado(no: No, g: float, limite_local: float) -> Tuple[Optional[No], float]:
                nonlocal nos_expandidos
                f = g + self.h(no.estado)
                if f > limite_local:
                    return None, f
                estados_explorados.add(no.estado)
                if no.estado == self.objetivo:
                    return no, f

                minimo = float("inf")
                nos_expandidos += 1
                for acao, viz, custo in self.vizinhos(no.estado):
                    if viz in caminho_atual:
                        continue
                    caminho_atual.append(viz)
                    filho = No(viz, no, acao, g + custo)
                    encontrado, novo_limite = dfs_limitado(filho, g + custo, limite_local)
                    if encontrado is not None:
                        return encontrado, novo_limite
                    minimo = min(minimo, novo_limite)
                    caminho_atual.pop()
                return None, minimo

            raiz = No(self.inicio)
            encontrado, proximo_limite = dfs_limitado(raiz, 0.0, limite)
            if encontrado is not None:
                caminho, acoes = self.reconstruir(encontrado)
                return ResultadoBusca("IDA*", True, caminho, acoes, len(estados_explorados), nos_expandidos, estados_explorados)
            if proximo_limite == float("inf"):
                break
            limite = proximo_limite
            iteracoes += 1

        return ResultadoBusca("IDA*", False, [], [], len(estados_explorados), nos_expandidos, estados_explorados)


def imprimir_metricas(resultado: ResultadoBusca) -> None:
    print("\n===== METRICAS =====")
    print(f"Algoritmo executado: {resultado.algoritmo}")
    print(f"Solucao encontrada: {resultado.encontrado}")
    print(f"Nos explorados: {resultado.nos_explorados}")
    print(f"Nos expandidos: {resultado.nos_expandidos}")
    print(f"Tamanho do caminho encontrado: {resultado.tamanho_caminho}")
    print("====================\n")


def executar_algoritmo(lab: LabirintoBusca, opcao: str) -> ResultadoBusca:
    if opcao == "1":
        return lab.busca_largura()
    if opcao == "2":
        return lab.busca_profundidade()
    if opcao == "3":
        return lab.busca_custo_uniforme()
    if opcao == "4":
        return lab.busca_gulosa()
    if opcao == "5":
        peso = float(input("Informe o peso w da Weighted A* (ex.: 2.0): ").strip())
        return lab.busca_weighted_astar(peso)
    if opcao == "6":
        return lab.busca_idastar()
    raise ValueError("Opcao invalida.")


def main() -> None:
    print("=== Labirinto: Simulador de Buscas ===")
    arquivo = input("Caminho do arquivo de labirinto (.txt): ").strip()
    lab = LabirintoBusca(arquivo)

    while True:
        print("\nEscolha o algoritmo:")
        print("1 - Busca em Largura (BFS)")
        print("2 - Busca em Profundidade (DFS)")
        print("3 - Busca de Custo Uniforme (UCS)")
        print("4 - Busca Gulosa")
        print("5 - Weighted A*")
        print("6 - IDA*")
        print("0 - Sair")
        opcao = input("Digite a opcao desejada [0-6]: ").strip()

        if opcao == "0":
            print("Encerrado.")
            break

        try:
            resultado = executar_algoritmo(lab, opcao)
            imprimir_metricas(resultado)
        except Exception as exc:
            print(f"Erro: {exc}")


if __name__ == "__main__":
    main()
