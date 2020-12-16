from bs4 import BeautifulSoup
import requests
import subprocess
import re
from datetime import datetime, timedelta, date


#Rimi soodukad
def rimiFail():
    print('r')
    Rsource = requests.get('https://www.rimi.ee/pakkumised').text
    Rcode = BeautifulSoup(Rsource, 'lxml')
    f = open('rimi.txt', 'w', encoding='UTF-8')
    for el in Rcode.find_all('div', class_='container__image-badge-price-basics'):
        try:
            Rtoode = el.find('div', class_='offer-card__name').text.strip()
            Reuro = el.find('div', class_='euro').text.strip()
            Rsendid = el.find('div', class_='cents').text.strip()
            f.write(Rtoode + ':' + Reuro + '.' + Rsendid + '€;') 
        except:
            #Kui ei olnud reaalset hinda, siis see leiab soodusprotsendi
            try:
                Rtoode = el.find('div', class_='offer-card__name').text.strip()
                Rprotsent = el.find('div', class_='new').text.strip()
                if Rprotsent == '-%':
                    raise Exception
                f.write(Rtoode + ':' + Rprotsent + ';')
            except:
                None
    f.close()


#Maxima soodukad
def maximaFail():
    print('m')
    Msource = requests.get('https://www.maxima.ee/pakkumised').text
    Mcode = BeautifulSoup(Msource, 'lxml')
    f = open('maxima.txt', 'w', encoding='UTF-8')
    for el in Mcode.find_all('div', class_='item bl_shadow'):
        try:
            Mtoode = el.find('div', class_='title').text.strip()
            Meuro = el.find('span', class_='value').text.strip()
            Msendid = el.find('span', class_='cents').text.strip()
            f.write(Mtoode + ':' + Meuro + "." + Msendid + "€;")
        except:
            None
    f.close()


#Toidumaailma soodukad
def toidumaailmFail():
    print('t')
    on_lehekülg = True
    lehe_esimene = []
    i = 1
    f = open('toidumaailm.txt', 'w', encoding='UTF-8')
    while on_lehekülg == True:
        Tsource = requests.get(f'https://www.kaubamaja.ee/gurmee/hea-hind?p={i}').text
        x = 0
        i += 1
        Tcode = BeautifulSoup(Tsource, 'lxml')
        for el in Tcode.find_all('a', class_='products-grid__link product-image'):
            Ttoode = el.find('h5', class_='products-grid__name product-name').text.strip()
            if Ttoode in lehe_esimene:
                on_lehekülg = False
                break
            if x == 0:
                lehe_esimene.append(Ttoode)
            x += 1
            Thind = el.find('span', class_='price').text.replace(',', '.').replace(u'\xa0', u'').replace(' ', '')
            f.write(Ttoode + ':' + Thind + ";")
    f.close()


#Kontrollib, kas fail on vanem kui kaks nädalat
def kuupäev(x):
    aasta = int(x[6:])
    kuu = int(x[0:2])
    päev = int(x[3:5])
    allalaetud = date(aasta, kuu, päev)
    täna = date.today()
    vahemik = (täna - allalaetud).days
    if vahemik > 14:
        return True
    else:
        return False 


#Laeb puuduvad või vanad failid alla
failid = []
puudu = ['rimiFail()', 'maximaFail()', 'toidumaailmFail()']
koguInfo = subprocess.check_output(['dir', '*txt'], shell=True).decode('utf-8')
kuupäevad = re.findall(r'\d{2}.\d{2}.\d{4}', koguInfo)
for sõne in koguInfo.split():
    if sõne.endswith('.txt'):
        failid.append(sõne)
for i in range(len(kuupäevad)):
    if failid[i] == 'rimi.txt':
        vana = kuupäev(kuupäevad[i])
        puudu.remove('rimiFail()')
        if vana == True:
            rimiFail()
    if failid[i] == 'maxima.txt':
        vana = kuupäev(kuupäevad[i])
        puudu.remove('maximaFail()')
        if vana == True:
            maximaFail()
    if failid[i] == 'toidumaailm.txt':
        vana = kuupäev(kuupäevad[i])
        puudu.remove('toidumaailmFail()')
        if vana == True:
            toidumaailmFail()
for funktsioon in puudu:
    eval(funktsioon)

#Failist info saamine
def infoSaamine(fail):
    sõnastik = {}
    with open(fail, 'r', encoding='UTF-8') as f:
        koguTekst = f.read().split(';')
        koguTekst.pop(-1)
        for paar in koguTekst:
            kaup = paar.split(':')
            sõnastik[kaup[0]] = kaup[1]
    return sõnastik

#Loob sõnastikud
Rimipakkumised = infoSaamine('rimi.txt')
Maximapakkumised = infoSaamine('maxima.txt')
Toidumaailmapakkumised = infoSaamine('toidumaailm.txt')

#Loop, mis otsib, kas toode on antud sõnastikus
def otsimis_loop(poekett, sõnastik, toote_nimi):
    print(poekett)
    for võti in sõnastik:
        for toode in võti.split():
            if toote_nimi in toode.lower():
                print(võti + " " + sõnastik[võti])
    print()

#Küsib toote nimetust ja prindib leitud tulemused
def otsi_toodet():
    otsitav_toode = input("Sisestage otsitav toode: ").lower()
    print()
    otsimis_loop('---Toidumaailma sooduspakkumised:\n', Toidumaailmapakkumised, otsitav_toode)
    otsimis_loop("---Maxima sooduspakkumised:\n", Maximapakkumised, otsitav_toode)
    otsimis_loop("---Rimi sooduspakkumised\n", Rimipakkumised, otsitav_toode)
    #Iga poeketi alla võiks lisada koodi, mis kirjutaks teksti, et pakkumised puuduvad,
    #juhul kui tõesti pole ühtegi sooduspakkumist vastavalt ketilt
    #
    #Samuti see funktsioon võiks selle info äkki tabelina display-ida
    # nt:
    # ---------------------------------
    # |    Rimi sooduspakkumised      |
    # ---------------------------------
    # | Apelsin, 1kg          | 1.60€ |
    # ---------------------------------
    #Ma leidsin mingi pythoni mooduli tableprint, nii et seda saaks ka kasutada


#Käivitab funktsiooni
otsi_toodet()


#Käivitab funktsiooni uuesti, et ei peaks igakord refreshima
while True:
    taaskord = input("Uue toote otsimiseks vajutage ENTER ning programmi lõpetamiseks X: ")
    if taaskord == 'X':
        break
    otsi_toodet()



