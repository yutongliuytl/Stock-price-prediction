import datetime as dt
import pandas_datareader.data as web
import os
import csv

file = open('stock_list.txt', 'r', encoding='utf-8-sig')
# the file should only have one line with all tickers
for line in file:
    # SHOULD only iterate once, splits all the tickers into a list to iterate through.
    data = [n for n in line.split(',')]

folder_name = 'stocks_data'
start = dt.datetime(2000, 1, 1)
end = dt.datetime.now()
for ticker in data:
    # If the file doesn't exist, create the file with the initial start date of 2000
    if not os.path.exists('{}/{}.csv'.format(folder_name, ticker)):
        df = web.DataReader(ticker, 'yahoo', start, end)
        df.to_csv('{}/{}.csv'.format(folder_name, ticker))
    else:
        # If the file already exists, check to see if the file needs to be updated.
        with open('{}/{}.csv'.format(folder_name,ticker), 'r') as csvFile:
            reader = csv.reader(csvFile)
            file = [row for row in reader]
            last_date = file[-1][0].split('-')
            last_date = dt.datetime(int(last_date[0]), int(last_date[1]), int(last_date[2]))
            # Compares the last date in the CSV with the current day
            if end.date() != last_date.date():
                # If the dates are different, move back the last_date to make the call by one day.
                # This is to ensure that we have correct information when making the call.
                last_date -= dt.timedelta(days=1)
                # If the dates are different, grab the data frame starting from the last date in csv
                df = web.DataReader(ticker, 'yahoo', last_date.date(), end.date())
                # Convert data frame into a list of strings.
                to_csv = df.to_csv(header=None).split('\r\n')[1:-1]
                # This section removes the last row in the existing csv and replaces it with the first row from the df.
                # This is to overwrite the old value, in case the value was taken before the closing time of that day.
                file[len(file) - 1] = to_csv[0].split(',')
                # After that, we iterate over the new values, starting from the 1st index.
                for line in to_csv[1:]:
                    file.append(line.split(','))
                with open('{}/{}.csv'.format(folder_name, ticker), 'w', newline='') as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerows(file)
        csvFile.close()
        writeFile.close()
        print('Updated {}'.format(ticker))


