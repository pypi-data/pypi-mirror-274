def mv2_train():

    print("""
    
    ## Mindspore
import mindspore
import mindspore.nn as nn
from mindspore.train import Model
from mindspore import Tensor, save_checkpoint
from mindspore.train.callback import ModelCheckpoint, CheckpointConfig, LossMonitor
from mindspore.train.serialization import load_checkpoint, load_param_into_net

# Create a model. The number of target classes is 5.
network = mobilenet_v2(5)

# Load the pre-trained weight.
param_dict = load_checkpoint("./mobilenetv2_ascend_v170_imagenet2012_official_cv_top1acc71.88.ckpt")

# Modify the weight data based on the modified model structure.
param_dict["dense.weight"] = mindspore.Parameter(Tensor(param_dict["dense.weight"][:5, :],mindspore.float32), name="dense.weight",requires_grad=True)
param_dict["dense.bias"] = mindspore.Parameter(Tensor(param_dict["dense.bias"][:5, ],mindspore.float32),name="dense.bias", requires_grad=True)

# Load the modified weight parameters to the model.
load_param_into_net(network, param_dict)
train_step_size = dataset_train.get_dataset_size()
epoch_size = 20
lr = nn.cosine_decay_lr(min_lr=0.0, max_lr=0.1,total_step=epoch_size * train_step_size,step_per_epoch=train_step_size,decay_epoch=200)

# Define the optimizer.
network_opt = nn.Momentum(params=network.trainable_params(), learning_rate=0.01, momentum=0.9)
# Define the loss function.
network_loss = loss = nn.SoftmaxCrossEntropyWithLogits(sparse=True, reduction="mean")
# Define evaluation metrics.
metrics = {"Accuracy": nn.Accuracy()}
# Initialize the model.
model = Model(network, loss_fn=network_loss, optimizer=network_opt, metrics=metrics)

# Monitor the loss value.
loss_cb = LossMonitor(per_print_times=train_step_size)
# Set the number of steps for saving a model and the maximum number of models that can be saved.
ckpt_config = CheckpointConfig(save_checkpoint_steps=100, keep_checkpoint_max=10)
# Save the model. Set the name, path, and parameters for saving the model.
ckpoint_cb = ModelCheckpoint(prefix="mobilenet_v2", directory='./ckpt', config=ckpt_config)

print("============== Starting Training ==============")
# Train a model, set the number of training times to 5, and set the training set and callback function.
model.train(5, dataset_train, callbacks=[loss_cb,ckpoint_cb], dataset_sink_mode=True)
# Use the test set to validate the model and output the accuracy of the test set.
metric = model.eval(dataset_val)
print(metric)




import matplotlib.pyplot as plt
import mindspore as ms
def visualize_model(best_ckpt_path, val_ds):
	num_class = 5 # Perform binary classification on wolf and dog images.
	net = mobilenet_v2(num_class)
	# Load model parameters.
	param_dict = ms.load_checkpoint(best_ckpt_path)
	ms.load_param_into_net(net, param_dict)
	model = ms.Model(net)
	# Load the validation dataset.
	data = next(val_ds.create_dict_iterator())
	images = data["image"].asnumpy()
	labels = data["label"].asnumpy()
	class_name = {0:'daisy',1:'dandelion',2:'roses',3:'sunflowers',4:'tulips'}
	# Predict the image type.
	output = model.predict(ms.Tensor(data['image']))
	pred = np.argmax(output.asnumpy(), axis=1)
	# Display the image and the predicted value of the image.
	plt.figure(figsize=(15, 7))
	for i in range(len(labels)):
		plt.subplot(3, 6, i + 1)
 		# If the prediction is correct, it is displayed in blue. If the prediction is incorrect, it is displayed in red.
 		color = 'blue' if pred[i] == labels[i] else 'red'
 		plt.title('predict:{}'.format(class_name[pred[i]]), color=color)
		picture_show = np.transpose(images[i], (1, 2, 0))
		mean = np.array([0.485, 0.456, 0.406])
		std = np.array([0.229, 0.224, 0.225])
		picture_show = std * picture_show + mean
		picture_show = np.clip(picture_show, 0, 1)
		plt.imshow(picture_show)
		plt.axis('off')	
		plt.show()

visualize_model('ckpt/mobilenet_v2-5_201.ckpt', dataset_val) 
    
    """)