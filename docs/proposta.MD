# Proposta do Jogo

## 1. Nome do jogo
OVERRIDE: Treine a IA

## 2. Integrantes do grupo
- Lucca Marinho Eterovik Tavares Pereira
- Guilherme Alves Cobalt Camara
- Gabriel Oliveira Gonzaga Araújo
- Maria Fernanda Ferreira Rangel

## 3. Tema específico
**IA no Cotidiano: robótica e automação, com supervisão humana e uso responsável.**

Muitas tarefas do dia a dia (triagem de produtos, filtros, recomendações) já são feitas por sistemas que aprendem com exemplos. O recorte do jogo é: *uma IA só é tão boa quanto os exemplos que recebe, e uma pessoa precisa supervisioná-la e conferir seus resultados.*

## 4. Uso responsável da IA na jogabilidade (e não só no cenário)
| Aspecto responsável | Como afeta uma regra do jogo |
|---|---|
| Confiabilidade e análise crítica | A IA erra, principalmente quando o manual muda. O jogador precisa conferir as decisões dela. Acertar "na sorte" com a IA em dúvida (peça com "?") não dá bônus. |
| Transparência | O painel "Cérebro da IA" mostra o que ela aprendeu (pesos), a precisão recente e a confiança de cada peça. |
| Viés / qualidade dos dados | Só as decisões do jogador treinam a IA. Se ele ensinar errado, ela aprende errado e passa a errar mais. |
| Supervisão humana | Quanto mais a IA aprende, mais ela automatiza, mas qualquer erro dela custa qualidade da fábrica. A pessoa continua responsável. |
| Inclusão | A cor das peças usa o par laranja/azul (seguro para daltonismo) e o tamanho também é uma característica. |
| Privacidade/segurança | Não usa serviços externos nem dados pessoais: tudo roda localmente. |

## 5. Tipo de jogo
Jogo 2D de reflexo e estratégia (triagem em esteira com simulação básica de IA), em Python e Pygame.

## 6. Descrição geral do jogo
Peças com **tamanho** e **cor** (laranja a azul) descem numa esteira. Na linha de decisão a IA aprova ou reprova a peça sozinha. Antes disso o jogador pode decidir com as setas, seguindo o **manual** da fase. Cada decisão do jogador é um exemplo de treino: a IA ajusta seus pesos (classificador de regressão logística simples, sem bibliotecas externas). Quando o manual muda, a IA precisa reaprender.

## 7. Objetivo do jogador
Ensinar a IA para automatizar a triagem, manter a qualidade da fábrica e superar o recorde.

## 8. Regras principais
- Cada fase tem um manual (grandes; azuis; grandes e azuis; pequenas) e 12 peças.
- Decisão correta: +10 pontos (+5 de automação se a IA acertar sozinha e confiante). Decisão errada: -1 de qualidade (começa com 5).
- Só as decisões do jogador treinam a IA, inclusive as erradas.
- A cada fase o manual muda e a esteira acelera. Concluir a fase dá +25.

## 9. Condição de vitória
Não há vitória final. O objetivo é chegar à maior fase possível e bater o recorde.

## 10. Condição de derrota
A qualidade chegar a zero. A tela final mostra pontuação, fase, recorde e quantos exemplos a IA aprendeu.

## 11. Elementos previstos no jogo
- **Elemento principal:** o jogador (supervisor), que controla as decisões com o teclado.
- **Desafios:** peças com características variadas, esteira que acelera, manual que muda a cada fase.
- **Interação:** aprovar/reprovar peças, ensinar a IA, observar o painel dela.
- **Indicadores:** pontos, qualidade, fase, recorde, precisão e automação da IA.
- Telas inicial, de jogo, de pausa e de fim.

## 12. Controles
| Tecla | Ação |
|---|---|
| Seta direita (ou D) | Aprovar a peça |
| Seta esquerda (ou A) | Reprovar a peça |
| ENTER | Iniciar / reiniciar |
| ESC | Pausar / retomar |

## 13. Organização do código
- `main.py`: ponto de entrada.
- `src/config.py`: constantes configuráveis (tela, cores, regras, IA).
- `src/funcoes.py`: regras do manual, IA (decidir/treinar), estatísticas, pontuação, dificuldade.
- `src/jogo.py`: estado, decisões, atualização, desenho e loop principal.
- `src/sprites.py`: desenho das peças com formas geométricas.
- `src/dados.py`: leitura e escrita do recorde.
- `tests/test_logica.py`: testes. `docs/`: proposta. `data/recorde.txt`: recorde.

## 14. Estruturas de dados
- **Listas:** peças na esteira, histórico de acertos da IA, manuais de regras.
- **Dicionários:** peça, IA (pesos), estado do jogo e manuais.
- **Tuplas:** cores e posições.
- **Variáveis:** pontuação, qualidade, fase, tempos.

## 15. Uso de arquivos
`data/recorde.txt` guarda o recorde. É carregado ao iniciar e salvo ao fim da partida. Se o arquivo não existir ou for inválido, o recorde é zero.

## 16. Recursos necessários
Python 3, Pygame, `math` e `random` (biblioteca padrão), `pytest` para os testes. Sem imagens, sons ou fontes de terceiros: tudo é desenhado com formas geométricas e a fonte padrão do sistema.

## 17. Testes planejados
- Regras do manual e mudança de manual por fase.
- IA começa sem saber, aprende uma regra, reaprende quando a regra muda e aprende errado se for ensinada errado.
- Pontuação (com e sem bônus de automação), perda de qualidade e derrota.
- Avanço de fase, precisão da IA e salvamento/leitura do recorde.

## 18. Principais dificuldades esperadas
- Fazer a IA aprender rápido o suficiente para o jogo ser divertido, sem ficar fácil demais.
- Equilibrar a velocidade da esteira e a duração das fases.
- Manter o código simples, em funções, e explicar a lógica da IA de forma clara.

## 19. Escopo mínimo para a entrega final
Esteira funcional, decisão do jogador por teclado, IA que aprende com os exemplos, manual que muda por fase, pontuação e qualidade, painel da IA, telas inicial e final, recorde em arquivo, README e testes de lógica.

## 20. Melhorias possíveis
- Novos tipos de característica (ex.: forma da peça) e peças "enganosas" para discutir viés.
- Efeitos sonoros e animações.
- Ranking com vários recordes.

## 21. Declaração de originalidade
A proposta e a mecânica (supervisionar e treinar uma IA numa esteira) foram definidas pelo grupo para este trabalho e não reaproveitam jogos de semestres anteriores. O código foi desenvolvido com apoio de uma ferramenta de IA (Claude, da Anthropic). O grupo se compromete a revisar e compreender todo o código e a explicar as partes em que trabalhou. Nenhum código, imagem, som ou fonte de terceiros foi utilizado.
