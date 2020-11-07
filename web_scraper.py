from bs4 import BeautifulSoup
import requests

#Rimi soodukad
Rimipakkumised = {}
Rsource = requests.get('https://www.rimi.ee/pakkumised').text
Rcode = BeautifulSoup(Rsource, 'lxml')
for el in Rcode.find_all('div', class_='container__image-badge-price-basics'):
    try:
        Rtoode = el.find('div', class_='offer-card__name').text.strip()
        Reuro = el.find('div', class_='euro').text.strip()
        Rsendid = el.find('div', class_='cents').text.strip()
        Rimipakkumised[Rtoode] = Reuro + "." + Rsendid + "€"
    except:
        #Kui ei olnud reaalset hinda, siis see leiab soodusprotsendi
        try:
            Rtoode = el.find('div', class_='offer-card__name').text.strip()
            Rprotsent = el.find('div', class_='new').text.strip()
            if Rprotsent == '-%':
                raise Exception
            Rimipakkumised[Rtoode] = Rprotsent
        except:
            None


#Maxima soodukad
Maximapakkumised = {}
Msource = requests.get('https://www.maxima.ee/pakkumised').text
Mcode = BeautifulSoup(Msource, 'lxml')
for el in Mcode.find_all('div', class_='item bl_shadow'):
    try:
        Mtoode = el.find('div', class_='title').text.strip()
        Meuro = el.find('span', class_='value').text.strip()
        Msendid = el.find('span', class_='cents').text.strip()
        Maximapakkumised[Mtoode] = Meuro + "." + Msendid + "€"
    except:
        None


#Toidumaailma soodukad
Toidumaailmapakkumised = {}
on_lehekülg = True
lehe_esimene = []
i = 1
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
        Toidumaailmapakkumised[Ttoode] = Thind


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



#            IDEE
#
#Saaks teha funktsiooni, et mitte kirjutada järgmist koguaeg:
# source = requests.get(link).text
# code = BeautifulSoup(source, 'lxml')


