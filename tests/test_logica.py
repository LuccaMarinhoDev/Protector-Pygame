import os
import random
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import config
from src.dados import carregar_recorde, salvar_recorde
from src.funcoes import (
    atualizar_recorde, criar_ia, criar_peca, ia_decide, ia_pede_ajuda, ia_treinar,
    manual_da_fase, peca_correta, perder_qualidade, precisao, registrar_resultado,
    jogador_perdeu,
)
from src.jogo import atualizar_estado, criar_estado, decisao_jogador, reiniciar_partida


def treinar(ia, regra, n):
    for _ in range(n):
        t, c = random.random(), random.random()
        ia_treinar(ia, t, c, peca_correta(t, c, regra), config.TAXA_APRENDIZADO)


def test_regras_do_manual():
    assert peca_correta(0.9, 0.1, "grande")
    assert not peca_correta(0.9, 0.1, "azul")
    assert peca_correta(0.9, 0.9, "grande_e_azul")
    assert not peca_correta(0.9, 0.1, "grande_e_azul")
    assert peca_correta(0.1, 0.1, "pequena")


def test_manual_muda_com_a_fase():
    assert manual_da_fase(1)["regra"] != manual_da_fase(2)["regra"]
    assert manual_da_fase(1) == manual_da_fase(5)


def test_ia_comeca_sem_saber_e_com_pouca_confianca():
    _, confianca = ia_decide(criar_ia(), 0.9, 0.9)
    assert ia_pede_ajuda(confianca, config.CONFIANCA_BAIXA)


def test_ia_aprende_regra_grande():
    random.seed(1)
    ia = criar_ia()
    treinar(ia, "grande", 40)
    assert ia_decide(ia, 0.9, 0.2)[0] is True
    assert ia_decide(ia, 0.1, 0.9)[0] is False
    assert ia["treinos"] == 40


def test_ia_reaprende_quando_a_regra_muda():
    random.seed(2)
    ia = criar_ia()
    treinar(ia, "grande", 40)
    treinar(ia, "pequena", 60)
    assert ia_decide(ia, 0.1, 0.5)[0] is True
    assert ia_decide(ia, 0.9, 0.5)[0] is False


def test_ia_aprende_errado_se_o_jogador_ensina_errado():
    ia = criar_ia()
    for _ in range(30):
        ia_treinar(ia, 0.9, 0.5, False, config.TAXA_APRENDIZADO)  # ensino errado
    assert ia_decide(ia, 0.9, 0.5)[0] is False


def test_precisao_usa_janela():
    h = []
    for acerto in [True] * 3 + [False] * 10:
        registrar_resultado(h, acerto, 10)
    assert len(h) == 10 and precisao(h) == 0
    assert precisao([]) == 0


def test_qualidade_e_derrota():
    assert perder_qualidade(1) == 0 and perder_qualidade(0) == 0
    assert jogador_perdeu(0) and not jogador_perdeu(1)


def test_decisao_do_jogador_treina_a_ia_e_pontua():
    e = criar_estado(); reiniciar_partida(e); e["pausa_fase"] = 0
    p = criar_peca(100, 100); p["tamanho"], p["cor"] = 0.9, 0.9; p["previsao_ia"] = True
    e["pecas"].append(p); e["geradas_na_fase"] = 1
    decisao_jogador(e, True)  # fase 1: grande = aprovar (correto)
    assert e["pontos"] == config.PONTOS_ACERTO and e["ia"]["treinos"] == 1
    assert p["estado"] == "saindo"


def test_erro_do_jogador_tira_qualidade():
    e = criar_estado(); reiniciar_partida(e); e["pausa_fase"] = 0
    p = criar_peca(100, 100); p["tamanho"] = 0.9; p["previsao_ia"] = True
    e["pecas"].append(p)
    decisao_jogador(e, False)
    assert e["qualidade"] == config.QUALIDADE_INICIAL - 1


def test_ia_decide_sozinha_na_linha_com_bonus():
    e = criar_estado(); reiniciar_partida(e); e["pausa_fase"] = 0; e["tempo_spawn"] = 99
    random.seed(3); treinar(e["ia"], "grande", 50)
    p = criar_peca(100, config.LINHA_DECISAO_Y - 1); p["tamanho"], p["cor"] = 0.9, 0.5
    e["pecas"].append(p)
    atualizar_estado(e, 0.1)
    assert p["decidida_por"] == "ia"
    assert e["pontos"] == config.PONTOS_ACERTO + config.BONUS_AUTOMACAO


def test_fase_avanca_e_derrota():
    e = criar_estado(); reiniciar_partida(e); e["pausa_fase"] = 0
    e["geradas_na_fase"] = config.PECAS_POR_FASE
    atualizar_estado(e, 0.1)
    assert e["fase"] == 2
    e["pausa_fase"] = 0; e["qualidade"] = 0
    atualizar_estado(e, 0.1)
    assert e["tela"] == "fim"


def test_recorde(tmp_path):
    assert atualizar_recorde(50, 30) == 50 and atualizar_recorde(10, 30) == 30
    arq = str(tmp_path / "r.txt")
    assert carregar_recorde(arq) == 0
    salvar_recorde(arq, 77)
    assert carregar_recorde(arq) == 77


def test_ia_em_duvida_nao_ganha_bonus_de_automacao():
    e = criar_estado(); reiniciar_partida(e); e["pausa_fase"] = 0; e["tempo_spawn"] = 99
    p = criar_peca(100, config.LINHA_DECISAO_Y - 1); p["tamanho"], p["cor"] = 0.9, 0.5
    e["pecas"].append(p)
    atualizar_estado(e, 0.1)  # IA sem treino: confiança 0, aprova por acaso (acerta na fase 1)
    assert p["decidida_por"] == "ia"
    assert e["pontos"] == config.PONTOS_ACERTO  # sem bônus
