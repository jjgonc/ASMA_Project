import time
from spade import quit_spade
from Agents.torreDeControlo import TorreControloAgent
from Agents.gestorDeGares import garesAgent
from Agents.criadorDeAvioes import criadorDeAvioesAgent
from Utilitarios.var import XMPP, PASSWORD, bcolors

def main():
    torreControloAgent = TorreControloAgent("torredecontrolo"+XMPP,PASSWORD)
    garesAgen = garesAgent("gestorgares"+XMPP,PASSWORD)
    criadorDeAvioes = criadorDeAvioesAgent("criadorDeAvioes"+XMPP,PASSWORD)

    futureT = torreControloAgent.start()
    futureT.result()

    futureG = garesAgen.start()
    futureG.result()

    futureC = criadorDeAvioes.start() 
    futureC.result()

    while torreControloAgent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            torreControloAgent.stop()
            torreControloAgent.stop()
            garesAgen.stop()
            for aviao in criadorDeAvioes.listAvioes:
                aviao.stop()
            criadorDeAvioes.stop()
            break
    print('Agents finished')

    # finish all the agents and behaviors running in your process
    quit_spade()
    

if __name__ == '__main__':
    main()
    
   