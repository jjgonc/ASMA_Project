from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Utilitarios.aviao import Aviao
from Utilitarios.var import XMPP,TEMPO_OPERACAO_PISTA,  bcolors
from Behaviours.TorreDeControlo.TorreDeControloMakePistaLivreBehav import TorreDeControloMakePistaLivreBehav
import datetime

def verificarPista(tipoAviao,pistas,numPistas):
        pista_escolhida = -1
        if tipoAviao == "Comercial" : 
            for i in range(numPistas):
                if (pistas[i].getOcupada() == False):
                    pista_escolhida = i
                    break
        else: # mercadoria
            for i in range(numPistas):
                #print(numPistas-i-1)
                if (pistas[numPistas-i-1].getOcupada() == False):
                    pista_escolhida = numPistas-i-1
                    break
        return pista_escolhida

def removeAviaoQueue(lista,aviao):
    ind = -1
    for i in range(0,len(lista)):
        if aviao.getID() == lista[i].getID():
            ind = i 
            break
    if ind !=-1:
        lista.pop(i)
    return lista

def appendComVerificacao(lista,aviao):
    existe = False
    for i in range(0,len(lista)):
        if aviao.getID() == lista[i].getID():
            lista[i] = aviao
            existe = True
            break
    if not existe:
        lista.append(aviao)
    

