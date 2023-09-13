from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from Utilitarios.var import XMPP, TEMPO_OPERACAO_GARE
from Behaviours.Aviao.tempoOperacaoAviaoBehaviour import tempoOperacaoAviaoBehaviour
import datetime

class informaEstacionamentoBehaviour(OneShotBehaviour):

    def __init__(self,gareID):
        super().__init__()
        self.gareID = gareID
    
    async def run(self):
        msg = Message(to=f'gestorgares{XMPP}')  
        msg.set_metadata("performative", "inform") 
        msg.body = f'InformaEstacionamento|{self.gareID}_{self.agent.aviao.encoder()}'  
        await self.send(msg)
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=TEMPO_OPERACAO_GARE)
        b = tempoOperacaoAviaoBehaviour(start_at= start_at)
        self.agent.add_behaviour(b)
