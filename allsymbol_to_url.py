
# This script will update the symbol to url dictionary i.e. the symbolurl.json file, run this in
# case you find new companies,etf etc whose data you are unable to retrieve through the mcontrol module

import requests
from bs4 import BeautifulSoup   #lxml and soup for parsing the pages
import lxml
import json    #json to store the dictionary


# the url where moneycontrol lists its all the entities and this will also be used in mcontrol as base url
base_url = 'https://www.moneycontrol.com/india/stockpricequote/'


symburl = dict()  #dictionary to store all data

#to run through all pages containing entities whose name start with all character a--z(26) + whose name starts
# with a character others total = 27 page

for i in range(27) :

    if i == 0:      # others is for symbols whose name does't start with a character
        startchar = 'others'
        print('Updating companies, etf, indices etc. whose name starts with a number ...')
    else :
        startchar = chr(64 + i)
        print('Updating companies, etf, indices etc. whose name starts with',startchar,'...')


    rs = requests.get(base_url+startchar)   #add startchar to complete the url like
    sp = BeautifulSoup(rs.content,'lxml')   #https://www.moneycontrol.com/india/stockpricequote/F

    ob = sp.find('table',{'class':'pcq_tbl'}).find_all('td') #the data is stored in html table

    for a in ob :
        if a.text == '' :   #few td elements are empty so ignore them
            continue
        #spliting by / to get last part of url
        # removing base_url in every url to save storage data as it is redundant
        symburl[a.a.get('href').split('/')[-1]] = a.a.get('href').replace(base_url,'')

print(len(symburl),'symbols found!')
#print(symburl)


# store symburl dictionary in a json file
json_obj = json.dumps(symburl)
with open("symbolurl.json", "w") as outfile:
    outfile.write(json_obj)

print('All the symbols have been successfully updated')
