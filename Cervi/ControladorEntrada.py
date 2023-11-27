from threading import Semaphore
from Controlador import Controlador
from vars_globais import *

class ControladorEntrada(Controlador):
    def __init__(self, observador):
        super().__init__(name="ControladorEntrada", observador=observador)

    def run(self):
        self.semaforo.acquire()
        while (len(fila_entrada)):
            cliente = fila_entrada[0]
            if (not(self.observador.experiencia_ativa)):
                self.observador.notify_prox_faixa_etaria(cliente.faixa_etaria)
                cliente.semaforo_entrada.release()
                self.semaforo.acquire()
                with mutex_fila_entrada:
                    fila_entrada.pop(0)
                self.observador.notify_entrada(cliente)
            else:
                if (self.observador.faixa_etaria_atual == cliente.faixa_etaria and self.observador.qtd_pessoas_na_exp < n_vagas):
                    with mutex_fila_entrada:
                        fila_entrada.pop(0)
                    self.observador.notify_entrada(cliente)
