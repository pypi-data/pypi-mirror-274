def tn():

    print("""
    
    !wget https://certification-data.obs.cn-north-4.myhuaweicloud.com/ENG/HCIPAI%20EI%20Developer/V2.1/nlpdata.zip


!unzip nlpdata.zip


import re
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score

def clean_str(string):
 	###
 	Tokenization/string cleaning for all datasets except for SST.
 	Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
 	###
 	string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
 	string = re.sub(r"\'s", " \'s", string)
 	string = re.sub(r"\'ve", " \'ve", string)
 	string = re.sub(r"n\'t", " n\'t", string)
 	string = re.sub(r"\'re", " \'re", string)
 	string = re.sub(r"\'d", " \'d", string)
 	string = re.sub(r"\'ll", " \'ll", string)
 	string = re.sub(r",", " , ", string)
 	string = re.sub(r"!", " ! ", string)
 	string = re.sub(r"\(", " \( ", string)
 	string = re.sub(r"\)", " \) ", string)
 	string = re.sub(r"\?", " \? ", string)
 	string = re.sub(r"\s{2,}", " ", string)
 	return string.strip().lower()


def load_data_and_labels(positive_data_file, negative_data_file):
 	###
 	Loads MR polarity data from files, splits the data into words and generates labels.
 	Returns split sentences and labels.
 	###
 	# Load data from files
 	positive_examples = list(open(positive_data_file, "r", encoding='utf-8').readlines())
 	positive_examples = [s.strip() for s in positive_examples]
 	negative_examples = list(open(negative_data_file, "r", encoding='utf-8').readlines())
 	negative_examples = [s.strip() for s in negative_examples]
 	# Split by words
 	x = positive_examples + negative_examples
 	x = [clean_str(sent) for sent in x]
 	x = np.array(x)
 	# Generate labels
 	positive_labels = [1] * len(positive_examples)
 	negative_labels = [0] * len(negative_examples)
 	y = np.concatenate([positive_labels, negative_labels], 0)


 	shuffle_indices = np.random.permutation(np.arange(len(y)))
 	shuffled_x = x[shuffle_indices]
 	shuffled_y = y[shuffle_indices]
	return shuffled_x, shuffled_y

positive_data_file = 'data/rt-polarity.pos'
negative_data_file = 'data/rt-polarity.neg'
x, y = load_data_and_labels(positive_data_file, negative_data_file)

test_size = 2000
x_train, y_train = x[:-2000], y[:-2000]
x_test, y_test = x[-2000:], y[-2000:]
label_map = {0: 'negative', 1: 'positive'}


class NB_Classifier(object):

 	def __init__(self):
 		# naive bayes
 		self.model = MultinomialNB( alpha=1) #Laplace smooth：1
 		# use tf-idf extract features
 		self.feature_processor = TfidfVectorizer()

 	def fit(self, x_train, y_train, x_test, y_test):
 		# tf-idf extract features
 		x_train_fea = self.feature_processor.fit_transform(x_train)
 		self.model.fit(x_train_fea, y_train)

 		train_accuracy = self.model.score(x_train_fea, y_train)\

		print("Training Accuracy：{}".format(round(train_accuracy, 3)))

 		x_test_fea = self.feature_processor.transform(x_test)
 		y_predict = self.model.predict(x_test_fea)
 		test_accuracy = accuracy_score(y_test, y_predict)
 		print("Test Accuracy：{}".format(round(test_accuracy, 3)))

 		y_predict = self.model.predict(x_test_fea)
 		print('Test set evaluate：')
 		print(classification_report(y_test, y_predict, target_names=['0', '1']))

 	def single_predict(self, text):
 		text_fea = self.feature_processor.transform([text])
 		predict_idx = self.model.predict(text_fea)[0]
 		predict_label = label_map[predict_idx]
 		predict_prob = self.model.predict_proba(text_fea)[0][predict_idx]

 		return predict_label, predict_prob

nb_classifier = NB_Classifier()
nb_classifier.fit(x_train, y_train, x_test, y_test)
nb_classifier.single_predict("beautiful actors, great movie")




class SVM_Classifier(object):

 	def __init__(self, use_chi=False):

 		self.use_chi = use_chi # Whether use chi-square test for feature selection
 		# SVM
 		self.model = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
 		# use tf-idf extract features
 		self.feature_processor = TfidfVectorizer()
 		# chi-square test for feature selection
 		if use_chi:
 			self.feature_selector = SelectKBest(chi2, k=10000) # 34814 -> 10000

 	def fit(self, x_train, y_train, x_test, y_test):

 		x_train_fea = self.feature_processor.fit_transform(x_train)
 		if self.use_chi:
 			x_train_fea = self.feature_selector.fit_transform(x_train_fea, y_train)
 		self.model.fit(x_train_fea, y_train)

 		train_accuracy = self.model.score(x_train_fea, y_train)
 		print("Training Accuracy：{}".format(round(train_accuracy, 3)))

 		x_test_fea = self.feature_processor.transform(x_test)
 		if self.use_chi:
 			x_test_fea = self.feature_selector.transform(x_test_fea)
 		y_predict = self.model.predict(x_test_fea)
 		test_accuracy = accuracy_score(y_test, y_predict)
 		print("Test Accuracy：{}".format(round(test_accuracy, 3)))
 		print('Test set evaluate：')
 		print(classification_report(y_test, y_predict, target_names=['negative', 'positive']))

 	def single_predict(self, text):
 		text_fea = self.feature_processor.transform([text])
 		if self.use_chi:
 			text_fea = self.feature_selector.transform(text_fea)
 		predict_idx = self.model.predict(text_fea)[0]
 		predict_label = label_map[predict_idx]
		return predict_label


svm_classifier = SVM_Classifier()
svm_classifier.fit(x_train, y_train, x_test, y_test)



svm_classifier = SVM_Classifier(use_chi=True)
svm_classifier.fit(x_train, y_train, x_test, y_test)

svm_classifier.single_predict("beautiful actors, great movie")


###  TextCNN Text Classification
vocab = set()
for doc in x:
 	for word in doc.split(' '):
 		if word.strip():
 			vocab.add(word.strip().lower())
# write to vocab.txt file
with open('data/vocab.txt', 'w') as file:
 	for word in vocab:
 		file.write(word)
 		file.write('\n')


test_size = 2000
x_train, y_train = x[:-2000], y[:-2000]
x_test, y_test = x[-2000:], y[-2000:]

label_map = {0: 'negative', 1: 'positive'}


class Config():
	embedding_dim = 100 # word embedding dimention
 	max_seq_len = 200 # max sequence length
 	vocab_file = 'data/vocab.txt' # vocab_file_length

config = Config()

class Preprocessor():
 	def __init__(self, config):
 		self.config = config
 		# initial the map of word and index
 		token2idx = {"[PAD]": 0, "[UNK]": 1} # {word：id}
 		with open(config.vocab_file, 'r') as reader:
 			for index, line in enumerate(reader):
 				token = line.strip()
 				token2idx[token] = index+2

 		self.token2idx = token2idx

 	def transform(self, text_list):
 		# tokenization, and transform word to coresponding index
 		idx_list = [[self.token2idx.get(word.strip().lower(), self.token2idx['[UNK]']) for word in text.split(' ')] for text in text_list]
 		idx_padding = pad_sequences(idx_list, self.config.max_seq_len, padding='post')

 		return idx_padding

preprocessor = Preprocessor(config)
preprocessor.transform(['I love working', 'I love eating'])




class TextCNN(object):
 	def __init__(self, config):
 		self.config = config
 		self.preprocessor = Preprocessor(config)
 		self.class_name = {0: 'negative', 1: 'positive'}

 	def build_model(self):
 		# build model architecture
 		idx_input = tf.keras.layers.Input((self.config.max_seq_len,))
 		input_embedding = tf.keras.layers.Embedding(len(self.preprocessor.token2idx), self.config.embedding_dim, input_length=self.config.max_seq_len, mask_zero=True)(idx_input)


		convs = []
 		for kernel_size in [2, 3, 4, 5]:
 			c = tf.keras.layers.Conv1D(128, kernel_size, activation='relu')(input_embedding)
 			c = tf.keras.layers.GlobalMaxPooling1D()(c)
 			convs.append(c)
 		fea_cnn = tf.keras.layers.Concatenate()(convs)
 		fea_cnn = tf.keras.layers.Dropout(rate=0.5)(fea_cnn)
 		fea_dense = tf.keras.layers.Dense(128, activation='relu')(fea_cnn)
		fea_dense = tf.keras.layers.Dropout(rate=0.5)(fea_dense)
	 	fea_dense = tf.keras.layers.Dense(64, activation='relu')(fea_dense)
 		fea_dense = tf.keras.layers.Dropout(rate=0.3)(fea_dense)
 		output = tf.keras.layers.Dense(2, activation='softmax')(fea_dense)

 		model = tf.keras.Model(inputs=idx_input, outputs=output)
 		model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

 		model.summary()

 		self.model = model

	def fit(self, x_train, y_train, x_valid=None, y_valid=None, epochs=5, batch_size=128, **kwargs):
 		# train
 		self.build_model()

 		x_train = self.preprocessor.transform(x_train)
 		if x_valid is not None and y_valid is not None:
 			x_valid = self.preprocessor.transform(x_valid)
 		self.model.fit(x=x_train, y=y_train,
 					validation_data= (x_valid, y_valid) if x_valid is not None and y_valid is not None else None,
					batch_size=batch_size, epochs=epochs, **kwargs)

 	def evaluate(self, x_test, y_test):
 		# evaluate
 		x_test = self.preprocessor.transform(x_test)
 		y_pred_probs = self.model.predict(x_test)
 		y_pred = np.argmax(y_pred_probs, axis=-1)
 		result = classification_report(y_test, y_pred, target_names=['negative', 'positive'])
 		print(result)


 	def single_predict(self, text):
 		# predict
		input_idx = self.preprocessor.transform([text])
 		predict_prob = self.model.predict(input_idx)[0]
 		predict_label_id = np.argmax(predict_prob)
	
		predict_label_name = self.class_name[predict_label_id]
 		predict_label_prob = predict_prob[predict_label_id]

 		return predict_label_name, predict_label_prob


textcnn = TextCNN(config)
textcnn.fit(x_train, y_train, x_test, y_test, epochs=10) # train



textcnn.evaluate(x_test, y_test) # Test Set Evaluation


textcnn.single_predict("beautiful actors, great movie.") # single sentence predict

    """)