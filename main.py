import sys
import time 
import random
import queue
from threading import Thread, Semaphore, Lock, Condition 

lock = Lock()
terminou_lock = Lock()
mutex_flag = Lock()
lista_relogio = Lock()

sessao_pronta = Condition()
item_no_buffer = Condition(lock)
semaforo_entrar_na_fila = Semaphore(1)
semaforo_print = Semaphore(0)
semaforo_print_final = Semaphore(0)

class Sessao(Thread):		       	                             # subclasse de Thread 
    def __init__(self, faixa_etaria_a):             
        self.pessoas_na_exp = 0
        self.faixa_etaria_a = faixa_etaria_a
        self.flag = True
        self.pronto = False
        super().__init__(name="Sessao")		                         # chama construtor da superclasse 

    def run(self):
        global fila_sessao
        global q_sessoes

        fila_sessao = []
        tempo_sessao = permanencia * unid_tempo / 1000
        tempo_inicial = time.time()
        
        self.pronto = True
        while time.time() - tempo_inicial < tempo_sessao:
            time.sleep(1 * unid_tempo / 1000)
            with mutex_flag:
                self.flag = True
        with mutex_flag:
            self.flag = None
        while len(fila_sessao) != 0:
            self.pessoas_na_exp -= 1
            fila_sessao[0].semaforo2.release()
            fila_sessao[0].join()
            fila_sessao.pop(0)
            semaforo_print.acquire()   

        with mutex_flag:
            print("[Ixfera] Pausando a experiencia %s." %(self.faixa_etaria_a))
            self.flag = False

class Cliente(Thread):		       	                             # subclasse de Thread 
    def __init__(self, name, faixa_etaria):             
        self.faixa_etaria = faixa_etaria
        self.semaforo = Semaphore(0)
        self.semaforo2 = Semaphore(0)
        self.semaforo_relogio = Semaphore(0)
        self.participou = False
        self.tempo_inicio = 0
        super().__init__(name=name)		                         # chama construtor da superclasse 

    def run(self):
        global fila_sessao
        global sessoes
        global q_pessoas

        semaforo_entrar_na_fila.acquire()
        fila_pra_entrar.append(self)
        semaforo_entrar_na_fila.release()   

        self.semaforo_relogio.acquire()
        self.tempo_inicio = time.time()

        self.semaforo.acquire()
        while True:
            if sessoes[len(sessoes)-1].pronto == True:
                fila_sessao.append(self)
                break
        self.semaforo2.acquire()
        print("[Pessoa %s / %s] Saiu da Ixfera (quantidade = %d)." %(self.name, self.faixa_etaria, sessoes[len(sessoes)-1].pessoas_na_exp))
        semaforo_print.release() 
        
        self.tempo_fim = time.time()
        self.tempo_final_milissegundos = round((self.tempo_fim - self.tempo_inicio) * 1000, 2)

        with lista_relogio:
            if self.faixa_etaria == "A":
                relogio_a.append(self.tempo_final_milissegundos)
            elif self.faixa_etaria == "B":
                relogio_b.append(self.tempo_final_milissegundos)
            else:
                relogio_c.append(self.tempo_final_milissegundos)

        q_pessoas += 1
        if q_pessoas == n_pessoas:
            semaforo_print_final.release()

def entrar_na_fila():
    z = 0
    while(z < n_pessoas):
        with lock:
            fila_clientes.append(fila_pra_entrar[0])
            print("[Pessoa %s / %s] Aguardando na fila." %(fila_pra_entrar[0].name, fila_pra_entrar[0].faixa_etaria))
            fila_pra_entrar[0].semaforo_relogio.release()
            fila_pra_entrar.pop(0)
            z += 1
            item_no_buffer.notify()
        if z != n_pessoas:
            intervalo_chegada = random.randint(1, max_intervalo)
            time.sleep(intervalo_chegada * unid_tempo / 1000)    

