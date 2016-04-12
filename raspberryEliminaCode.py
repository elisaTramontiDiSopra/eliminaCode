#!/usr/bin/python
# -*- coding: utf-8 -*-

#import RPi.GPIO as GPIO
import time, requests, json, urllib3
from firebase import firebase

pinBottone = 17 #6 pin basso
loop = True
http = urllib3.PoolManager()
url = 'http://elisapessa.altervista.org/eliminaCode/eliminaCode.php'
urlLogin = 'http://gmail.com'

test = True

#FIEBASE
urlDB = 'https://eliminacode.firebaseio.com'
firebase = firebase.FirebaseApplication(urlDB, None)

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(pinBottone, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def recuperaNumeriClienti():
    #QUI SI DOVRANNO RECUPERARE I DATI IN FORMATO JSON CO HTTP
    #responseObject = requests.get(url)
    #responseText = responseObject.text
    variabili = json.loads(responseText)
    numeroServito = variabili['numeroServito']
    ultimoNumeroPrenotato = variabili ('ultimoNumeroPrenotato')
    print ('numeroServito ', numeroServito)
    print ('utimoNumeroPrenotato ', ultimoNumeroPrenotato)
    return numeroServito, ultimoNumeroPrenotato

def determinaSeIlPulsanteEPremuto():
    while (test == True):
    #if (GPIO.input(pinBottone) == False):
        print('ho premuto il pulsante')
        #preleva la data per metterti nella giusta tabella del database
        dataOdierna = time.strftime('%d%m%Y')
        print(dataOdierna)
        numeroServito, ultimoPrenotato, analogico = leggoDaFirebase(dataOdierna)
        print('numeroServito ', numeroServito)
        print ('ultimoPrenotato ', ultimoPrenotato)
        aggiornaFirebase(ultimoPrenotato, analogico, dataOdierna)
        #stampa il biglietto
        calcolaAttesa(numeroServito, ultimoPrenotato)
        #eventualmente invia i dati dell'utente
        #determinaSeIlPulsanteEPremuto()
        time.sleep(0.2)

def leggoDaFirebase(dataOdierna):
    jsonRispostaFirebase = firebase.get(dataOdierna, None)
    numeroServito =  int(jsonRispostaFirebase['numeroServito'])
    ultimoPrenotato = int(jsonRispostaFirebase['ultimoNumeroPrenotato'])
    analogico = int(jsonRispostaFirebase['analogico'])
    return numeroServito, ultimoPrenotato, analogico

def aggiornaFirebase(ultimoPrenotato, analogico, dataOdierna):
    print('inizio aggiorna')
    urlUpdate = urlDB + '/' + dataOdierna
    #ultimoNumeroPrenotato = ultimoNumeroPrenotato+1
    print(ultimoPrenotato)
    resultUltimo = firebase.patch(urlUpdate, data={'ultimoNumeroPrenotato': str(ultimoPrenotato + 1)})
    resultAnalogico = firebase.patch(urlUpdate, data={'analogico':str(int(analogico) + 1)})
    print (resultUltimo)
    print(resultAnalogico)

def calcolaAttesa(numeroServito, ultimoNumeroPrenotato):
    codaPersone = ultimoNumeroPrenotato - numeroServito
    jsonRispostaFirebaseTempistiche = firebase.get('TempiAttesa', None)
    mediaPaziente = jsonRispostaFirebaseTempistiche['mediaPaziente']
    tempoAttesa = mediaPaziente * codaPersone
    print('Hai ', codaPersone, ' persone davanti a te.')
    print('Il tempo stimato di attesa è di ', tempoAttesa)


print('Avvio... \n')
while loop == True:
    determinaSeIlPulsanteEPremuto()