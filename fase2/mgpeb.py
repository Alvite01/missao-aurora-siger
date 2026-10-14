"""
MGPEB - Modulo de Gerenciamento de Pouso e Estabilizacao de Base
Missao Aurora Siger - FIAP - Fase 2 (PBL)

Prototipo simples que simula, de forma didatica, como a base Aurora Siger
organiza o pouso de seus modulos em Marte. O programa usa apenas recursos
basicos do Python (listas, dicionarios, funcoes, if/elif/else, while e for),
sem bibliotecas externas.

Estrutura do arquivo:
  1. Dados dos modulos e parametros da simulacao
  2. Estruturas lineares: fila, listas auxiliares e pilha
  3. Algoritmos de busca (linear e binaria)
  4. Algoritmos de ordenacao (insercao e selecao)
  5. Regras logicas (funcoes booleanas = portas AND, OR, NOT)
  6. Modelo matematico da descida (funcao linear + funcao quadratica)
  7. Simulacao completa (funcao principal)

Para executar:  python mgpeb.py
"""

# ---------------------------------------------------------------------------
# 1. DADOS DOS MODULOS E PARAMETROS DA SIMULACAO
# ---------------------------------------------------------------------------
# Cada modulo e um dicionario com os atributos pedidos na atividade.
# prioridade: 1 = mais alta | criticidade: 1 (baixa) a 5 (maxima)
# combustivel em % | massa em kg | eta = horario estimado de chegada a orbita
# Os valores abaixo sao simulados (nao sao dados reais de missao).

MODULOS_INICIAIS = [
    {"id": "HAB-01", "nome": "Habitacao", "carga": "habitat inflavel",
     "prioridade": 2, "combustivel": 62, "massa": 5200, "criticidade": 4,
     "eta": "10:15", "sensores_ok": True, "area_livre": True},
    {"id": "ENE-02", "nome": "Energia", "carga": "paineis solares",
     "prioridade": 1, "combustivel": 48, "massa": 4100, "criticidade": 5,
     "eta": "10:05", "sensores_ok": True, "area_livre": True},
    {"id": "LAB-03", "nome": "Laboratorio cientifico", "carga": "sensores cientificos",
     "prioridade": 4, "combustivel": 35, "massa": 3300, "criticidade": 2,
     "eta": "10:40", "sensores_ok": False, "area_livre": True},
    {"id": "LOG-04", "nome": "Logistica", "carga": "equipamento de mineracao",
     "prioridade": 5, "combustivel": 71, "massa": 6000, "criticidade": 3,
     "eta": "11:10", "sensores_ok": True, "area_livre": False},
    {"id": "MED-05", "nome": "Suporte medico", "carga": "equipamento medico",
     "prioridade": 3, "combustivel": 18, "massa": 2800, "criticidade": 5,
     "eta": "10:25", "sensores_ok": True, "area_livre": True},
]

# Limites usados nas regras de decisao
COMBUSTIVEL_MINIMO = 20    # % minimo de combustivel para tentar o pouso
VENTO_MAXIMO = 20          # m/s - limite de vento na area de pouso
VENTO_ATUAL = 12           # m/s - condicao atmosferica simulada

# Parametros do modelo de descida (secao 6)
ALTURA_ENTRADA = 2000.0    # m   - altura ao abrir o paraquedas
VEL_PARAQUEDAS = 80.0      # m/s - velocidade de descida sob paraquedas
DESACEL_RETRO = 5.0        # m/s2 - desaceleracao liquida dos retrofoguetes
VEL_POUSO = 2.0            # m/s - velocidade desejada no toque
LIMIAR_ALTURA = 700.0      # m   - altura abaixo da qual os retros podem disparar
LIMITE_VELOCIDADE = 20.0   # m/s - velocidade acima da qual os retros sao necessarios


# ---------------------------------------------------------------------------
# 2. ESTRUTURAS LINEARES
# ---------------------------------------------------------------------------
# FILA (FIFO): modulos aguardando autorizacao. Entra no fim, sai do inicio.
# LISTAS: modulos pousados, em espera e em alerta.
# PILHA (LIFO): historico de eventos; permite desfazer a ultima acao.

fila_pouso = []        # fila principal
lista_pousados = []    # modulos que ja pousaram
lista_espera = []      # modulos adiados (ex.: area ocupada)
lista_alerta = []      # modulos com problema critico
pilha_eventos = []     # pilha de eventos (ultimo a entrar = primeiro a sair)


def enfileirar(fila, modulo):
    """Coloca um modulo no final da fila."""
    fila.append(modulo)


