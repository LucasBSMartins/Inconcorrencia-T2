import random
import time

class IxferaTM:
    def __init__(self):
        self.pessoas = {'A': [], 'B': [], 'C': []}
        self.fila = []
        self.espera = {'A': 0, 'B': 0, 'C': 0}
        self.experiencia = None
        self.ocupacao = 0
        self.inicio_simulacao = 0
        self.final_simulacao = 0

    def agendar_pessoa(self, idade, faixa_etaria):
        pessoa = {'id': idade, 'faixa': faixa_etaria}
        self.pessoas[faixa_etaria].append(pessoa)
        self.fila.append(pessoa)

    def iniciar_simulacao(self):
        self.inicio_simulacao = time.time()
        self.proximo_ingresso()

    def proximo_ingresso(self):
        if len(self.fila) == 0:
            self.final_simulacao = time.time()
            self.relatorio_estatistico()
            return

        proximo = self.fila.pop(0)
        print(f'[Pessoa {proximo["id"]} / {proximo["faixa"]}] Aguardando na fila.')

        if self.experiencia is None or self.experiencia != proximo['faixa']:
            if self.experiencia is not None:
                self.ocupacao += time.time() - self.inicio_experiencia
            self.inicio_experiencia = time.time()
            self.experiencia = proximo['faixa']
            print(f'[Ixfera] Iniciando a experiencia {proximo["faixa"]}.')

        self.ocupacao += time.time() - self.inicio_experiencia
        self.inicio_experiencia = time.time()

        print(f'[Pessoa {proximo["id"]} / {proximo["faixa"]}] Entrou na Ixfera (quantidade = {len(self.fila) + 1}).')
        time.sleep(random.uniform(0.1, 2))
        self.proximo_ingresso()

    def relatorio_estatistico(self):
        total_espera = sum(self.espera.values())
        total_tempo = self.final_simulacao - self.inicio_simulacao
        media_espera = {k: (v / len(self.pessoas[k])) for k, v in self.espera.items()}
        ocupacao = (self.ocupacao / total_tempo) * 100

        print('Tempo medio de espera:', ', '.join([f'Faixa {k}: {v:.2f}' for k, v in media_espera.items()]))
        print(f'Taxa de ocupacao: {ocupacao:.2f}%')

if __name__ == '__main__':
    ixfera = IxferaTM()

    # Agende as pessoas com base na faixa etária
    for idade in range(1, 601):
        faixa_etaria = 'A' if idade < 12 else ('B' if idade < 18 else 'C')
        ixfera.agendar_pessoa(idade, faixa_etaria)

    # Inicie a simulação
    ixfera.iniciar_simulacao()