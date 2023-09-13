from spade.agent import Agent
from Utilitarios.var import bcolors
from Behaviours.AgenteInformacao.agenteInformacaoListenerBehaviour import AgenteInformacaoListenerBehaviour



class AgenteInformacao(Agent):
    estado = {}
    historico = []
    pistas = {}
    listaEsperaAterrar = []
    listaEsperaDescolar = []
    gares = {}

    async def setup(self):
        print(bcolors.OKCYAN + "Agent {}".format(str(self.jid)) + " starting ..." + bcolors.ENDC)

        a = AgenteInformacaoListenerBehaviour()
        self.add_behaviour(a)

