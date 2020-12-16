import subprocess
import re
from datetime import datetime, timedelta, date

failid = []
puudu = ['rimiFail()', 'maximaFail()', 'toidumaailmFail()']
koguInfo = subprocess.check_output(['dir', '*txt'], shell=True).decode('utf-8')
kuupäevad = re.findall(r'\d{2}.\d{2}.\d{4}', koguInfo)
for sõne in koguInfo.split():
    if sõne.endswith('.txt'):
        failid.append(sõne)
print(failid)
for i in range(len(kuupäevad)):
    if failid[i] == 'rimi.txt':
        puudu.remove('rimiFail()')
        print(puudu)
    if failid[i] == 'maxima.txt':
        puudu.remove('maximaFail()')
        print(puudu)
    if failid[i] == 'toidumaailm.txt':
        puudu.remove('toidumaailmFail()')
        print(puudu)

# N = 2

# date_N_days_ago = datetime.now() - timedelta(days=N)

# print(datetime.now())
# print(date_N_days_ago)

# a = date(12/15/2020)
# b = date(2020,3,3)
# print((a-b).days)

