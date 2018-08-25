# import json
import csv
from ase.io import write
from ase.db import connect

filepath = '../../data/cgcnn/data_perovskites/'
database = filepath + 'cubic_perovskites.db'
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
skipped_count = 0
idprop_list = []
for row in db.select('unique_id>0'):
	if counter < 10000:
		idprop_list.append([counter, row.energy])
		atoms = row.toatoms()
		filename = filepath + str(counter) + '.cif'
		write(filename, atoms)
		print('Written ', counter, '.cif')
		counter += 1

# Write id_prop.csv
with open(filepath + '/id_prop.csv', 'w') as file:
	writer = csv.writer(file)
	writer.writerows(idprop_list)
print("Written id_prop.csv")

# row = read('data_cmr/cubic_perovskites.db@' + str(counter))
# chemical_formula = row[0].get_chemical_formula()
# print(chemical_formula)
# calc = row[0].get_calculator()
# print(calc.results['energy'])