def atracao():

    global sessoes
    sessoes = []
    todos_participaram = False

    while(not(todos_participaram)):
        with lock:
            if (len(fila_clientes) != 0):
                if (len(sessoes)) == 0:
                    cliente_0 = fila_clientes[0]
                    faixa_etaria_sessao = cliente_0.faixa_etaria
                    cliente_0.participou = True           
                    cliente_0.semaforo.release()     
                    sessoes.append(Sessao(faixa_etaria_a=faixa_etaria_sessao))
                    sessoes[0].start()
                    sessoes[0].pessoas_na_exp += 1
                    print("[Ixfera] Iniciando a experiencia %s." %(sessoes[0].faixa_etaria_a))
                    print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(cliente_0.name, cliente_0.faixa_etaria, sessoes[0].pessoas_na_exp))
                participaram = 0
                for i in range(len(fila_clientes)):
                    with mutex_flag:
                        if fila_clientes[i].participou == True:
                            participaram += 1
                        else:
            
                            if fila_clientes[i].participou == False and (sessoes[len(sessoes)-1].flag == False):
                                cliente_0 = fila_clientes[i]
                                faixa_etaria_sessao = cliente_0.faixa_etaria
                                cliente_0.participou = True           
                                cliente_0.semaforo.release()     
                                sessoes.append(Sessao(faixa_etaria_a=faixa_etaria_sessao))
                                sessoes[len(sessoes)-1].start()
                                sessoes[len(sessoes)-1].pessoas_na_exp += 1
                                print("[Ixfera] Iniciando a experiencia %s." %(sessoes[len(sessoes)-1].faixa_etaria_a))
                                print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(cliente_0.name, cliente_0.faixa_etaria, sessoes[len(sessoes)-1].pessoas_na_exp))
                            elif fila_clientes[i].participou == False and (sessoes[len(sessoes)-1].flag == True) and sessoes[len(sessoes)-1].pessoas_na_exp < n_vagas and fila_clientes[i].faixa_etaria == sessoes[len(sessoes)-1].faixa_etaria_a:
                                fila_clientes[i].semaforo.release()
                                cliente_0 = fila_clientes[i]
                                cliente_0.participou = True
                                sessoes[len(sessoes)-1].pessoas_na_exp += 1
                                print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(cliente_0.name, cliente_0.faixa_etaria, sessoes[len(sessoes)-1].pessoas_na_exp))

                if participaram == n_pessoas:
                    todos_participaram = True

    


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

tempo_inicio = time.time()

# Obter entrada do usuário para os parâmetros
n_pessoas = int(input("Número total de pessoas: "))
n_vagas = int(input("Número total de vagas na atração: "))
permanencia = int(input("Permanência na atração: "))
max_intervalo = int(input("Intervalo máximo entre chegadas: "))
semente = int(input("Semente do gerador de números aleatórios: "))
unid_tempo = int(input("Tempo correspondente a uma unidade de tempo (em milissegundos): "))
fila_clientes = []
fila_pra_entrar = []
relogio_a = []
relogio_b = []
relogio_c = []
pessoas_na_exp = 0
q_pessoas = 0


# Chamar a função de simulação com os parâmetros fornecidos
lista_clientes = criar_threads(n_pessoas, semente)
ixfera = Thread(target=atracao)
fila = Thread(target=entrar_na_fila)
fila.start()

ixfera.start()  
# Esperar a atração terminar
ixfera.join()
fila.join()

semaforo_print_final.acquire()
q_sessoes = len(sessoes)
while len(sessoes) != 0:
    sessoes[0].join()
    sessoes.pop(0)

tempo_fim = time.time()
print("[Ixfera] Simulacao finalizada")
print("")
tempo_final_milissegundos = round((tempo_fim - tempo_inicio) * 1000, 2)

media_a = round(sum(relogio_a) / len(relogio_a),2)
media_b = round(sum(relogio_b) / len(relogio_b),2)
media_c = round(sum(relogio_c) / len(relogio_c),2)

print("Tempo medio de espera:")
print("Faixa A: %.2f" %(media_a))
print("Faixa B: %.2f" %(media_b))
print("Faixa C: %.2f" %(media_c))
print("")

tempo_final = round(tempo_final_milissegundos/q_sessoes,2)
print("Taxa de ocupacao: %.2f" %tempo_final)



