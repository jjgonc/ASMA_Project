from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from Utilitarios.var import XMPP, PROBABILITY
from Behaviours.Aviao.requestDescolagemBehaviour import requestDescolagemBehaviour
import random



class decidirDescolarBehaviour(PeriodicBehaviour):
    probability = PROBABILITY

    async def run(self):
        rand = random.randint(0,99)
        if(rand <= self.probability):
            #Aviao vai descolar
            a = requestDescolagemBehaviour()
            self.agent.add_behaviour(a)
            self.kill()
            

    


        



        