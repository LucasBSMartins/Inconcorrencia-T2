import sys
import time 
import random
import queue
from threading import Thread, Semaphore, Lock, Condition 

lock = Lock()
sessao_lock = Lock()
remover_lock = Lock()
item_no_buffer = Condition(lock)
entrar_na_exp = Condition(sessao_lock)

semaforo_entrar_na_fila = Semaphore(1)
semaforo_sessao = Semaphore(1)


def sessao(faixa_etaria_a):
    global faixa_etaria_atual
    global sessao_em_progresso

    faixa_etaria_atual = faixa_etaria_a
    with sessao_lock:
        sessao_em_progresso = True
        print("[Ixfera] Iniciando a experiencia %s." %(faixa_etaria_atual))
        entrar_na_exp.notify()
    time.sleep(permanencia * unid_tempo / 1000)
    with sessao_lock:
        sessao_em_progresso = False
        print("[Ixfera] Pausando a experiencia %s." %(faixa_etaria_atual))
        semaforo_sessao.release()

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

def entrar_na_fila():
    z = 0
    global sessao_em_progresso
    global pessoas_na_sessao
    
    while(z < n_pessoas):
        with lock:
            with sessao_lock:
                if sessao_em_progresso:
                    entrar_na_exp.wait()
                    if fila_pra_entrar[0].faixa_etaria == faixa_etaria_atual and pessoas_na_sessao < n_vagas:
                        fila_pra_entrar[0].participou = True
                        pessoas_na_sessao += 1
                        print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(fila_pra_entrar[0].name, fila_pra_entrar[0].faixa_etaria, pessoas_na_sessao))
                        fila_pra_entrar.pop(0)
                else:
                    fila_clientes.put(fila_pra_entrar[0])
                    print("[Pessoa %s / %s] Aguardando na fila." %(fila_pra_entrar[0].name, fila_pra_entrar[0].faixa_etaria))
                    fila_pra_entrar.pop(0)
                    z += 1
                    item_no_buffer.notify()

        intervalo_chegada = random.randint(1, max_intervalo)
        time.sleep(intervalo_chegada * unid_tempo / 1000)    

def atracao():
    remover = False
    global faixa_etaria_atual
    global fila_remover
    global pessoas_na_sessao

    while(not(terminou) or len(fila_clientes) != 0):
        with lock:
            if remover:
                with remover_lock:
                    while len(fila_remover) != 0:
                        pessoas_na_sessao -= 1 
                        print("[Pessoa %s / %s] Saiu da Ixfera (quantidade = %d)." %(fila_remover[0].name, fila_remover[0].faixa_etaria, pessoas_na_sessao))
                        fila_remover.pop(0)
                remover = False       
            if fila_clientes.empty():
                item_no_buffer.wait()
            else:
                pessoas_na_sessao = 0
                cliente_0 = fila_clientes.get()
                fila_remover.append(cliente_0)
                faixa_etaria_sessao = cliente_0.faixa_etaria
                pessoas_na_sessao += 1
                print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(cliente_0.name, faixa_etaria_sessao, pessoas_na_sessao))
                for i in range(fila_clientes.qsize()):
                    if fila_clientes[i].faixa_etaria == faixa_etaria_sessao:
                        fila_remover.append(fila_clientes[i])
                        pessoas_na_sessao += 1
                        print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(fila_clientes[i].name, faixa_etaria_sessao, pessoas_na_sessao))
                        if pessoas_na_sessao == n_vagas:
                            break
                sessao_nova = Thread(target=sessao(faixa_etaria_a=faixa_etaria_sessao))
                sessao_nova.start()
                remover = True
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
n_vagas = 2#int(input("Número total de vagas na atração: "))
permanencia = 3000#int(input("Permanência na atração: "))
max_intervalo = 2# int(input("Intervalo máximo entre chegadas: "))
semente = 2#int(input("Semente do gerador de números aleatórios: "))
unid_tempo = 2 #int(input("Tempo correspondente a uma unidade de tempo (em milissegundos): "))
fila_clientes = queue.Queue(n_pessoas)
fila_pra_entrar = []
fila_remover = []
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