from var_global import *

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