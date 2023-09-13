from spade import agent
from Behaviours.CriadorDeAvioes.criaAvioesBehaviour import criarAvioesBehaviour
from Utilitarios.var import INTERVALO_CHEGADA_AVIOES

class criadorDeAvioesAgent(agent.Agent):

    listAvioes = []

    async def setup(self):
        
        a = criarAvioesBehaviour(INTERVALO_CHEGADA_AVIOES)
        self.add_behaviour(a)
        
        