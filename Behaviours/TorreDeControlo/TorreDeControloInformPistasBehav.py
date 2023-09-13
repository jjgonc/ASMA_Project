from spade.behaviour import OneShotBehaviour
from spade.message import Message
from Utilitarios.var import XMPP

class TorreDeControloInformPistasBehav(OneShotBehaviour):
    async def run(self):
        data = ""
        for i in range(0,self.agent.numPistas):
            if i == self.agent.numPistas-1:
                data = data + str(self.agent.pistas[i].encoder()) 
            else:
                data = data + str(self.agent.pistas[i].encoder()) + "/"

        msg = Message(to=f'agenteinformacao{XMPP}')
        msg.set_metadata("performative","inform")
        msg.body = "InformPistas|" + data 
        await self.send(msg)


 