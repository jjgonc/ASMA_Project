from spade.behaviour import TimeoutBehaviour
from spade.message import Message
from Utilitarios.localizacao import Localizacao
from Utilitarios.var import XMPP, bcolors
import datetime


class TorreDeControloMakePistaLivreBehav(TimeoutBehaviour):
    def __init__(self,start_at,pistaID,msgInfo):
        super().__init__(start_at)
        self.pistaID = int(pistaID)
        self.msgInfo = msgInfo

    async def run(self):
        #Avisa agente informação que aviao ja aterrou ou descolou
        await self.send(self.msgInfo)
        
        self.agent.pistas[self.pistaID].makeLivre()
        print(bcolors.FAIL + "Pista " + str(self.pistaID) + " está novamente livre." + bcolors.ENDC)  
             
