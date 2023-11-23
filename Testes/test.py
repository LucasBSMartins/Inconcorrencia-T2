import sys
import time 
import random
import queue
from threading import Thread, Semaphore, Lock, Condition 

lock = Lock()
sessao_lock = Lock()
remover_lock = Lock()
terminou_lock = Lock()
item_no_buffer = Condition(lock)
entrar_na_exp = Condition(sessao_lock)

a = Semaphore(0)
semaforo_entrar_na_fila = Semaphore(1)
semaforo_sessao = Semaphore(1)

class Cliente(Thread):		       	                             # subclasse de Thread 
    def __init__(self, name, faixa_etaria):             
        self.faixa_etaria = faixa_etaria
        self.semaforo = Semaphore(0)
        self.participou = False
        super().__init__(name=name)		                         # chama construtor da superclasse 

    def run(self):
        semaforo_entrar_na_fila.acquire()
        fila_pra_entrar.append(self)
        semaforo_entrar_na_fila.release()


def sessao(faixa_etaria_a):
    global faixa_etaria_atual
    global sessao_em_progresso
    global pessoas_na_sessao
    global fila_sessao

    pessoas_na_sessao = 0
    tempo_sessao = permanencia * unid_tempo / 1000
    tempo_inicial = time.time()
    fila_clientes_na_sessao = []
    faixa_etaria_atual = faixa_etaria_a

    while time.time() - tempo_inicial < tempo_sessao:
        if len(fila_sessao) != 0:
            with sessao_lock:
                with terminou_lock:
                    if not(terminou):
                        a.acquire()
                sessao_em_progresso = True
                cliente_sessao = fila_sessao.pop(0)
                fila_clientes_na_sessao.append(cliente_sessao)
                pessoas_na_sessao += 1
            print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(cliente_sessao.name, faixa_etaria_atual, pessoas_na_sessao))

    print("[Ixfera] Pausando a experiencia %s." %(faixa_etaria_atual))
    with sessao_lock:
        sessao_em_progresso = False
    while len(fila_clientes_na_sessao) != 0:
        pessoas_na_sessao -= 1 
        print("[Pessoa %s / %s] Saiu da Ixfera (quantidade = %d)." %(fila_clientes_na_sessao[0].name, fila_clientes_na_sessao[0].faixa_etaria, pessoas_na_sessao))
        with terminou_lock:
            if not(terminou):
                with lock:
                    fila_clientes.pop(fila_clientes_na_sessao[0])
                    fila_clientes_na_sessao.pop(0)
            else:
                fila_clientes.pop(fila_clientes_na_sessao[0])
                fila_clientes_na_sessao.pop(0)
    semaforo_sessao.release()

def entrar_na_fila():
    z = 0
    global sessao_em_progresso
    global pessoas_na_sessao
    global terminou

    while(z < n_pessoas):
        with lock:
            fila_clientes.put(fila_pra_entrar[0])
            print("[Pessoa %s / %s] Aguardando na fila." %(fila_pra_entrar[0].name, fila_pra_entrar[0].faixa_etaria))
            z += 1
            item_no_buffer.notify()
            with sessao_lock:
                if sessao_em_progresso and pessoas_na_sessao < n_vagas:
                    fila_sessao.append(fila_pra_entrar[0])
            
            fila_pra_entrar.pop(0)
            a.release()

        intervalo_chegada = random.randint(1, max_intervalo)
        time.sleep(intervalo_chegada * unid_tempo / 1000)    
    with terminou_lock:
        terminou = True

def atracao():
    global faixa_etaria_atual
    global fila_remover
    global pessoas_na_sessao

    while(not(terminou) or len(fila_clientes) != 0):
        with lock:       
            if fila_clientes.empty():
                item_no_buffer.wait()
            else:
                semaforo_sessao.acquire()
                pessoas_na_sessao = 0
                cliente_0 = fila_clientes.get()
                faixa_etaria_sessao = cliente_0.faixa_etaria
                fila_verificar = queue.Queue(n_pessoas)
                fila_verificar = fila_clientes
                while not(fila_verificar.empty()):
                    if fila_verificar.get().faixa_etaria == faixa_etaria_sessao:
                        fila_sessao.append(fila_verificar.get())
                        pessoas_na_sessao += 1
                        if pessoas_na_sessao == n_vagas:
                            break
                sessao_nova = Thread(target=sessao(faixa_etaria_a=faixa_etaria_sessao))
                sessao_nova.start()
        sessao_nova.join()


def criar_threads(n_pessoas, semente):
    random.seed(semente)
    lista_clientes = []

    print("[Ixfera] Simulacao iniciada")

    for i in range(n_pessoas):
        x = random.randint(0,2)
        if x == 1:
            faixa_e = "A"
        elif x == 2:
            faixa_e = "B"
        else: 
            faixa_e = "C"

        lista_clientes.append(Cliente(name=str(i), faixa_etaria=faixa_e))
        lista_clientes[i].start()


    return lista_clientes

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
n_pessoas = 10#int(input("Número total de pessoas: "))
n_vagas = 3#int(input("Número total de vagas na atração: "))
permanencia = 3000#int(input("Permanência na atração: "))
max_intervalo = 2# int(input("Intervalo máximo entre chegadas: "))
semente = 2#int(input("Semente do gerador de números aleatórios: "))
unid_tempo = 2 #int(input("Tempo correspondente a uma unidade de tempo (em milissegundos): "))
fila_clientes = queue.Queue(n_pessoas)
fila_pra_entrar = []
fila_remover = []
fila_sessao = []
terminou = False
faixa_etaria_atual = ""
sessao_em_progresso = False

# Chamar a função de simulação com os parâmetros fornecidos
lista_clientes = criar_threads(n_pessoas, semente)
ixfera = Thread(target=atracao)
fila = Thread(target=entrar_na_fila)
fila.start()
ixfera.start()
for i in range(len(lista_clientes)):
    lista_clientes[i].join()

ixfera.join()
fila.join()
print("[Ixfera] Simulacao finalizada")