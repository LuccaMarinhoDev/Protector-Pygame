# Regras do jogo e a "IA" em funções simples (fáceis de testar, sem depender da tela).
import math
import random

# ---------- manual de regras (muda a cada fase) ----------
# Cada peça tem duas características entre 0 e 1: "tamanho" e "cor" (0 = laranja, 1 = azul; combinação segura para daltonismo).
MANUAIS = [
    {"texto": "Aprovar peças GRANDES", "regra": "grande"},
    {"texto": "Aprovar peças AZUIS", "regra": "azul"},
    {"texto": "Aprovar peças GRANDES e AZUIS", "regra": "grande_e_azul"},
    {"texto": "Aprovar peças PEQUENAS", "regra": "pequena"},
]


def manual_da_fase(fase):
    """Devolve o manual da fase (as regras se repetem em ciclo)."""
    return MANUAIS[(fase - 1) % len(MANUAIS)]


def peca_correta(tamanho, cor, regra):
    """Resposta verdadeira: True = a peça deve ser aprovada."""
    if regra == "grande":
        return tamanho > 0.5
    if regra == "azul":
        return cor > 0.5
    if regra == "grande_e_azul":
        return tamanho > 0.5 and cor > 0.5
    if regra == "pequena":
        return tamanho < 0.5
    return False


def sortear_caracteristica():
    """Sorteia um valor de 0 a 1 longe de 0.5, para a peça não ser ambígua."""
    valor = random.random()
    while abs(valor - 0.5) < 0.12:
        valor = random.random()
    return valor


def criar_peca(x, y):
    """Cria uma peça nova como dicionário."""
    return {
        "x": float(x), "y": float(y),
        "tamanho": sortear_caracteristica(),
        "cor": sortear_caracteristica(),
        "estado": "esteira",        # esteira -> saindo
        "destino": None,            # True = aprovar, False = reprovar
        "decidida_por": None,       # "jogador" ou "ia"
        "previsao_ia": None,        # o que a IA achava (guardado para as estatísticas)
        "confianca": 0.0,
    }


# ---------- a IA: um classificador que aprende (regressão logística simples) ----------
def criar_ia():
    """A IA começa sem saber nada: pesos zerados."""
    return {"peso_tamanho": 0.0, "peso_cor": 0.0, "vies": 0.0, "treinos": 0}


def sigmoide(z):
    """Transforma qualquer número em probabilidade entre 0 e 1."""
    z = max(-30.0, min(30.0, z))
    return 1 / (1 + math.exp(-z))


def probabilidade_aprovar(ia, tamanho, cor):
    """Probabilidade (0 a 1) da IA achar que a peça deve ser aprovada."""
    z = ia["peso_tamanho"] * (tamanho - 0.5) + ia["peso_cor"] * (cor - 0.5) + ia["vies"]
    return sigmoide(z)


def ia_decide(ia, tamanho, cor):
    """A IA decide e diz o quão confiante está (0 a 1)."""
    p = probabilidade_aprovar(ia, tamanho, cor)
    return p >= 0.5, abs(p - 0.5) * 2


def ia_treinar(ia, tamanho, cor, resposta, taxa):
    """Aprende com UM exemplo rotulado (resposta True/False): ajusta os pesos."""
    p = probabilidade_aprovar(ia, tamanho, cor)
    erro = (1.0 if resposta else 0.0) - p
    ia["peso_tamanho"] += taxa * erro * (tamanho - 0.5) * 4
    ia["peso_cor"] += taxa * erro * (cor - 0.5) * 4
    ia["vies"] += taxa * erro * 0.5
    ia["treinos"] += 1
    return ia


def ia_pede_ajuda(confianca, limite):
    """Quando a confiança é baixa, a IA pede ajuda ao supervisor humano."""
    return confianca < limite


# ---------- estatísticas ----------
def registrar_resultado(historico, acertou, janela):
    """Guarda se a IA acertou e mantém só as últimas 'janela' decisões."""
    historico.append(bool(acertou))
    while len(historico) > janela:
        historico.pop(0)
    return historico


def precisao(historico):
    """Percentual (0 a 100) de acertos da IA nas últimas decisões."""
    if not historico:
        return 0
    return round(100 * sum(historico) / len(historico))


# ---------- pontuação e fim de jogo ----------
def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual."""
    return pontos_atual + pontos_ganhos


def perder_qualidade(qualidade, dano=1):
    """Reduz a qualidade da fábrica sem deixar ficar negativa."""
    return max(0, qualidade - dano)


def jogador_perdeu(qualidade):
    """A partida termina quando a qualidade chega a zero."""
    return qualidade <= 0


def atualizar_recorde(pontos, recorde):
    """Devolve o maior valor entre a pontuação e o recorde."""
    return pontos if pontos > recorde else recorde


def limitar_valor(valor, minimo, maximo):
    """Mantém o valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


# ---------- dificuldade ----------
def velocidade_da_fase(fase, inicial, aumento, maxima):
    """Velocidade da esteira: aumenta a cada fase até um limite."""
    return min(maxima, inicial + aumento * (fase - 1))


def intervalo_da_fase(fase, inicial, minimo):
    """Tempo entre peças: diminui a cada fase até um mínimo."""
    return max(minimo, inicial - 0.1 * (fase - 1))
