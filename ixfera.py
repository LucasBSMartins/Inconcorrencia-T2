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
        self.fila_sessao = []
        super().__init__(name="Sessao")		                         # chama construtor da superclasse 

    def run(self):
        # Comeca contagem de tempo que demorou uma sessao
        demora = time.time() * 1000
        global tempo_sessao_total

        # Calcula o tempo que uma sessao deve demorar e começa a contar o tempo da sessao
        tempo_sessao = permanencia * (unid_tempo / 1000)
        tempo_inicial = time.time() 

        # Seta a flag "em_andamento"
        with mutex_em_andamento:
            self.em_andamento = True

        # Fica no loop pelo tempo total de uma sessao
        while (time.time()) - tempo_inicial < tempo_sessao:
            time.sleep(1/100000000000000000000000)

        # Seta a flag "em_andamento"
        with mutex_em_andamento:
            self.em_andamento = None

        # Libera o cliente, e libera o semaforo para printar sua saída da sessao
        # Apos isso, espera a liberacao do semaforo avisando que o cliente printou evitando prints fora de ordem
        while len(self.fila_sessao) != 0:
            self.pessoas_na_exp -= 1
            self.fila_sessao[0].semaforo_cliente_saiu.release()
            self.fila_sessao[0].join()
            self.fila_sessao.pop(0)
            semaforo_print.acquire()   

        # Seta a flag "em_andamento" e printa fim da sessao
        with mutex_em_andamento:
            print("[Ixfera] Pausando a experiencia %s." %(self.faixa_etaria_a))
            self.em_andamento = False

        # Salva os valores de tempo de execucao e libera o semaforo avisando o fim da sessao
        demora_final = time.time() * 1000
        tempo_sessao_total += (demora_final - demora)
        semaforo_acabar_experiencia.release()


class Cliente(Thread):		       	                             # subclasse de Thread 
    def __init__(self, name, faixa_etaria):             
        self.faixa_etaria = faixa_etaria
        self.semaforo_entrar_na_sessao = Semaphore(0)
        self.semaforo_cliente_saiu = Semaphore(0)
        self.semaforo_relogio = Semaphore(0)
        self.tempo_inicio_cliente = 0
        super().__init__(name=name)		                         # chama construtor da superclasse 

    def run(self):
        global sessoes, q_pessoas

        # Liberacao para a contagem de tempo
        self.semaforo_relogio.acquire()
        self.tempo_inicio_cliente = time.time() * 1000

        # Espera a liberacao do semaforo para entrar na sessao
        self.semaforo_entrar_na_sessao.acquire()
        
        # Adiciona o cliente na fila da sessao
        sessoes[len(sessoes)-1].fila_sessao.append(self)

        # Aguarda o cliente participar da sessao
        self.semaforo_cliente_saiu.acquire()

        # Calcula o tempo que demorou para participar na fila e adiciona para somar depois
        self.tempo_fim = time.time() * 1000
        self.tempo_final_milissegundos = (self.tempo_fim - self.tempo_inicio_cliente)

        if self.faixa_etaria == "A":
            relogio_a.append(self.tempo_final_milissegundos)
        elif self.faixa_etaria == "B":
            relogio_b.append(self.tempo_final_milissegundos)
        else:
            relogio_c.append(self.tempo_final_milissegundos)

        print("[Pessoa %s / %s] Saiu da Ixfera (quantidade = %d)." %(self.name, self.faixa_etaria, sessoes[len(sessoes)-1].pessoas_na_exp))
        semaforo_print.release() 

        # Se a quantidade de pessoas que participaram for igual o numero de pessoas totais, libera o print de estatisticas
        q_pessoas += 1
        if q_pessoas == n_pessoas:
            semaforo_print_final.release()

    def cliente_entrar_na_sessao(self, sessoes):
        # Se for somente entrar numa sessao, usa esta funcao
        # Libera o semaforo para entrar na sessao e printa
        self.semaforo_entrar_na_sessao.release() 
        sessoes[len(sessoes)-1].pessoas_na_exp += 1
        print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(self.name, self.faixa_etaria, sessoes[len(sessoes)-1].pessoas_na_exp))
    
    def cliente_entrar_na_sessao_e_criar(self, sessoes):
        # Se for o primeiro cliente a entrar, cria uma sessao e a inicia
        # Libera o semaforo para entrar na sessao e printa
        self.semaforo_entrar_na_sessao.release() 
        sessoes.append(Sessao(faixa_etaria_a=self.faixa_etaria))
        sessoes[len(sessoes)-1].start()
        sessoes[len(sessoes)-1].pessoas_na_exp += 1
        print("[Ixfera] Iniciando a experiencia %s." %(sessoes[len(sessoes)-1].faixa_etaria_a))
        print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(self.name, self.faixa_etaria, sessoes[len(sessoes)-1].pessoas_na_exp))

