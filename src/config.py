# Configurações centrais do jogo (tela, cores, caminhos e regras).
import os

PASTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60
TITULO_JOGO = "OVERRIDE - Treine a IA"

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (150, 160, 175)
FUNDO = (12, 16, 28)
PAINEL = (20, 26, 44)
ESTEIRA = (34, 40, 62)
CIANO = (90, 200, 255)
VERMELHO = (235, 70, 80)
VERDE = (90, 220, 130)
AMARELO = (255, 215, 80)
ROXO = (180, 120, 255)

CAMINHO_RECORDE = os.path.join(PASTA_RAIZ, "data", "recorde.txt")

# Layout
TOPO_AREA = 50
LARGURA_JOGO = 580            # o resto da tela (à direita) é o painel da IA
CENTRO_ESTEIRA_X = 290
LARGURA_ESTEIRA = 120
LINHA_DECISAO_Y = 440         # onde a IA decide se o jogador não decidiu antes
RAIO_BASE_PECA = 14
RAIO_EXTRA_PECA = 26

# Regras
QUALIDADE_INICIAL = 5         # "vidas" da fábrica
PECAS_POR_FASE = 12           # a cada fase o manual de regras muda
PAUSA_ENTRE_FASES = 2.5       # segundos mostrando o aviso de novo manual
PONTOS_ACERTO = 10
BONUS_AUTOMACAO = 5           # bônus quando a IA acerta sozinha
BONUS_FASE = 25               # bônus ao concluir uma fase
JANELA_PRECISAO = 10         # a precisão da IA considera as últimas N decisões

# Esteira
VELOCIDADE_INICIAL = 70       # pixels por segundo
AUMENTO_VELOCIDADE = 8        # por fase
VELOCIDADE_MAXIMA = 170
INTERVALO_INICIAL = 1.8       # segundos entre peças
INTERVALO_MINIMO = 0.9
VELOCIDADE_SAIDA = 420        # peça sendo desviada para o lado

# IA
TAXA_APRENDIZADO = 0.9
CONFIANCA_BAIXA = 0.35        # abaixo disso a IA "pede ajuda" (mostra ?)
