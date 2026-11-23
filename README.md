# OVERRIDE: Treine a IA

Projeto final de Introdução a Algoritmos (PUC Minas), feito com Python e Pygame, a partir do template da disciplina.
Tema: **IA no Cotidiano: Aplicações e Uso Responsável**.

## Integrantes
Lucca Marinho Eterovik Tavares Pereira, Guilherme Alves Cobalt Camara, Gabriel Oliveira Gonzaga Araújo, Maria Fernanda Ferreira Rangel

## Descrição
Você supervisiona uma linha de triagem automatizada. Peças com tamanho e cor (laranja a azul) descem numa esteira e a IA decide se aprova ou reprova. A IA começa sem saber nada e **aprende com as suas decisões** (aprendizado supervisionado). Quando aprende, decide sozinha. Quando o manual muda, ela erra até reaprender. Se você ensinar errado, ela aprende errado.

## Uso responsável da IA no jogo
- **Confiabilidade:** a IA erra e precisa ser conferida. Acertar com a IA em dúvida ("?") não dá bônus.
- **Transparência:** o painel mostra o que a IA aprendeu, sua precisão e sua confiança.
- **Qualidade dos dados:** ensinar errado piora a IA.
- **Supervisão humana:** erros da IA custam qualidade da fábrica; a responsabilidade é da pessoa.
- **Inclusão:** cores laranja/azul, seguras para daltonismo.

## Como a IA funciona
Classificador simples (regressão logística): `p = sigmoide(peso_tamanho*(tamanho-0.5) + peso_cor*(cor-0.5) + viés)`. A cada exemplo dado pelo jogador os pesos são ajustados proporcionalmente ao erro. Código em `src/funcoes.py` (`ia_decide`, `ia_treinar`).

## Controles
- Seta direita (ou D): aprovar | Seta esquerda (ou A): reprovar
- ENTER: iniciar/reiniciar | ESC: pausar

## Regras
- Siga o MANUAL da fase. Acerto: +10 (+5 se a IA acertou sozinha e confiante). Erro: -1 de qualidade (começa com 5).
- Cada fase tem 12 peças; depois o manual muda e a esteira acelera. A partida acaba com qualidade zero.
- O recorde fica em `data/recorde.txt`.

## Como executar
```bash
pip install -r requirements.txt
python main.py
python -m pytest
```

## Estrutura do projeto
- `main.py`: ponto de entrada
- `src/config.py`: valores configuráveis | `src/funcoes.py`: regras e IA | `src/jogo.py`: estado, loop e telas | `src/sprites.py`: desenho das peças | `src/dados.py`: recorde
- `tests/test_logica.py`: testes de lógica | `docs/proposta.MD`: proposta | `data/`: recorde | `assets/`: vazio (sem recursos externos)

## Recursos externos e uso de IA
- Nenhuma imagem, som, fonte ou código de terceiros: os gráficos são formas do Pygame e a fonte é a padrão do sistema.
- Bibliotecas: Pygame (LGPL) e pytest (MIT).
- O código foi desenvolvido com apoio de uma ferramenta de IA (Claude, da Anthropic) e revisado pelo grupo.
