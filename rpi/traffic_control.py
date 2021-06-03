
from ligacao import Variaveis
import time

x  = Variaveis()
while True:
    x.atualizar()
    #print(time.time())
    x.Android()
    print("Android")
    x.Congestionamento1()
    print("CONG1")
    x.Congestionamento2()
    print("CONG2")
    x.temporizador_15_rua1()
    print("TEMP1")
    x.temporizador_15_rua2()
    print("TEMP2")
    time.sleep(1)

#congestionamento: + 10 carros em menos 2s --> mudar verde
#mudar luz se carros esperarem mais de 15 segundos
#nao ter luz vermelha com 10 carros mais de 10 segundos