def mnv2_dv():


    print("""
    
    ## Data Visualization
import matplotlib.pyplot as plt
import numpy as np


data = next(dataset_train.create_dict_iterator())
images = data["image"]
labels = data["label"]

# class_name corresponds to label. Labels are marked in ascending order of the folder character string.
class_name = {0:'daisy',1:'dandelion',2:'roses',3:'sunflowers',4:'tulips'}

plt.figure(figsize=(15, 7))
for i in range(len(labels)):
	#Obtain an image and its label.
	data_image = images[i].asnumpy()
	data_label = labels[i]
	
	# Process images for display.
	data_image = np.transpose(data_image, (1, 2, 0))
	mean = np.array([0.485, 0.456, 0.406])
	std = np.array([0.229, 0.224, 0.225])
	data_image = std * data_image + mean
	data_image = np.clip(data_image, 0, 1)
	# Display the image.
	plt.subplot(3, 6, i + 1)
	plt.imshow(data_image)
	plt.title(class_name[int(labels[i].asnumpy())])
	plt.axis("off")
	plt.show()
    
    """)