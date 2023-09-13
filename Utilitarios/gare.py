from Utilitarios.aviao import Aviao
from Utilitarios.localizacao import Localizacao

class Gare:
  def __init__(self, id, tipo, estado, localizacao, aviao):
    self.id = id
    self.tipo = tipo
    self.estado = estado
    self.localizacao = localizacao
    self.aviao = None

  def getLoc(self):
    return self.localizacao
  
  def getID(self):
    return self.getID
  
  def getEstado(self):
    return self.estado
  
  def setEstado(self, estado):
    self.estado = estado
  
  def getTipo(self):
    return self.tipo
  
  def getAviao(self):
    return self.aviao
  
  def setAviao(self, aviao):
    self.aviao = aviao

  def encoder(self):
    if(self.aviao != None):
      return f'{self.id}_{self.tipo}_{str(self.estado)}_{(Localizacao.encoder(self.localizacao))}_{Aviao.encoder(self.aviao)}'
    else :
      return f'{self.id}_{self.tipo}_{str(self.estado)}_{(Localizacao.encoder(self.localizacao))}_{None}'
    
  def decoder(self, data):
    
    splitted = data.split('_')
    if(splitted[5] == None):
      return Gare(splitted[0],splitted[1],bool(splitted[2]),Localizacao(int(splitted[3]),int(splitted[4])), splitted[5])
    else:
       return Gare(splitted[0],splitted[1],bool(splitted[2]),Localizacao(int(splitted[3]),int(splitted[4])), Aviao(splitted[5],splitted[6],splitted[7],splitted[8],splitted[9]))


  def __str__(self):
    return f"{self.id} {self.tipo} {self.estado} {self.localizacao}"
