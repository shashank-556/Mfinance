# Moneycontrol Data Scraper

*The project is still in development phase*

A python module that helps you retrieve financial data of public Indian companies listed on the National Stock Exchange and the Bombay Stock Exchange from the popular website [Moneycontrol](https://www.moneycontrol.com/)</br>
*This is not an official Moneycontrol python library or api*

Currently you can retrieve following data
1. Small summary about the business of the company
2. Basic data about the company like Share Price, Market Cap, PE etc.
___
### Quick Start
Clone this repo and write your own scripts in your local repo

```python
import mcontrol as mc


#the comp module
#the comp module currently accepts url as argument but soon it will be changed to company name
ril = mc.comp('https://www.moneycontrol.com/india/stockpricequote/refineries/relianceindustries/RI')

# about the company
print(ril.about)

# a dictionary listing basic details like closing price, market cap, pe etc
print(ril.info)
```
___

### Requirements
requests</br>
beautifulsoup4
