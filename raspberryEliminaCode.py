#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time, requests, json, urllib3
from firebase import firebase


pinBottone = 17 #6 pin basso
loop = True
#numeroServito = 0
http = urllib3.PoolManager()
url = 'http://elisapessa.altervista.org/eliminaCode/eliminaCode.php'
urlLogin = 'http://gmail.com'

#temporaneeee
responseText = 'eliminaCodde = {numeroServito: 5, utimoNumeroPrenotato: 12}'



#FIEBASE
urlDB = 'https://eliminacode.firebaseio.com'
firebase = firebase.FirebaseApplication(urlDB, None)



GPIO.setmode(GPIO.BCM)
GPIO.setup(pinBottone, GPIO.IN, pull_up_down=GPIO.PUD_UP)









def recuperaNumeriClienti():
    #QUI SI DOVRANNO RECUPERARE I DATI IN FORMATO JSON CO HTTP
    #responseObject = requests.get(url)
    #responseText = responseObject.text
    variabili = json.loads(responseText)
    numeroServito = variabili['numeroServito']
    utimoNumeroPrenotato = variabili ('utimoNumeroPrenotato')
    print ('numeroServito ', numeroServito)
    print ('utimoNumeroPrenotato ', utimoNumeroPrenotato)
    return numeroServito, utimoNumeroPrenotatovariabili

'''

def sliceVariabili():
    #inizioNumServito = responseText.find(chiaveNumeroServito) + len(chiaveNumeroServito) + 2
    variabili = splitlines(responseText)
    print(variabili)

    return numeroServito, ultimoNumeroPrenotato
'''

'''
#chiamata HTTP
def recuperoNumeroServito():
    paginaHTTP = http.request('GET', url)
    contenutoPagina = paginaHTTP.data
    return contenutoPagina
'''

def determinaSeIlPulsanteEPremuto():
    if (GPIO.input(pinBottone) == False):
        numeroServito = recuperaNumeriClienti()
        #numeroServito += 1
        print('ho premuto il pulsante')
        print(numeroServito)
        time.sleep(0.2)

def leggoDaFirebase():
    jsonRispostaFirebase = firebase.get(dataOdierna, None)
    numeroServito = jsonRispostaFirebase['numeroServito']
    ultimoNumeroPrenotato = jsonRispostaFirebase['ultimoNumeroPrenotato']
    return numeroServito, ultimoNumeroPrenotato

def aggiornaFirebase(numeroServito, ultimoNumeroPrenotato):
    print('inizio aggiorna')
    urlUpdate = urlDB + '/' + dataOdierna
    result = firebase.patch(urlUpdate, data={'ultimoNumeroPrenotato':str(int(ultimoNumeroPrenotato) + 1)})
    print(result)


print('Avvio... \n')
while loop == True:
    #preleva la data per metterti nella giusta tabella del database
    dataOdierna = time.strftime('%d%m%Y')
    #print(dataOdierna)
    #preleva dati dal db
    numeroServito, ultimoNumeroPrenotato = leggoDaFirebase()
    print('numeroServito ', numeroServito)
    print ('ultimoNumeroPrenotato ', ultimoNumeroPrenotato)
    #invia aggiornamenti contatori
    aggiornaFirebase(numeroServito, ultimoNumeroPrenotato)
    #stampa il biglietto
    #eventualmente invia i dati dell'utente

    #determinaSeIlPulsanteEPremuto()
    loop = False