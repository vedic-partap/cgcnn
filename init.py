from main import main
import math

TOTAL_SIZE = 10
DISABLE_CUDA = False
FILEPATH = 'data/sample-regression/'
train_size = math.floor(0.6 * TOTAL_SIZE)
val_size = math.floor(0.2 * TOTAL_SIZE)
test_size = TOTAL_SIZE - train_size - val_size


def init(data_options, task='regression', disable_cuda=True, workers=0, epochs=30,
				start_epoch=0, batch_size=256, lr=0.01, lr_milestones=[100], momentum=0.9,
				weight_decay=0.0, print_freq=10, resume='', train_size=None, val_size=1000,
				test_size=1000, optimizer='SGD', atom_fea_len=64, h_fea_len=128, n_conv=3, n_h=1):
	return main(data_options, task=task, disable_cuda=disable_cuda, workers=workers, epochs=epochs,
			start_epoch=start_epoch, batch_size=batch_size, lr=lr, lr_milestones=lr_milestones,
			momentum=momentum, weight_decay=weight_decay, print_freq=print_freq, resume=resume,
			train_size=train_size, val_size=val_size, test_size=test_size, optimizer=optimizer,
			atom_fea_len=atom_fea_len, h_fea_len=h_fea_len, n_conv=n_conv, n_h=n_h,
			print_checkpoints=True, save_checkpoints=True)


if __name__ == '__main__':
	# Set the tuned params here
	# conv_layer = 2
	conv_layer = 1
	step = math.exp(-5)
	decay = math.exp(-6)

	error = init(FILEPATH, disable_cuda=DISABLE_CUDA, train_size=train_size,
					val_size=val_size, test_size=test_size, optimizer='Adam', n_conv=conv_layer,
					lr=step, weight_decay=decay)

	# For testing purposes: atom_fea_len=4, h_fea_len=16, batch_size=32, epochs=5