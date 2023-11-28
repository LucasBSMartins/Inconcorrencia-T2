import time, random
from Controlador import Controlador
from vars_globais import *

class ControladorFila(Controlador):
    def __init__(self, observador):
        self.total_pessoas = 0
        super().__init__(name="ControladorFila", observador=observador)

    def run(self):
        while (True):
            with mutex_fila_entrada:
                cliente = fila_pre_entrada.get()
                fila_entrada.append(cliente)
                semaforo_print.acquire()
                self.observador.notify_chegou_na_fila(cliente)
                self.total_pessoas += 1

            if (self.total_pessoas != n_pessoas):
                time.sleep(unid_tempo / 1000 * random.randint(0, max_intervalo))
            if (self.total_pessoas == n_pessoas):
                break

