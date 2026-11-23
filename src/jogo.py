# Loop principal e lógica de estado do jogo (usa as funções de funcoes.py).
import pygame

from src import config
from src.dados import carregar_recorde, salvar_recorde
from src.funcoes import (
    atualizar_recorde,
    calcular_pontos,
    criar_ia,
    criar_peca,
    ia_decide,
    ia_pede_ajuda,
    ia_treinar,
    intervalo_da_fase,
    jogador_perdeu,
    limitar_valor,
    manual_da_fase,
    peca_correta,
    perder_qualidade,
    precisao,
    registrar_resultado,
    velocidade_da_fase,
)
from src.sprites import desenhar_peca


# ---------------------------------------------------------------- estado
def criar_estado(recorde=0):
    """Cria o dicionário com tudo que muda durante a partida."""
    return {
        "tela": "inicio",            # inicio, jogando, pausa, fim
        "pecas": [],
        "ia": criar_ia(),
        "pontos": 0,
        "qualidade": config.QUALIDADE_INICIAL,
        "fase": 1,
        "geradas_na_fase": 0,
        "tempo_spawn": 0.0,
        "pausa_fase": config.PAUSA_ENTRE_FASES,
        "historico_ia": [],          # a IA teria acertado? (últimas decisões)
        "decisoes_ia": 0,            # peças decididas pela IA sozinha
        "decisoes_total": 0,
        "recorde": recorde,
        "mensagem": "",
        "tempo_mensagem": 0.0,
        "tempo_total": 0.0,
    }


def reiniciar_partida(estado):
    """Começa uma nova partida mantendo o recorde."""
    recorde = estado["recorde"]
    novo = criar_estado(recorde)
    novo["tela"] = "jogando"
    estado.clear()
    estado.update(novo)


def avisar(estado, texto):
    """Mostra uma mensagem de feedback por alguns segundos."""
    estado["mensagem"] = texto
    estado["tempo_mensagem"] = 1.6


# ---------------------------------------------------------------- decisões
def resolver_peca(estado, peca, aprovar, quem):
    """Registra a decisão (do jogador ou da IA), confere com o manual e pontua."""
    regra = manual_da_fase(estado["fase"])["regra"]
    certa = peca_correta(peca["tamanho"], peca["cor"], regra)

    # estatística honesta: a IA teria acertado essa peça?
    registrar_resultado(estado["historico_ia"], peca["previsao_ia"] == certa, config.JANELA_PRECISAO)

    peca["estado"] = "saindo"
    peca["destino"] = aprovar
    peca["decidida_por"] = quem
    estado["decisoes_total"] += 1

    if quem == "jogador":
        # APRENDIZADO SUPERVISIONADO: a IA aprende com o rótulo que o jogador deu
        # (se o jogador errar, a IA aprende errado: "lixo entra, lixo sai").
        ia_treinar(estado["ia"], peca["tamanho"], peca["cor"], aprovar, config.TAXA_APRENDIZADO)
    else:
        estado["decisoes_ia"] += 1

    if aprovar == certa:
        ganho = config.PONTOS_ACERTO
        if quem == "ia" and not ia_pede_ajuda(peca["confianca"], config.CONFIANCA_BAIXA):
            ganho += config.BONUS_AUTOMACAO
            avisar(estado, "IA acertou sozinha! +%d (automação)" % ganho)
        elif quem == "ia":
            # acertou, mas estava em dúvida: sem bônus (confiar sem conferir é arriscado)
            avisar(estado, "Acertou na sorte: a IA estava em dúvida. Sem bônus.")
        estado["pontos"] = calcular_pontos(estado["pontos"], ganho)
    else:
        estado["qualidade"] = perder_qualidade(estado["qualidade"])
        if quem == "ia":
            avisar(estado, "A IA errou! Ensine-a com as setas.")
        else:
            avisar(estado, "Você errou e a IA aprendeu o erro!")


def decisao_jogador(estado, aprovar):
    """Seta direita = aprovar, esquerda = reprovar. Age na peça mais próxima da linha."""
    if estado["tela"] != "jogando":
        return
    na_esteira = [p for p in estado["pecas"] if p["estado"] == "esteira"]
    if not na_esteira:
        return
    peca = max(na_esteira, key=lambda p: p["y"])
    resolver_peca(estado, peca, aprovar, "jogador")


