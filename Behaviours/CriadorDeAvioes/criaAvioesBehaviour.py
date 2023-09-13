
from spade.behaviour import PeriodicBehaviour
import random 
from Utilitarios.aviao import Aviao
from Agents.aviao import AviaoAgent
from Utilitarios.var import XMPP, PASSWORD


class criarAvioesBehaviour(PeriodicBehaviour):
    
    companhias = ['RYANAIR', 'TAP', 'EASYJET', 'SATA', 'FLY EMIRATES']
    destinos = ['Dammam', 'Pequim', 'Denver', 'Porto', 'Lisboa', 'Atlanta', 'Al Garhoud', 'Doha Hamad', 'Amesterdão', 'Madrid', 'Londres', 'Munique', 'Paris', 'Cancún', 'Amarante', 'Santo Tirso', 'Barcelos']
    idAviao = 0

    async def run(self):

        iComp = random.randint(0,4)
        iOri = random.randint(0,16)
        iDest = random.randint(0,16)
        randTipo = random.randint(0,99)
        tipo = ''

        while self.destinos[iOri] == self.destinos[iDest]:
            iOri = random.randint(0,16)
            iDest = random.randint(0,16)

        if randTipo < 33:
            tipo = 'Mercadorias'
        else:
            tipo = 'Comercial'
        #if  self.idAviao < 15:
        aviao = Aviao(f'aviao{self.idAviao}', self.companhias[iComp],tipo,self.destinos[iOri],self.destinos[iDest])
        aviaoAgent = AviaoAgent(f'aviao{self.idAviao}'+XMPP,PASSWORD,aviao)
        self.idAviao = self.idAviao + 1
        self.agent.listAvioes.append(aviaoAgent)
        await aviaoAgent.start(auto_register=True)

        
        
