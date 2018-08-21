import json
from pymatgen import MPRester
from ase.io import read
from ase.db import connect

database = 'data_cmr/cubic_perovskites.db'
API_KEY = "Ll5wvb1s4FcrB78V"

db = connect(database)
max_data_to_pick = len(db) - 470
counter = 1000
while counter < 2000:
	print(counter)
	row = read('data_cmr/cubic_perovskites.db@' + str(counter))
	chemical_formula = row[0].get_chemical_formula()
	print(chemical_formula)
	calc = row[0].get_calculator()
	print(calc.results['energy'])

	with MPRester(API_KEY) as m:
		query = {"full_formula": chemical_formula}
		dataset = m.query(query, ["material_id", "pretty_formula"])
		print(json.dumps(dataset, sort_keys=True, indent=4, separators=(',', ': ')))
	counter += 1