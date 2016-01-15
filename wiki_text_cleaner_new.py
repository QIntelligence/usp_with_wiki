import re
import sys
import codecs
from nltk import sent_tokenize
from nltk import word_tokenize
import nltk
def clean_wikipedia(lines_to_clean):
	cleaned_lines = []
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	new_lines_to_clean = []
	for line in lines_to_clean:
		new_lines_to_clean += sent_tokenize(line)
	lines_to_clean = new_lines_to_clean 
	for i in range(len(lines_to_clean)):
		line = lines_to_clean[i]
		if line.replace(' ','') == '/n':
			print ''
		#	print str(len(line.split(' ')))
		elif 70 > len(word_tokenize(line)) > 0:
			line = re.sub('([.,!?()])', r' \1 ', line)
			line = re.sub('\s{2,}', ' ', line)
			p = re.compile("(\d\s\.\s\d)|([A-Z]\s\.\s[A-Z])|([a-z]\s\.\s[a-z])")
			to_fix = p.findall(line)
			for number in to_fix:
				for sub in number:
					if len(sub) > 1:
						number = sub
						break
				start_index = line.index(number)
				end_index = start_index + len(number)
				new_number = number.replace(' . ', '.')
				line = line[:start_index] + new_number + line[end_index:]
			cleaned_lines.append(line)
		#print str(len(line.split(' ')))
		#print sent_tokenize(line)
	return cleaned_lines


if __name__ == '__main__':
	text_file = sys.argv[1]
	outfile = sys.argv[2]

	with codecs.open(text_file, 'rb', encoding = 'utf8') as text_file:
		lines = text_file.readlines()
	cleaned_lines = clean_wikipedia(lines)
	with codecs.open(outfile , 'wb', encoding = 'utf8') as outfile:
		for line in cleaned_lines:
			outfile.write(line)
		outfile.close()




			

