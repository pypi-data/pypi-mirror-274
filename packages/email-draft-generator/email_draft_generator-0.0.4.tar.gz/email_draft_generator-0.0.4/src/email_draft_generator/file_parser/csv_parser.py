import csv
import concurrent.futures

def parse(data):
	"""Takes a CSV file with fields `name,email` and parses it into a list of companies"""
	companies = []
	reader =  csv.DictReader(data, fieldnames=["name", "email"])
	with concurrent.futures.ProcessPoolExecutor() as executor:
		for row in reader:
			companies.append(row)
	return companies