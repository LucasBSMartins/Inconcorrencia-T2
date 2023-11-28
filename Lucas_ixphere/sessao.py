from var_global import *
    
class Sessao(Thread):		       	                                 # subclasse de Thread 
    def __init__(self, faixa_etaria_a):             
        self.pessoas_na_exp = 0
        self.faixa_etaria_a = faixa_etaria_a
        self.flag = True
        self.pronto = False
        super().__init__(name="Sessao")		                         # chama construtor da superclasse

    def run(self):
        global fila_sessao, q_sessoes, tempo_sessao_total
        

        fila_sessao = []
        tempo_sessao = permanencia * unid_tempo / 1000
        demora = time.time()
        
        self.pronto = True
        
        with mutex_flag:
            self.flag = True
        while time.time() - demora < tempo_sessao:
            time.sleep(1 / 10000000)

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