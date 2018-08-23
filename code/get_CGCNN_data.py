# import json
# import os
import csv, math
from pymatgen import MPRester
# from pymatgen.core.structure import Structure

# Initializations
API_KEY = "Ll5wvb1s4FcrB78V"
material_hash_counter = 0		# Unique ID used for storing data
filepath = "../../data/cgcnn/data_mp_full/"
write_to_file = True
# if not os.path.exists(filepath):
# 	os.makedirs(filepath)
materials_id_list = []		# list of ids to fetch data for
with open(filepath + 'mpids_100.csv', 'r') as csv_file:
	csv_reader = csv.reader(csv_file)
	for row in csv_reader:
		materials_id_list.append(str(row[0]))
# print(matecrials_id_list)

with MPRester(API_KEY) as m:
	# data = m.get_data("Fe2O3", data_type="vasp", prop="formation_energy_per_atom")
	print("Querying Materials Project Database...")
	query = {"material_id": {"$in": materials_id_list}}
	# query0 = "Li-O-*"
	# query1 = {"elements":{"$in":["Li", "Na", "K"], "$all": ["O"]}, "nelements":2}
	# query2 = {"elements":{"$in":["Li", "Na", "K"]}, "nelements":2}
	# query3 = {"formula_anonymous": {"$in":["A", "A2", "A3", "AB", "AB2", "AB3", "AB4", "ABC", "ABC2", "ABC3", "ABC4"]}}
	dataset = m.query(query, ["material_id", "formation_energy_per_atom", "cif"])
	print("Done Querying. Fetched " + str(len(dataset)) + " data")
	print("Processing dataset...")
	# print(json.dumps(dataset, sort_keys=True, indent=4, separators=(',', ': ')))
	material_id_hash_list = []
	idprop_list = []
	cif_list = []
	for row in dataset:
		material_id, formation_energy_per_atom, cif = [row["material_id"], row["formation_energy_per_atom"], row["cif"]]
		idprop_list.append([material_hash_counter, formation_energy_per_atom])
		material_id_hash_list.append([material_hash_counter, material_id])
		cif_list.append([material_hash_counter, cif])
		material_hash_counter += 1
	print("Finished processing dataset!")

if write_to_file:
	# Write id_prop.csv
	with open(filepath + '/id_prop.csv', 'w') as file:
		writer = csv.writer(file)
		writer.writerows(idprop_list)
	print("Written id_prop.csv")

	# Write the cif files
	for row in cif_list:
		unique_id, cif = row
		with open(filepath + '/' + str(unique_id) + '.cif', 'w') as file:
			file.write(cif)
		print("Written " + str(unique_id) + ".csf")

	# Write materials id hash map: This contains the Unique ID and the material_id (as obtained from original dataset)
	with open(filepath + '/material_id_hash.csv', 'w') as file:
		writer = csv.writer(file)
		writer.writerows(material_id_hash_list)
	print("Written material_id_hash.csv")

	# Generate the command to execute for model training
	total_dataset = len(dataset)
	train_data_count = math.floor(0.6 * total_dataset)
	validation_data_count = math.floor(0.2 * total_dataset)
	test_data_count = total_dataset - train_data_count - validation_data_count
	print("python main.py --train-size "+str(train_data_count)+" --val-size "+str(validation_data_count)+" --test-size "+str(test_data_count)+" ../data/cgcnn/data_mp_full/ge")

# # Read the CIF and create the structure
# crystal = Structure.from_file('data/0.cif')
# print(crystal)


