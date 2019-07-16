import csv

with open('training_set.csv', encoding="ISO 8859-1") as file: 
	training_set = csv.DictReader(file)
	for row in training_set:
		print(row)
		break

