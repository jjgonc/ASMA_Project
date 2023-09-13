from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from Utilitarios.var import XMPP



class informaDistGaresntoBehaviour(OneShotBehaviour):
    
    async def run(self):
        msg = Message(to=f'agenteInformacao{XMPP}')  
        msg.set_metadata("performative", "inform")  
        msg.body = "InformGares|" + str(self.agent.numGares) 
        await self.send(msg)
