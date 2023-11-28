import time
from threading import Thread, Lock
from vars_globais import *

class Sessao(Thread):
    def __init__(self, faixa_etaria, observador):
        self.faixa_etaria = faixa_etaria
        self.terminou = False
        self.observador = observador
        super().__init__(name="Sessao")

    def run(self):
        tempo_sessao = permanencia * unid_tempo * 1000
        tempo_inicial = time.time()
        self.observador.secao_em_andamento = True

        # Espera dar o tempo da sessao
        while (time.time() - tempo_inicial < tempo_sessao):
            time.sleep(unid_tempo / 1000)

        
        while (len(pessoas_dentro_atracao)):
            with mutex_pessoas_na_exp:
                cliente = pessoas_dentro_atracao[0]
            cliente.semaforo_saida.release()
            cliente.join()
            self.terminou = True
            self.observador.observador.notify_saida(cliente)
        self.observador.observador.notify_fim_experiencia(self.faixa_etaria)
