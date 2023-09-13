from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from Utilitarios.var import XMPP, bcolors

class informarAterragemBehaviour(OneShotBehaviour):
    async def run(self):
        print(bcolors.OKBLUE + str(self.agent.aviao.getID()) + ": Informar Aterragem à Torre" + bcolors.ENDC)
        msg = Message(to=f'torredecontrolo{XMPP}') 
        msg.set_metadata("performative", "request")  
        msg.body = "RequestAterrar|" + self.agent.aviao.encoder()
        await self.send(msg)
        