import csv 
with open("guests.csv", 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                print (row)