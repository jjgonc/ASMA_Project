from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from Behaviours.Aviao.informaEstacionamento import *
from Utilitarios.var import bcolors, TEMPO_OPERACAO_GARE, TEMPO_OPERACAO_PISTA
from Behaviours.Aviao.requestPistaDescolarBehav import RequestPistaDescolarBehav


class listenBehaviour(CyclicBehaviour):
    async def run(self):
        msgResposta = await self.receive(timeout=300)  
        if msgResposta:
            performative = msgResposta.get_metadata('performative')
            msgRespostaParsed = msgResposta.body.split("|")
            if performative == 'confirm': 
                if msgRespostaParsed[0] == "ConfirmarAterrar":
                    msgConfirmacao = msgRespostaParsed[1].split("_")
                    gareId, pistaId, pistaLoc, pistaOcup = msgConfirmacao[0], msgConfirmacao[1], msgConfirmacao[2], msgConfirmacao[3] 
                    print(bcolors.OKBLUE + str(self.agent.aviao.getID()) + ": Confirmação de aterragem recebida na pista " + str(pistaId) + " e estacionnar na gare " + str(gareId) + "." + bcolors.ENDC)
                    a = informaEstacionamentoBehaviour(gareId)
                    self.agent.add_behaviour(a)
                    self.agent.aviao.setObjetivo('Nenhum')

                elif msgRespostaParsed[0] == "ConfirmLibertarGare":
                    gareId = msgRespostaParsed[1]

                elif msgRespostaParsed[0] == 'ConfirmGareDescolar':
                    gare = msgRespostaParsed[1]
                    print(bcolors.OKBLUE + str(self.agent.aviao.getID()) + ": A operacionar na gare " + gare + " para descolar"  + bcolors.ENDC)   
                    msg = Message(to=f'torredecontrolo{XMPP}')
                    msg.set_metadata("performative","request")
                    msg.body =  "RequestPistaDescolar|" + self.agent.aviao.encoder()
                    start_at = datetime.datetime.now() + datetime.timedelta(seconds=TEMPO_OPERACAO_GARE)
                    a = RequestPistaDescolarBehav(start_at=start_at,msg=msg)
                    self.agent.add_behaviour(a)

                elif msgRespostaParsed[0] == 'ConfirmGareDescolarEspera':
                    msg = Message(to=f'torredecontrolo{XMPP}')
                    msg.set_metadata("performative","request")
                    msg.body =  "RequestPistaDescolarEspera|" + self.agent.aviao.encoder()
                    start_at = datetime.datetime.now() + datetime.timedelta(seconds=TEMPO_OPERACAO_GARE)
                    a = RequestPistaDescolarBehav(start_at=start_at,msg=msg)
                    self.agent.add_behaviour(a)

                elif msgRespostaParsed[0] == 'ConfirmPistaDescolar':
                    #Recebe a pista para descolar e manda msg para libertar gare
                    pista = msgRespostaParsed[1]
                    print(bcolors.OKBLUE + str(self.agent.aviao.getID()) + ": A descolar na pista " + pista + " e a enviar ao Gestor de Gares para libertar gare"  + bcolors.ENDC)   
                    msg = Message(to=f'gestorgares{XMPP}')
                    msg.set_metadata("performative","request")
                    msg.body = "LibertarGare|" + str(self.agent.aviao.aviaoID) 
                    await self.send(msg)
            
            elif performative == 'refuse':
                if msgRespostaParsed[0] == "RecusarAterrar":
                    print(bcolors.OKBLUE + str(self.agent.aviao.getID()) + ": A aguardar nova resposta de aterragem" + bcolors.ENDC)   #a dar voltas no ar até receber uma resposta
            
                elif msgRespostaParsed[0] == "AterrarOutro":
                    print(bcolors.OKBLUE + str(self.agent.aviao.getID()) + ": Aterrar noutro aeroporto" + bcolors.ENDC)
                    await self.agent.stop()
            
            else:
                print(bcolors.OKBLUE + self.agent.aviao.getID() + ": Mensagem de resposta inválida" + bcolors.ENDC)
        else:
            
            if self.agent.aviao.getObjetivo() == 'Aterrar':
            
                msg = Message(to=f'torredecontrolo{XMPP}')  
                msg.set_metadata("performative", "inform")  
                msg.body = "InformarAbandonar|" + self.agent.aviao.encoder() 
                await self.send(msg)
                print(bcolors.OKBLUE + str(self.agent.aviao.getID()) + ": Tempo de espera excedido. Avisei a Torre de Controlo. A deixar o aeroporto..." + bcolors.ENDC)
                await self.agent.stop()



        