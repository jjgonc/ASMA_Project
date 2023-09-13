class Aviao:
    def __init__(self,aviaoID,companhia,tipo,origem,destino):
        self.aviaoID = aviaoID
        self.companhiaAerea = companhia
        self.tipoAviao = tipo
        self.origem = origem
        self.destino = destino
        self.objetivo = ""
        
    def getID(self):
        return self.aviaoID
    
    def getCompanhiaAerea(self):
        return self.companhiaAerea
    
    def getTipoAviao(self):
        return self.tipoAviao
    
    def getObjetivo(self):
        return self.objetivo

    def setObjetivo(self,obj):
        self.objetivo = obj

    def getOrigem(self):
        return self.origem
    
    def getDestino(self):
        return self.destino

    def encoder(self):
        return str(self.aviaoID) + "_" + self.companhiaAerea + "_" + self.tipoAviao + "_" + self.origem + "_" + self.destino

    def decoder(msg):
        list = msg.split("_")
        aid , companhia , tipo , origem , destino = list[0], list[1], list[2], list[3], list[4]
        return Aviao(aid,companhia,tipo,origem,destino)
    