def desenfileirar(fila):
    """Remove e devolve o modulo que esta no inicio da fila (ou None)."""
    if len(fila) == 0:
        return None
    return fila.pop(0)


def empilhar(pilha, evento):
    """Registra um evento no topo da pilha."""
    pilha.append(evento)


def desempilhar(pilha):
    """Remove e devolve o evento do topo da pilha (ou None)."""
    if len(pilha) == 0:
        return None
    return pilha.pop()


def cadastrar_modulos(modulos):
    """Cadastra os modulos na fila principal."""
    for modulo in modulos:
        enfileirar(fila_pouso, dict(modulo))   # dict() copia o original


def registrar_evento(acao, modulo, destino):
    """Empilha um evento para manter historico e permitir desfazer."""
    empilhar(pilha_eventos, {"acao": acao, "id": modulo["id"], "destino": destino})


def desfazer_ultimo_evento():
    """Desfaz o ultimo evento: o modulo volta para o INICIO da fila."""
    evento = desempilhar(pilha_eventos)
    if evento is None:
        print("   Nenhum evento para desfazer.")
        return
    destinos = {"pousados": lista_pousados, "espera": lista_espera,
                "alerta": lista_alerta}
    lista = destinos[evento["destino"]]
    for i in range(len(lista)):
        if lista[i]["id"] == evento["id"]:
            modulo = lista.pop(i)
            fila_pouso.insert(0, modulo)
            print("   Desfeito: " + modulo["id"] + " voltou ao inicio da fila.")
            return


# ---------------------------------------------------------------------------
# 3. ALGORITMOS DE BUSCA
# ---------------------------------------------------------------------------

def busca_menor(lista, campo):
    """Busca linear do modulo com o MENOR valor de um campo. Custo O(n)."""
    if len(lista) == 0:
        return None
    menor = lista[0]
    for modulo in lista:
        if modulo[campo] < menor[campo]:
            menor = modulo
    return menor


def busca_linear(lista, campo, valor):
    """Busca linear: devolve todos os modulos com campo == valor. Custo O(n)."""
    encontrados = []
    for modulo in lista:
        if modulo[campo] == valor:
            encontrados.append(modulo)
    return encontrados


def busca_binaria_prioridade(lista_ordenada, prioridade):
    """
    Busca binaria pela prioridade. Custo O(log n).
    ATENCAO: a lista PRECISA estar ordenada por prioridade.
    Devolve o modulo encontrado ou None.
    """
    inicio = 0
    fim = len(lista_ordenada) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        valor = lista_ordenada[meio]["prioridade"]
        if valor == prioridade:
            return lista_ordenada[meio]
        elif valor < prioridade:
            inicio = meio + 1
        else:
            fim = meio - 1
    return None


# ---------------------------------------------------------------------------
# 4. ALGORITMOS DE ORDENACAO
# ---------------------------------------------------------------------------

def ordenacao_insercao(lista, chave):
    """
    Ordenacao por insercao (estavel). Custo O(n2) no pior caso, mas rapida
    para listas pequenas ou quase ordenadas - adequada a um sistema embarcado
    com pouca memoria. 'chave' e uma funcao que devolve o criterio do modulo.
    """
    for i in range(1, len(lista)):
        atual = lista[i]
        j = i - 1
        while j >= 0 and chave(lista[j]) > chave(atual):
            lista[j + 1] = lista[j]
            j = j - 1
        lista[j + 1] = atual


def ordenacao_selecao(lista, campo):
    """Ordenacao por selecao pelo menor valor de um campo. Custo O(n2)."""
    for i in range(len(lista) - 1):
        posicao_menor = i
        for j in range(i + 1, len(lista)):
            if lista[j][campo] < lista[posicao_menor][campo]:
                posicao_menor = j
        lista[i], lista[posicao_menor] = lista[posicao_menor], lista[i]


def criterio_pouso(modulo):
    """Criterio da fila: menor prioridade numerica primeiro; em empate, a
    maior criticidade primeiro (por isso o sinal negativo)."""
    return (modulo["prioridade"], -modulo["criticidade"])


# ---------------------------------------------------------------------------
# 5. REGRAS LOGICAS (FUNCOES BOOLEANAS)
# ---------------------------------------------------------------------------
# Cada funcao abaixo corresponde a um diagrama de portas logicas do relatorio.

def combustivel_ok(modulo):
    """COMB_OK = combustivel >= limite minimo."""
    return modulo["combustivel"] >= COMBUSTIVEL_MINIMO


def atmosfera_ok(vento_atual=None):
    """ATM_OK = vento atual <= limite; aceita valor para testar fronteiras."""
    if vento_atual is None:
        vento_atual = VENTO_ATUAL
    return vento_atual <= VENTO_MAXIMO


