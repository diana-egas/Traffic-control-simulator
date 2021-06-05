from firebase import firebase
from requests.sessions import Request
import json
import time
#get dos valores da firebase + atribuição de valores às variaveis
class Variaveis(object):
    def __init__(self) -> None:
        self.firebase = firebase.FirebaseApplication('https://traffic-control-simulator-default-rtdb.europe-west1.firebasedatabase.app')
        self.jsonz = self.firebase.get('/',None)
        self.semaforo1 = self.jsonz["crossing"]["street1"]
        self.semaforo2 = self.jsonz["crossing"]["street2"]
        self.carros1 = self.jsonz["crossing"]["street1_cars"]
        self.carros2 = self.jsonz["crossing"]["street2_cars"]
        self.peoes1 = self.jsonz["crossing"]["street1_pedestrians"]
        #self.peoes2 = self.jsonz["crossing"]["street2_pedestrians"]
        self.num_peoes = self.jsonz["crossing"]["pedestrian_number"]
        self.Light = self.jsonz["Request"]["Light"]
        self.Traffic_Light = self.jsonz["Request"]["Traffic Light"]
        #self.anterior1 = 0
        #self.anterior2 = 0
        self.tempo1 = 0
        self.tempo2 =0
    #a cada iteração atualizar valor das variaveis da firebase
    def atualizar(self):
        self.firebase = firebase.FirebaseApplication('https://traffic-control-simulator-default-rtdb.europe-west1.firebasedatabase.app')
        self.jsonz = self.firebase.get('/',None)
        self.semaforo1 = self.jsonz["crossing"]["street1"]
        self.semaforo2 = self.jsonz["crossing"]["street2"]
        self.carros1 = self.jsonz["crossing"]["street1_cars"]
        self.carros2 = self.jsonz["crossing"]["street2_cars"]
        self.peoes1 = self.jsonz["crossing"]["street1_pedestrians"]
        self.num_peoes = self.jsonz["crossing"]["pedestrian_number"]
        #self.peoes2 = self.jsonz["crossing"]["street2_pedestrians"]

        self.Light = self.jsonz["Request"]["Light"]
        self.Traffic_Light = self.jsonz["Request"]["Traffic Light"]

    """def Rua_1(self):
        self.semaforo1 = self.firebase.get('/crossing/street1',None)
        #print(semaforo)
        self.carros1 = self.firebase.get('/crossing/street1_cars',None)
        #print(carros)
        self.peoes1 = self.firebase.get('/crossing/street1_pedestrians',None)
        #print(peoes)

    def Rua_2(self):
        self.semaforo2 = self.firebase.get('/crossing/street2',None)
        #print(semaforo)
        self.carros2 = self.firebase.get('/crossing/street2_cars',None)
        #print(carros)
        #self.peoes2 = self.firebase.get('/crossing/street2_pedestrians',None)
        #print(peoes)"""

    #Alteração dos valores da rua 1(A) para cor oposta + cor peoes
    def CorRua_1(self): #RUA A NO FIREBASE
        self.semaforo1 = self.firebase.get('/crossing/street1',None)
        if self.semaforo1 == "Red": #semaforo vermelho
            #print("vermelho")
            self.firebase.put('/crossing',"street1", "Green") #mudar semaforo para verde
            self.firebase.put('/crossing',"street1_pedestrians", "Red") #peoes vermelho

        else: #semaforo verde #lia amarelo e mudava
            #print("verde")
            self.firebase.put('/crossing',"street1", "Yellow")
            time.sleep(1)
            self.firebase.put('/crossing',"street1", "Red") #mudar semaforo para vermelho
            self.firebase.put('/crossing',"street1_pedestrians", "Green") #peoes verde
        self.semaforo1 = self.firebase.get('/crossing/street1',None) #get para atualizar valor

    def CorRua_2(self):
        self.semaforo2 = self.firebase.get('/crossing/street2',None)
        #print(semaforo)
        if self.semaforo2 == "Red":
            #print("vermelho")
            self.firebase.put('/crossing',"street2", "Green")
            #self.firebase.put('/crossing',"street2_pedestrians", "Red")
        else:
            #print("verde")
            self.firebase.put('/crossing',"street2", "Yellow")
            time.sleep(1)
            self.firebase.put('/crossing',"street2", "Red")
            #self.firebase.put('/crossing',"street2_pedestrians", "Green")

    #Pedidos da aplicação Android
    def Android(self):
        self.Light = self.firebase.get('/Request/Light',None)
        self.Traffic_Light = self.firebase.get('/Request/Traffic Light',None)
        if(self.Traffic_Light== "horizontal"): #Rua 1
            #print("entrei vertical")
            #fazer alterações necessárias ás restantes ruas
            if(self.Light == "Green" and self.semaforo2 != "Red"):
                self.firebase.put('/crossing',"street2", "Yellow")
                time.sleep(1)
                self.firebase.put('/crossing',"street1_pedestrians", "Red")
                self.firebase.put('/crossing',"street2", "Red")
            
            self.firebase.put('/crossing',"street1", self.Light)
                #self.firebase.put('/crossing',"street2_pedestrians", "Green")

            if(self.Light == "Red"):
                self.firebase.put('/crossing',"street1", "Yellow")
                time.sleep(1)
                self.firebase.put('/crossing',"street1_pedestrians", "Green")
                self.firebase.put('/crossing',"street2", "Green")
                #self.firebase.put('/crossing',"street2_pedestrians", "Red")

        if(self.Traffic_Light=="vertical"): #rua2
            #fazer alterações necessárias ás restantes ruas
            if(self.Light == "Green" and self.semaforo1 != "Red"):
                #self.firebase.put('/crossing',"street2_pedestrians", "Red")
                self.firebase.put('/crossing',"street1", "Yellow")
                time.sleep(1)
                self.firebase.put('/crossing',"street1", "Red")
                self.firebase.put('/crossing',"street1_pedestrians", "Green")

            self.firebase.put('/crossing',"street2", self.Light)

            if(self.Light == "Red"):

                self.firebase.put('/crossing',"street1", "Yellow")
                time.sleep(1)
                self.firebase.put('/crossing',"street1_pedestrians", "Green")
                self.firebase.put('/crossing',"street1", "Green")
                #self.firebase.put('/crossing',"street2_pedestrians", "Red")

        if(self.Traffic_Light=="pedestre"): #pedestres relativamente À rua 1
            print("entrou pedestres")
            #fazer alterações necessárias ás restantes ruas
            if(self.Light == "Green" and self.semaforo1 != "Red"):
                #self.firebase.put('/crossing',"street2_pedestrians", "Red")
                self.firebase.put('/crossing',"street1", "Yellow")
                time.sleep(1)
                self.firebase.put('/crossing',"street1", "Red")
                self.firebase.put('/crossing',"street2", "Green")

            if(self.Light == "Red"):
                self.firebase.put('/crossing',"street2", "Yellow")
                time.sleep(1)
                self.firebase.put('/crossing',"street1", "Green")
                self.firebase.put('/crossing',"street2", "Red")
                #self.firebase.put('/crossing',"street2_pedestrians", "Red")
            
            self.firebase.put('/crossing',"street1_pedestrians", self.Light) #colocar o semaforo na cor pedida
        
        self.firebase.put('/Request', "Traffic Light","lixo")
            
    #deteção congestionamento
    def Congestionamento1(self):
        print("entrou congestionamento1")
        #nr de carros maior que 10 na rua 1 
        if (float(self.carros1) >= 10  and self.semaforo1 == "Red" ):
            print("verificou condicao 10 carros")
            #alteração dos semaforos de cada rua (para o oposto)
            self.CorRua_2()
            self.CorRua_1()
            self.tempo2 = self.tempo2 +10
            time.sleep(10)
            #colocar nr de carros a 0
            #self.
            #self.firebase.put('/crossing',"street1_cars", "0")

    def Congestionamento2(self):
        print("entrou congestionamento2")
        if (float(self.carros2 + 0.3 * self.num_peoes) >= 10  and self.semaforo2 == "Red" ):
            print("verificou condicao 10 carros")
            self.CorRua_1()
            self.CorRua_2()
            self.tempo1 = self.tempo1 +10
            time.sleep(10)
            #colocar nr de carros a 0
            #self.carros2 = 0
            #self.firebase.put('/crossing',"street2_cars", 0)

    #carros não podem esperar mais de 15 sg em sinal vermelho
    def temporizador_15_rua1(self):
        print("entrou temp1", "tempo", self.tempo1)
        if self.carros1==0: self.tempo1 = 0
        if self.carros1 > 0: #se houver carros incrementar contador
            self.tempo1 = self.tempo1 +1
        if self.tempo1 == 15: #quando passam 15 seg com + de 15 carros muda luz
            print("verificou mudança de luz")
            #luz muda

            self.CorRua_2()
            self.CorRua_1()
            self.tempo1 = 0

    def temporizador_15_rua2(self):
        print("entrou temp2", "tempo", self.tempo2)
        if float(self.carros2 + 0.3 * self.num_peoes) == 0: self.tempo2 = 0
        if float(self.carros2 + 0.3 * self.num_peoes) > 0:
            self.tempo2 = self.tempo2 + 1
        if self.tempo2 == 15:
            print("verificou mudança de luz")
            #luz muda
            self.CorRua_1()
            self.CorRua_2()
            self.tempo2 = 0