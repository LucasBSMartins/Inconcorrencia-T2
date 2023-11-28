import sys
import time 
import random
from threading import Thread, Semaphore, Lock, Condition 

lock = Lock()
mutex_flag = Lock()
lista_relogio_lock = Lock()

item_no_buffer = Condition(lock)
semaforo_entrar_na_fila = Semaphore(1)
semaforo_print = Semaphore(0)
semaforo_print_final = Semaphore(0)

fila_clientes = []
fila_pra_entrar = []
relogio_a = []
relogio_b = []
relogio_c = []
sessoes = []
pessoas_na_exp = 0
q_pessoas = 0
q_sessoes = 0
tempo_sessao_total = 0
n_pessoas, n_vagas, permanencia, max_intervalo, semente, unid_tempo = 0, 0, 0, 0, 0, 0