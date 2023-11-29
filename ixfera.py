import sys
import time 
import random
from threading import Thread, Semaphore, Lock, Condition 

lock = Lock()
mutex_em_andamento = Lock()
lista_relogio_lock = Lock()

semaforo_acabar_experiencia = Semaphore(0)
item_no_buffer = Condition(lock)
semaforo_entrar_na_fila = Semaphore(1)
semaforo_print = Semaphore(0)
semaforo_print_final = Semaphore(0)

class Sessao(Thread):		       	                                 # subclasse de Thread 
    def __init__(self, faixa_etaria_a):             
        self.pessoas_na_exp = 0
        self.faixa_etaria_a = faixa_etaria_a
        self.em_andamento = True
        self.pronto_para_entrar = False
        super().__init__(name="Sessao")		                         # chama construtor da superclasse 

    def run(self):
        demora = time.time()
        global fila_sessao, tempo_sessao_total, q_sessoes

        fila_sessao = []
        tempo_sessao = permanencia * (unid_tempo / 1000)
        tempo_inicial = time.time()
    
        self.pronto_para_entrar = True

        with mutex_em_andamento:
            self.em_andamento = True
        
        while time.time() - tempo_inicial < tempo_sessao:
            time.sleep(1/100000000000000000000000)
   
        with mutex_em_andamento:
            self.em_andamento = None

        while len(fila_sessao) != 0:
            self.pessoas_na_exp -= 1
            fila_sessao[0].semaforo_cliente_saiu.release()
            fila_sessao[0].join()
            fila_sessao.pop(0)
            semaforo_print.acquire()   

        with mutex_em_andamento:
            print("[Ixfera] Pausando a experiencia %s." %(self.faixa_etaria_a))
            self.em_andamento = False
        
        
        demora_final = time.time()
        tempo_sessao_total += (demora_final - demora) * 1000
        semaforo_acabar_experiencia.release()


class Cliente(Thread):		       	                             # subclasse de Thread 
    def __init__(self, name, faixa_etaria):             
        self.faixa_etaria = faixa_etaria
        self.semaforo_entrar_na_sessao = Semaphore(0)
        self.semaforo_cliente_saiu = Semaphore(0)
        self.semaforo_relogio = Semaphore(0)
        self.participou = False
        self.tempo_inicio_cliente = 0
        super().__init__(name=name)		                         # chama construtor da superclasse 

    def run(self):
        global fila_sessao, sessoes, q_pessoas

        fila_pra_entrar.append(self)

        self.semaforo_relogio.acquire()
        self.tempo_inicio_cliente = time.time()

        self.semaforo_entrar_na_sessao.acquire()

        while True:
            if sessoes[len(sessoes)-1].pronto_para_entrar == True:
                fila_sessao.append(self)
                break

        self.semaforo_cliente_saiu.acquire()
        self.tempo_fim = time.time()
        self.tempo_final_milissegundos = (self.tempo_fim - self.tempo_inicio_cliente) * 1000

        if self.faixa_etaria == "A":
            relogio_a.append(self.tempo_final_milissegundos)
        elif self.faixa_etaria == "B":
            relogio_b.append(self.tempo_final_milissegundos)
        else:
            relogio_c.append(self.tempo_final_milissegundos)

        print("[Pessoa %s / %s] Saiu da Ixfera (quantidade = %d)." %(self.name, self.faixa_etaria, sessoes[len(sessoes)-1].pessoas_na_exp))
        semaforo_print.release() 
    
        q_pessoas += 1
        if q_pessoas == n_pessoas:
            semaforo_print_final.release()

    def cliente_entrar_na_sessao(self, sessoes):
        self.participou = True           
        self.semaforo_entrar_na_sessao.release() 
        sessoes[len(sessoes)-1].pessoas_na_exp += 1
        print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(self.name, self.faixa_etaria, sessoes[len(sessoes)-1].pessoas_na_exp))
    
    def cliente_entrar_na_sessao_e_criar(self, sessoes):
        self.participou = True           
        self.semaforo_entrar_na_sessao.release() 
        sessoes.append(Sessao(faixa_etaria_a=self.faixa_etaria))
        sessoes[len(sessoes)-1].start()
        sessoes[len(sessoes)-1].pessoas_na_exp += 1
        print("[Ixfera] Iniciando a experiencia %s." %(sessoes[len(sessoes)-1].faixa_etaria_a))
        print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(self.name, self.faixa_etaria, sessoes[len(sessoes)-1].pessoas_na_exp))

def entrar_na_fila():
    pessoas_dentro_da_fila = 0
    while(pessoas_dentro_da_fila < n_pessoas):
        with lock:
            fila_clientes.append(fila_pra_entrar[0])
            print("[Pessoa %s / %s] Aguardando na fila." %(fila_pra_entrar[0].name, fila_pra_entrar[0].faixa_etaria))
            fila_pra_entrar[0].semaforo_relogio.release()
            fila_pra_entrar.pop(0)
            pessoas_dentro_da_fila += 1
            item_no_buffer.notify()
        if pessoas_dentro_da_fila != n_pessoas:
            intervalo_chegada = random.randint(0, max_intervalo)
            time.sleep(intervalo_chegada * unid_tempo / 1000)    

