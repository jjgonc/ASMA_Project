from spade.behaviour import TimeoutBehaviour
from spade.message import Message
from Utilitarios.var import XMPP, bcolors


class AgenteInformacaoRemoveEstadoAtualBehav(TimeoutBehaviour):
    def __init__(self,start_at,aviaoID):
        super().__init__(start_at)
        self.aviaoID = aviaoID

    async def run(self):
        if self.aviaoID in self.agent.estado:
            self.agent.estado.pop(self.aviaoID)  

