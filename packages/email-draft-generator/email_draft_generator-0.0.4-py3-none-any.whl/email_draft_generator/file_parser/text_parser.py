import concurrent.futures

def parse(data):
	"""Takes a text file and converts it to a list of companies.
Data format is a newline-seperated list of company names and e-mail adresses like this:
```
Company Name 1
e-mail@company1.com
Company Name 2
e-mail@company2.com
Company Name 3
e-mail@company3.com
...
```
"""
	companies = []
	with concurrent.futures.ProcessPoolExecutor() as executor:
		for i in range(0, len(data), 2):
			companies.append({
				'name': data[i].strip(),
				'email': data[i+1].strip()
			})
	return companies