def atracao():

    global sessoes, tempo_inicio
    participaram = 0
    tempo_inicio = time.time()

    if (len(fila_clientes) == 0):
        item_no_buffer.wait()

    cliente_atual = fila_clientes[0]
    cliente_atual.cliente_entrar_na_sessao_e_criar(sessoes)   
    fila_clientes.pop(0)
    participaram += 1

    while(participaram != n_pessoas):
        with lock:
            if (len(fila_clientes) == 0):
                item_no_buffer.wait()

        with mutex_em_andamento:
            if fila_clientes[0].participou == False and (sessoes[len(sessoes)-1].em_andamento == False):
                cliente_atual = fila_clientes[0]
                cliente_atual.cliente_entrar_na_sessao_e_criar(sessoes)    
                with lock:
                    fila_clientes.pop(0)
                participaram += 1

            elif fila_clientes[0].participou == False and (sessoes[len(sessoes)-1].em_andamento == True):
                if sessoes[len(sessoes)-1].pessoas_na_exp < n_vagas and fila_clientes[0].faixa_etaria == sessoes[len(sessoes)-1].faixa_etaria_a:
                    cliente_atual = fila_clientes[0]
                    cliente_atual.cliente_entrar_na_sessao(sessoes)
                    with lock:
                        fila_clientes.pop(0)
                    participaram += 1
    
        if (len(fila_clientes)) and (len(sessoes)):
            if sessoes[len(sessoes)-1].pessoas_na_exp == n_vagas or fila_clientes[0].faixa_etaria != sessoes[len(sessoes)-1].faixa_etaria_a:
                semaforo_acabar_experiencia.acquire()
      
def criar_threads():
    random.seed(semente)
    threads_clientes = []
    faixa_e = ["A", "B", "C"]

    print("[Ixfera] Simulacao iniciada")

    for i in range(n_pessoas):

        x = random.randint(0,2)

        threads_clientes.append(Cliente(name=str(i), faixa_etaria=faixa_e[x]))
        threads_clientes[i].start()

    return threads_clientes

if __name__ == "__main__":
    # Verificar se a quantidade correta de argumentos foi fornecida
    
    if len(sys.argv) != 7:
        print("Uso correto: python3 ixfera.py <N_PESSOAS> <N_VAGAS> <PERMANENCIA> <MAX_INTERVALO> <SEMENTE> <UNID_TEMPO>")
        sys.exit(1)

    # Obter os parâmetros da linha de comando
    n_pessoas = int(sys.argv[1])
    n_vagas = int(sys.argv[2])
    permanencia = int(sys.argv[3])
    max_intervalo = int(sys.argv[4])
    semente = int(sys.argv[5])
    unid_tempo = int(sys.argv[6])
    if n_pessoas < 1:
        print("<N_PESSOAS> precisa ser maior que 0.")
        sys.exit()
    if n_vagas < 1:
        print("<N_VAGAS> precisa ser maior que 0.")
        sys.exit()
    if permanencia < 1:
        print("<PERMANENCIA> precisa ser maior que 0.")
        sys.exit()
    if max_intervalo < 0:
        print("<PERMANENCIA> precisa ser maior ou igual a 0.")
        sys.exit()
    if unid_tempo < 0:
        print("<UNID_TEMPO> precisa ser  maior que 0.")
        sys.exit()
    '''

    # Obter entrada do usuário para os parâmetros
    n_pessoas = int(input("Número total de pessoas: "))
    n_vagas = int(input("Número total de vagas na atração: "))
    permanencia = int(input("Permanência na atração: "))
    max_intervalo = int(input("Intervalo máximo entre chegadas: "))
    semente = int(input("Semente do gerador de números aleatórios: "))
    unid_tempo = int(input("Tempo correspondente a uma unidade de tempo (em milissegundos): "))
    '''

    fila_clientes = []
    fila_pra_entrar = []
    relogio_a = []
    relogio_b = []
    relogio_c = []
    sessoes = []
    pessoas_na_exp = 0
    q_pessoas = 0
    tempo_sessao_total = 0

    # Chamar a função de simulação com os parâmetros fornecidos
    threads_clientes = criar_threads()
    ixfera = Thread(target=atracao)
    fila = Thread(target=entrar_na_fila)
    fila.start()
    ixfera.start()  

    # Esperar a atração terminar
    ixfera.join()
    fila.join()

    semaforo_print_final.acquire()

    while len(sessoes) != 0:
        sessoes[0].join()
        sessoes.pop(0)
    tempo_fim = time.time()
    print("[Ixfera] Simulacao finalizada.")
    print("")
    tempo_final_milissegundos = (tempo_fim - tempo_inicio) * 1000

    if (len(relogio_a) != 0):
        media_a = (sum(relogio_a) / len(relogio_a)) 
    if (len(relogio_b) != 0):
        media_b = (sum(relogio_b) / len(relogio_b)) 
    if (len(relogio_c) != 0):
        media_c = (sum(relogio_c) / len(relogio_c)) 

    print("Tempo medio de espera:")
    if (len(relogio_a) != 0):
        print("Faixa A: %.2f" %(media_a))
    else:
        print("Não foram gerados clientes da faixa A")
    if (len(relogio_b) != 0):
        print("Faixa B: %.2f" %(media_b))
    else:
        print("Não foram gerados clientes da faixa B")
    if (len(relogio_c) != 0):
        print("Faixa C: %.2f" %(media_c))
    else:
        print("Não foram gerados clientes da faixa C")
    print("")

    taxa = tempo_sessao_total/tempo_final_milissegundos
    print("Taxa de ocupacao: %.2f" %(taxa))