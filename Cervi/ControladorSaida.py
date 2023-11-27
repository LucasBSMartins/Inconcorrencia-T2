from threading import Semaphore
from Controlador import Controlador
from vars_globais import *

class ControladorSaida(Controlador):
    def __init__(self, observador):
        super().__init__(name="ControladorSaida", observador=observador)

    def run(self):
        self.semaforo.acquire()
