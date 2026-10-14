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

- `aurora_siger.ipynb` — notebook da Fase 1 com todo o código: telemetria, faixas seguras, algoritmo
  de verificação, script de execução, cálculo de autonomia energética e reflexão crítica.
- `fase2/mgpeb.py` — protótipo em Python da Fase 2 (MGPEB).
- `fase2/Relatorio_MGPEB_Aurora_Siger_Fase2.pdf` — relatório técnico da Fase 2.
- `README.md` — este arquivo.

## Fase 2 — MGPEB (pouso e estabilização da base)

Na Fase 2 o projeto passa da decolagem para o pouso em Marte. O script `fase2/mgpeb.py` simula como
a base organiza o pouso de cinco módulos (energia, habitação, suporte médico, laboratório e
logística) e reúne o que foi visto na fase:

- **Estruturas lineares:** uma fila com os módulos aguardando autorização, listas para os módulos
  pousados, em espera e em alerta, e uma pilha de eventos que permite desfazer a última ação.
- **Busca e ordenação:** busca linear e binária, e ordenação por inserção e por seleção para
  organizar a fila por prioridade.
- **Portas lógicas:** a autorização de pouso segue as funções abaixo, escritas com `if / elif / else`.
- **Função matemática:** a altura durante a descida (linear com o paraquedas e quadrática na
  frenagem dos retrofoguetes), usada para definir a altura de ignição.
- **Testes:** no final da execução, a função `testar_regras_limite()` confere dez casos de
  fronteira (por exemplo combustível em 19% e 20%, vento em 20 e 21 m/s, retrofoguetes a 700 e 699 m).

```
AUTORIZA = COMB_OK AND ATM_OK AND AREA_LIVRE AND (NOT ERRO_SENSORES)
ALERTA   = (NOT COMB_OK) OR ERRO_SENSORES
RETRO    = (ALTURA < LIMIAR) AND (VELOCIDADE > LIMITE) AND (NOT ERRO_SENSORES)
```

Para executar (só precisa do Python 3, sem instalar nada):

```
python fase2/mgpeb.py
```

Trecho da saída:

```
ENE-02  -> POUSO AUTORIZADO  (todas as condicoes satisfeitas)
HAB-01  -> POUSO AUTORIZADO  (todas as condicoes satisfeitas)
MED-05  -> ALERTA            (combustivel abaixo do minimo (18%))
LAB-03  -> ALERTA            (falha na integridade dos sensores)
LOG-04  -> ADIADO            (area de pouso ocupada)
Retrofoguetes disparam em t = 16.5 s, a 680 m de altura
Resultado: 10/10 testes aprovados
```

Os valores dos módulos e da descida são fictícios, escolhidos só para a simulação. O relatório com
os diagramas de portas lógicas, a modelagem matemática e a parte de ESG está em `fase2/`.

## Prints da execução

### Verificação de decolagem — algoritmo rodando contra os 10 cenários de teste
<img width="756" height="648" alt="image" src="https://github.com/user-attachments/assets/76a3b977-c9d8-4d81-8745-841a9b246570" />

### Análise energética — cálculo de autonomia
<img width="772" height="321" alt="image" src="https://github.com/user-attachments/assets/8adc6df6-3567-47d8-b819-61d967334073" />

## Integrantes do grupo

- Gabriel Eduardo Alvite Mendes — RM 576675
- Henrique Ferreira Rungue — RM 575739 
- Beatriz Lopes de Lima  — RM 575983

