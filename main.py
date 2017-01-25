import csv
f = open('data/nyse_list.csv', 'rb')
reader = csv.reader(f)
for row in reader:
    print row[0]
f.close()