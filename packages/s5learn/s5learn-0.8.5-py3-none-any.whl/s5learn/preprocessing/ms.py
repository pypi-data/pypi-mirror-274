

def ms():

    print("""
    
    ### Dataset Generator
import os
import mindspore.dataset as ds
import matplotlib.pyplot as plt


class DatasetGenerator:
	def __init__(self):
		...
		...
	def __getitem__(self):
		...
		...

		return ...
	def __len__(self):
		return len(...)

dataset_generator = DatasetGenerator()
dataset = ds.GeneratorDataset(dataset_generator, ["data", "label"], shuffle=False)

### LENET5
class LeNet5(nn.Cell):
	
	### Lenet network structure ###
	
	def __init__(self, num_class=10, num_channel=1):
		super(LeNet5, self).__init__()
 		# Define the required operations.
		self.conv1 = nn.Conv2d(num_channel, 6, 5, pad_mode='valid')
 		self.conv2 = nn.Conv2d(6, 16, 5, pad_mode='valid')
 		self.fc1 = nn.Dense(16 * 4 * 4, 120)
 		self.fc2 = nn.Dense(120, 84)
		self.fc3 = nn.Dense(84, num_class)
		self.relu = nn.ReLU()
 		self.max_pool2d = nn.MaxPool2d(kernel_size=2, stride=2)
 		self.flatten = nn.Flatten()
 	def construct(self, x):
 		# Use the defined operations to build a feedforward network.
 		x = self.conv1(x)
 		x = self.relu(x)
 		x = self.max_pool2d(x)
 		x = self.conv2(x)
 		x = self.relu(x)
 		x = self.max_pool2d(x)
 		x = self.flatten(x)
 		x = self.fc1(x)
		x = self.relu(x)
 		x = self.fc2(x)
 		x = self.relu(x)
 		x = self.fc3(x)
 		return x

net = LeNet5()

loss = nn.loss.SoftmaxCrossEntropyWithLogits(sparse=True, reduction='mean')
metrics={"Accuracy": Accuracy()}
opt = nn.Adam(net.trainable_params(), lr) 

# Build a model.
model = Model(net, loss, opt, metrics)

## Callbacks
config_ck = CheckpointConfig(save_checkpoint_steps=1875, keep_checkpoint_max=10)
ckpoint_cb = ModelCheckpoint(prefix="checkpoint_net",directory = "./ckpt" ,config=config_ck)
loss_cb = LossMonitor(per_print_times=1875)
time_cb = TimeMonitor(data_size=ds_train.get_dataset_size())
# Train the model.

print("============== Starting Training ==============")
model.train(num_epoch, ds_train,callbacks=[ckpoint_cb,loss_cb,time_cb ],dataset_sink_mode=False)


    
    """)