# Desenhos feitos só com formas geométricas (sem imagens externas).
import pygame

from src import config


def cor_da_peca(cor):
    """0 = laranja ... 1 = azul (par de cores seguro para daltonismo)."""
    return int(240 * (1 - cor) + 40 * cor), int(150 * (1 - cor) + 130 * cor), int(30 * (1 - cor) + 240 * cor)


def raio_da_peca(tamanho):
    """Raio do círculo: peças maiores têm tamanho próximo de 1."""
    return int(config.RAIO_BASE_PECA + config.RAIO_EXTRA_PECA * tamanho)


def desenhar_peca(tela, peca, fonte, piscar):
    """Desenha a peça; se a IA estiver em dúvida mostra um '?' piscando."""
    x, y = int(peca["x"]), int(peca["y"])
    raio = raio_da_peca(peca["tamanho"])
    pygame.draw.circle(tela, cor_da_peca(peca["cor"]), (x, y), raio)
    pygame.draw.circle(tela, config.BRANCO, (x, y), raio, 2)
    if peca["estado"] == "esteira" and peca["confianca"] < config.CONFIANCA_BAIXA and piscar:
        texto = fonte.render("?", True, config.AMARELO)
        tela.blit(texto, texto.get_rect(center=(x, y)))
    if peca["decidida_por"] == "jogador":
        pygame.draw.circle(tela, config.CIANO, (x, y), raio + 5, 2)
    elif peca["decidida_por"] == "ia":
        pygame.draw.circle(tela, config.ROXO, (x, y), raio + 5, 2)
