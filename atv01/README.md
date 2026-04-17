# Atividade — Agente Inteligente de Controle de Temperatura

Disciplina: CSI457 / CSI701 - Inteligência Artificial  
Universidade Federal de Ouro Preto

## Integrantes

- Adryan Martins Batista dos Santos  
- Lucas Lucio Silva Caixeta  
- Mateus Serretti Mendes Peixoto  

---

## Parte 1 — Especificação do Agente

A especificação formal do agente foi desenvolvida previamente e está descrita no arquivo em LaTeX enviado junto ao trabalho.

### Percepções

- Temperatura atual  
- Temperatura desejada  
- Estado do sistema  
- Tempo/ciclo de execução  
- Histórico de leituras anteriores  
- Tendência de aquecimento ou resfriamento do ambiente  

### Ações

- Ligar aquecedor  
- Ligar resfriador  
- Desligar sistema  
- Manter estado atual  

### Função do Agente

`f : P* → A`

O agente recebe percepções do ambiente e escolhe a melhor ação possível para atingir seu objetivo.

- Se a temperatura estiver acima da faixa ideal, aciona o resfriamento.  
- Se a temperatura estiver abaixo da faixa ideal, aciona o aquecimento.  
- Se a temperatura estiver adequada, desliga o sistema.  
- Caso não haja necessidade de mudança, mantém o estado atual.  

### Critério de Racionalidade

- Manter a temperatura próxima da desejada  
- Reduzir consumo de energia  
- Evitar acionamentos desnecessários  
- Garantir conforto térmico  
- Adaptar-se automaticamente ao ambiente  

---

## Parte 2 — Implementação

A implementação foi realizada em Python no arquivo `agente_temperatura.py`.

Classe principal: `AgenteTemperatura`

### O código possui:

- percepção do ambiente  
- memória de temperaturas anteriores  
- tomada de decisão automática  
- acionamento de aquecedor ou resfriador  
- simulação automática do ambiente  
- menu interativo para testes  
- histórico de ações realizadas  

---

## Parte 3 — Testes

Foram executadas simulações automáticas baseadas nos cenários propostos.

### Cenário 1 — Ambiente quente

Temperatura inicial: `35°C`  
Temperatura desejada: `25°C`

**Resultado:** o agente ligou o sistema de resfriamento e reduziu gradualmente a temperatura até a faixa ideal.

### Cenário 2 — Ambiente frio

Temperatura inicial: `18°C`  
Temperatura desejada: `25°C`

**Resultado:** o agente ligou o aquecedor e elevou gradualmente a temperatura até a faixa ideal.

### Cenário 3 — Simulação personalizada

O usuário pode informar qualquer temperatura inicial e qualquer temperatura desejada.

**Resultado:** o agente analisa a situação e controla automaticamente o ambiente até estabilizar.

---

## Parte 4 — Análise Crítica

### 1. O agente implementado corresponde à especificação?

Sim. O agente segue a proposta inicial, utilizando percepções, memória, ações e tomada de decisão para controle inteligente da temperatura.

### 2. O uso de IA alterou alguma decisão originalmente planejada?

Sim. A inteligência artificial aplicada no agente permitiu aprendizado simples do ambiente, autonomia nas decisões e adaptação automática durante a execução.

### 3. O agente pode ser considerado racional?

Sim. O agente escolhe ações com base nas informações disponíveis e busca atingir o objetivo com menor custo e maior eficiência.

### 4. Principais limitações

- Simulação simplificada do ambiente  
- Não utiliza sensores reais  
- Modelo térmico básico  
- Não considera fatores externos, como clima ou pessoas no local  

### 5. Possíveis melhorias

- Integração com sensores reais  
- Uso de aprendizado de máquina avançado  
- Interface gráfica completa  
- Controle remoto via internet  
- Otimização energética em tempo real  

---

## Parte 5 — Uso de Inteligência Artificial

A inteligência artificial foi aplicada diretamente no comportamento do agente por meio de:

- percepção do ambiente;  
- memória de estados anteriores;  
- tomada de decisão automática;  
- adaptação dinâmica ao ambiente;  
- escolha racional entre aquecer, resfriar ou manter.  

Esses recursos permitem que o agente atue de forma autônoma e eficiente.

---

## Arquivos Entregues

```text
README.md
app.py
src/agente_temperatura.py
templates/index.html
requirements.txt
Especificação_do_Agente_de_IA.tex
```

---

## Interface Web com Flask

Foi adicionada uma interface HTML integrada ao agente usando Flask.

### Como executar

1. Instale as dependencias:

```bash
pip install -r requirements.txt
```

2. Execute o servidor:

```bash
python app.py
```

3. Abra no navegador:

`http://127.0.0.1:5000`

### Como funciona a integracao

- A rota `GET /` retorna a pagina HTML.
- O formulario envia `temperatura_atual` e `temperatura_desejada` em JSON para `POST /decidir`.
- O backend cria o `AgenteTemperatura`, chama `decidir()` e devolve o resultado em JSON.
- O JavaScript exibe a acao do agente na tela.
