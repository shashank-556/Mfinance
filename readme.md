# Moneycontrol Data Scraper


A python module that allows you to access the financial data of public Indian companies listed on the National Stock Exchange and the Bombay Stock Exchange from the popular website [Moneycontrol](https://www.moneycontrol.com/) in a pythonic way.</br>
*This is not an official Moneycontrol python library or api*

Currently you can retrieve following data
1. Small summary about the business of the company
2. Basic data about the company like Share Price, Market Cap, PE etc.
3. Latest share price
4. Basic info about the peers of the company
5. Financial ratios and per share data of the company
6. Latest shareholding pattern
___
### Quick Start
Clone this repo and write your own scripts in your local repo
###### comp
The comp is the main class of mc module. Data of any entity can be retrieved using this class.</br>
The comp class accepts one argument. The *symbol* of the company, etf etc. The symbol of any entity can be found in its url on moneycontrol.<br><br>
<br>Symbol of Reliance Industries Ltd. is RI
![Symbol of Reliance](image/relurl.png)
Symbol of Asian Paints is AP31
![Symbol of Asian Paints](image/aiurl.png)

<br>

```python
import mcontrol as mc


#the comp module will return all the data about the company
#the comp module accepts the company symbol as argument

ril = mc.comp('RI')

# about the company
print(ril.about)

# a dictionary listing basic details like closing price, market cap, pe etc
print(ril.info)

# to get the latest price
print(ril.latestPrice)

# returns a list of dictionary containing info about the peers of the company
print(ril.peers())

# to get the peers result as pandas dataframe
print(ril.peers(dframe=True))
# or
print(ril.peers(True)) 

# returns a dictionary with basic per share data like eps, bvps and financial ratios
print(ril.pershare())

# returns a dictionary with latest shareholding data
print(ril.latestShareholding())

# url of the company on moneycontrol
print(ril.url)
```

___

### Requirements
lxml</br>
beautifulsoup4
