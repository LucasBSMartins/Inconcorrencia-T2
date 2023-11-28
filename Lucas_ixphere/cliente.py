from var_global import *

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
        global fila_sessao
        global sessoes
        global q_pessoas

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