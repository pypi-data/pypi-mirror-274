def ss_seqseq():


    print("""
    
    # Libraries
import warnings
warnings.filterwarnings("ignore")
import time
import tensorflow as tf
import scipy.io.wavfile as wav
import numpy as np
from six.moves import xrange as range
from python_speech_features import mfcc
from tensorflow.keras.layers import Input,LSTM,Dense
from tensorflow.keras.models import Model,load_model
import pandas as pd
import numpy as np



## Data Path
audio_filename = "data/audio.wav"
target_filename = "data/label.txt"

## Read data and perform feature extraction
def sparse_tuple_from(sequences, dtype=np.int32):
	indices = []
 	values = []
 	for n, seq in enumerate(sequences):
 		indices.extend(zip([n]*len(seq), range(len(seq))))
 		values.extend(seq)

 	indices = np.asarray(indices, dtype=np.int64)
 	values = np.asarray(values)
 	shape = np.asarray([len(sequences), np.asarray(indices).max(0)[1]+1], dtype=np.int64)
 	return indices, values, shape

def get_audio_feature():
	# Read the content of the wav file, fs is the sampling rate, audio_filename is the data
 	fs, audio = wav.read(audio_filename)
 	#Extract mfcc features
 	inputs = mfcc(audio, samplerate=fs)
 	#Standardize characteristic data, subtract the mean divided by the standard deviation
 	feature_inputs = np.asarray(inputs[np.newaxis, :])
 	feature_inputs = (feature_inputs - np.mean(feature_inputs))/np.std(feature_inputs)
 	# Characteristic data sequence length
 	feature_seq_len = [feature_inputs.shape[1]]
 	return feature_inputs, feature_seq_len

feature_inputs, feature_seq_len = get_audio_feature()



def get_audio_label():
	with open(target_filename, 'r') as f:
 		# The original text is “i like you , do you like me”
 		line = f.readlines()[0].strip()
 	# Put it in the list, replace the space with ' '
 	#['i', ' ', 'like', ' ', 'you',' ', ',',' ', 'do', ' ', 'you', ' ', 'like', ' ', 'me']
 	targets = line.split(' ')
 	targets.insert(0,'<START>')
 	targets.append("<END>")
 	print(targets)
 	# Convert the list into sparse triples
 	train_targets = sparse_tuple_from([targets])
 	return targets,train_targets

line_targets,train_traget=get_audio_label()



### Configure Parameters
target_characters = list(set(line_targets))
INUPT_LENGTH = feature_inputs.shape[-2]
OUTPUT_LENGTH = train_traget[-1][-1]
INPUT_FEATURE_LENGTH = feature_inputs.shape[-1]
OUTPUT_FEATURE_LENGTH = len(target_characters)
N_UNITS = 256
BATCH_SIZE = 1
EPOCH = 20
NUM_SAMPLES = 1
target_texts = []
target_texts.append(line_targets)


## Create Seq2Seq model
def create_model(n_input,n_output,n_units):
	#encoder
 	encoder_input = Input(shape = (None, n_input))
 	# The input dimension n_input is the dimension of the input xt at each time step
 	encoder = LSTM(n_units, return_state=True)
 	# n_units is the number of neurons in each gate in the LSTM unit, and only when return_state is
	#set to True will it return to the last state h, c
 	_,encoder_h,encoder_c = encoder(encoder_input)
 	encoder_state = [encoder_h,encoder_c]
 	#Keep the final state of the encoder as the initial state of the decoder
 	#decoder
 	decoder_input = Input(shape = (None, n_output))
 	#The input dimension of decoder is the number of characters
 	decoder = LSTM(n_units,return_sequences=True, return_state=True)
 	# When training the model, the output sequence of the decoder is required to compare and
	#optimize the result, so return_sequences should also be set to True
 	decoder_output, _, _ = decoder(decoder_input,initial_state=encoder_state)


	#In the training phase, only the output sequence of the decoder is used, and the final state h.c is
	#not required
 	decoder_dense = Dense(n_output,activation='softmax')
 	decoder_output = decoder_dense(decoder_output)
 	# The output sequence passes through the fully connected layer to get the result
 	#Generated training model
 	model = Model([encoder_input,decoder_input],decoder_output)
 	# The first parameter is the input of the training model, including the input of encoder and
	#decoder, and the second parameter is the output of the model, including the output of the decoder
 	# Inference stage, used in the prediction process
 	# Inference model—encoder
 	encoder_infer = Model(encoder_input,encoder_state)

 	# Inference model -decoder
 	decoder_state_input_h = Input(shape=(n_units,))
 	decoder_state_input_c = Input(shape=(n_units,))
 	# The state of the last moment h,c
 	decoder_state_input = [decoder_state_input_h, decoder_state_input_c]

	decoder_infer_output, decoder_infer_state_h, decoder_infer_state_c =
	decoder(decoder_input,initial_state=decoder_state_input)
 	#The current state
 	decoder_infer_state = [decoder_infer_state_h, decoder_infer_state_c]
 	decoder_infer_output = decoder_dense(decoder_infer_output)# Current time output
 	decoder_infer = Model([decoder_input]+decoder_state_input,[decoder_infer_output]+decoder_infer_state)

	return model, encoder_infer, decoder_infer

model_train, encoder_infer, decoder_infer = create_model(INPUT_FEATURE_LENGTH,OUTPUT_FEATURE_LENGTH, N_UNITS)
model_train.compile(optimizer='adam', loss='categorical_crossentropy')
model_train.summary()




encoder_input = feature_inputs
decoder_input = np.zeros((NUM_SAMPLES,OUTPUT_LENGTH,OUTPUT_FEATURE_LENGTH))
decoder_output = np.zeros((NUM_SAMPLES,OUTPUT_LENGTH,OUTPUT_FEATURE_LENGTH))
target_dict = {char:index for index,char in enumerate(target_characters)}
target_dict_reverse = {index:char for index,char in enumerate(target_characters)}
print(decoder_input.shape)

for seq_index,seq in enumerate(target_texts):
	for char_index,char in enumerate(seq):
 		print(char_index,char)
 		decoder_input[seq_index,char_index,target_dict[char]] = 1.0
 		if char_index > 0:
 			decoder_output[seq_index,char_index-1,target_dict[char]] = 1.0


#Get training data, in this example only one sample of training data
model_train.fit([encoder_input,decoder_input],decoder_output,batch_size=BATCH_SIZE,epochs=EPOCH,validation_split=0)



## Model Testing
def predict_chinese(source,encoder_inference, decoder_inference, n_steps, features):
# First obtain the hidden state of the predicted input sequence through the inference encoder
 	state = encoder_inference.predict(source)
 	# The first character'\t' is the starting mark
 	predict_seq = np.zeros((1,1,features))
 	predict_seq[0,0,target_dict['<START>']] = 1
 	output = ''
 	# Start to predict about the hidden state obtained by the encoder
 	# Each cycle uses the last predicted character as input to predict the next character until the
	#terminator is predicted
 	for i in range(n_steps):#n_steps is maximum sentence length
 		# Input the hidden state of h, c at the last moment to the decoder, and the predicted
		#character predict_seq of the last time
 		yhat,h,c = decoder_inference.predict([predict_seq]+state)
 		# Note that yhat here is the result output after Dense, so it is different from h


 		char_index = np.argmax(yhat[0,-1,:])
 		char = target_dict_reverse[char_index]
		# print(char)

 		state = [h,c] # This state will continue to be passed as the next initial state
 		predict_seq = np.zeros((1,1,features))
 		predict_seq[0,0,char_index] = 1
 		if char == '<END>': # Stop when the terminator is predicted
 			break
 		output +=" " +char
	return output

out = predict_chinese(encoder_input,encoder_infer,decoder_infer,OUTPUT_LENGTH,OUTPUT_FEATURE_LENGTH)
print(out)

    
    """)