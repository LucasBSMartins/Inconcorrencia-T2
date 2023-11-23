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
experiencia_rolando = False
z = 0

fila_clientes = []
listapop = []
fila_pra_produzir = []

contador_threads_terminadas = Lock()

somar_pessoas = Lock()
quantidade = 0

entrar_na_fila = Lock()
threads_terminadas = 0

entrar_na_experiencia = Lock()
experienciaa = Condition(entrar_na_experiencia)
pessoas_na_esfera = []


lock = Lock()
item_no_buffer = Condition(lock)


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

    entrar_fila(self)

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
        global experiencia_rolando


        while (not(terminou)):

            with lock:
                if len(fila_clientes) == 0:
                    item_no_buffer.wait()
                
                with entrar_na_experiencia:
                    if not(experiencia_rolando):
                        experienciaa.wait()
                        self.faixa_etaria = fila_clientes[0].faixa_etaria
                        faixa_etaria_atual = self.faixa_etaria
                        listapop = []
                        listapop.append(fila_clientes[0])
                        print("[Ixfera] Iniciando a experiencia %s " %(self.faixa_etaria))
                        fila_clientes[0].semaforo.release()
                    else:
                        for i in range(fila_clientes):
                            if len(listapop) == n_vagas:
                                break
                            if fila_clientes[i].faixa_etaria == self.faixa_etaria:
                                listapop.append(fila_clientes[i])
                                fila_clientes[i].semaforo.release()
                    if len(listapop) != 0 and len(fila_clientes) != 0:
                            for i in range(len(listapop)):
                                j = 0
                                while True:
                                    if fila_clientes[j] == listapop[i]:
                                        fila_clientes.pop(j)
                                        break
                                    j += 1
                    

def entrar_fila(cliente):
    global fila_clientes
    global fila_pra_produzir
    global z

    with entrar_na_fila:
        fila_pra_produzir.append(cliente)
    
    while (len(fila_pra_produzir) != 0):
        with lock:
            z += 1
            fila_clientes.append(fila_pra_produzir[0])
            print("[Pessoa %d / %s] Aguardando na fila" %((z), fila_pra_produzir[0].faixa_etaria))
            fila_pra_produzir[0].name = "Pessoa " + str(z)
            fila_pra_produzir.pop(0)
            item_no_buffer.notify()
        intervalo_chegada = random.randint(1, max_intervalo)
        time.sleep(intervalo_chegada * unid_tempo / 1000)

def experiencia(cliente):
    
    with entrar_na_experiencia:
        global pessoas_na_esfera
        global experiencia_rolando
        pessoas_na_esfera.append(cliente)

        if not(experiencia_rolando):
            if len(listapop) == 1:
                experiencia_rolando = True
                time.sleep(permanencia * unid_tempo / 1000)
                experiencia_rolando = False
                experienciaa.notify()
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
item_no_buffer = Condition(lock)

# Chamar a função de simulação com os parâmetros fornecidos
clientes = criar_threads(n_pessoas, semente)

atracao = Atracao(name="Atracao", nvagas=n_vagas, fila_clientes=fila_clientes)
atracao.start()

atracao.join()
print("[Ixfera] Simulacao finalizada")
for i in range(len(fila_clientes)):
    clientes[i].join()