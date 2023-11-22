import threading
import queue
import time
import random

BUFFER_SIZE = 5
NUM_PRODUTORES = 2
NUM_CONSUMIDORES = 2

buffer = queue.Queue(BUFFER_SIZE)
lock = threading.Lock()
encerrar_programa = False

class Produtor(threading.Thread):
    def run(self):
        global encerrar_programa
        while not encerrar_programa:
            item = random.randint(1, 100)
            with lock:
                if buffer.full():
                    print("Buffer cheio. Produtor aguardando.")
                    lock.release()
                    time.sleep(1)
                    lock.acquire()
                buffer.put(item)
                print(f"Produzido {item}. Tamanho do buffer: {buffer.qsize()}")
            time.sleep(random.uniform(0.1, 0.5))

class Consumidor(threading.Thread):
    def run(self):
        global encerrar_programa
        while not encerrar_programa:
            with lock:
                if buffer.empty():
                    print("Buffer vazio. Consumidor aguardando.")
                    lock.release()
                    time.sleep(1)
                    lock.acquire()
                item = buffer.get()
                print(f"Consumido {item}. Tamanho do buffer: {buffer.qsize()}")
            time.sleep(random.uniform(0.1, 0.5))

# Inicializar produtores e consumidores
produtores = [Produtor() for _ in range(NUM_PRODUTORES)]
consumidores = [Consumidor() for _ in range(NUM_CONSUMIDORES)]

# Iniciar threads
for produtor in produtores:
    produtor.start()

for consumidor in consumidores:
    consumidor.start()

# Aguardar um tempo arbitrário ou até o usuário decidir encerrar o programa
time.sleep(10)

# Informar as threads para encerrar
encerrar_programa = True

# Aguardar até que todas as threads terminem
for produtor in produtores:
    produtor.join()

for consumidor in consumidores:
    consumidor.join()

print("Programa encerrado.")
