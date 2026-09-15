# Aurora Siger — Relatório Operacional de Pré-Decolagem

> Simulação de verificação pré-decolagem da nave fictícia Aurora Siger: um algoritmo em Python
> analisa telemetria (temperatura, energia, pressão dos tanques e status dos módulos críticos)
> para liberar ou abortar a decolagem, testado contra 10 cenários distintos, além de calcular a
> autonomia energética da nave. Projeto acadêmico (FIAP).

## Sobre o projeto

A missão Aurora Siger acompanha os instantes finais antes da decolagem (T-15 minutos). A partir
de dados fictícios de telemetria — temperatura interna e externa, integridade estrutural, nível
de energia, pressão dos tanques de combustível e oxidante, e status dos módulos críticos — o
notebook decide automaticamente se a nave está **PRONTA PARA DECOLAR** ou se a **DECOLAGEM deve
ser ABORTADA**, informando o motivo específico da falha, e estima por quantas horas a energia
disponível sustenta a operação de decolagem.

O projeto está organizado em partes, cada uma cobrindo um item do enunciado:

| Parte | Conteúdo | Item do enunciado |
|---|---|---|
| 1 e 2 | Faixas seguras e telemetria (10 cenários de teste) | 5.1 |
| 3 | Algoritmo de verificação | 5.2 |
| 4 | Script em Python (execução) | 5.3 |
| 5 | Análise energética | 5.4 |
| 6 | Análise assistida por IA | 5.5 |
| 7 | Reflexão crítica | 5.6 |

## Algoritmo de verificação

A função `verificar_decolagem` testa cinco condições **em sequência**: integridade estrutural →
energia → temperaturas (interna e externa) → pressão dos tanques (combustível e oxidante) →
status dos módulos críticos. A primeira condição que falhar já retorna `"DECOLAGEM ABORTADA"`
com o motivo específico; só chega a `"PRONTO PARA DECOLAR"` quem passar por todas elas. A
verificação dos módulos críticos (propulsão, navegação, suporte de vida, comunicação) percorre
**todos** os módulos, não apenas o primeiro — um `for` garante que qualquer módulo offline seja
detectado, não só o primeiro da lista.

## Como executar

1. Abra o arquivo `aurora_siger.ipynb` no [Google Colab](https://colab.research.google.com/)
   (Arquivo → Abrir notebook → aba GitHub → cole o link deste repositório) ou no Jupyter
   Notebook / VS Code, localmente.
2. Execute as células em ordem, de cima para baixo (`Shift + Enter` em cada uma, ou
   "Executar tudo" / "Run All").
3. O resultado da verificação para o cenário ativo aparece impresso logo após a célula de
   execução do script (`STATUS: ...`), seguido do resultado para os 10 cenários de teste; a
   autonomia energética estimada aparece na última célula de código.

## Exemplo de execução

Resultado do algoritmo para o cenário ativo (`teste_01`):

```
STATUS: PRONTO PARA DECOLAR
MOTIVO: todas as verificações passaram
```

Resultado para os 10 cenários de teste definidos na Parte 2 — cobrindo o caso de sucesso e cada
tipo de falha (estrutura, energia, temperatura, pressão, módulo):

```
teste_01: PRONTO PARA DECOLAR — todas as verificações passaram
teste_02: DECOLAGEM ABORTADA — energia insuficiente
teste_03: PRONTO PARA DECOLAR — todas as verificações passaram
teste_04: DECOLAGEM ABORTADA — temperatura interna fora da faixa
teste_05: PRONTO PARA DECOLAR — todas as verificações passaram
teste_06: PRONTO PARA DECOLAR — todas as verificações passaram
teste_07: DECOLAGEM ABORTADA — estrutura comprometida
teste_08: PRONTO PARA DECOLAR — todas as verificações passaram
teste_09: DECOLAGEM ABORTADA — energia insuficiente
teste_10: PRONTO PARA DECOLAR — todas as verificações passaram
```

Análise energética para o cenário ativo:

```
Energia disponível: 49.70 kWh
Autonomia estimada: 2.76 horas
```

> ⚠️ *Estes valores são de exemplo. Se o grupo ajustar a telemetria, as faixas seguras ou os
> parâmetros de consumo/perdas, os resultados mudam de acordo — os cálculos continuam
> funcionando sem precisar alterar o código.*

## Estrutura do repositório

- `aurora_siger.ipynb` — notebook com todo o código: telemetria, faixas seguras, algoritmo de
  verificação, script de execução, cálculo de autonomia energética e reflexão crítica.
- `README.md` — este arquivo.

## Prints da execução
<img width="756" height="648" alt="image" src="https://github.com/user-attachments/assets/76a3b977-c9d8-4d81-8745-841a9b246570" />
<img width="772" height="321" alt="image" src="https://github.com/user-attachments/assets/8adc6df6-3567-47d8-b819-61d967334073" />

## Integrantes do grupo

- Gabriel Eduardo Alvite Mendes — RM 576675
- Henrique Ferreira Rungue — RM 575739 
- Beatriz Lopes de Lima  — RM 575983

