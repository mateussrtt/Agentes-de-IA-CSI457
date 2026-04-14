# Atividade — Agente Inteligente de Controle de Temperatura

Disciplina: CSI457 / CSI701 - Inteligência Artificial  
Universidade Federal de Ouro Preto

## Integrantes

- Adryan Martins Batista dos Santos  
- Lucas Lucio Silva Caixeta  
- Mateus Serretti Mendes Peixoto  

---

Parte 1 — Especificação do Agente

A especificação formal do agente foi desenvolvida previamente e está descrita no arquivo em LaTeX enviado junto ao trabalho.

Percepções
Temperatura atual
Temperatura desejada
Estado do sistema
Tempo/ciclo de execução
Tendência da temperatura
Histórico de ações anteriores
Ações
Ligar aquecedor
Desligar aquecedor
Ligar resfriador
Desligar resfriador
Manter
Função do Agente
f : P* → A

O agente utiliza as percepções recebidas para escolher a ação mais adequada.

Se a temperatura atual estiver abaixo da desejada, liga o aquecedor.
Se a temperatura atual estiver acima da desejada, liga o resfriador.
Se estiver próxima da meta, mantém o estado atual.

Também utiliza histórico e margem de tolerância para evitar oscilações frequentes.

Critério de Racionalidade
Manter a temperatura próxima da desejada
Reduzir consumo de energia
Evitar trocas constantes de estado
Garantir conforto térmico
Parte 2 — Implementação

A implementação foi realizada em Python no arquivo:

agente_temperatura.py

Classe principal:

AgenteTemperatura

O código possui métodos de:

percepção do ambiente
tomada de decisão
execução da ação
testes automáticos dos cenários propostos
Parte 3 — Testes

Foram executados os cenários solicitados pelo professor.

Cenário 1 — Oscilação
[24.9, 25.1, 24.8, 25.2]

Resultado: o agente manteve estabilidade, evitando mudanças desnecessárias.

Cenário 2 — Calor extremo
[30, 32, 35]

Resultado: o agente acionou o sistema de resfriamento.

Cenário 3 — Resfriamento gradual
[28, 27, 26, 25, 24]

Resultado: o agente reduziu a temperatura até atingir a faixa ideal.

Parte 4 — Análise Crítica
1. O agente corresponde à especificação?

Sim. O comportamento implementado segue as regras definidas anteriormente.

2. O uso de IA alterou decisões planejadas?

Não. A IA foi utilizada apenas como apoio técnico.

3. O agente pode ser considerado racional?

Sim. Suas ações são escolhidas visando atingir o objetivo proposto.

4. Principais limitações
Ambiente simplificado
Sem sensores reais
Não realiza previsão futura
5. Possíveis melhorias
Uso de aprendizado de máquina
Integração com sensores reais
Interface gráfica
Controle mais preciso da temperatura
Parte 5 — Uso de Inteligência Artificial

A IA foi utilizada como ferramenta de apoio nas seguintes etapas:

organização do projeto
estruturação textual
revisão lógica do código
auxílio técnico em Python

Todas as decisões finais foram revisadas e validadas pelo grupo.