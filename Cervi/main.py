import sys, time, random
from Cliente import Cliente
from Ixfera import Ixfera
from vars_globais import *

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Uso correto: python3 main.py <N_PESSOAS> <N_VAGAS> <PERMANENCIA> <MAX_INTERVALO> <SEMENTE> <UNID_TEMPO>")
        sys.exit(1)

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

    random.seed(semente)
    for i in range(n_pessoas):
        faixa_e = random.choice(['A', 'B', 'C'])
        threads_clientes.append(Cliente(name=str(i), faixa_etaria=faixa_e))
    
    ixfera= Ixfera()

    for thread in threads_clientes:
        thread.start()

    ixfera.start()

    for thread in threads_clientes:
        thread.join()
    ixfera.join()
    
