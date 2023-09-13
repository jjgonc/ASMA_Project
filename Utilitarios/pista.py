from Utilitarios.localizacao import Localizacao

class Pista:
    def __init__(self,i,localizacao,ocupada=False):
        self.id = i
        self.loc = localizacao
        self.ocupada = ocupada
        self.aviao = None
        
    def getLoc(self):
        return self.loc

    def encoder(self):
        return str(self.id) + "_" + self.loc.encoder() + "_" + str(self.ocupada)

    def decoder(msg):
        list = msg.split("_")
        i = list[0]
        pos = list[1].split(",")
        x = int(pos[0])
        y = int(pos[1])
        loc = Localizacao(x,y)

        ocup = list[2]
        return Pista(i,loc,ocup)
    
    def getAviao(self):
        return self.aviao

    def setAviao(self,aviao):
        self.aviao = aviao
    
    def makeOcupada(self):
        self.ocupada = True
    
    def makeLivre(self):
        self.ocupada = False
        self.aviao = None

    def getOcupada(self):
        return self.ocupada
        
    