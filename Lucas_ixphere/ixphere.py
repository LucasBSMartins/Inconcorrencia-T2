from var_global import *
from criar_threads import criar_threads
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


# Chamar a função de simulação com os parâmetros fornecidos
criar_threads()
