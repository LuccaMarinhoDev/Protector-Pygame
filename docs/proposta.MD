# Proposta Inicial do Jogo

Este documento deve ser preenchido pelo grupo na etapa inicial do projeto.

A proposta deve apresentar uma ideia simples, clara e viável para ser desenvolvida com **Python e Pygame** dentro do prazo disponível. Consulte o enunciado publicado no Canvas para conhecer o eixo temático e as orientações vigentes.

## 1. Nome provisório do jogo

Informe o nome provisório do jogo.
# Proposta Inicial do Jogo

## Nome do jogo
OVERRIDE

## Integrantes do grupo
- Lucca Marinho Eterovik Tavares Pereira
- Guilherme Alves Cobalt Camara
- Gabriel Oliveira Gonzaga Araújo
- Maria Fernanda Ferreira Rangel

## Tema específico
Inteligência artificial na segurança de ambientes inteligentes, com foco na utilização responsável de robôs autônomos para proteger informações e equipamentos.

## Relevância do tema e uso responsável da IA
A inteligência artificial pode auxiliar na proteção de ambientes e na identificação de ameaças. Entretanto, sistemas autônomos precisam respeitar regras de segurança para não prejudicar pessoas ou equipamentos autorizados. O jogo representa essa situação por meio de robôs que protegem um servidor e devem distinguir invasores de agentes autorizados antes de atacar.

## Tipo de jogo
Jogo 2D de ação e sobrevivência, desenvolvido em Python com a biblioteca Pygame.

## Descrição geral
O jogador controla um personagem responsável pela proteção de um servidor central. Inicialmente, ele possui dois robôs de defesa que o acompanham e atacam invasores automaticamente. Além dos invasores, agentes autorizados aparecem no cenário e podem acessar o servidor sem sofrer ataques.

A partida é dividida em ondas de dificuldade crescente. Ao eliminar invasores, existe uma pequena chance de aparecerem melhorias no mapa. O jogador pode coletá-las para aumentar a velocidade, o alcance de ataque ou a quantidade de robôs da equipe.

## Integração da inteligência artificial com a jogabilidade
Os robôs de defesa tomam decisões automaticamente. Eles verificam a autorização dos agentes próximos, identificam invasores dentro de seu alcance e priorizam aqueles que representam maior ameaça ao servidor.

Os invasores também possuem um comportamento adaptativo simples: o jogo registra os lados do cenário pelos quais conseguiram alcançar o servidor e aumenta a frequência de invasões nesses locais nas próximas ondas.

A IA será simulada com funções, condicionais, listas e dicionários, sem necessidade de modelos de aprendizado de máquina ou serviços externos. A atuação dos robôs será limitada por regras de autorização, representando a importância da segurança e da supervisão humana em sistemas autônomos.

## Objetivo do jogador
Proteger o servidor durante o maior tempo possível, eliminar invasores, coletar melhorias e superar o recorde de pontuação.

## Regras principais
- O jogador começa com dois robôs de defesa.
- Os robôs acompanham o jogador e atacam invasores automaticamente dentro de seu alcance.
- Agentes autorizados podem chegar ao servidor sem causar danos e não devem ser atacados.
- Cada invasor que alcançar o servidor reduz sua integridade em um ponto.
- O servidor começa com três pontos de integridade.
- A eliminação de invasores aumenta a pontuação e pode gerar itens de melhoria.
- As melhorias podem aumentar a velocidade do jogador, a velocidade dos robôs, o alcance de ataque ou adicionar um robô à equipe.
- As melhorias duram até o final da partida e possuem limites para manter o equilíbrio.
- A quantidade e a velocidade dos invasores aumentam progressivamente a cada onda.

## Condição de vitória
Não existe uma vitória definitiva. O objetivo é sobreviver ao maior número possível de ondas e superar o recorde histórico.

## Condição de derrota
A partida termina quando o servidor perde todos os seus pontos de integridade. Ao final, serão exibidos a pontuação, a onda alcançada e o recorde histórico.

## Elementos previstos
- Personagem controlado pelo jogador.
- Servidor central.
- Robôs de defesa autônomos.
- Invasores e agentes autorizados.
- Itens de melhoria coletáveis.
- Indicadores de pontuação, integridade do servidor e onda atual.
- Tela inicial e tela de fim de jogo.

## Controles previstos

| Tecla | Ação |
|---|---|
| Setas direcionais / WASD | Movimentar o personagem |
| ENTER | Iniciar ou reiniciar a partida |
| ESC | Pausar ou retomar a partida |

Os ataques e a coleta de melhorias acontecem automaticamente.

## Organização inicial do código
- `main.py`: inicialização, movimentação, atualização e exibição do jogo.
- `logica.py`: decisões dos robôs, comportamento dos invasores, colisões e melhorias.
- `arquivos.py`: leitura e escrita do recorde.
- `tests/test_logica.py`: testes das principais funções.
- `assets/`: imagens produzidas pelo grupo ou recursos devidamente creditados.
- `docs/proposta.md`: proposta inicial do jogo.
- `README.md`: descrição, controles e instruções de execução.

O código será organizado em funções simples, com nomes claros para as variáveis e valores de configuração fáceis de alterar.

## Estruturas de dados previstas
- **Listas:** armazenar robôs, invasores, agentes autorizados e melhorias presentes no mapa.
- **Dicionários:** armazenar atributos dos personagens e estatísticas das invasões.
- **Tuplas:** representar coordenadas e cores.
- **Variáveis:** controlar pontuação, integridade do servidor, tempo e onda atual.

