import sys
import fileinput
import json
import concurrent.futures

def main():
	"""Takes a text file and converts it to a JSON file that can be read by the program
	File format is a newline-seperated list of company names and e-mail adresses like this:
	```
	Company Name 1
	e-mail@company1.com
	Company Name 2
	e-mail@company2.com
	Company Name 3
	e-mail@company3.com
	```
	"""
	try:
		chars = []
		for char in fileinput.input():
			chars.append(char)
		lines = ''.join(chars).split('\n')
		companies = []
		with concurrent.futures.ProcessPoolExecutor() as executor:
			for i in range(0, len(lines), 2):
				companies.append({
					'name': lines[i].strip(),
					'email': lines[i+1].strip()
				})
	except:
		raise ValueError("Invalid input file")

	json.dump(companies, sys.stdout, indent="\t")