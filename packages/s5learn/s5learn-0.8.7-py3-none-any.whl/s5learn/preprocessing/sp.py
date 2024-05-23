def sp():

    print("""
    
    ## Libraries
import os
import wave as we
import numpy as np
import matplotlib.pyplot as plt

from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib.backend_bases import RendererBase

from scipy import signal
from scipy.io import wavfile

from scipy.fftpack import fft
import warnings
warnings.filterwarnings("ignore")

## View the waveform sequence of the wav file
## View basic attributes of the wav file
filename = 'data/thchs30/train/A2_0.wav '
WAVE = we.open(filename)

for item in enumerate(WAVE.getparams()):
	print (item)

a = WAVE.getparams().nframes # Total number of frames

f = WAVE.getparams().framerate # Sampling frequency

sample_time = 1/f # Interval of sampling points

time = a/f # Sound signal length

sample_frequency, audio_sequence = wavfile.read(filename)

x_seq = np.arange(0,time,sample_time)

plt.plot(x_seq,audio_sequence, 'blue' )
plt.xlabel('time (s)')
plt.show()

## Obtain file name
audio_path = 'data/train/audio/'
pict_Path = 'data/train/audio/'
samples = []
# Verify that the file exists, if not here, create it
if not os.path.exists(pict_Path):
	os.makedirs(pict_Path)

subFolderList = []
for x in os.listdir(audio_path):
	if os.path.isdir(audio_path + '/' + x):
		subFolderList.append(x)
		if not os.path.exists(pict_Path + '/' + x):
			os.makedirs(pict_Path +'/'+ x)

# View the name and number of sub-files
print("----list----:",subFolderList)
print("----len----:",len(subFolderList))


sample_audio = []
total = 0
for x in subFolderList:
	# Get all wav files
	all_files = [y for y in os.listdir(audio_path + x) if '.wav' in y]
	total += len(all_files)
	sample_audio.append(audio_path + x + '/'+ all_files[0])

	# View the number of files in each subfolder
	print('%s : count: %d ' % (x , len(all_files)))

# View the total number of wav files
print("TOTAL:",total)



def log_specgram(audio, sample_rate, window_size=20, step_size=10, eps=1e-10):
	nperseg = int(round(window_size * sample_rate / 1e3))
	noverlap = int(round(step_size * sample_rate / 1e3))
	freqs, _, spec = signal.spectrogram(audio, fs=sample_rate, window='hann', ,nperseg=nperseg,,
				noverlap=noverlap, detrend=False)

 	return freqs, np.log(spec.T.astype(np.float32) + eps)

## Visualize multiple spectrums of one sample

fig = plt.figure(figsize=(20,20))
for i, filepath in enumerate(sample_audio[:16]):
	# Make subplots
	plt.subplot(4,4,i+1)
	# pull the labels
	label = filepath.split('/')[-2]
	plt.title(label)

	# create spectrogram
	samplerate, test_sound = wavfile.read(filepath)
	_, spectrogram = log_specgram(test_sound, samplerate)

 	plt.imshow(spectrogram.T, aspect='auto', origin='lower')
 	plt.axis('off')
plt.show()


## Visualize the waveforms of multiple samples
fig = plt.figure(figsize=(10,10))
for i, filepath in enumerate(sample_audio[:16]):
 	plt.subplot(4,4,i+1)
 	samplerate, test_sound = wavfile.read(filepath)
 	plt.title(filepath.split('/')[-2])
 	plt.axis('off')
 	plt.plot(test_sound)
plt.show()

## Visualize multiple waveforms of one sample
fig = plt.figure(figsize=(8,8))
for i, filepath in enumerate(yes_samples):
 	plt.subplot(3,3,i+1)
 	samplerate, test_sound = wavfile.read(filepath)
 	plt.title(filepath.split('/')[-2])
 	plt.axis('off')
 	plt.plot(test_sound)
plt.show()

    
    """)