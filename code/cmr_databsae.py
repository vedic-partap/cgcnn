# import json
from ase.io import read
from ase.db import connect

database = '../../data/cgcnn/data_perovskites/cubic_perovskites.db'

db = connect(database)
# for row in db.select(combination='ABO3'):
# 	if 'Pb' in row.formula and 'Mn' in row.formula:
# 		print(row)
# 		print(row.heat_of_formation_all)
# 		print(row.combination)
# 		formula = row.A_ion + row.B_ion + row.anion
# 		print(formula)
max_data_to_pick = len(db) - 470
counter = 0
combination_dict = {}
skipped_count = 0
for row in db.select('unique_id>0'):
	print(row)
	if counter % 1000 == 0:
		print(counter)
	counter += 1
	if counter > 10:
		break
	# row = read('data_cmr/cubic_perovskites.db@' + str(counter))
	# chemical_formula = row[0].get_chemical_formula()
	# print(chemical_formula)
	# calc = row[0].get_calculator()
	# print(calc.results['energy'])