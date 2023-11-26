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

class Sessao(Thread):		       	                                 # subclasse de Thread 
    def __init__(self, faixa_etaria_a):             
        self.pessoas_na_exp = 0
        self.faixa_etaria_a = faixa_etaria_a
        self.flag = True
        self.pronto = False
        super().__init__(name="Sessao")		                         # chama construtor da superclasse 

    def run(self):
        demora = time.time()
        global fila_sessao, tempo_sessao_total, q_sessoes
    

        fila_sessao = []
        tempo_sessao = permanencia * unid_tempo / 1000
        tempo_inicial = time.time()
    
        self.pronto = True
        with mutex_flag:
                self.flag = True
        while time.time() - tempo_inicial < tempo_sessao:
            time.sleep(1 * unid_tempo / 1000)
        with mutex_flag:
            self.flag = None
        while len(fila_sessao) != 0:
            self.pessoas_na_exp -= 1
            fila_sessao[0].semaforo1.release()
            fila_sessao[0].join()
            fila_sessao.pop(0)
            semaforo_print.acquire()   

        with mutex_flag:
            print("[Ixfera] Pausando a experiencia %s." %(self.faixa_etaria_a))
            self.flag = False
        
        demora_final = time.time()
        tempo_sessao_total += (demora_final - demora) * 1000

class Cliente(Thread):		       	                             # subclasse de Thread 
    def __init__(self, name, faixa_etaria):             
        self.faixa_etaria = faixa_etaria
        self.semaforo0 = Semaphore(0)
        self.semaforo1 = Semaphore(0)
        self.semaforo_relogio = Semaphore(0)
        self.participou = False
        self.tempo_inicio = 0
        super().__init__(name=name)		                         # chama construtor da superclasse 

    def run(self):
        global fila_sessao, sessoes, q_pessoas


        semaforo_entrar_na_fila.acquire()
        fila_pra_entrar.append(self)
        semaforo_entrar_na_fila.release()   

        self.semaforo_relogio.acquire()
        self.tempo_inicio = time.time()

        self.semaforo0.acquire()
        while True:
            if sessoes[len(sessoes)-1].pronto == True:
                fila_sessao.append(self)
                break

        self.semaforo1.acquire()
        self.tempo_fim = time.time()
        self.tempo_final_milissegundos = (self.tempo_fim - self.tempo_inicio) * 1000

        with lista_relogio_lock:
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
    todos_participaram = False
    participaram = 0
    tempo_inicio = time.time()

    if (len(fila_clientes) == 0):
        item_no_buffer.wait()

    cliente_0 = fila_clientes[0]
    cliente_0.participou = True           
    cliente_0.semaforo0.release()     
    sessoes.append(Sessao(faixa_etaria_a=cliente_0.faixa_etaria))
    sessoes[0].start()
    sessoes[0].pessoas_na_exp += 1
    print("[Ixfera] Iniciando a experiencia %s." %(sessoes[0].faixa_etaria_a))
    print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(cliente_0.name, cliente_0.faixa_etaria, sessoes[0].pessoas_na_exp))
    

    while(not(todos_participaram)):
        length = len(fila_clientes)
        for i in range(length):
            with mutex_flag:
                if fila_clientes[i].participou == False and (sessoes[len(sessoes)-1].flag == False):
                    cliente_0 = fila_clientes[i]
                    cliente_0.participou = True           
                    cliente_0.semaforo0.release()     
                    sessoes.append(Sessao(faixa_etaria_a=cliente_0.faixa_etaria))
                    sessoes[len(sessoes)-1].start()
                    sessoes[len(sessoes)-1].pessoas_na_exp += 1
                    print("[Ixfera] Iniciando a experiencia %s." %(sessoes[len(sessoes)-1].faixa_etaria_a))
                    print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(cliente_0.name, cliente_0.faixa_etaria, sessoes[len(sessoes)-1].pessoas_na_exp))
                
                elif fila_clientes[i].participou == False and (sessoes[len(sessoes)-1].flag == True) and sessoes[len(sessoes)-1].pessoas_na_exp < n_vagas and fila_clientes[i].faixa_etaria == sessoes[len(sessoes)-1].faixa_etaria_a:
                    cliente_0 = fila_clientes[i]
                    cliente_0.participou = True
                    cliente_0.semaforo0.release()
                    sessoes[len(sessoes)-1].pessoas_na_exp += 1
                    print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(cliente_0.name, cliente_0.faixa_etaria, sessoes[len(sessoes)-1].pessoas_na_exp))

            if sessoes[len(sessoes)-1].pessoas_na_exp == n_vagas:
                break

        if (len(fila_clientes) != 0):
            with lock:
                i = 0
                length_l = len(fila_clientes)
                apagadas = 0
                while True:
                    if fila_clientes[i].participou == True:
                        fila_clientes.pop(i)
                        participaram += 1
                        apagadas += 1 
                    else:
                        i += 1
                    if i == length_l-apagadas:
                        break

        if participaram == n_pessoas:
            todos_participaram = True
      
def criar_threads(n_pessoas, semente):
    random.seed(semente)
    threads_clientes = []

    print("[Ixfera] Simulacao iniciada")

    for i in range(n_pessoas):
        x = random.randint(0,2)
        if x == 1:
            faixa_e = "A"
        elif x == 2:
            faixa_e = "B"
        else: 
            faixa_e = "C"

        threads_clientes.append(Cliente(name=str(i), faixa_etaria=faixa_e))
        threads_clientes[i].start()


    return threads_clientes

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
    threads_clientes = criar_threads(n_pessoas, semente)
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
    print("[Ixfera] Simulacao finalizada.")
    print("")
    tempo_final_milissegundos = (tempo_fim - tempo_inicio) * 1000

    media_a = (sum(relogio_a) / len(relogio_a)) 
    media_b = (sum(relogio_b) / len(relogio_b)) 
    media_c = (sum(relogio_c) / len(relogio_c)) 

    print("Tempo medio de espera:")
    print("Faixa A: %.2f" %(media_a))
    print("Faixa B: %.2f" %(media_b))
    print("Faixa C: %.2f" %(media_c))
    print("")

    taxa = tempo_sessao_total/tempo_final_milissegundos
    print("Taxa de ocupacao: %.2f" %(taxa))