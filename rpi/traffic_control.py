from ligacao import Variaveis
import time
#boatr
# ciclo while infinito


x  = Variaveis()
while True:
    x.atualizar()
    #print(time.time())
    x.Android()
    x.Congestionamento1()
    time.sleep(1)
#congestionamento
#default:
    #x.CorRua_1
    #x.CorRua_2
#congestionamento: + 10 carros em menos 2s --> mudar verde
#mudar luz se carros esperarem mais de 15 segundos
#nao ter luz vermelha com 10 carros mais de 10 segundos
