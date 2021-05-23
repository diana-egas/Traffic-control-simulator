from firebase import firebase
from requests.sessions import Request
import json
class Variaveis(object):
    def __init__(self) -> None:
        self.firebase = firebase.FirebaseApplication('https://traffic-control-simulator-default-rtdb.europe-west1.firebasedatabase.app')
        self.jsonz = self.firebase.get('/',None)
        self.semaforo1 = self.jsonz["crossing"]["street1"]
        self.semaforo2 = self.jsonz["crossing"]["street2"]
        self.carros1 = self.jsonz["crossing"]["street1_cars"]
        self.carros2 = self.jsonz["crossing"]["street2_cars"]
        self.peoes1 = self.jsonz["crossing"]["street1_pedestrians"]
        self.peoes2 = self.jsonz["crossing"]["street2_pedestrians"]
        self.Light = self.jsonz["Request"]["Light"]
        self.Traffic_Light = self.jsonz["Request"]["Traffic Light"]
        self.anterior1 = 0
        self.anterior2 = 0
        self.tempo1 = 0
        self.tempo2 =0
    def atualizar(self):
        self.firebase = firebase.FirebaseApplication('https://traffic-control-simulator-default-rtdb.europe-west1.firebasedatabase.app')
        self.jsonz = self.firebase.get('/',None)
        self.semaforo1 = self.jsonz["crossing"]["street1"]
        self.semaforo2 = self.jsonz["crossing"]["street2"]
        self.carros1 = self.jsonz["crossing"]["street1_cars"]
        self.carros2 = self.jsonz["crossing"]["street2_cars"]
        self.peoes1 = self.jsonz["crossing"]["street1_pedestrians"]
        self.peoes2 = self.jsonz["crossing"]["street2_pedestrians"]
        self.Light = self.jsonz["Request"]["Light"]
        self.Traffic_Light = self.jsonz["Request"]["Traffic Light"]

    def Rua_1(self):
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
        self.peoes2 = self.firebase.get('/crossing/street2_pedestrians',None)
        #print(peoes)

    def CorRua_1(self):
        print("oi")
        if self.semaforo1 == "Red":
            #print("vermelho")
            self.firebase.put('/crossing',"street1", "Green")
            self.firebase.put('/crossing',"street1_pedestrians", "Red")
        else:
            #print("verde")
            self.firebase.put('/crossing',"street1", "Red")
            self.firebase.put('/crossing',"street1_pedestrians", "Green")
        self.semaforo1 = self.firebase.get('/crossing/street1',None)
    def CorRua_2(self):
        self.semaforo2 = self.firebase.get('/crossing/street2',None)
        #print(semaforo)
        if self.semaforo2 == "Red":
            #print("vermelho")
            self.firebase.put('/crossing',"street2", "Green")
            self.firebase.put('/crossing',"street2_pedestrians", "Red")
        else:
            #print("verde")
            self.firebase.put('/crossing',"street2", "Red")
            self.firebase.put('/crossing',"street2_pedestrians", "Green")
    def Android(self):
        self.Light = self.firebase.get('/Request/Light',None)
        self.Traffic_Light = self.firebase.get('/Request/Traffic Light',None)
        print(self.Light)
        print(self.Traffic_Light)
    
    def Congestionamento1(self):
        print("Entre")
        if (self.carros1 >= 10 and self.anterior1 >= 10 and self.semaforo1 == "Red" ):
            self.CorRua_1()
            self.CorRua_2()
        self.anterior1 = self.carros1

    def Congestionamento2(self):
        print("o diogo adormeceu")
        if (self.carros2 >= 10 and self.anterior2 >= 10 and self.semaforo2 == "Red" ):
            self.semaforo2  = "Green"
        self.anterior2 = self.carros2
    
    def temporizador_15_rua1(self):
        if self.carros1==0: self.tempo = 0
        if self.carros1 > 0:
            self.tempo = self.tempo1 +1
        if self.tempo1 == 15:
            #luz muda
            self.CorRua_1()
            self.CorRua_2()

    def temporizador_15_rua2(self):
        if self.carros2==0: self.tempo2 = 0
        if self.carros2 > 0:
            self.tempo2 = self.tempo2 +1
        if self.tempo2 == 15:
            #luz muda
            self.CorRua_2()
            self.CorRua_1()

    #Rua_1()
    #Rua_2()
    #CorRua_1()
    #Android()