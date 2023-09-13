from spade.agent import Agent
from Behaviours.Aviao.informarAterragemBehaviour import informarAterragemBehaviour
from Behaviours.Aviao.listenBehaviour import listenBehaviour
from Utilitarios.aviao import Aviao 
from Utilitarios.var import XMPP, bcolors


class AviaoAgent(Agent):
    
    def __init__(self,jid,password,aviao):
        super().__init__(jid,password)
        self.aviao = aviao

    async def setup(self):
        
        print(bcolors.OKBLUE + "Agent {}".format(str(self.aviao.aviaoID)) + " starting..." + bcolors.ENDC)

        a = informarAterragemBehaviour()
        b = listenBehaviour()
        self.add_behaviour(a)
        self.add_behaviour(b)
        
    