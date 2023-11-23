import sys
from queue import Queue
import time 
import random
from threading import Thread, Semaphore, Lock, Condition

n_pessoas = 0
n_vagas = 0
permanencia = 0
max_intervalo = 0
semente = 0
unid_tempo = 0
terminou = False

fila_clientes = []
listapop = []

contador_threads_terminadas = Lock()

somar_pessoas = Lock()
quantidade = 0

entrar_na_fila = Lock()
threads_terminadas = 0

entrar_na_experiencia = Lock()
pessoas_na_esfera = []

lock = Lock()


class Clientes_na_fila(Thread):		       	                 # subclasse de Thread 
  def __init__(self, faixa_etaria):             
    self.faixa_etaria = faixa_etaria
    self.semaforo = Semaphore(0)
    self.semaforo_exp = Semaphore(0)
    super().__init__(name="")		                         # chama construtor da superclasse 

  def run(self):				                             # método executado pela thread 
    global threads_terminadas
    global max_intervalo
    global unid_tempo
    global quantidade

    entrar_fila(self, max_intervalo, unid_tempo)

    if self.faixa_etaria == "A":
        self.semaforo.acquire()
        with somar_pessoas:
            quantidade += 1
            print("[%s / %s] Entrou na Ixfera (quantidade = %d)" %(self.name, self.faixa_etaria, quantidade))
            experiencia(self)
        self.semaforo_exp.acquire()

    elif self.faixa_etaria == "B":
        self.semaforo.acquire()
        with somar_pessoas:
            quantidade += 1
            print("[%s / %s] Entrou na Ixfera (quantidade = %d)" %(self.name, self.faixa_etaria, quantidade))
            experiencia(self)
        self.semaforo_exp.acquire()

    else:
        self.semaforo.acquire()
        with somar_pessoas:
            quantidade += 1
            print("[%s / %s] Entrou na Ixfera (quantidade = %d)" %(self.name, self.faixa_etaria, quantidade))
            experiencia(self)
        self.semaforo_exp.acquire()

    with contador_threads_terminadas:
        threads_terminadas += 1
        quantidade -= 1
        print("[%s / %s] Saiu da Ixfera (quantidade = %d)" %(self.name, self.faixa_etaria, quantidade))

        if threads_terminadas == len(listapop):
            quantidade = 0
            sem_controle.release()

class Atracao(Thread):
    def __init__(self, name, nvagas, fila_clientes):             
        self.nvagas = nvagas
        self.fila_clientes = fila_clientes
        super().__init__(name=name)                    

    def run(self):
        global threads_terminadas
        global faixa_etaria_atual
        global fila_clientes
        global listapop
        global terminou

        sem_comecar.acquire()

        while ((len(fila_clientes) != 0) and (terminou)):

            sem_controle.acquire()
            with contador_threads_terminadas:
                threads_terminadas = 0

            self.faixa_etaria = fila_clientes[0].faixa_etaria
            faixa_etaria_atual = self.faixa_etaria
            listapop = []
            z = 0
            print("[Ixfera] Iniciando a experiencia %s " %(self.faixa_etaria))
    
            if self.faixa_etaria == "A":
                for i in range(len(fila_clientes)):
                    if fila_clientes[i].faixa_etaria == "A":
                        fila_clientes[i].semaforo.release()
                        listapop.append(i)
                        z += 1
                        if z == self.nvagas:
                           break 
            elif self.faixa_etaria == "B":
                for i in range(len(fila_clientes)):
                    if fila_clientes[i].faixa_etaria == "B":
                        fila_clientes[i].semaforo.release()
                        listapop.append(i)
                        z += 1
                        if z == self.nvagas:
                            break 
            else:
                for i in range(len(fila_clientes)):
                    if fila_clientes[i].faixa_etaria == "C":
                        fila_clientes[i].semaforo.release()
                        listapop.append(i)
                        z += 1
                        if z == self.nvagas:
                            break 
    
            for i in range(len(listapop)):
                fila_clientes.pop(listapop[i]-i)

def entrar_fila(cliente, max_intervalo, unid_tempo):
    global fila_clientes

    with entrar_na_fila:

        fila_clientes.append(cliente)
        print("[Pessoa %d / %s] Aguardando na fila" %((len(fila_clientes)), cliente.faixa_etaria))
       
        if len(fila_clientes) == n_pessoas:
            sem_comecar.release()

    cliente.name = "Pessoa " + str(len(fila_clientes))
    intervalo_chegada = random.randint(1, max_intervalo)
    time.sleep(intervalo_chegada * unid_tempo / 1000)
       
def experiencia(cliente):
    
    with entrar_na_experiencia:
        global pessoas_na_esfera
        pessoas_na_esfera.append(cliente)
        
        if len(listapop) == len(pessoas_na_esfera):
            time.sleep(permanencia * unid_tempo / 1000)
            print("[Ixfera] Pausando a experiencia %s" %(cliente.faixa_etaria))
            for i in range(len(pessoas_na_esfera)):
                pessoas_na_esfera[i].semaforo_exp.release()
            pessoas_na_esfera = []

def criar_threads(n_pessoas, semente):
    random.seed(semente)
    clientes = []

    print("[Ixfera] Simulacao iniciada")

    for i in range(n_pessoas):
        x = random.randint(0,2)
        if x == 1:
            faixa_e = "A"
        elif x == 2:
            faixa_e = "B"
        else: 
            faixa_e = "C"

        clientes.append(Clientes_na_fila(faixa_etaria=faixa_e))
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

sem_controle = Semaphore(value=1)
sem_comecar = Semaphore(value=0)
sem_fim_exp = Semaphore(value=0)

# Chamar a função de simulação com os parâmetros fornecidos
clientes = criar_threads(n_pessoas, semente)

atracao = Atracao(name="Atracao", nvagas=n_vagas, fila_clientes=fila_clientes)
atracao.start()

atracao.join()
print("[Ixfera] Simulacao finalizada")
for i in range(len(fila_clientes)):
    clientes[i].join()