def entrar_na_fila():
    pessoas_dentro_da_fila = 0
    faixa_e = ["A", "B", "C"]
    while(pessoas_dentro_da_fila < n_pessoas):
        # Adciona cliente na fila e cria sua thread
        with lock:
            x = random.randint(0,2)
            fila_clientes.append(Cliente(name=str(pessoas_dentro_da_fila), faixa_etaria=faixa_e[x]))
            fila_clientes[len(fila_clientes)-1].start()
            print("[Pessoa %s / %s] Aguardando na fila." %(fila_clientes[len(fila_clientes)-1].name, fila_clientes[len(fila_clientes)-1].faixa_etaria))
            fila_clientes[len(fila_clientes)-1].semaforo_relogio.release()       # Libera a contagem de tempo que o cliente está na fila
            pessoas_dentro_da_fila += 1
            item_no_buffer.notify()
        if pessoas_dentro_da_fila != n_pessoas:
            # Intervalo de tempo randomico entre a chegada de duas pessoas
            intervalo_chegada = random.randint(0, max_intervalo)
            time.sleep(intervalo_chegada * unid_tempo / 1000)    

def atracao():

    global sessoes, tempo_inicio
    participaram = 0
    tempo_inicio = time.time()* 1000      # Marca inicio da ixfera

    # Aguarda ter cliente na Fila
    if (len(fila_clientes) == 0):
        item_no_buffer.wait()

    # Inicia a primeira sessão
    cliente_atual = fila_clientes[0]
    cliente_atual.cliente_entrar_na_sessao_e_criar(sessoes)   
    with lock:
        fila_clientes.pop(0)
    participaram += 1

    while(participaram != n_pessoas):
        # Aguarda ter cliente na Fila
        with lock:
            if (len(fila_clientes) == 0):
                item_no_buffer.wait()

        # Utiliza o mutex que bloqueia a flag "em_andamento"
        with mutex_em_andamento:
            
            # Se uma sessao nao está em andamento cria uma com o cliente 0
            if (sessoes[len(sessoes)-1].em_andamento == False):
                cliente_atual = fila_clientes[0]
                cliente_atual.cliente_entrar_na_sessao_e_criar(sessoes)    
                with lock:
                    fila_clientes.pop(0)
                participaram += 1
            
            # Se a flag em_andamento for True, o cliente for da faixa etaria atual, o proximo da fila e a sessao
            # ter vagas disponiveis, adiciona o cliente na sessao
            elif (sessoes[len(sessoes)-1].em_andamento == True):
                if sessoes[len(sessoes)-1].pessoas_na_exp < n_vagas and fila_clientes[0].faixa_etaria == sessoes[len(sessoes)-1].faixa_etaria_a:
                    cliente_atual = fila_clientes[0]
                    cliente_atual.cliente_entrar_na_sessao(sessoes)
                    with lock:
                        fila_clientes.pop(0)
                    participaram += 1

        # Se o proximo cliente na fila for uma pessoa com faixa etaria diferente da atual da sessao
        # ou o numero maximo de vagas for atingido, aguarda o encerramento da sessao
        if (len(fila_clientes)) and (len(sessoes)):
            if sessoes[len(sessoes)-1].pessoas_na_exp == n_vagas or fila_clientes[0].faixa_etaria != sessoes[len(sessoes)-1].faixa_etaria_a:
                semaforo_acabar_experiencia.acquire()

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
        print("<PERMANENCIA> precisa ser maior que 0.")
        sys.exit()
    if semente < 0:
        print("<SEMENTE> precisa ser maior ou igual que zero")
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
    
    # Variáveis globais
    fila_clientes = []
    fila_pre_entrada = []
    relogio_a = []
    relogio_b = []
    relogio_c = []
    sessoes = []
    pessoas_na_exp = 0
    q_pessoas = 0
    tempo_sessao_total = 0
    random.seed(semente)

    # Chamar a função de simulação com os parâmetros fornecidos
    print("[Ixfera] Simulacao iniciada")
    ixfera = Thread(target=atracao)
    fila = Thread(target=entrar_na_fila)
    fila.start()
    ixfera.start()  

    # Esperar a atração terminar
    ixfera.join()
    fila.join()

    # Liberado quando o último cliente sai da esfera
    semaforo_print_final.acquire()

    # Finaliza as threads sessoes
    while len(sessoes) != 0:
        sessoes[0].join()
        sessoes.pop(0)
    
    # Marca quando é finalizado a ixfera
    tempo_fim = time.time() * 1000

    print("[Ixfera] Simulacao finalizada.")
    print("")

    tempo_final_milissegundos = (tempo_fim - tempo_inicio) 

    # Printa valor do relatório de estatísticas
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
    taxa = float (str (taxa)[:4])
    print("Taxa de ocupacao: %.2f" %(taxa))