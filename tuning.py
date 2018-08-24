from main import main
import math, json

TOTAL_SIZE = 10
DISABLE_CUDA = False
FILEPATH = 'data/sample-regression/'
train_size = math.floor(0.6 * TOTAL_SIZE)
val_size = math.floor(0.2 * TOTAL_SIZE)
test_size = TOTAL_SIZE - train_size - val_size

def tune(data_options, task='regression', disable_cuda=True, workers=0, epochs=30,
				start_epoch=0, batch_size=256, lr=0.01, lr_milestones=[100], momentum=0.9,
				weight_decay=0.0, print_freq=10, resume='', train_size=None, val_size=1000,
				test_size=1000, optimizer='SGD', atom_fea_len=64, h_fea_len=128, n_conv=3, n_h=1):
	return main(data_options, task=task, disable_cuda=disable_cuda, workers=workers, epochs=epochs,
			start_epoch=start_epoch, batch_size=batch_size, lr=lr, lr_milestones=lr_milestones,
			momentum=momentum, weight_decay=weight_decay, print_freq=print_freq, resume=resume,
			train_size=train_size, val_size=val_size, test_size=test_size, optimizer=optimizer,
			atom_fea_len=atom_fea_len, h_fea_len=h_fea_len, n_conv=n_conv, n_h=n_h,
			print_checkpoints=False, save_checkpoints=False)


if __name__ == '__main__':
	
	hyperparams = {
		'n_conv': range(1,6),
		'weight_decay': [math.exp(-6), math.exp(-4), math.exp(-2), math.exp(0)], 
		'adam_step': [math.exp(-8), math.exp(-7), math.exp(-6), math.exp(-5), math.exp(-4), math.exp(-3)],
	}

	results = []
	best_mae = 1e10
	best_params = {}
	for conv_layer in hyperparams['n_conv']:
		for step in hyperparams['adam_step']:
			for decay in hyperparams['weight_decay']:
				print('testing for conv_layer ', conv_layer, ' step ', step, ' decay: ', decay)
				error = tune(FILEPATH, disable_cuda=DISABLE_CUDA, train_size=train_size,
								val_size=val_size, test_size=test_size, optimizer='Adam', n_conv=conv_layer,
								lr=step, weight_decay=decay)
				params = {'n_conv': conv_layer, 'adam_step': step, 'weight_decay': decay, 'mae': error}
				if error < best_mae:
					best_mae = error
					best_params = params
				results.append(params)

	print(json.dumps(results, sort_keys=True, indent=4, separators=(',', ': ')))
	print('The best parameters are:')
	print(json.dumps(best_params, sort_keys=True, indent=4, separators=(',', ': ')))