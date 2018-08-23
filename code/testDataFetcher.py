import json
from pymatgen import MPRester

API_KEY = "Ll5wvb1s4FcrB78V"
with MPRester(API_KEY) as m:
	print("Querying Materials Project Database...")
	# query0 = "**O3"
	# query1 = {"elements":{"$in":["Li", "Na", "K"], "$all": ["O"]}, "nelements":2}
	# query2 = {"elements":{"$in":["Li", "Na", "K"]}, "nelements":3}
	# query3 = {"formula_anonymous": "ABC3"}
	# query4 = {"formula_anonymous": {"$in":["A", "A2", "A3", "AB", "AB2", "AB3", "AB4", "ABC", "ABC2", "ABC3", "ABC4"]}}
	query5 = "Ni-As-N-O"
	dataset = m.query(query5, ["material_id", "pretty_formula"])
	print(json.dumps(dataset, sort_keys=True, indent=4, separators=(',', ': ')))
	print("Done Querying. Fetched " + str(len(dataset)) + " data")
