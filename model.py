import csv

with open('training_set.csv') as file: 
	training_set = csv.DictReader(file)
	for row in training_set:
		print(row)
		break

