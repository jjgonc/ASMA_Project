
class Informacao():
    def __init__(self, aviao, gareID, pistaID, estado, descricao):
        self.aviao = aviao
        self.gareID = gareID
        self.pistaID = pistaID
        self.estado = estado
        self.descricao = descricao

    def getAviao(self):
        return self.aviao
    
    def getGareID(self):
        return self.gareID
    
    def getPistaID(self):
        return self.pistaID
    
    def getEstado(self):
        return self.estado

    def getDescricao(self):
        return self.descricao
    
    def setDescricao(self, descricao):
        self.descricao = descricao
    
    def setEstado(self, estado):
        self.estado = estado

    def encoder(self):
        return [self.aviao.getID(), self.aviao.getOrigem(), self.aviao.getDestino(), self.aviao.getCompanhiaAerea(), self.aviao.getTipoAviao(), self.gareID, self.pistaID, self.estado, self.descricao]
        
    def __str__(self):
        return str(self.aviao.getID()+ self.aviao.getOrigem()+ self.aviao.getDestino()+self.aviao.getCompanhiaAerea()+ self.aviao.getTipoAviao()+ self.gareID+ self.pistaID+ self.estado+ self.descricao)
    