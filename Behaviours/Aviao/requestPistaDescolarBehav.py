from spade.behaviour import TimeoutBehaviour
from spade.message import Message
from Utilitarios.localizacao import Localizacao
from Utilitarios.var import XMPP, bcolors
import datetime


class RequestPistaDescolarBehav(TimeoutBehaviour):
    def __init__(self,start_at,msg):
        super().__init__(start_at)
        self.msg = msg

    async def run(self):
        await self.send(self.msg)
        

