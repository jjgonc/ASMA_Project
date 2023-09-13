from spade.behaviour import CyclicBehaviour
from Utilitarios.var import XMPP, TEMPO_ESTADO, TEMPO_OPERACAO_PISTA,TEMPO_OPERACAO_GARE, bcolors
from Utilitarios.aviao import Aviao
from Utilitarios.pista import Pista
from Utilitarios.informacao import Informacao
from Behaviours.AgenteInformacao.agenteInformacaoRemoveEstadoAtualBehav import AgenteInformacaoRemoveEstadoAtualBehav
from Behaviours.AgenteInformacao.agenteInformacaoRemoveGareOcupBehav import AgenteInformacaoRemoveGareOcupAterrarBehav
import datetime

class AgenteInformacaoListenerBehaviour(CyclicBehaviour):
  
    def informacaoRequestAterragem(self, data):
        list = data.split('_')
        jid, companhia, tipo, origem, destino = list[0],list[1],list[2],list[3],list[4]
        aviao = Aviao(jid, companhia, tipo, origem, destino)
        info = Informacao(aviao, "-", "-", "Pediu", "Aterrar")
        self.agent.estado[jid] = info
        self.agent.historico.append(info)

    def informacaoFimAterragem(self, data):
        list = data.split('_')
        gare, pistaID, jid, companhia, tipo, origem, destino = list[0],list[1],list[2],list[3],list[4],list[5],list[6]
        aviao = Aviao(jid, companhia, tipo, origem, destino)
        info = Informacao(aviao, gare, pistaID, "Feito", "Aterrar")
        self.agent.estado[jid] = info
        self.agent.historico.append(info)
        self.agent.pistas[int(pistaID)].makeLivre()  
        self.agent.gares[int(gare)] = aviao
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=TEMPO_OPERACAO_GARE)
        a = AgenteInformacaoRemoveGareOcupAterrarBehav(start_at=start_at,gareID=int(gare))
        self.agent.add_behaviour(a)

    def informacaoAterragemEspera(self, data):
        list = data.split('_')
        jid, companhia, tipo, origem, destino = list[0],list[1],list[2],list[3],list[4]
        aviao = Aviao(jid, companhia, tipo, origem, destino)
        info = Informacao(aviao, "-", "-", "FilaDeEspera", "Aterrar")
        self.agent.estado[jid] = info
        self.agent.historico.append(info)
        self.agent.listaEsperaAterrar.append(aviao)

    def informAterrarRecusado(self, data):
        list = data.split('_')
        jid, companhia, tipo, origem, destino = list[0],list[1],list[2],list[3],list[4]
        aviao = Aviao(jid, companhia, tipo, origem, destino)
        info = Informacao(aviao, "-" ,"-" , "Recusado", "Aterrar")
        self.agent.estado[jid] = info
        self.agent.historico.append(info)
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=TEMPO_ESTADO)
        a = AgenteInformacaoRemoveEstadoAtualBehav(start_at=start_at,aviaoID=jid)
        self.agent.add_behaviour(a)

    
    def informacaoInicioAterragem(self, data):
        list = data.split('_')
        gare, pistaID, jid, companhia, tipo, origem, destino = list[0],list[1],list[2],list[3],list[4],list[5],list[6]
        aviao = Aviao(jid, companhia, tipo, origem, destino)
        info = Informacao(aviao, gare, pistaID, "A acontecer", "Aterrar")
        self.agent.pistas[int(pistaID)].makeOcupada()
        self.agent.pistas[int(pistaID)].setAviao(aviao)
        self.agent.estado[jid] = info
        self.agent.historico.append(info)
        # verifica se o aviao ta na lista de espera
        for i in range(0,len(self.agent.listaEsperaAterrar)):
            if aviao.getID() == self.agent.listaEsperaAterrar[i].getID():
                self.agent.listaEsperaAterrar.pop(i)
                break


    def removeAviaoGare(self,aviaoDescolar):
        for gare,aviao in self.agent.gares.items():
            if aviao != None:
                if aviao.aviaoID == aviaoDescolar.aviaoID:
                    self.agent.gares[gare] = None


    def informacaoFimDescolar(self, data):
        list = data.split('_')
        pistaID, jid, companhia, tipo, origem, destino = list[0],list[1],list[2],list[3],list[4],list[5]
        aviao = Aviao(jid, companhia, tipo, origem, destino)
        info = Informacao(aviao, "-", pistaID, "Feito", "Descolar")
        self.agent.estado[aviao.getID()] = info
        self.agent.historico.append(info)
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=TEMPO_ESTADO)
        a = AgenteInformacaoRemoveEstadoAtualBehav(start_at=start_at,aviaoID=aviao.getID())
        self.agent.add_behaviour(a)
        self.agent.pistas[int(pistaID)].makeLivre()  


    def informacaoDescolarEsperaGare(self, data):
        list = data.split('_')
        jid, companhia, tipo, origem, destino = list[0],list[1],list[2],list[3],list[4]
        aviao = Aviao(jid, companhia, tipo, origem, destino)
        info = Informacao(aviao, "-", "-", "FilaDeEsperaGare", "Descolar")
        self.agent.estado[jid] = info
        self.agent.historico.append(info)
        self.agent.listaEsperaDescolar.append(aviao)

    def informacaoDescolarEsperaPista(self, data):
        list = data.split('_')
        jid, companhia, tipo, origem, destino = list[0],list[1],list[2],list[3],list[4]
        aviao = Aviao(jid, companhia, tipo, origem, destino)
        info = Informacao(aviao, str(self.agent.estado[jid].getGareID()), "-", "FilaDeEsperaPista", "Descolar")
        self.agent.estado[jid] = info
        self.agent.historico.append(info)
        self.agent.listaEsperaDescolar.append(aviao)

    def informacaoOperacaoGareDescolar(self, data):
        list = data.split('_')
        jid, companhia, tipo, origem, destino, gare = list[0],list[1],list[2],list[3],list[4],list[5]
        aviao = Aviao(jid, companhia, tipo, origem, destino)
        info = Informacao(aviao, gare, "-", "Operacao", "Descolar")
        self.agent.estado[jid] = info
        self.agent.historico.append(info)
        self.agent.gares[int(gare)] = aviao

        # verifica se o aviao ta na lista de espera
        for i in range(0,len(self.agent.listaEsperaDescolar)):
            if aviao.getID() == self.agent.listaEsperaDescolar[i].getID():
                self.agent.listaEsperaDescolar.pop(i)
                break        

    def informacaoRequestDescolar(self, data):
        list = data.split('_')
        jid, companhia, tipo, origem, destino = list[0],list[1],list[2],list[3],list[4]
        aviao = Aviao(jid, companhia, tipo, origem, destino)
        info = Informacao(aviao, "-", "-", "Pediu", "Descolar")
        self.agent.estado[jid] = info
        self.agent.historico.append(info)
        # print("informacaoRequestDescolar", info)

    def informDescolarRecusado(self, data):
        list = data.split('_')
        jid, companhia, tipo, origem, destino = list[0],list[1],list[2],list[3],list[4]
        aviao = Aviao(jid, companhia, tipo, origem, destino)
        info = Informacao(aviao, "-", "-", "Recusado", "Descolar")
        self.agent.estado[jid] = info
        self.agent.historico.append(info)


    def informacaoInicioDescolar(self, data):
        list = data.split('_')
        pistaID, jid, companhia, tipo, origem, destino = list[0],list[1],list[2],list[3],list[4],list[5]
        aviao = Aviao(jid, companhia, tipo, origem, destino)
        info = Informacao(aviao, "-", pistaID , "A acontecer", "Descolar")
        self.agent.pistas[int(pistaID)].makeOcupada()
        self.agent.pistas[int(pistaID)].setAviao(aviao)
        self.agent.estado[jid] = info
        self.agent.historico.append(info)
        # verifica se o aviao ta na lista de espera
        for i in range(0,len(self.agent.listaEsperaDescolar)):
            if aviao.getID() == self.agent.listaEsperaDescolar[i].getID():
                self.agent.listaEsperaDescolar.pop(i)
                break
        self.removeAviaoGare(aviao)

    def informacaoPistas(self,data):
        list = data.split("/")
        for i in range(0,len(list)):
            self.agent.pistas[i] = Pista.decoder(list[i])

    def distribuicaoGares(self,data):
        numGares = int(data)
        
        for i in range(0,numGares):
            self.agent.gares[i] = None

    def informacaoAbandonarEspera(self,data):
        # print(data)
        aviao = Aviao.decoder(data)
        for i in range(0,len(self.agent.listaEsperaAterrar)):
            if aviao.getID() == self.agent.listaEsperaAterrar[i].getID():
                self.agent.listaEsperaAterrar.pop(i)
                break
        self.agent.estado[aviao.getID()].setEstado("Abandonou")  
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=TEMPO_ESTADO)
        a = AgenteInformacaoRemoveEstadoAtualBehav(start_at=start_at,aviaoID=aviao.getID())
        self.agent.add_behaviour(a)

    async def run(self):
        msg = await self.receive(timeout=300)  
        if msg:
            performative = msg.get_metadata("performative")
        
            msg_body = msg.body.split('|')
            requestId, data = msg_body[0], msg_body[1]

            if performative == "inform":
                if requestId == 'InformRequestAterrar':
                    self.informacaoRequestAterragem(data)
                if requestId == 'InformFimAterragem':
                    self.informacaoFimAterragem(data)
                if requestId == "InformAterrarEspera":
                    self.informacaoAterragemEspera(data)
                if requestId == 'InformAterrarRecusado':
                    self.informAterrarRecusado(data)
                if requestId == 'InformInicioAterragem':
                    self.informacaoInicioAterragem(data)

                if requestId == 'InformFimDescolar':
                    self.informacaoFimDescolar(data)
                if requestId == "InformDescolarEsperaGare":
                    self.informacaoDescolarEsperaGare(data)
                if requestId == "InformDescolarEsperaPista":
                    self.informacaoDescolarEsperaPista(data)
                if requestId == 'InformRequestDescolar':
                    self.informacaoRequestDescolar(data)
                if requestId == 'InformDescolarRecusado':
                    self.informacaoDescolarRecusado(data)
                if requestId == 'InformInicioDescolar':
                    self.informacaoInicioDescolar(data)
                if requestId == 'InformOperacaoGareDescolar':
                    self.informacaoOperacaoGareDescolar(data)

                if requestId == "InformPistas":
                    self.informacaoPistas(data)
                
                if requestId == 'InformGares':
                    self.distribuicaoGares(data)
                if requestId == 'InformAbandonarEspera':
                    self.informacaoAbandonarEspera(data)
