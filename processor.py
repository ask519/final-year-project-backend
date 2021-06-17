from pickle import load
from numpy import argmax
from keras.preprocessing.sequence import pad_sequences
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.inception_resnet_v2 import preprocess_input
from keras.models import Model
from keras.models import load_model
from PIL import Image
import os


# extract features from each photo in the directory
def extract_features(filename):
	# load the model
	model = InceptionResNetV2()
	# re-structure the model
	model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
	# load the photo
	print(filename)
	image = load_img(filename, target_size=(299, 299))
	# convert the image pixels to a numpy array
	image = img_to_array(image)
	# reshape data for the model
	image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
	# prepare the image for the VGG model
	image = preprocess_input(image)
	# get features
	feature = model.predict(image, verbose=0)
	return feature

# map an integer to a word
def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None

# generate a description for an image
def generate_caption(photoFileName, max_length = 34):
	
	tokenizer = load(open('tokenizer.pkl', 'rb'))
	model = load_model('loss2.927-val_loss3.389-irnv2.h5')
	photo = extract_features(photoFileName)


	# seed the generation process
	in_text = 'startseq'
	# iterate over the whole length of the sequence
	for i in range(max_length):
		# integer encode input sequence
		sequence = tokenizer.texts_to_sequences([in_text])[0]
		# pad input
		sequence = pad_sequences([sequence], maxlen=max_length)
		# predict next word
		yhat = model.predict([photo,sequence], verbose=0)
		# convert probability to integer
		yhat = argmax(yhat)
		# map integer to word
		word = word_for_id(yhat, tokenizer)
		# stop if we cannot map the word
		if word is None:
			break
		# append as input for generating the next word
		in_text += ' ' + word
		# stop if we predict the end of the sequence
		if word == 'endseq':
			break
	description = in_text

	return description

#print(generate_caption(photoFileName= "test.jpeg" ))