# ---------------------------------------------------------------- atualização
def atualizar_estado(estado, dt):
    """Avança o jogo: gera peças, move a esteira, a IA decide e controla fases e derrota."""
    if estado["tela"] != "jogando":
        return
    estado["tempo_total"] += dt
    if estado["tempo_mensagem"] > 0:
        estado["tempo_mensagem"] -= dt

    fase = estado["fase"]
    velocidade = velocidade_da_fase(fase, config.VELOCIDADE_INICIAL,
                                    config.AUMENTO_VELOCIDADE, config.VELOCIDADE_MAXIMA)

    # --- pausa entre fases (mostra o novo manual) ---
    if estado["pausa_fase"] > 0:
        estado["pausa_fase"] -= dt
        return

    # --- gera peças ---
    estado["tempo_spawn"] -= dt
    if estado["geradas_na_fase"] < config.PECAS_POR_FASE and estado["tempo_spawn"] <= 0:
        estado["pecas"].append(criar_peca(config.CENTRO_ESTEIRA_X, config.TOPO_AREA + 10))
        estado["geradas_na_fase"] += 1
        estado["tempo_spawn"] = intervalo_da_fase(fase, config.INTERVALO_INICIAL, config.INTERVALO_MINIMO)

    # --- move peças e deixa a IA decidir quando chegam na linha ---
    for peca in estado["pecas"]:
        if peca["estado"] == "esteira":
            peca["y"] += velocidade * dt
            aprovar, confianca = ia_decide(estado["ia"], peca["tamanho"], peca["cor"])
            peca["previsao_ia"] = aprovar
            peca["confianca"] = confianca
            if peca["y"] >= config.LINHA_DECISAO_Y:
                resolver_peca(estado, peca, aprovar, "ia")
        else:
            sentido = 1 if peca["destino"] else -1
            peca["x"] += sentido * config.VELOCIDADE_SAIDA * dt
            peca["y"] += velocidade * dt * 0.3

    estado["pecas"] = [p for p in estado["pecas"] if 20 < p["x"] < config.LARGURA_JOGO - 20]

    # --- fim de jogo ---
    if jogador_perdeu(estado["qualidade"]):
        estado["recorde"] = atualizar_recorde(estado["pontos"], estado["recorde"])
        estado["tela"] = "fim"
        return

    # --- fim da fase: novo manual, a IA precisa reaprender ---
    if estado["geradas_na_fase"] >= config.PECAS_POR_FASE and not estado["pecas"]:
        estado["fase"] += 1
        estado["geradas_na_fase"] = 0
        estado["pausa_fase"] = config.PAUSA_ENTRE_FASES
        estado["pontos"] = calcular_pontos(estado["pontos"], config.BONUS_FASE)