class TorreDeControloListenerBehav(CyclicBehaviour):
    async def requestAterrar(self,mensagem):
        # ja tem avioes em espera para aterrar vai para a fila
        if (len(self.agent.avioesEmEsperaAterrarQueue)>0):
            mensagem = mensagem + "_-1_-1,-1_False" 
            await self.recusarAterrar(mensagem,"RefuseGare")
        
        else:
            aviao = Aviao.decoder(mensagem)
            pista_escolhida = verificarPista(aviao.tipoAviao,self.agent.pistas,self.agent.numPistas)
            msg2 = Message(to=f'agenteinformacao{XMPP}')
            msg2.set_metadata("performative","inform")
            msg2.body = "InformRequestAterrar|" + aviao.encoder()
            await self.send(msg2)
            if pista_escolhida == -1:
                print(bcolors.FAIL + "TC: Não há pistas disponiveis para aterrar para o aviao " + aviao.aviaoID + bcolors.ENDC)
                #tive de acrecentar os detalhes inventados da pista pq o recusaraterrar recebe estes dados
                mensagem = mensagem + "_" + str(pista_escolhida) + "_-1,-1_False" 
                await self.recusarAterrar(mensagem,"RefuseGare")

            else:  
                msg = Message(to=f'gestorgares{XMPP}')
                msg.set_metadata("performative","request")
                msg.body = "RequestGare|"+mensagem+"_"+ self.agent.pistas[pista_escolhida].encoder()
                await self.send(msg)
                self.agent.pistas[pista_escolhida].makeOcupada()
    
    async def confirmarAterrar(self,mensagem,idMsg):
        list2 = mensagem.split("_")
        jid, companhia, tipo, origem, destino, gare , pistaID, pistaLoc, pistaOcup = list2[0],list2[1],list2[2],list2[3],list2[4],list2[5],list2[6],list2[7],list2[8]
        msg = Message(to= jid + XMPP)
        msg.set_metadata("performative","confirm")
        msg.body = "ConfirmarAterrar|"+gare+"_"+pistaID+"_"+pistaLoc+"_"+pistaOcup
        await self.send(msg)

        # se for uma confirmação para um aviao que ta em espera
        if idMsg == "ConfirmGareEspera":
            self.agent.avioesEmEsperaAterrarQueue.pop(0)
        
        msgI = Message(to=f'agenteinformacao{XMPP}')
        msgI.set_metadata("performative","inform")
        msgI.body = "InformInicioAterragem|" + gare + "_" + pistaID + "_" + jid + "_" + companhia + "_" + tipo + "_" + origem + "_" + destino
        await self.send(msgI)

        #print("PistaID: ", pistaID)
        msg2 = Message(to=f'agenteinformacao{XMPP}')
        msg2.set_metadata("performative","inform")
        msg2.body = "InformFimAterragem|" + gare + "_" + pistaID + "_" + jid + "_" + companhia + "_" + tipo + "_" + origem + "_" + destino
        
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=TEMPO_OPERACAO_PISTA)
        a = TorreDeControloMakePistaLivreBehav(start_at=start_at,pistaID=pistaID,msgInfo=msg2)
        self.agent.add_behaviour(a)
        
    
    async def recusarAterrar(self,mensagem,idMsg):
        list2 = mensagem.split("_")
        jid, companhia, tipo, origem, destino, pistaID, pistaLoc, pistaOcup = list2[0],list2[1],list2[2],list2[3],list2[4],list2[5],list2[6],list2[7]
        aviao = Aviao.decoder(jid + "_" + companhia + "_" + tipo + "_" + origem + "_" + destino)

        if int(pistaID) != -1:
            self.agent.pistas[int(pistaID)].makeLivre()
        
        
        if idMsg == 'RefuseGare':
            if len(self.agent.avioesEmEsperaAterrarQueue) < self.agent.numMaxEsperaAterrar:
                # aviao fica em fila espera para aterrar
                aviao.setObjetivo("Aterrar")
                appendComVerificacao(self.agent.avioesEmEsperaAterrarQueue,aviao)
                msg = Message(to=f'{aviao.aviaoID}{XMPP}')
                msg.set_metadata("performative","refuse")
                msg.body = "RecusarAterrar|"+ mensagem
                await self.send(msg)
                msg2 = Message(to=f'agenteinformacao{XMPP}')
                msg2.set_metadata("performative","inform")
                msg2.body = "InformAterrarEspera|"+jid + "_" + companhia + "_" + tipo + "_" + origem + "_" + destino
                await self.send(msg2)
            
            else: 
                # manddar aviao aterrar noutro aeroporto
                msg = Message(to=f'{aviao.aviaoID}{XMPP}')
                msg.set_metadata("performative","refuse")
                msg.body = "AterrarOutro|"
                await self.send(msg)
                msg2 = Message(to=f'agenteinformacao{XMPP}')
                msg2.set_metadata("performative","inform")
                msg2.body = "InformAterrarRecusado|" + aviao.encoder()
                await self.send(msg2)

    #---------------------------------- DESCOLAR ----------------------------------------

    async def requestDescolar(self, mensagem):
        aviao = Aviao.decoder(mensagem)
       #print("Entrei no requestDescolar para o " +aviao.aviaoID)
        msg2 = Message(to=f'agenteinformacao{XMPP}')
        msg2.set_metadata("performative","inform")
        msg2.body = "InformRequestDescolar|" + aviao.encoder()       
        await self.send(msg2)
            
        msg = Message(to=f'gestorgares{XMPP}')
        msg.set_metadata("performative","request")
        msg.body = "RequestGareDescolar|"+ aviao.encoder()
        await self.send(msg)
    
    
    
    
    async def refuseGareDescolar(self,mensagem,idMsg):
        list2 = mensagem.split("_")
        jid, companhia, tipo, origem, destino = list2[0],list2[1],list2[2],list2[3],list2[4]
        aviao = Aviao.decoder(jid + "_" + companhia + "_" + tipo + "_" + origem + "_" + destino)

    
        if idMsg == 'RefuseGareDescolar':
                # aviao fica em fila espera para descolar
                print(bcolors.FAIL + "TC - " +idMsg + ": Aviao " + aviao.aviaoID + " pretende descolar mas não existem gares disponiveis " + bcolors.ENDC) 

                aviao.setObjetivo("DescolarSemGare")
                appendComVerificacao(self.agent.avioesEmEsperaDescolarQueue,aviao)
                #print("Adicionei o aviao " + aviao.aviaoID + " À lista de espera com " + aviao.objetivo)
                
                msg = Message(to=f'{aviao.aviaoID}{XMPP}')
                msg.set_metadata("performative","refuse")
                msg.body = "RecusarDescolar|"+ mensagem
                await self.send(msg)
                
                msg2 = Message(to=f'agenteinformacao{XMPP}')
                msg2.set_metadata("performative","inform")
                msg2.body = "InformDescolarEsperaGare|"+jid + "_" + companhia + "_" + tipo + "_" + origem + "_" + destino
                await self.send(msg2)
            
    
    
    async def confirmGareDescolar(self,mensagem,idMsg):
        aviao = Aviao.decoder(mensagem)
        gareID = mensagem.split("_")[5]
        print(bcolors.FAIL + "TC - " +idMsg + ": Aviao " + aviao.aviaoID + " pretende descolar, e foi lhe atribuida a gare " + gareID + bcolors.ENDC) 

        msg = Message(to=f'{aviao.aviaoID}{XMPP}')
        msg.set_metadata("performative","confirm")
        msg.body = idMsg + "|" + gareID
        await self.send(msg)
            
        # se ele tiver na lista de espera sai
        self.agent.avioesEmEsperaDescolarQueue = removeAviaoQueue(self.agent.avioesEmEsperaDescolarQueue,aviao)

        msg2 = Message(to=f'agenteinformacao{XMPP}')
        msg2.set_metadata("performative","inform")
        msg2.body = "InformOperacaoGareDescolar|" + aviao.encoder()  +"_"+ gareID    
        await self.send(msg2)

    async def requestPistaDescolar(self,mensagem):
        aviao = Aviao.decoder(mensagem)
        pista_escolhida = verificarPista(aviao.tipoAviao,self.agent.pistas,self.agent.numPistas)
        if pista_escolhida == -1:   # verificar se existe pista disponivel
                print(bcolors.FAIL + "TC: Aviao " + aviao.aviaoID + " pretende descolar, mas não existe pista disponível" + bcolors.ENDC) 
                
                aviao.setObjetivo("DescolarComGare")
                appendComVerificacao(self.agent.avioesEmEsperaDescolarQueue,aviao) 

                #Avisar Avião
                msg = Message(to=f'{aviao.aviaoID}{XMPP}')
                msg.set_metadata("performative","refuse")
                msg.body = "RecusarDescolar|"+mensagem
                await self.send(msg)
                
                #Avisar agente de informação
                msg2 = Message(to=f'agenteinformacao{XMPP}')
                msg2.set_metadata("performative","inform")
                msg2.body = "InformDescolarEsperaPista|" + aviao.encoder()       
                await self.send(msg2)

        else:  
            
            #Remover Avião da Queue para descolar
            self.agent.avioesEmEsperaDescolarQueue = removeAviaoQueue(self.agent.avioesEmEsperaDescolarQueue,aviao)


            print(bcolors.FAIL + f"TC: Descolagem do {aviao.aviaoID} autorizada! Pista " + str(pista_escolhida)+ " ocupada" + bcolors.ENDC)
            self.agent.pistas[pista_escolhida].makeOcupada()
            
            msg = Message(to=f'{aviao.aviaoID}{XMPP}')
            msg.set_metadata("performative","confirm")
            msg.body = "ConfirmPistaDescolar|" + str(pista_escolhida)
            await self.send(msg)
            
            
            msgI = Message(to=f'agenteinformacao{XMPP}')
            msgI.set_metadata("performative","inform")
            msgI.body = "InformInicioDescolar|" + str(pista_escolhida) + "_" + aviao.encoder()
            await self.send(msgI)

            msg2 = Message(to=f'agenteinformacao{XMPP}')
            msg2.set_metadata("performative","inform")
            msg2.body = "InformFimDescolar|" + str(pista_escolhida) + "_" + aviao.encoder()
            start_at = datetime.datetime.now() + datetime.timedelta(seconds=TEMPO_OPERACAO_PISTA)
            a = TorreDeControloMakePistaLivreBehav(start_at=start_at,pistaID=pista_escolhida,msgInfo=msg2)
            self.agent.add_behaviour(a)


    async def retirarFilaEspera(self,mensagem):
        aviao = Aviao.decoder(mensagem)
        for i in range(0,len(self.agent.avioesEmEsperaAterrarQueue)):
            if aviao.getID() == self.agent.avioesEmEsperaAterrarQueue[i].getID():
                self.agent.avioesEmEsperaAterrarQueue.pop(i)
                print(bcolors.FAIL + "Aviao " + str(aviao.getID()) + " retirado da lista de espera." + bcolors.ENDC)
                msg2 = Message(to=f'agenteinformacao{XMPP}')
                msg2.set_metadata("performative","inform")
                msg2.body = "InformAbandonarEspera|" + aviao.encoder()       
                await self.send(msg2)
                break


    async def run(self):
        msg = await self.receive(timeout=300)

        if msg:
            #print("TC: Message received with content " + msg.body)
            performative = msg.get_metadata('performative')
            #print("----------------------------------------\n")
            list = msg.body.split("|")
            idMsg , mensagem = list[0], list[1]
            if performative == 'request':
                if idMsg == "RequestAterrar":
                    await self.requestAterrar(mensagem)

                elif idMsg == "RequestDescolar":
                    await self.requestDescolar(mensagem)
                elif idMsg == 'RequestPistaDescolar' or idMsg == 'RequestPistaDescolarEspera':
                    await self.requestPistaDescolar(mensagem)
                

            elif performative == 'confirm':
                if idMsg == "ConfirmGare" or idMsg == "ConfirmGareEspera":
                    await self.confirmarAterrar(mensagem,idMsg)
                if idMsg == 'ConfirmGareDescolar' or idMsg == 'ConfirmGareDescolarEspera':
                    await self.confirmGareDescolar(mensagem,idMsg)
                    

            elif performative == 'refuse':
                if idMsg == "RefuseGare" or idMsg == "RefuseGareEspera":
                    await self.recusarAterrar(mensagem,idMsg)
                if idMsg == "RefuseGareDescolar" or idMsg == "RefuseGareDescolarEspera":
                    await self.refuseGareDescolar(mensagem,idMsg)

            elif performative == 'inform':
                if idMsg == "InformarAbandonar":
                    await self.retirarFilaEspera(mensagem)

        else:
            print(bcolors.FAIL + "Agent {}:".format(str(self.agent.jid)) + "Did not received any message after 30 seconds" + bcolors.ENDC)
