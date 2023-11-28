from threading import Thread, Semaphore, Lock
from Sessao import Sessao
from ControladorFila import ControladorFila
from ControladorSessoes import ControladorSessoes
from ControladorEntrada import ControladorEntrada
from vars_globais import *

class Ixfera(Thread):
    def __init__(self):
        self.controladores = {
            "Fila" : ControladorFila(self),
            "Entrada" : ControladorEntrada(self),
            "Sessoes" : ControladorSessoes(self)
        }
        self.total_pessoas = 0
        self.qtd_pessoas_na_exp = 0
        self.mutex_pessoas_na_exp = Lock()
        self.semaforo = Semaphore(0)
        self.experiencia_ativa = False
        self.faixa_etaria_atual = None
        super().__init__(name="Ixfera")

    def run(self):
        print("[Ixfera] Simulacao iniciada")

        # Iniciar threads dos controladores
        for control in self.controladores.values():
            control.start()
        
        # Controle de Saida das Pessoas
        while True:
            for pessoa in pessoas_dentro_atracao:
                if (pessoa.assistiu):
                    self.notify_saida(pessoa)
            if (self.total_pessoas == n_pessoas):
                self.controladores['Sessoes'].end = True
                break
        
        # Sincronizar threads dos controladores
        for control in self.controladores.values():
            control.join()

        print("[Ixfera] Simulacao finalizada")


    # Notificações vindas dos controladores

    def notify_prox_faixa_etaria(self, faixa_etaria):
        self.controladores['Sessoes'].prox_faixa_etaria = faixa_etaria
        self.controladores['Sessoes'].semaforo.release()

    def notify_chegou_na_fila(self, cliente):
        print(f'[Pessoa {cliente.name} / {cliente.faixa_etaria}] Aguardando na fila.')
        self.controladores['Entrada'].semaforo.release()

    def notify_inicio_experiencia(self, experiencia):
        print(f'[Ixfera] Iniciando a experiencia {experiencia}')
        self.faixa_etaria_atual = experiencia
        self.experiencia_ativa = True
        self.controladores['Entrada'].semaforo.release()

    def notify_fim_experiencia(self, experiencia):
        self.faixa_etaria_atual = None
        self.experiencia_ativa = False
        print(f'[Ixfera] Pausando a experiencia {experiencia}')

    def notify_entrada(self, cliente):
        with self.mutex_pessoas_na_exp:
            self.qtd_pessoas_na_exp += 1
            pessoas_dentro_atracao.append(cliente)
        print(f'[Pessoa {cliente.name} / {cliente.faixa_etaria}] Entrou na Ixfera (quantidade = {self.qtd_pessoas_na_exp})')

    def notify_saida(self, cliente):
        with self.mutex_pessoas_na_exp:
            self.qtd_pessoas_na_exp -= 1
            pessoas_dentro_atracao.pop(0)
        print(f'[Pessoa {cliente.name} / {cliente.faixa_etaria}] Saiu da Ixfera (quantidade = {self.qtd_pessoas_na_exp})')
        self.total_pessoas += 1
