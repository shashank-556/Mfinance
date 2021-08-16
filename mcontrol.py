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
        #call method to create soup object
        rs = requests.get(self.url)

        #rs = open('temp.html','r').read()  # reading html from a file to avoid wasting time change line 15,19 later
        self.sp = BeautifulSoup(rs.content,'lxml')  #soup object is stored in sp attribute

        # scrape latest price
        self.latestPrice = float(self.sp.find(id = 'nsecp').text.replace(',',''))


        #about the company
        self.about = self.sp.find('div',{'class':'com_overviewcnt'}).text.strip()

        # to update basic details like pe,price in a dictionary
        # create a dictionary with these keys
        # key_list contains all the ids of info dictionary
        key_list = ['open','previousClose','volume','valueInLakhs','VWAP','beta',
        'high','low','upperCircuitLimit','lowerCircuitLimit','52weekHigh','52weekLow','eps',
        'pe','sectorPE','bvps','pb','faceValue','marketCap','dividendYield',
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

        # peer data is stored in a table
        self.__peer = self.sp.find('div',{'id':'peers'}).table.find_all('tr')

    # returns all about the peers in a list of dictionaries
    def peers(self) :

        #temp = self.sp.find('div',{'id':'peers'}).table.find_all('tr')
        # the final list
        peers_list = []
        #list to initialise the dictionary
        temp_list = ['name','symbol','price','change%','marketCap','pe','pb','roe%','1yrPerformance%','netProfit','netSales','debtToEquity']
        # dictionary to store data of single company with its keys as temp_list
        temp_dict = dict.fromkeys(temp_list)
        # to parse the temp object 0 index contains table headings 1 index is about the current company
        # so ignore 0 and 1 index
        for itm in range(2,len(self.__peer)) :
            # a dumb counter to keep track of temp_list indices
            cntr = 0
            for a in self.__peer[itm] :
                # use .string to convert bs4string to string
                # some string are empty ignore them
                if a.string.strip() == '' :
                    continue
                # to convert numbers to float
                try :
                    temp_dict[temp_list[cntr]] = float(a.string.strip().replace(',',''))
                except :
                    temp_dict[temp_list[cntr]] = a.string.strip()

                # symbol is not part of html table to insert it on your own after name
                if cntr == 0 :
                    cntr+=1
                    temp_dict[temp_list[cntr]] = a.a.get('href').split('/')[-1]

                cntr+=1

            # use dict.copy() to as only dict insert the same dictionary for all indices
            peers_list.append(temp_dict.copy())

        return peers_list

    # returns a dictionary of pershare values and ratios
    def pershare(self) :

        temp_list = ['eps','bvps','pe','sectorPE','pb','debtToEquity','roe%','faceValue','dividendYield']

        temp_dict = dict.fromkeys(temp_list)

        temp_dict['eps'] = self.info['eps']
        temp_dict['bvps'] = self.info['bvps']
        temp_dict['pe'] = self.info['pe']
        temp_dict['sectorPE'] = self.info['sectorPE']
        temp_dict['pb'] = self.info['pb']
        temp_dict['faceValue'] = self.info['faceValue']
        temp_dict['dividendYield'] = self.info['dividendYield']

        #debt to equity and roe are in the peers section
        try :
            temp_dict['debtToEquity'] = float(self.__peer[1].find_all('td')[10].string)
        except :
            temp_dict['debtToEquity'] = self.__peer[1].find_all('td')[10].string

        try :
            temp_dict['roe%'] = float(self.__peer[1].find_all('td')[6].string)
        except :
            temp_dict['roe%'] = self.__peer[1].find_all('td')[6].string

        return temp_dict



if __name__ == '__main__':
    import sys
    a = sys.argv[1]
    c = comp(a)
    print(c.info)
    print(c.about)
    print(c.latestPrice)
    print(c.peers())
    print(c.pershare())
