import requests
import fake_useragent
from bs4 import BeautifulSoup
from requests.sessions import session
import json
from dotenv import dotenv_values

config = dotenv_values(".env")

session = requests.Session()

url = [
    "https://sport.innopolis.university/admin/sport/attendance/?training__group__id__exact=151&training__group__semester__id__exact=12&student__pk__exact=",
    'https://sport.innopolis.university/admin/sport/attendance/?training__group__id__exact=152&training__group__semester__id__exact=12&student__pk__exact=',
    'https://sport.innopolis.university/admin/sport/attendance/?training__group__id__exact=153&training__group__semester__id__exact=12&student__pk__exact=',
    'https://sport.innopolis.university/admin/sport/attendance/?training__group__id__exact=148&training__group__semester__id__exact=12&student__pk__exact=',
    'https://sport.innopolis.university/admin/sport/attendance/?training__group__id__exact=149&training__group__semester__id__exact=12&student__pk__exact=',
    'https://sport.innopolis.university/admin/sport/attendance/?training__group__id__exact=150&training__group__semester__id__exact=12&student__pk__exact=',
]

studs = []
with open('get_hours/studs.txt') as f:
    for line in f:
        studs.append(line.strip())



link = 'https://sso.university.innopolis.ru/adfs/oauth2/authorize/?response_type=code&client_id=7d0eb0b9-ad73-4942-be55-284facc99a95&resource=7d0eb0b9-ad73-4942-be55-284facc99a95&redirect_uri=https%3A%2F%2Fsport.innopolis.university%2Foauth2%2Fcallback&state=cHJvZmlsZQ%3D%3D&scope=openid&client-request-id=43f6793d-ddfa-4fa2-3575-0580000800bf'
user = fake_useragent.UserAgent().random

header = {
    'user-agent': user
}

data = {
    'UserName' : config['LOGIN'],
    'Password' : config['PASSWORD']
}


response = session.post(link, data=data, headers=header).text
for email in studs:
    new_l=[]
    for urls in url:
        try: 
            a = email.replace("@", "%40")
            prof = 'https://sport.innopolis.university/admin/sport/student/autocomplete/?term=' + a
            prof_responce = session.get(prof, headers=header).text 
            category_dict = json.loads(prof_responce)

            pri = category_dict['results'][0]
            pri2 = pri['id']
        except:
            print("Stud not find: " + email)
        else :

            link2 = urls + pri2
            hr = session.get(link2, headers=header).text
            hrs = BeautifulSoup(hr, "lxml")
            hj = hrs.find_all("td", class_="field-hours")
            sums = 0
            
            for kl in hj:
                sums += float(kl.text)
            kk = int(sums)
            new_l.append(kk)
    bh = str(sum(new_l))
    print(email + ' ' + bh)
    with open('get_hours/hours.txt', 'a') as f:
        f.write(email + " " + bh + '\n')