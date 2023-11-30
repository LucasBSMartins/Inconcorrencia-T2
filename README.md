# Trabalho 2 - Programação Concorrente

# Simulador IxferaTM

## Requisitos

- Python v3.10.12 ou superior

## Como Executar

```bash
python3 ixphere.py <N_PESSOAS> <N_VAGAS> <PERMANENCIA> <MAX_INTERVALO> <SEMENTE> <UNID_TEMPO>
```
• N_PESSOAS: é um número inteiro maior do que zero que representa o número total de pessoas que irão ingressar na atração (cada faixa etária deverá conter aproximadamente 1/3 do total de pessoas);

• N_VAGAS: é um número inteiro maior do que zero que representa o número total de vagas (lugares) na atração;

• PERMANENCIA: é um número inteiro maior do que zero que representa a quantidade de unidades de tempo que
as pessoas permanecem na atração;

• MAX_INTERVALO: é um número inteiro maior do que zero que representa o intervalo máximo (medido em
unidades de tempo da simulação) entre a chegada de duas pessoas quaisquer na fila;

• SEMENTE: é um número inteiro maior ou igual à zero que representa a semente a ser utilizada para inicializar o gerador de números aleatórios;

• UNID_TEMPO: é um número inteiro maior do que zero que representa o tempo, em milissegundos, correspondente a uma unidade de tempo na simulação (quanto maior esse valor, mais lenta será a simulação).