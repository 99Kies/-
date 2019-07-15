import csv

with open('movies.csv','r',encoding='gbk') as csvfile:
    reader = csv.reader(csvfile)
    print(type(reader))
    print(reader)
    for row in reader:
        print(row)