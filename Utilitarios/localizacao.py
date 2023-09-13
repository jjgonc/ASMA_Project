class Localizacao:
  
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def getX(self):
    return self.x
  
  def getY(self):
    return self.y
  
  def dist(self, loc):
    return pow(self.y - loc.getY(),2) + pow(self.x - loc.getX(),2)
  
  def encoder(self):
    return f'{self.x},{self.y}'
  
  def decoder(loc):
    splitted = loc.split(",")
    x = int(splitted[0])
    y = int(splitted[1])
    return Localizacao(x,y)
