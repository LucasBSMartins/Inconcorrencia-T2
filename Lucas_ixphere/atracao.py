from var_global import *
from sessao import Sessao

def atracao():

    global sessoes, tempo_inicio
    todos_participaram = False
    participaram = 0
    tempo_inicio = time.time()
    with lock:
        if (len(fila_clientes) == 0):
            item_no_buffer.wait()

    cliente = fila_clientes[0]
    cliente.participou = True           
    cliente.semaforo0.release()     
    sessoes.append(Sessao(faixa_etaria_a=cliente.faixa_etaria))
    sessoes[0].start()
    sessoes[0].pessoas_na_exp += 1
    print("[Ixfera] Iniciando a experiencia %s." %(sessoes[0].faixa_etaria_a))
    print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(cliente.name, cliente.faixa_etaria, sessoes[0].pessoas_na_exp))
    

    while(not(todos_participaram)):
        length = len(fila_clientes)         # Salva o tamanho da fila evitando que o valor no for seja alterado
        for i in range(length):
            with mutex_flag:
                if fila_clientes[i].participou == False and (sessoes[len(sessoes)-1].flag == False):
                    cliente = fila_clientes[i]
                    cliente.participou = True           
                    cliente.semaforo0.release()     
                    sessoes.append(Sessao(faixa_etaria_a=cliente.faixa_etaria))
                    sessoes[len(sessoes)-1].start()
                    sessoes[len(sessoes)-1].pessoas_na_exp += 1
                    print("[Ixfera] Iniciando a experiencia %s." %(sessoes[len(sessoes)-1].faixa_etaria_a))
                    print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(cliente.name, cliente.faixa_etaria, sessoes[len(sessoes)-1].pessoas_na_exp))
                
                elif fila_clientes[i].participou == False and (sessoes[len(sessoes)-1].flag == True) and sessoes[len(sessoes)-1].pessoas_na_exp < n_vagas and fila_clientes[i].faixa_etaria == sessoes[len(sessoes)-1].faixa_etaria_a:
                    cliente = fila_clientes[i]
                    cliente.participou = True
                    cliente.semaforo0.release()
                    sessoes[len(sessoes)-1].pessoas_na_exp += 1
                    print("[Pessoa %s / %s] Entrou na Ixfera (quantidade = %d)." %(cliente.name, cliente.faixa_etaria, sessoes[len(sessoes)-1].pessoas_na_exp))

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