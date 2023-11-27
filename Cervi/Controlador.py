from threading import Thread, Semaphore

class Controlador(Thread):
    def __init__(self, name, observador):
        self.semaforo = Semaphore(0)
        self.observador = observador
        super().__init__(name=name)

