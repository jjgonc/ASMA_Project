

from spade import agent
from Utilitarios.gare import Gare 
from Utilitarios.localizacao import Localizacao
from Behaviours.gestorDeGares.listener import ReceiveGareBehav
from Utilitarios.var import bcolors
from Behaviours.gestorDeGares.informDistGares import informaDistGaresntoBehaviour
from Utilitarios.var import NUM_PISTAS,NUM_GARES


class garesAgent(agent.Agent):

    dict_gares = {}
    numGares = NUM_GARES
    numPistas = NUM_PISTAS

    async def setup(self):
        print(bcolors.OKGREEN + "Agent {}".format(str(self.jid)) + " starting..." + bcolors.ENDC)
        
        garesMercadorias = 0
        garesComerciais = 0
        for i in range(self.numGares):
            tipo = ''
            localizacao = 0

            if i < self.numGares * 0.7:
                tipo = 'Comercial'
                localizacao = Localizacao(garesComerciais,0)
                garesComerciais = garesComerciais + 1
            else:
                tipo = 'Mercadorias'
                localizacao = Localizacao(garesMercadorias, self.numPistas + 1)
                garesMercadorias = garesMercadorias + 1

            gare = Gare(i,tipo,False,localizacao, None)
            self.dict_gares[str(i)] = gare

        a = ReceiveGareBehav()
        b = informaDistGaresntoBehaviour()
        self.add_behaviour(a)
        self.add_behaviour(b)
        
        