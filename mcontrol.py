import requests
from bs4 import BeautifulSoup
import lxml
import json


def convert_symbol_to_url(symbol) :
    with open('symbolurl.json','r') as fh :
        di = json.load(fh)
        try :
            return di[symbol]
        except KeyError:
            print("Given symbol doesn't exist. Please check and enter the correct symbol\nIn case the symbol is correct then run the allsymbol_to_url.py script to update the list of symbols\nIf the error still occurs then please report the issue on Github page with the symbol")
            quit()


class comp :

    base_url = 'https://www.moneycontrol.com/india/stockpricequote/'

    #all the methods below call methods below upto #####...#####, they create attributes(sp(soupobject),url,about,basic(dictionary))


    def __init__(self,symbol) :  # initialise the instance with symbol, chage: initialisation with company name
        self.url = comp.base_url+convert_symbol_to_url(symbol)
        self.spobj()          #call method to create soup object

    def spobj(self) :
        rs = requests.get(self.url)

        #rs = open('temp.html','r').read()  # reading html from a file to avoid wasting time change line 15,19 later

        self.sp = BeautifulSoup(rs.content,'lxml')  #soup object is stored in sp attribute
        self.updt()      # to store about & basic-stuff in attributes

    def updt(self) :
        self.up_about() # to update company about
        self.basic_details() # to update basic details like pe,price in a dictionary


    def up_about(self) :    #about the company
        self.about = self.sp.find('div',{'class':'com_overviewcnt'}).text


    def  basic_details(self) :


         #create a dictionary with these keys
         #key_list contains all the ids of info dictionary
        key_list = ['open','previousClose','volume','valueInLakhs','VWAP','beta',
        'todaysHigh','todaysLow','upperCircuitLimit','lowerCircuitLimit','52weekHigh','52weekLow',
        'pe','eps','sectorPE','bookValuePerShare','pb','faceValue','marketCap','dividendYield',
        '20dayAvgVolume','20dayAvgDelivery%']

        self.info = dict.fromkeys(key_list)

        counter = 0  #just variable like i to update the dictionary by keepin track of ids

         #the overview data is stored in multiple classes
        ovtablelist = self.sp.find('div',{'id':'stk_overview'}).find_all('div',{'class':'oview_table'})
        for i in range(4) :

            li = ovtablelist[i].find_all('td')
            for a in range(len(li)) :   #runs through all the table data <td> elements
                if a&1 == 0 :
                    continue

                #beta value returns string with 2 decimal hence it gives error,it is
                # being stored as string only
                try :
                    self.info[key_list[counter]] = float(li[a].text.replace(',',''))  #replace to remove all ',' in numbers
                except :                                                              # so they can be converted to float
                    self.info[key_list[counter]] =li[a].text.replace(',','')

                counter +=1


    #### ............................................................####

    #def print_html(self) :
    #    return self.sp.find_all('table')



#cs = comp('RI')
#print(cs.about)
#print(cs.info)
