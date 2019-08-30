import datetime as dt
import pandas_datareader.data as web
import os
import csv

file = open('stock_list.txt', 'r', encoding='utf-8-sig')
# the file should only have one line with all tickers
for line in file:
    # SHOULD only iterate once.
    data = [n for n in line.split(',')]

folder_name = 'stocks_data'
for ticker in data:
    # just in case your connection breaks, we'd like to save our progress!
    if not os.path.exists('{}/{}.csv'.format(folder_name, ticker)):
        start = dt.datetime(2000, 1, 1)
        end = dt.datetime.now()
        df = web.DataReader(ticker, 'yahoo', start, end)
        df.to_csv('{}/{}.csv'.format(folder_name, ticker))
    else:
        # todo: update the ticker here
        print('Already have {}'.format(ticker))