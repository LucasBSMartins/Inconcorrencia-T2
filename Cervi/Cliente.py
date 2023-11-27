import time
from threading import Thread, Semaphore
from vars_globais import *

class Cliente(Thread):
    def __init__(self, name, faixa_etaria):
        self.faixa_etaria = faixa_etaria
        self.assistiu = False
        self.semaforo_entrada = Semaphore(0)
        self.semaforo_saida = Semaphore(0)
        super().__init__(name=name)

    def run(self):
        with mutex_fila_pre_entrada:
            fila_pre_entrada.put(self)

        self.semaforo_entrada.acquire()
        time.sleep(permanencia)
        self.assistiu = True
        self.semaforo_saida.acquire()

