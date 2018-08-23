from main import main
import math, json

def init(data_options, task='regression', disable_cuda=True, workers=0, epochs=30,
				start_epoch=0, batch_size=256, lr=0.01, lr_milestones=[100], momentum=0.9,
				weight_decay=0.0, print_freq=10, resume='', train_size=None, val_size=1000,
				test_size=1000, optimizer='SGD', atom_fea_len=64, h_fea_len=128, n_conv=3, n_h=1):
	return main(data_options, task=task, disable_cuda=disable_cuda, workers=workers, epochs=epochs,
			start_epoch=start_epoch, batch_size=batch_size, lr=lr, lr_milestones=lr_milestones,
			momentum=momentum, weight_decay=weight_decay, print_freq=print_freq, resume=resume,
			train_size=train_size, val_size=val_size, test_size=test_size, optimizer=optimizer,
			atom_fea_len=atom_fea_len, h_fea_len=h_fea_len, n_conv=n_conv, n_h=n_h)


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
				error = init('data/sample-regression/', train_size=6, val_size=2, test_size=2, optimizer='Adam',
								n_conv=conv_layer, lr=step, weight_decay=decay)
				params = {'n_conv': conv_layer, 'adam_step': step, 'weight_decay': decay, 'mae': error}
				if error < best_mae:
					best_mae = error
					best_params = params
				results.append(params)

	print(json.dumps(results, sort_keys=True, indent=4, separators=(',', ': ')))
	print('The best parameters are:')
	print(json.dumps(best_params, sort_keys=True, indent=4, separators=(',', ': ')))