# ---------------------------------------------------------------- desenho
def desenhar_barra_peso(tela, fonte, nome, valor, x, y):
    """Barra centrada: direita = a IA dá mais importância, esquerda = importância ao contrário."""
    largura = 160
    pygame.draw.rect(tela, config.ESTEIRA, (x, y + 18, largura, 12))
    meio = x + largura // 2
    tamanho = int(limitar_valor(valor, -6, 6) / 6 * (largura // 2))
    cor = config.VERDE if tamanho >= 0 else config.VERMELHO
    pygame.draw.rect(tela, cor, (min(meio, meio + tamanho), y + 18, abs(tamanho), 12))
    pygame.draw.line(tela, config.BRANCO, (meio, y + 15), (meio, y + 33), 1)
    tela.blit(fonte.render("%s: %+.1f" % (nome, valor), True, config.BRANCO), (x, y))


def desenhar_texto(tela, fonte, texto, x, y, cor=config.BRANCO, centro=False):
    """Escreve um texto na tela (centralizado se centro=True)."""
    img = fonte.render(texto, True, cor)
    pos = img.get_rect(center=(x, y)) if centro else (x, y)
    tela.blit(img, pos)


def desenhar_jogo(tela, estado, fontes):
    """Desenha a esteira, as peças, o HUD e o painel do cérebro da IA."""
    pequena, media, grande = fontes
    tela.fill(config.FUNDO)
    ia = estado["ia"]

    # esteira, lixeiras e linha de decisão
    pygame.draw.rect(tela, config.ESTEIRA, (config.CENTRO_ESTEIRA_X - config.LARGURA_ESTEIRA // 2,
                                            config.TOPO_AREA, config.LARGURA_ESTEIRA,
                                            config.LINHA_DECISAO_Y - config.TOPO_AREA + 30))
    pygame.draw.rect(tela, (70, 30, 40), (20, 400, 120, 110), border_radius=8)
    pygame.draw.rect(tela, (25, 70, 45), (440, 400, 120, 110), border_radius=8)
    desenhar_texto(tela, media, "REPROVAR", 80, 455, config.VERMELHO, True)
    desenhar_texto(tela, media, "APROVAR", 500, 455, config.VERDE, True)
    desenhar_texto(tela, pequena, "<- seta", 80, 480, config.CINZA, True)
    desenhar_texto(tela, pequena, "seta ->", 500, 480, config.CINZA, True)
    pygame.draw.line(tela, config.AMARELO, (config.CENTRO_ESTEIRA_X - 70, config.LINHA_DECISAO_Y),
                     (config.CENTRO_ESTEIRA_X + 70, config.LINHA_DECISAO_Y), 2)
    desenhar_texto(tela, pequena, "a IA decide aqui", config.CENTRO_ESTEIRA_X,
                   config.LINHA_DECISAO_Y + 40, config.AMARELO, True)

    piscar = int(estado["tempo_total"] * 4) % 2 == 0
    for peca in estado["pecas"]:
        desenhar_peca(tela, peca, media, piscar)

    # HUD
    pygame.draw.rect(tela, config.PAINEL, (0, 0, config.LARGURA_TELA, config.TOPO_AREA))
    desenhar_texto(tela, media, "Pontos: %d" % estado["pontos"], 15, 14)
    desenhar_texto(tela, media, "Qualidade: " + "#" * estado["qualidade"], 185, 14, config.VERDE)
    desenhar_texto(tela, media, "Fase: %d" % estado["fase"], 410, 14, config.CIANO)
    desenhar_texto(tela, media, "Recorde: %d" % max(estado["recorde"], estado["pontos"]), 520, 14, config.AMARELO)
    desenhar_texto(tela, pequena, "MANUAL: " + manual_da_fase(estado["fase"])["texto"], 15, 58, config.AMARELO)

    # painel do cérebro da IA
    px = config.LARGURA_JOGO + 20
    pygame.draw.rect(tela, config.PAINEL, (config.LARGURA_JOGO, config.TOPO_AREA,
                                           config.LARGURA_TELA - config.LARGURA_JOGO,
                                           config.ALTURA_TELA - config.TOPO_AREA))
    desenhar_texto(tela, media, "CÉREBRO DA IA", px, 70, config.ROXO)
    desenhar_texto(tela, pequena, "O que ela aprendeu:", px, 98, config.CINZA)
    desenhar_barra_peso(tela, pequena, "tamanho", ia["peso_tamanho"], px, 120)
    desenhar_barra_peso(tela, pequena, "cor azul", ia["peso_cor"], px, 165)
    desenhar_texto(tela, pequena, "Exemplos vistos: %d" % ia["treinos"], px, 220)
    prec = precisao(estado["historico_ia"])
    desenhar_texto(tela, pequena, "Precisão (últimas %d): %d%%" % (config.JANELA_PRECISAO, prec), px, 250)
    pygame.draw.rect(tela, config.ESTEIRA, (px, 272, 160, 12))
    pygame.draw.rect(tela, config.VERDE if prec >= 70 else config.VERMELHO, (px, 272, int(160 * prec / 100), 12))
    if estado["decisoes_total"]:
        auto = round(100 * estado["decisoes_ia"] / estado["decisoes_total"])
    else:
        auto = 0
    desenhar_texto(tela, pequena, "Automação: %d%%" % auto, px, 300)
    pygame.draw.rect(tela, config.ESTEIRA, (px, 322, 160, 12))
    pygame.draw.rect(tela, config.ROXO, (px, 322, int(160 * auto / 100), 12))
    for i, linha in enumerate(["Você ENSINA a IA", "com as setas.", "Quanto mais ela",
                               "acerta, mais a", "fábrica se automatiza.", "", "Cuidado: se você",
                               "errar, ela aprende", "o erro!", "", "Anel ciano = você",
                               "Anel roxo = IA", "? = IA em dúvida"]):
        desenhar_texto(tela, pequena, linha, px, 360 + i * 17, config.CINZA)

    # mensagem de feedback
    if estado["tempo_mensagem"] > 0:
        desenhar_texto(tela, media, estado["mensagem"], config.LARGURA_JOGO // 2, 100, config.AMARELO, True)

    # aviso de novo manual
    if estado["pausa_fase"] > 0:
        fundo = pygame.Surface((config.LARGURA_JOGO, 120))
        fundo.set_alpha(220)
        fundo.fill(config.PAINEL)
        tela.blit(fundo, (0, 220))
        desenhar_texto(tela, grande, "FASE %d - NOVO MANUAL!" % estado["fase"], config.LARGURA_JOGO // 2, 255, config.CIANO, True)
        desenhar_texto(tela, media, manual_da_fase(estado["fase"])["texto"], config.LARGURA_JOGO // 2, 295, config.AMARELO, True)
        if estado["fase"] > 1:
            desenhar_texto(tela, pequena, "A regra mudou: a IA vai errar até reaprender com você.",
                           config.LARGURA_JOGO // 2, 322, config.CINZA, True)


def desenhar_tela_cheia(tela, fontes, linhas, titulo):
    """Tela de texto usada no início e no fim da partida."""
    pequena, media, grande = fontes
    tela.fill(config.FUNDO)
    desenhar_texto(tela, grande, titulo, config.LARGURA_TELA // 2, 90, config.CIANO, True)
    for i, (texto, cor) in enumerate(linhas):
        desenhar_texto(tela, media, texto, config.LARGURA_TELA // 2, 170 + i * 34, cor, True)


def desenhar(tela, estado, fontes):
    """Escolhe o que desenhar conforme a tela atual (início, jogo, pausa ou fim)."""
    if estado["tela"] == "inicio":
        desenhar_tela_cheia(tela, fontes, [
            ("Você é o SUPERVISOR de uma fábrica automatizada.", config.BRANCO),
            ("Peças passam na esteira e a IA tenta classificá-las.", config.BRANCO),
            ("Siga o MANUAL da fase: seta ESQUERDA = reprovar, DIREITA = aprovar.", config.AMARELO),
            ("Cada decisão sua é um exemplo de treino: a IA APRENDE com você.", config.ROXO),
            ("Quando ela aprende, passa a decidir sozinha (automação).", config.VERDE),
            ("Mas o manual muda e ela precisa reaprender. Se você ensinar", config.CINZA),
            ("errado, ela aprende errado!", config.VERMELHO),
            ("", config.BRANCO),
            ("ENTER para começar   |   ESC pausa", config.CIANO),
        ], "OVERRIDE: Treine a IA")
    elif estado["tela"] == "fim":
        desenhar_tela_cheia(tela, fontes, [
            ("Pontuação: %d" % estado["pontos"], config.AMARELO),
            ("Fase alcançada: %d" % estado["fase"], config.BRANCO),
            ("Recorde: %d" % estado["recorde"], config.VERDE),
            ("Exemplos que a IA aprendeu com você: %d" % estado["ia"]["treinos"], config.ROXO),
            ("", config.BRANCO),
            ("ENTER para jogar de novo", config.CIANO),
        ], "A fábrica parou!")
    else:
        desenhar_jogo(tela, estado, fontes)
        if estado["tela"] == "pausa":
            desenhar_texto(tela, fontes[2], "PAUSADO", config.LARGURA_JOGO // 2, 300, config.BRANCO, True)


# ---------------------------------------------------------------- loop
def executar_jogo():
    """Inicia o Pygame e roda o loop principal."""
    pygame.init()
    tela = pygame.display.set_mode((config.LARGURA_TELA, config.ALTURA_TELA))
    pygame.display.set_caption(config.TITULO_JOGO)
    relogio = pygame.time.Clock()
    fontes = (pygame.font.SysFont("arial", 15), pygame.font.SysFont("arial", 20, bold=True),
              pygame.font.SysFont("arial", 34, bold=True))
    estado = criar_estado(carregar_recorde(config.CAMINHO_RECORDE))
    rodando = True

    while rodando:
        dt = min(relogio.tick(config.FPS) / 1000, 0.05)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and estado["tela"] in ("inicio", "fim"):
                    reiniciar_partida(estado)
                elif evento.key == pygame.K_ESCAPE:
                    if estado["tela"] == "jogando":
                        estado["tela"] = "pausa"
                    elif estado["tela"] == "pausa":
                        estado["tela"] = "jogando"
                elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                    decisao_jogador(estado, True)
                elif evento.key in (pygame.K_LEFT, pygame.K_a):
                    decisao_jogador(estado, False)

        tela_antes = estado["tela"]
        atualizar_estado(estado, dt)
        if tela_antes == "jogando" and estado["tela"] == "fim":
            salvar_recorde(config.CAMINHO_RECORDE, estado["recorde"])

        pygame.display.set_caption("%s | Fase %d | Pontos %d" % (config.TITULO_JOGO, estado["fase"], estado["pontos"]))
        desenhar(tela, estado, fontes)
        pygame.display.flip()

    pygame.quit()
