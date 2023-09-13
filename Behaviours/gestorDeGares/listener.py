from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Utilitarios.localizacao import Localizacao
from Utilitarios.pista import Pista
from Utilitarios.aviao import Aviao
from Utilitarios.var import XMPP, bcolors,ESTACIONAMENTO


def verificarGare(gares,loc,tipo):
    dist = 1000
    gareId = False
    for key in gares:
        if gares[key].getTipo() == tipo:
            distAux = gares[key].getLoc().dist(loc)
            if  distAux < dist and gares[key].getEstado() == False:
                dist = distAux
                gareId = key
    return gareId

class ReceiveGareBehav(CyclicBehaviour):
    async def requestGareDescolar(self,data,requestId):
        
        aviao = Aviao.decoder(data)
        gareID = verificarGare(self.agent.dict_gares,ESTACIONAMENTO,aviao.getTipoAviao())

        if gareID != False:

            self.agent.dict_gares[gareID].setEstado(True) 
            msg = Message(to=f'torredecontrolo{XMPP}')                   
            if requestId == 'RequestGareDescolar':
                msg.body = f'ConfirmGareDescolar|{aviao.encoder()}_{gareID}'          
            elif requestId == 'RequestGareDescolarEspera':
                msg.body = f'ConfirmGareDescolarEspera|{aviao.encoder()}_{gareID}'          
            msg.set_metadata("performative", "confirm")                 
            await self.send(msg)

            self.agent.dict_gares[gareID].setEstado(True)
            self.agent.dict_gares[gareID].setAviao(aviao)
        
        else :
            msg = Message(to=f'torredecontrolo{XMPP}')                    
            if requestId == 'RequestGareDescolar':
                msg.body = f'RefuseGareDescolar|{aviao.encoder()}'            
            elif requestId == 'RequestGareDescolarEspera':
                msg.body = f'RefuseGareDescolarEspera|{aviao.encoder()}'            
            msg.set_metadata("performative", "refuse")                 
            await self.send(msg)


    async def requestGare(self,data,requestId):

        jid, companhia, tipoAviao, origem, destino, idPista, loc , estado = data.split('_')
        aviao = Aviao.decoder(jid + "_" + companhia + "_" + tipoAviao + "_" + origem + "_" + destino)
        pista = Pista.decoder(idPista + "_" + loc + "_" + estado)
        gareID = verificarGare(self.agent.dict_gares,pista.getLoc(),tipoAviao)

        if gareID != False:
            self.agent.dict_gares[gareID].setEstado(True) 
            msg = Message(to=f'torredecontrolo{XMPP}')    

            if requestId == 'RequestGare':
                msg.body = f'ConfirmGare|{aviao.encoder()}_{gareID}_{pista.encoder()}'          
            elif requestId == 'RequestGareEspera':
                msg.body = f'ConfirmGareEspera|{aviao.encoder()}_{gareID}_{pista.encoder()}'   

            msg.set_metadata("performative", "confirm")                 
            await self.send(msg)
        else :
            msg = Message(to=f'torredecontrolo{XMPP}')                    
            if requestId == 'RequestGare':
                msg.body = f'RefuseGare|{aviao.encoder()}_{pista.encoder()}'            
            elif requestId == 'RequestGareEspera':
                msg.body = f'RefuseGareEspera|{aviao.encoder()}_{pista.encoder()}'            
            msg.set_metadata("performative", "refuse")               
            await self.send(msg)


    def informEstacionamento(self,data):
        gareID, jid, companhia, tipoAviao, origem, destino = data.split('_')
        aviao = Aviao.decoder(jid + "_" + companhia + "_" + tipoAviao + "_" + origem + "_" + destino)
        self.agent.dict_gares[gareID].setEstado(True)
        self.agent.dict_gares[gareID].setAviao(aviao)
        print(f'{bcolors.OKGREEN}Gare {gareID} ocupada {bcolors.ENDC}')

    async def libertarGare(self,data):  
        aviaoJID  = data
        for gare in self.agent.dict_gares:
            if self.agent.dict_gares[gare].getAviao() != None:
                if self.agent.dict_gares[gare].getAviao().getID() == aviaoJID:
                    self.agent.dict_gares[gare].setEstado(False)
                    self.agent.dict_gares[gare].setAviao(None)
                    print(f'{bcolors.OKGREEN}Gare {gare} libertada pelo {aviaoJID} {bcolors.ENDC}')

                    msg = Message(to=aviaoJID + XMPP)                 
                    msg.body = f'ConfirmLibertarGare|{gare}'         
                    msg.set_metadata("performative", "confirm")                 
                    await self.send(msg)
                    

    async def run(self):

        msg = await self.receive(timeout=300)  
        if msg:
            performative = msg.get_metadata("performative")
    
            msg_body = msg.body.split('|')
            requestId, data = msg_body[0], msg_body[1]

            if performative == "request": 
                if requestId == 'RequestGare' or requestId == 'RequestGareEspera':
                    await self.requestGare(data,requestId)
                elif requestId == 'LibertarGare':
                    await self.libertarGare(data)
                elif requestId == 'RequestGareDescolar' or requestId == 'RequestGareDescolarEspera':
                    await self.requestGareDescolar(data,requestId)

            if performative == "inform":
                if requestId == 'InformaEstacionamento':
                    self.informEstacionamento(data)

                