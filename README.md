# Trabalho 2 - Programação Concorrente

# Simulador IxferaTM

## Descrição

Uma nova atração que está fazendo muito sucesso em Florianópolis, denominada IxferaTM, foi instalada no estaci-
onamento externo do Villa Romana Shopping. A atração é uma cópia descarada, mas obviamente em proporção muito
menor, do SphereTMde Las Vegas nos EUA (https://www.thespherevegas.com). Ao entrar na atração, os turistas
passam por uma experiência incrível, com tela em 360 graus, som de alta qualidade e diversos efeitos sensoriais.
A IxferaTMpossui três experiências (A, B e C) desenvolvidas para faixas etárias diferentes:
•Experiência A: somente para crianças de 4 a 11 anos (faixa etária A);
•Experiência B: somente para adolescentes entre 12 e 18 anos (faixa etária B); e
•Experiência C: somente para adultos acima de 19 anos (faixa etária C).
As regras de funcionamento da IxferaTMsão:
1. Uma única fila fora da IxferaTMé utilizada para organizar as pessoas em ordem de chegada (pessoas de diferentes
faixas etárias podem estar na fila);
2. Existe somente uma única experiência em curso na IxferaTM(A, B ou C). Devido as experiências estarem
relacionadas às faixas etárias, nunca haverá pessoas de faixas etárias diferentes simultaneamente na atração;
3. Quando a primeira pessoa ingressa na atração, a IxferaTMinicia automaticamente a experiência equivalente à
faixa etária desta pessoa e outras pessoas da mesma faixa etária podem ingressar na atração;
4. Quando a IxferaTMestá funcionando para uma experiência x, ele permanence recebendo pessoas da faixa etária
x na ordem de chegada na fila até que uma outra pessoa de faixa etária diferente x′seja a primeira da fila.
Quando isso acontecer, x′deverá aguardar que todas as pessoas da faixa etária x saiam da atração para x′poder
entrar;
5. A experiência é automaticamente pausada quando não há ninguém na IxferaTMe não existem pessoas aguardando
na fila;
6. Existe um número limitado de vagas (N_VAGAS) na atração, portanto, nunca haverá mais do que N_VAGAS pessoas
simultaneamente na atração;
7. Após entrar na atração, cada pessoa permanece nela por PERMANENCIA unidades de tempo.

## Requisitos

- Python v3.10.12 ou superior

## Como Executar

```bash
python3 ixphere.py <N_PESSOAS> <N_VAGAS> <PERMANENCIA> <MAX_INTERVALO> <SEMENTE> <UNID_TEMPO>
```
• <N_PESSOAS>: é um número inteiro maior do que zero que representa o número total de pessoas que irão ingressar na atração (cada faixa etária deverá conter aproximadamente 1/3 do total de pessoas);

• <N_VAGAS>: é um número inteiro maior do que zero que representa o número total de vagas (lugares) na atração;

• <PERMANENCIA>: é um número inteiro maior do que zero que representa a quantidade de unidades de tempo que
as pessoas permanecem na atração;

• <MAX_INTERVALO>: é um número inteiro maior do que zero que representa o intervalo máximo (medido em
unidades de tempo da simulação) entre a chegada de duas pessoas quaisquer na fila;

• <SEMENTE>: é um número inteiro maior ou igual à zero que representa a semente a ser utilizada para inicializar o gerador de números aleatórios;

• <UNID_TEMPO>: é um número inteiro maior do que zero que representa o tempo, em milissegundos, correspondente a uma unidade de tempo na simulação (quanto maior esse valor, mais lenta será a simulação).