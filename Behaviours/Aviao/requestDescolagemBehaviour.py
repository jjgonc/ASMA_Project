from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from Utilitarios.var import XMPP, bcolors
from spade.message import Message

class requestDescolagemBehaviour(OneShotBehaviour):
    async def run(self):
        print(bcolors.OKBLUE + str(self.agent.aviao.getID()) +": Informar Descolagem à Torre" + bcolors.ENDC)
        msg = Message(to=f'torredecontrolo{XMPP}')
        msg.set_metadata("performative", "request")
        msg.body = "RequestDescolar|" + self.agent.aviao.encoder() 
        await self.send(msg)
