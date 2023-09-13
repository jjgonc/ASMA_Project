from spade.behaviour import TimeoutBehaviour
from spade.message import Message
from Utilitarios.var import XMPP, bcolors


class AgenteInformacaoRemoveGareOcupAterrarBehav(TimeoutBehaviour):
    def __init__(self,start_at,gareID):
        super().__init__(start_at)
        self.gareID = int(gareID)

    async def run(self):
        self.agent.gares[self.gareID] = None

