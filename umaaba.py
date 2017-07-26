import requests
from bs4 import BeautifulSoup
import xlsxwriter
gyms=['lea', 'mogilska', 'solvaypark', 'wadowicka', 'krakowska', 'aleksandry', 'plaza', 'zakopianska', 'nastoku', 'bratyslawska']
counter=1
workbook = xlsxwriter.Workbook('allgyms.xlsx')
worksheet = workbook.add_worksheet()
def gym_spider(gym):
        godziny = []
        zajecia = []
        url = 'http://fitnessplatinium.pl/'+gym+'/grafik/'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "lxml")
        dni=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']



        for hour in soup.findAll('td', {'class': 'hour'}):
            if hour.contents==[]:
                hour.contents=['']
            godziny.append(hour.contents)
        for n,i in enumerate(godziny):
            if i==['']:
                godziny[n]=godziny[n-1]
        temp=[]
        for a in godziny:
            if isinstance(a, list):
                temp.extend(a)
        print(temp)


        for aula in soup.findAll('td', {'class': 'active'}):
            if aula.contents==None:
                aula.contents=[]
            else:
                aula.contents=str(aula.findAll('h6'))[5:-6]
            zajecia.append([aula.contents])



        worksheet.write_row('A1',('Aula', 'Dia', 'Hora', 'Academia'))
        for c in zajecia:
            if "&amp" in c[0]:
                c[0]=c[0].replace("&amp;","&")
            c.append(dni[zajecia.index(c)%7])
            c.append(str(temp[int(zajecia.index(c)/7)]))
            c.append(gym)
        klasy=[]
        for c in zajecia:
            if c[0]!='':
                klasy.append(c)
        for c in klasy:
            worksheet.write_row(counter, 0, c)
            counter+=1
            print(counter)
        print(klasy)

        global counter


for gym in gyms:
    gym_spider(gym)
workbook.close()