def pouso_autorizado(comb_ok, atm_ok, area_livre, erro_sensores):
    """AUTORIZA = COMB_OK AND ATM_OK AND AREA_LIVRE AND (NOT ERRO_SENSORES)"""
    return comb_ok and atm_ok and area_livre and (not erro_sensores)


def modulo_em_alerta(comb_ok, erro_sensores):
    """ALERTA = (NOT COMB_OK) OR ERRO_SENSORES"""
    return (not comb_ok) or erro_sensores


def disparar_retro(altura, velocidade, erro_sensores):
    """RETRO = (ALTURA < LIMIAR) AND (VELOCIDADE > LIMITE) AND (NOT ERRO_SENSORES)"""
    return (altura < LIMIAR_ALTURA) and (velocidade > LIMITE_VELOCIDADE) and (not erro_sensores)


def decidir_pouso(modulo, vento_atual=None):
    """
    Aplica as funcoes booleanas com if / elif / else e devolve:
    (decisao, motivo). A decisao e uma das categorias: 'pousar',
    'alerta' ou 'espera'.
    """
    comb = combustivel_ok(modulo)
    atm = atmosfera_ok(vento_atual)
    area = modulo["area_livre"]
    erro = not modulo["sensores_ok"]

    if pouso_autorizado(comb, atm, area, erro):
        return "pousar", "todas as condicoes satisfeitas"
    elif modulo_em_alerta(comb, erro):
        if not comb:
            return "alerta", "combustivel abaixo do minimo (" + str(modulo["combustivel"]) + "%)"
        return "alerta", "falha na integridade dos sensores"
    elif not atm:
        return "espera", "vento acima do limite"
    else:
        return "espera", "area de pouso ocupada"


# ---------------------------------------------------------------------------
# 6. MODELO MATEMATICO DA DESCIDA
# ---------------------------------------------------------------------------
# Fase 1 (paraquedas): funcao LINEAR   h(t) = H0 - v0 * t
# Fase 2 (retrofoguetes): funcao QUADRATICA  h(t) = h1 - v0*t + (a/2)*t^2

def altura_paraquedas(t):
    """Altura (m) em funcao do tempo (s) durante a fase de paraquedas."""
    return ALTURA_ENTRADA - VEL_PARAQUEDAS * t


def altura_retro(t, h_ignicao):
    """Altura (m) durante a frenagem, t contado desde a ignicao dos retros."""
    return h_ignicao - VEL_PARAQUEDAS * t + (DESACEL_RETRO / 2.0) * t * t


def altura_minima_ignicao():
    """Altura minima de ignicao: h = (v0^2 - vf^2) / (2a)."""
    return (VEL_PARAQUEDAS ** 2 - VEL_POUSO ** 2) / (2.0 * DESACEL_RETRO)


def simular_descida():
    """Percorre a descida de 0,5 em 0,5 s ate a regra RETRO disparar."""
    print("\n[Modelo de descida]")
    h_min = altura_minima_ignicao()
    print("   Altura minima de ignicao (modelo): %.1f m" % h_min)
    print("   Limiar adotado (LIMIAR_ALTURA):    %.1f m (margem de %.0f%%)"
          % (LIMIAR_ALTURA, (LIMIAR_ALTURA / h_min - 1) * 100))
    t = 0.0
    altura = altura_paraquedas(t)
    while not disparar_retro(altura, VEL_PARAQUEDAS, False):
        t = t + 0.5
        altura = altura_paraquedas(t)
    print("   Retrofoguetes disparam em t = %.1f s, a %.0f m de altura" % (t, altura))
    duracao = (VEL_PARAQUEDAS - VEL_POUSO) / DESACEL_RETRO
    h_final = altura_retro(duracao, altura)
    print("   Frenagem dura %.1f s e termina a %.1f m do solo a %.0f m/s"
          % (duracao, h_final, VEL_POUSO))


# ---------------------------------------------------------------------------
# 7. SIMULACAO COMPLETA
# ---------------------------------------------------------------------------

def mostrar_fila(titulo, lista):
    """Imprime uma lista de modulos de forma resumida."""
    print(titulo)
    for m in lista:
        print("   %-7s %-22s prio=%d comb=%2d%% crit=%d eta=%s"
              % (m["id"], m["nome"], m["prioridade"], m["combustivel"],
                 m["criticidade"], m["eta"]))


