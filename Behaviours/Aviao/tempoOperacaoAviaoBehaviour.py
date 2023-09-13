from spade.behaviour import TimeoutBehaviour
from spade.message import Message
from Utilitarios.localizacao import Localizacao
from Utilitarios.var import XMPP
import datetime
from Behaviours.Aviao.decidirDescolar import decidirDescolarBehaviour 


class tempoOperacaoAviaoBehaviour(TimeoutBehaviour):
    async def run(self): 
        msg = Message(to=f'gestorgares{XMPP}')
        msg.set_metadata("performative","request")
        msg.body = "LibertarGare|" + str(self.agent.aviao.aviaoID)  
        await self.send(msg)

        a = decidirDescolarBehaviour(period = 30)   
        self.agent.add_behaviour(a)

