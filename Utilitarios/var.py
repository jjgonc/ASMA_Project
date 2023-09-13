from Utilitarios.localizacao import Localizacao


XMPP = '@localhost'
PASSWORD="123456789"
TEMPO_OPERACAO_PISTA = 10
TEMPO_OPERACAO_GARE = 15
TEMPO_ESTADO = 15
NUM_PISTAS = 2 
NUM_MAX_ESPERA = 5 
NUM_GARES = 10
INTERVALO_CHEGADA_AVIOES = 8
ESTACIONAMENTO = Localizacao(NUM_GARES*0.7 + 1,(NUM_PISTAS + 2)/2)
PROBABILITY = 30 # prob de decidir descolar


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