def testar_regras_limite():
    """Dez testes de fronteira, sem dependencias externas.

    Executa apenas com dados de teste isolados; nao altera a fila da simulacao.
    Um resultado incorreto provoca AssertionError e impede falso sucesso.
    """
    print("\n[7] Testes de limites e comportamento seguro")
    base = {"id": "TST-01", "combustivel": 20,
            "sensores_ok": True, "area_livre": True}
    testes = []

    m = dict(base); m["combustivel"] = 19
    testes.append(("Combustivel 19% -> alerta", decidir_pouso(m, 20)[0] == "alerta"))
    testes.append(("Combustivel 20% -> autorizado", decidir_pouso(base, 20)[0] == "pousar"))
    testes.append(("Vento 20 m/s -> autorizado", decidir_pouso(base, 20)[0] == "pousar"))
    testes.append(("Vento 21 m/s -> espera", decidir_pouso(base, 21)[0] == "espera"))
    testes.append(("RETRO a 700 m -> desligado", not disparar_retro(700, 21, False)))
    testes.append(("RETRO a 699 m -> ligado", disparar_retro(699, 21, False)))
    testes.append(("RETRO a 20 m/s -> desligado", not disparar_retro(699, 20, False)))
    testes.append(("RETRO a 21 m/s -> ligado", disparar_retro(699, 21, False)))
    m = dict(base); m["sensores_ok"] = False
    testes.append(("Falha de sensor -> alerta", decidir_pouso(m, 20)[0] == "alerta"
                    and not disparar_retro(699, 21, True)))
    m = dict(base); m["area_livre"] = False
    testes.append(("Area ocupada -> espera", decidir_pouso(m, 20)[0] == "espera"))

    for nome, resultado in testes:
        if not resultado:
            raise AssertionError("Teste falhou: " + nome)
        print("   OK - " + nome)
    print("   Resultado: %d/%d testes aprovados" % (len(testes), len(testes)))
    return len(testes)


def main():
    print("=" * 66)
    print(" MGPEB - Missao Aurora Siger: simulacao de pouso")
    print("=" * 66)

    # (1) Cadastro nas estruturas lineares
    cadastrar_modulos(MODULOS_INICIAIS)
    mostrar_fila("\n[1] Fila cadastrada (ordem de cadastro):", fila_pouso)

    # (2) Buscas
    print("\n[2] Buscas")
    m = busca_menor(fila_pouso, "combustivel")
    print("   Menor combustivel: " + m["id"] + " (" + str(m["combustivel"]) + "%)")
    for m in busca_linear(fila_pouso, "criticidade", 5):
        print("   Criticidade maxima: " + m["id"] + " - " + m["carga"])

    # (3) Ordenacao da fila por prioridade (desempate por criticidade)
    ordenacao_insercao(fila_pouso, criterio_pouso)
    mostrar_fila("\n[3] Fila ordenada por prioridade/criticidade:", fila_pouso)

    # busca binaria (lista ja esta ordenada por prioridade)
    m = busca_binaria_prioridade(fila_pouso, 3)
    print("   Busca binaria, prioridade 3: " + m["id"])

    # (4) Processamento da fila com as regras logicas
    print("\n[4] Decisao de pouso (vento atual: %d m/s, limite: %d m/s)"
          % (VENTO_ATUAL, VENTO_MAXIMO))
    while len(fila_pouso) > 0:
        modulo = desenfileirar(fila_pouso)
        decisao, motivo = decidir_pouso(modulo)
        if decisao == "pousar":
            lista_pousados.append(modulo)
            registrar_evento("pouso autorizado", modulo, "pousados")
            rotulo = "POUSO AUTORIZADO"
        elif decisao == "alerta":
            lista_alerta.append(modulo)
            registrar_evento("alerta", modulo, "alerta")
            rotulo = "ALERTA"
        else:
            lista_espera.append(modulo)
            registrar_evento("adiado", modulo, "espera")
            rotulo = "ADIADO"
        print("   %-7s -> %-17s (%s)" % (modulo["id"], rotulo, motivo))

    mostrar_fila("\n[5] Pousados:", lista_pousados)
    mostrar_fila("    Em espera:", lista_espera)
    mostrar_fila("    Em alerta:", lista_alerta)

    # (5) Pilha de eventos: desfazer o ultimo registro
    print("\n[6] Pilha de eventos: %d registros. Desfazendo o ultimo..." % len(pilha_eventos))
    desfazer_ultimo_evento()
    mostrar_fila("    Fila apos desfazer:", fila_pouso)

    # (6) Modelo de descida
    simular_descida()

    # (7) Validacao explicita dos limites adotados nas regras logicas
    testar_regras_limite()
    print("\nSimulacao encerrada.")


if __name__ == "__main__":
    main()
