import sys
from queue import Queue
import time 
import random
from threading import Thread, Semaphore, Lock, Condition
#from atracao import *

sem_cliente_A = None
sem_cliente_B = None
sem_cliente_C = None
sem_controle = Semaphore(value=1)

contador_threads_terminadas = Lock()
threads_terminadas = 0


class Clientes_na_fila(Thread):		       	                 # subclasse de Thread 
  def __init__(self, name, faixa_etaria):             
    self.faixa_etaria = faixa_etaria
    super().__init__(name=name)		                         # chama construtor da superclasse 

  def run(self):				                             # método executado pela thread 
    global threads_terminadas
    intervalo_chegada = random.randint(1, max_intervalo)
    time.sleep(intervalo_chegada * unid_tempo / 1000)
    print("%s entrou na fila" %(self.name))

    if self.faixa_etaria == "A":
        print(self.name + " espera")
        sem_cliente_A.acquire()
        print(self.name + " terminou semaforo " + self.faixa_etaria)
    elif self.faixa_etaria == "B":
        print(self.name + " espera")
        sem_cliente_B.acquire()
        print(self.name + " terminou semaforo " + self.faixa_etaria)
    else:
        print(self.name + " espera")
        sem_cliente_C.acquire()
        print(self.name + " terminou semaforo " + self.faixa_etaria)
    with contador_threads_terminadas:
        threads_terminadas += 1


class Atracao(Thread):
    def __init__(self, name, nvagas, fila_clientes):             
        self.nvagas = nvagas
        self.fila_clientes = fila_clientes
        super().__init__(name=name)                     # chama construtor da superclasse 

    def run(self):
        global threads_terminadas
        global faixa_etaria_atual
        global fila_clientes
        while (len(fila_clientes) != 0):

            sem_controle.acquire()
            with contador_threads_terminadas:
                threads_terminadas = 0

            self.faixa_etaria = fila_clientes[0].faixa_etaria
            faixa_etaria_atual = self.faixa_etaria
            listapop = []
            z = 0
            print(self.faixa_etaria)

            if self.faixa_etaria == "A":
                for i in range(len(fila_clientes)):
                    if fila_clientes[i].faixa_etaria == "A":
                        sem_cliente_A.release()
                        listapop.append(i)
                        z += 1
                        if z == self.nvagas:
                            break 
            elif self.faixa_etaria == "B":
                for i in range(len(fila_clientes)):
                    if fila_clientes[i].faixa_etaria == "B":
                        sem_cliente_B.release()
                        listapop.append(i)
                        z += 1
                        if z == self.nvagas:
                            break 
            else:
                for i in range(len(fila_clientes)):
                    if fila_clientes[i].faixa_etaria == "C":
                        sem_cliente_C.release()
                        listapop.append(i)
                        z += 1
                        if z == self.nvagas:
                            break 
            while (True):
                with contador_threads_terminadas:
                    if threads_terminadas == len(listapop):
                        sem_controle.release()
                        break
            for i in range(len(listapop)):
                fila_clientes.pop(listapop[i]-i)





def criar_threads(n_pessoas, n_vagas, permanencia, max_intervalo, semente, unid_tempo):
    random.seed(semente)
    clientes = []

    global sem_cliente_A
    global sem_cliente_B
    global sem_cliente_C
    sem_cliente_A = Semaphore(value=0)
    sem_cliente_B = Semaphore(value=0)
    sem_cliente_C = Semaphore(value=0)


    for i in range(n_pessoas):
        x = random.randint(0,2)
        if x == 1:
            faixa_e = "A"
        elif x == 2:
            faixa_e = "B"
        else: 
            faixa_e = "C"

        clientes.append(Clientes_na_fila(name="cliente " + str(i), faixa_etaria=faixa_e))
        clientes[i].start()

    return clientes

'''
if __name__ == "__main__":
    # Verificar se a quantidade correta de argumentos foi fornecida
    if len(sys.argv) != 7:
        print("Uso correto: python3 ixphere.py <N_PESSOAS> <N_VAGAS> <PERMANENCIA> <MAX_INTERVALO> <SEMENTE> <UNID_TEMPO>")
        sys.exit(1)

    # Obter os parâmetros da linha de comando
    n_pessoas = int(sys.argv[1])
    n_vagas = int(sys.argv[2])
    permanencia = int(sys.argv[3])
    max_intervalo = int(sys.argv[4])
    semente = int(sys.argv[5])
    unid_tempo = int(sys.argv[6])
'''

# Obter entrada do usuário para os parâmetros
n_pessoas = int(input("Número total de pessoas: "))
n_vagas = int(input("Número total de vagas na atração: "))
permanencia = int(input("Permanência na atração: "))
max_intervalo = int(input("Intervalo máximo entre chegadas: "))
semente = int(input("Semente do gerador de números aleatórios: "))
unid_tempo = int(input("Tempo correspondente a uma unidade de tempo (em milissegundos): "))

# Chamar a função de simulação com os parâmetros fornecidos
clientes = criar_threads(n_pessoas, n_vagas, permanencia, max_intervalo, semente, unid_tempo)
fila_clientes = clientes

atracao = Atracao(name="Atracao", nvagas=n_vagas, fila_clientes=fila_clientes)
atracao.start()

atracao.join()
for i in range(len(fila_clientes)):
    fila_clientes[i].join()