## Recursos necessários
- Python 3.
- Biblioteca Pygame.
- Biblioteca random para geração de elementos aleatórios.
- Biblioteca unittest para testes.
- Formas geométricas para a primeira versão e imagens simples produzidas ou selecionadas pelo grupo para a versão final.

## Uso previsto de arquivos
O recorde histórico será armazenado em um arquivo chamado `recorde.txt`. O programa carregará o recorde ao iniciar e atualizará o arquivo quando a pontuação anterior for superada. Caso o arquivo não exista, o recorde inicial será zero.

## Testes planejados
- Verificar se o personagem respeita os limites do cenário.
- Verificar se os robôs selecionam invasores e ignoram agentes autorizados.
- Testar a adaptação das próximas ondas conforme o histórico das invasões.
- Verificar a redução da integridade do servidor e a condição de derrota.
- Testar a coleta e os efeitos das melhorias.
- Verificar o cálculo da pontuação e o salvamento do recorde.

## Principais dificuldades esperadas
- Implementar a movimentação automática dos robôs.
- Fazer com que os robôs selecionem corretamente seus alvos.
- Equilibrar a dificuldade das ondas e a frequência das melhorias.
- Organizar o código de maneira simples e compreensível.

## Escopo mínimo para a entrega final
- Uma arena funcional de ação e sobrevivência.
- Movimentação do personagem pelo teclado.
- Dois robôs iniciais com seleção automática de alvos.
- Identificação de agentes autorizados e invasores.
- Adaptação simples dos invasores ao histórico das ondas.
- Sistema de ondas e melhorias coletáveis.
- Integridade do servidor, pontuação e tela de fim de jogo.
- Leitura e escrita do recorde em arquivo.
- Código organizado em funções, documentação e testes de lógica.

## Melhorias possíveis
- Ataque automático simples do personagem principal.
- Novos tipos de invasores com diferentes velocidades e resistências.
- Melhorias de dano e velocidade de ataque dos robôs.
- Efeitos sonoros e novos cenários.

## Declaração de originalidade
A proposta combina uma mecânica de sobrevivência com o controle indireto de agentes autônomos, melhorias coletáveis e adaptação dos invasores. O grupo se compromete a revisar e compreender o código desenvolvido, identificar o uso de ferramentas de inteligência artificial e indicar eventuais códigos reaproveitados ou recursos de terceiros conforme as orientações da disciplina.

**Nome:**

> Escreva aqui.

## 2. Integrantes do grupo

- Nome 1:
- Nome 2:
- Nome 3:
- Nome 4:

## 3. Tema escolhido

Indique qual tema específico o grupo escolheu **dentro do eixo temático definido no enunciado**.

**Tema:**

> Escreva aqui.

**Como esse tema se relaciona com o jogo?** Explique brevemente (2 a 4 linhas) como ele aparecerá nos objetivos, nas regras ou nos desafios, e não apenas nas imagens ou no cenário.

> Escreva aqui.

## 4. Tipo de jogo

Indique o estilo do jogo. Exemplos: desviar de obstáculos, coleta de itens, labirinto, perguntas e respostas, memória, Pong, Snake, Breakout, corrida ou sobrevivência simples.

**Tipo escolhido:**

> Escreva aqui.

## 5. Descrição geral do jogo

Explique, em poucas linhas, como o jogo funcionará. O que aparece na tela? O que o jogador controla? O que ele precisa fazer e quais desafios encontrará?

**Descrição:**

> Escreva aqui.

## 6. Objetivo do jogador

Descreva o objetivo principal. Por exemplo: coletar itens, sobreviver por determinado tempo, chegar ao final de um percurso ou completar desafios.

**Objetivo:**

> Escreva aqui.

## 7. Regras principais

Liste até cinco regras que expliquem o funcionamento do jogo. Exemplos: o jogador começa com três vidas; acertos somam pontos; colisões retiram vidas.

- Regra 1:
- Regra 2:
- Regra 3:
- Regra 4:
- Regra 5:

## 8. Condição de vitória

Explique como o jogador vence ou conclui a partida. Exemplos: alcançar uma pontuação, finalizar uma fase ou completar todas as tarefas.

**Condição de vitória:**

> Escreva aqui.

## 9. Condição de derrota ou encerramento

Explique quando a partida termina ou como o jogador perde. Exemplos: esgotar as vidas, acabar o tempo ou atingir o limite de erros.

**Condição de derrota ou encerramento:**

> Escreva aqui.

## 10. Elementos previstos no jogo

Descreva brevemente os elementos mais importantes, sem precisar detalhar a implementação.

- **Personagem ou elemento principal:**
- **Obstáculos ou desafios:**
- **Itens ou objetos de interação (se houver):**
- **Pontuação, vidas, tempo ou progresso:**

## 11. Controles previstos

Informe como o jogador vai interagir com o jogo (por exemplo, setas para movimentar, espaço para agir ou mouse para selecionar).

**Controles:**

> Escreva aqui.

## 12. Principais dificuldades esperadas

Cite até três dificuldades que o grupo espera enfrentar. Exemplos: movimentação, colisões, controle de tempo, testes ou uso do GitHub.

- Dificuldade 1:
- Dificuldade 2:
- Dificuldade 3:

## 13. Escopo mínimo para a entrega final

Descreva a **versão mais simples que já seria jogável**, com as interações e regras essenciais. Evite planejar funcionalidades demais.

**Escopo mínimo:**

> Escreva aqui.

## 14. Possíveis melhorias, caso haja tempo

Liste até três funcionalidades extras para implementar somente depois que a versão mínima estiver funcionando. Exemplos: sons, fases, ranking, animações ou menu inicial.

- Melhoria 1:
- Melhoria 2:
- Melhoria 3:
