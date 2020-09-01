import os
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Back, Style
import time
from datetime import date
from datetime import datetime
from datetime import timedelta


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
'start':'1',
'limit':'100',
'convert': 'BRL'
}
headers = {
'Accepts': 'application/json',
'X-CMC_PRO_API_KEY': '99e767ce-a99e-4fdf-be6c-94d6aedf7752',
}

session = Session()
session.headers.update(headers)

print()
print('MY PORTFOLIO')
print()

portfolio_value = 0.00
last_updated = 0

table = PrettyTable(['Asset', 'Amount Owned', 'BRL Value', 'Price', '1h', '24h', '7d'])

portifolio = ['Bitcoin']
grana = [1]
x = 0
try:
    response = session.get(url, params=parameters)
    data  = json.loads(response.text)
    currencys = data['data']
    for currency in currencys:
        name = currency['name']
        if(name in portifolio):

            rank = currency['cmc_rank']
            name = currency['name']
            last_updated = currency['last_updated']
            symbol = currency['symbol']
            quotes = currency['quote']['BRL']
            hour_change = quotes['percent_change_1h']
            day_change = quotes['percent_change_24h']
            week_change = quotes['percent_change_7d']
            price = quotes['price']

            value = float(price) * float(grana[x])

            if hour_change > 0:
                hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
            else:
                hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

            if day_change > 0:
                day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
            else:
                day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

            if week_change > 0:
                week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
            else:
                week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

            portfolio_value += value

            value_string = '{:,}'.format(round(value,2))

            table.add_row([name + ' (' + symbol + ')',
                            grana[x],
                            '$' + value_string,
                            '$' + str(price),
                            str(hour_change),
                            str(day_change),
                            str(week_change)])
            x = x + 1

    

    print(table)
    print()

    portfolio_value_string = '{:,}'.format(round(portfolio_value,2))
    last_updated_string = datetime.fromtimestamp(last_updated).strftime('%Y/%m/%d/%H/%M%')

    print('Total Portfolio Value: ' + Back.GREEN + '$' + portfolio_value_string + Style.RESET_ALL)
    print()
    print('API Results Last Updated on ' + last_updated_string)
    print()

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)