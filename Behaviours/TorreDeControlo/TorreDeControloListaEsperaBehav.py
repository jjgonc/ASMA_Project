from spade.behaviour import PeriodicBehaviour
from spade.message import Message
from Utilitarios.var import XMPP,TEMPO_OPERACAO_PISTA, TEMPO_OPERACAO_GARE, bcolors
from Behaviours.TorreDeControlo.TorreDeControloMakePistaLivreBehav import TorreDeControloMakePistaLivreBehav
import datetime

def verificaSeExisteObjetivoLista(objetivo,lista):
    ind = -1
    for i in range(0,len(lista)):
        if objetivo == lista[i].getObjetivo():
            ind = i
            break   
    return ind

def lenObjetivoLista(objetivo,lista):
    count = 0
    for i in range(0,len(lista)):
        if objetivo == lista[i].getObjetivo():
            count+=1    
    return count

def verificarPista(tipoAviao,pistas,numPistas):
        pista_escolhida = -1
        if tipoAviao == "Comercial" : 
            for i in range(numPistas):
                if (pistas[i].getOcupada() == False):
                    pista_escolhida = i
                    break
        else: # mercadoria
            for i in range(numPistas):
                if (pistas[numPistas-i-1].getOcupada() == False):
                    pista_escolhida = numPistas-i-1
                    break
        return pista_escolhida

class TorreDeControloListaEsperaBehav(PeriodicBehaviour):
    async def run(self): 
        if (len(self.agent.avioesEmEsperaAterrarQueue) > 0 or len(self.agent.avioesEmEsperaDescolarQueue) > 0):

            # tem + avioes em espera para descolar na pista entao da prioridade a descolar
            if (len(self.agent.avioesEmEsperaDescolarQueue) > len(self.agent.avioesEmEsperaAterrarQueue)):
                    # se tem avioes à espera de gare , chama avião para pedir gare
                    ind = verificaSeExisteObjetivoLista("DescolarSemGare",self.agent.avioesEmEsperaDescolarQueue)
                    if ind != -1:
                        aviao = self.agent.avioesEmEsperaDescolarQueue[ind]
                        msg = Message(to=f'gestorgares{XMPP}')
                        msg.set_metadata("performative","request")
                        msg.body = "RequestGareDescolarEspera|"+ aviao.encoder()    
                        await self.send(msg)
                    
                    # se tem avioes à espera de pissta , verifica se tem pista e se sim chama aviao para descolar
                    ind = verificaSeExisteObjetivoLista("DescolarComGare",self.agent.avioesEmEsperaDescolarQueue)
                    if ind != -1:
                        aviao = self.agent.avioesEmEsperaDescolarQueue[ind]
                        pista = verificarPista(aviao.tipoAviao,self.agent.pistas,self.agent.numPistas)
                        if pista != -1:                    
                        
                            print(bcolors.FAIL + f"TC: Descolagem do {aviao.aviaoID} autorizada! Pista " + str(pista)+ " ocupada, a enviar mensagem para gestor de gares para libertar" + bcolors.ENDC)
                            self.agent.pistas[pista].makeOcupada()

                            msg = Message(to=f'{aviao.aviaoID}{XMPP}')
                            msg.set_metadata("performative","confirm")
                            msg.body = "ConfirmPistaDescolar|" + str(pista)
                            await self.send(msg)
                            
                            
                            msgI = Message(to=f'agenteinformacao{XMPP}')
                            msgI.set_metadata("performative","inform")
                            msgI.body = "InformInicioDescolar|" + str(pista) + "_" + aviao.encoder()
                            await self.send(msgI)

                            self.agent.avioesEmEsperaDescolarQueue.pop(ind)

                            msg2 = Message(to=f'agenteinformacao{XMPP}')
                            msg2.set_metadata("performative","inform")
                            msg2.body = "InformFimDescolar|" + str(pista) + "_" + aviao.encoder()
                            start_at = datetime.datetime.now() + datetime.timedelta(seconds=TEMPO_OPERACAO_PISTA)
                            a = TorreDeControloMakePistaLivreBehav(start_at=start_at,pistaID=pista,msgInfo=msg2)
                            self.agent.add_behaviour(a)
                         


            else :
                pista = verificarPista(self.agent.avioesEmEsperaAterrarQueue[0].getTipoAviao(),self.agent.pistas,self.agent.numPistas)
                if pista != -1:
                        msg = Message(to=f'gestorgares{XMPP}')
                        msg.set_metadata("performative","request")
                        msg.body = "RequestGareEspera|"+self.agent.avioesEmEsperaAterrarQueue[0].encoder()+"_"+ self.agent.pistas[pista].encoder()
                        await self.send(msg)
                        self.agent.pistas[pista].makeOcupada()
                        print(bcolors.FAIL + "Pista " + str(pista) + " ocupada! \n" + bcolors.ENDC)
