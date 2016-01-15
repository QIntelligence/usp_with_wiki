import mechanize
import re
import sys
import nltk.data
import nltk.tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import os 
import os.path 
import codecs
import time
from nltk import word_tokenize
from nltk import sent_tokenize
def parse_sentence(string_to_parse, tagger, lemmatizer):


	br = mechanize.Browser(factory=mechanize.RobustFactory())
	responce = br.open('http://nlp.stanford.edu:8080/parser/index.jsp')

	br.form = list(br.forms())[0] 
	control = br.form.find_control("query")

	control.value = string_to_parse

	responce = br.submit()
	lines = responce.readlines()
	start_index = 0


	#universal dependencies
 	start_index = 0
	end_index = 0
	
	for i in range(len(lines)):
		if 'Universal dependencies<' in lines[i]:
			start_index = i + 2 
		if 'Universal dependencies,' in lines[i]:
			end_index = i - 3


	relevent_lines = lines[start_index:end_index]

	cleaned_lines = []
	for i in range(len(relevent_lines)):
		line = relevent_lines[i]
		if i == 0:
			line = line[35:-1]
		elif i == len(relevent_lines) -1:
			line = line[:-1]
		else:
			line = line[:-1]
		cleaned_lines.append(line)

	dependencies = cleaned_lines

	#morpheme parser

	for i in range(len(lines)):
		if 'Tagging' in lines[i]:
			start_index = i +2 
		if 'Parse' in lines[i]:
			end_index = i - 3


	relevent_lines = lines[start_index:end_index]

	cleaned_lines = []
	for i in range(len(relevent_lines)):
		line = relevent_lines[i]

		if '<div style' in line:
			pass
		elif line.replace(' ','') == '<br/>\n':
			pass
		elif line.replace(' ','') == '\n':
			pass
		else:
			line = line.replace(' ','')
			cleaned_lines.append(line)

	for i in range(len(cleaned_lines)):
		line = cleaned_lines[i]
		line = line[:-7]
		new_line = ''
		found = False
		for j in range(len(line)):
			character = line[len(line) - j -1]
			if character == '/' and not found:
				character = '_'
				found = True
			new_line = character + new_line
		cleaned_lines[i] = new_line

	morphemes = cleaned_lines
	
        
	text=nltk.word_tokenize(string_to_parse)
	tagged_text = nltk.tag._pos_tag(text, None,tagger)


	wordnet_lemmatizer = lemmatizer
	lemmas = []
	for word in tagged_text:
		POS_TAG = penn_to_wn(word[1])
		if POS_TAG:
			lemma = wordnet_lemmatizer.lemmatize(word[0], POS_TAG)
		else:
			lemma = wordnet_lemmatizer.lemmatize(word[0])

		lemma = lemma.replace('(', '-lrb-')
		lemma = lemma.replace(')', '-rrb-')
		lemmas.append(lemma)


	return lemmas, morphemes, dependencies

def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']


def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']


def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']


def penn_to_wn(tag):
    if is_adjective(tag):
        return 'a'
    elif is_noun(tag):
        return 'n'
    elif is_adverb(tag):
        return 'r'
    elif is_verb(tag):
        return 'v'
    return None

if __name__ == '__main__':

	text_dir = sys.argv[1]
        lemmatizer = WordNetLemmatizer()
        tagger = nltk.tag.perceptron.PerceptronTagger()
	#text_files = [f for f in listdir(text_dir) if isfile(join(text_dir, f))]
	text_files = []
	for dirpath, dirnames, filenames in os.walk(text_dir+'text/'):
		for filename in [f for f in filenames if f.endswith(".txt")]:
			text_files.append(os.path.join(dirpath, filename))

	#print text_files
	index = 0
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	reload(sys)  
	sys.setdefaultencoding('utf8')
	for text_file in text_files:
		print(text_file)	

		with codecs.open(text_file, 'rb', encoding = 'utf8') as text_file:
			data = text_file.read()
		sentences = sent_tokenize(data)


		lemma_file = open(text_dir+'morph/0/'+str(index)+'.morph', 'wb')
		morpheme_file = open(text_dir+'morph/0/'+str(index)+'.input', 'wb')
		dependency_file = open(text_dir+'dep/0/'+str(index)+'.dep', 'wb')

                index_sent = 0
                start = time.time()
		for sentence in sentences:
		#	print sent_tokenize(sentence)
			if 70 > len(word_tokenize(sentence)) > 0:
				if index_sent % 100 == 0:
					end = time.time()
					print str(index_sent) + '/' + str(len(sentences))+ ' sentences completed'
					print str((end - start)/100.0) + 'seconds per sentence' 
					start = time.time()
				lemmas, morphemes, dependencies = parse_sentence(sentence, tagger, lemmatizer)
				for morpheme in morphemes:
					morpheme_file.write(morpheme+'\n')
				for dependency in dependencies:
					dependency_file.write(dependency+'\n')
				for lemma in lemmas:
					lemma_file.write(lemma+'\n')
				morpheme_file.write('\n')
				dependency_file.write('\n')
				lemma_file.write('\n')
                        index_sent += 1
		morpheme_file.close()
		dependency_file.close()
		lemma_file.close()
		index += 1




	





