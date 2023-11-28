from threading import Semaphore
from Controlador import Controlador
from Sessao import Sessao
from vars_globais import *

class ControladorSessoes(Controlador):
    def __init__(self, observador):
        self.sessoes = []
        self.faixa_etaria = None
        self.prox_faixa_etaria = None
        self.end = False
        super().__init__(name="ControladorSessoes", observador=observador)

    def run(self):
        self.semaforo.acquire() # Esperar ser chamado 

        while (True):
            # Se não tem nenhuma sessão ativa
            if (not(self.observador.experiencia_ativa)):
                # Cria e inicia proxima sessao
                self.sessoes.append(Sessao(faixa_etaria=self.prox_faixa_etaria, observador=self))
                self.sessoes[len(self.sessoes)-1].start()
                self.observador.notify_inicio_experiencia(self.sessoes[0].faixa_etaria)
            #else:
                # Espera acabar sessao atual
                #if (self.sessoes[len(self.sessoes)-1].terminou):
                    #self.observador.notify_fim_experiencia(self.faixa_etaria)

            if (self.end):
                break

