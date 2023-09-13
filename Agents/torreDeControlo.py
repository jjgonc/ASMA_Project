from spade import agent
from Behaviours.TorreDeControlo.TorreDeControloListenerBehav import TorreDeControloListenerBehav
from Behaviours.TorreDeControlo.TorreDeControloListaEsperaBehav import TorreDeControloListaEsperaBehav
from Behaviours.TorreDeControlo.TorreDeControloInformPistasBehav import TorreDeControloInformPistasBehav
from Utilitarios.pista import Pista
from Utilitarios.localizacao import Localizacao
from Utilitarios.var import TEMPO_OPERACAO_PISTA, bcolors, NUM_PISTAS, NUM_MAX_ESPERA

class TorreControloAgent(agent.Agent):

    avioesEmEsperaAterrarQueue = []
    avioesEmEsperaDescolarQueue = []
    pistas = {}
    numPistas = NUM_PISTAS
    numMaxEsperaAterrar = NUM_MAX_ESPERA

    async def setup(self):
        print(bcolors.FAIL + "Agent {}".format(str(self.jid)) + " starting ..." + bcolors.ENDC)

        self.torreControloId = "TorreDeControlo@localhost"
        
        for i in range(self.numPistas):
            localizacao = Localizacao(0,i+1)
            pista = Pista(i,localizacao,False)
            self.pistas[i] = pista

        a = TorreDeControloListenerBehav()
        b = TorreDeControloListaEsperaBehav(period=TEMPO_OPERACAO_PISTA/2)
        c = TorreDeControloInformPistasBehav()

        self.add_behaviour(a)
        self.add_behaviour(b)
        self.add_behaviour(c)
