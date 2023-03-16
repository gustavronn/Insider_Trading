import requests
from bs4 import BeautifulSoup as bs
#import numpy as np

def get_soup(company_name = str, page = str, from_date = ''):

    parameters = {'Transaktionsdatum.From': from_date ,'Utgivare': company_name,'Page': page}
    #Utgivare = Filo + Mining &
    URL = "https://marknadssok.fi.se/Publiceringsklient/sv-SE/Search/Search?SearchFunctionType=Insyn&PersonILedandeSt%C3%A4llningNamn=&Transaktionsdatum.From=&Transaktionsdatum.To=&Publiceringsdatum.From=&Publiceringsdatum.To=&button=search&"
    page = requests.get(URL, params=parameters)

    soup = bs(page.content, "html.parser")
    return soup
#results = soup.find(id="grid-list")
#transaction_table = results.find_all("table", class_="table table-bordered table-hover table-striped zero-margin-top")
#print(transactions)
#headers = soup.tr
#header_list = headers.find_all("th")
#print(header_list)
#for h in header_list:
#    pass
    #print(h.text)
def get_transactions(soup):
    transactions = soup.find_all("tr")
    transaction_table=[]
    transactions.pop(0)
    period_balance = 0
    for t in transactions:
        transaction_info = t.find_all("td")
    #print(transaction_info)
        status = transaction_info[14]
        status = status.text
        #print(status)
        if status == 'Reviderad':
            continue
        kind = transaction_info[5]
        kind = kind.text

        volume = transaction_info[10]
        volume = volume.text
        volume = volume.replace("\xa0","")
        #volume.replace("\xa0","")
        price = transaction_info[12]
        price = price.text
        price = price.replace(",",".")
        #print(kind,price, volume)
        if kind == 'Förvärv' or kind == 'Tilldelning' or kind == 'Lösen ökning':
            cost = int(volume)*float(price)
        elif kind == 'Avyttring' or kind == 'Utbyte minskning' or kind == 'Lösen minskning':
            cost = -int(volume) * float(price)
        #print(kind, volume, price, cost)
        transaction_table.append([kind, volume, price, cost])
        period_balance +=cost
    return transaction_table, period_balance
#print(transaction_table)
#transaction_array = np.array(transaction_table)
#print(transaction_array)

def get_all_pages(company_name, pages,from_date):
    transactions = []
    period_balance = 0
    for page in pages:
        soup = get_soup(company_name,page, from_date=from_date)
        transactions_per_page, period_balance_per_page = get_transactions(soup)
        if len(transactions_per_page) == 0:
            continue
        for transaction in transactions_per_page:
            transactions.append(transaction)
        period_balance += period_balance_per_page
    #print(transactions, period_balance)
    return transactions

company_name = 'Lundin + Mining + Corporation'
pages = ['1','2','3','4']
from_date = '2021-11-15'
transactions = get_all_pages(company_name,pages,from_date)
for transaction in transactions:
    print(transaction)
