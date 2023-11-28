from threading import Lock, Semaphore
from queue import Queue

mutex_fila_pre_entrada = Lock()
mutex_fila_entrada = Lock()
semaforo_print = Semaphore(1)

threads_clientes = []
fila_entrada = []
fila_pre_entrada = Queue()
pessoas_dentro_atracao = []
n_pessoas, n_vagas, permanencia, max_intervalo, semente, unid_tempo = 0, 0, 0, 0, 0, 0

