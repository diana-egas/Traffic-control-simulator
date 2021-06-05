
from ligacao import Variaveis
import time

x  = Variaveis()

while True:
    x.atualizar()
    print(time.time())
    x.Android()
    #quando semaforo vermelho
    if(x.semaforo1 =="Red"):
        x.Congestionamento1()
    if(x.semaforo2 =="Red"):
        x.Congestionamento2()

    if(x.semaforo1 =="Red"):
        x.temporizador_15_rua1()
    else:
        x.tempo1 = 0

    if(x.semaforo2 =="Red"):
        x.temporizador_15_rua2()
    else:
        x.tempo2 = 0

    print("TEMP2")
    time.sleep(1)

#congestionamento: + 10 carros em menos 2s --> mudar verde
#mudar luz se carros esperarem mais de 15 segundos
#nao ter luz vermelha com 10 carros mais de 10 segundos