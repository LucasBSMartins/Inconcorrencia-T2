from cliente import Cliente
from var_global import *
from atracao import atracao
from entrar_na_fila import entrar_na_fila

def printar_taxas(tempo_fim, tempo_inicio):
    print("[Ixfera] Simulacao finalizada.")
    print("")
    tempo_final_milissegundos = (tempo_fim - tempo_inicio) * 1000

    media_a = sum(relogio_a) / len(relogio_a)
    media_b = sum(relogio_b) / len(relogio_b)
    media_c = sum(relogio_c) / len(relogio_c)

    print("Tempo medio de espera:")
    print("Faixa A: %.2f" %(media_a))
    print("Faixa B: %.2f" %(media_b))
    print("Faixa C: %.2f" %(media_c))
    print("")

    taxa = (tempo_sessao_total)/tempo_final_milissegundos
    print("Taxa de ocupacao: %.2f" %(taxa))


def criar_threads():
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

    fila = Thread(target=entrar_na_fila)
    ixfera = Thread(target=atracao)
    fila.start()
    ixfera.start()

    tempo_inicio = time.time()
    ixfera.join()
    tempo_fim = time.time()
    fila.join()

    semaforo_print_final.acquire()
    q_sessoes = len(sessoes)
    while len(sessoes) != 0:
        sessoes[0].join()
        sessoes.pop(0)

    printar_taxas(tempo_fim, tempo_inicio)