def mnv2_dp():


    print("""
    
    ## Libraries
import mindspore.dataset as ds
import mindspore.dataset.vision.c_transforms as CV
from mindspore import dtype as mstype


### Dataset Preparation
train_data_path = 'flower_photos_train'
val_data_path = 'flower_photos_test'

def create_dataset(data_path, batch_size=18, training=True):
	###Define the dataset.###
	data_set = ds.ImageFolderDataset(data_path, num_parallel_workers=8, shuffle=True,
	class_indexing={'daisy': 0, 'dandelion': 1, 'roses': 2, 'sunflowers': 3, 'tulips': 4})
 	# Perform image enhancement on the dataset.
 	image_size = 224
 	mean = [0.485 * 255, 0.456 * 255, 0.406 * 255]
 	std = [0.229 * 255, 0.224 * 255, 0.225 * 255]
 	if training:
 		trans = [
 			CV.RandomCropDecodeResize(image_size, scale=(0.08, 1.0), ratio=(0.75, 1.333)),
 			CV.RandomHorizontalFlip(prob=0.5),
 			CV.Normalize(mean=mean, std=std),
 			CV.HWC2CHW()
 			]
	else:
 		trans = [
 		CV.Decode(),
 		CV.Resize(256), CV.CenterCrop(image_size), CV.HWC2CHW()]
 

	# Perform the data map, batch, and repeat operations.
 	data_set = data_set.map(operations=trans, input_columns="image", num_parallel_workers=8)
 	
 	data_set = data_set.batch(batch_size, drop_remainder=True)
 	
	return data_set


dataset_train = create_dataset(train_data_path)
dataset_val = create_dataset(val_data_path)

    
    """)