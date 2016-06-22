import re
import nltk
import pickle


def read_file(filename, thinner):
	# read in the training set. the file is very large, 
	# so we only take a subset, defined by thinner (larger thinner, fewer lines) 
	f = open(filename, 'r')

	content = []
	for index, line in enumerate(f):
		if (index % thinner == 0):
			content.append(line)
			
	return content

def clean_tweet(string):

	values = string.split('\"') # split the input lines into categories
	sentiment_score = ((int(values[1]) - 2) / 2.) # this gives -1 for neg, 0 for neut, 1 for pos

	tweet_text = values[-2] # actual tweet text

	# Regex the tweets to remove links, usernames, text emoticons, 
	# and all punctuation bar '!' (I thought that '!' may be informative one way or another). 
	patterns = ['http.*?(\s|$)', '\@\w*\s', '\p.*?(\s|$)','[^\w\s\d!]+']

	for pattern in patterns:
		
		tweet_text = re.sub(pattern, ' ', tweet_text)

	# lower case everything, remove any short words, split into a list of strings.
	tweet_text = [e.lower() for e in re.findall("[\w']+|!", tweet_text) if(len(e) >= 3 or e == '!')]
	
	return (tweet_text, sentiment_score)


def tweet_treat(filename, thinner):

	content = read_file(filename, thinner)

	treated_tweets = []
	for line in content:
		treated_tweets.append(clean_tweet(line))

	return treated_tweets



def get_words_in_tweets(tweets):
    	# return a set of all words used in the tweets
   	all_words = []
    
    	for (words, sentiment) in tweets:
		all_words.extend(words)
    
    	return all_words
		  
def get_word_features(wordlist):
	# return the 2000 most commonly used words.
	wordlist = nltk.FreqDist(wordlist)

	word_features = wordlist.most_common(2000)
	
	return [i[0] for i in word_features]

def extract_features(document):
    # this reruns, for a given input list, a dictionary associating 
    # the words with a Boolean indicating whether or not they appear in
    # our list of the 2000 most commonly used words.
    	document_words = set(document)
    	
	features = {}
    	
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	
    	return features


def tester(filename, classifier):
	# this function tests the classifier on some of the tweets it hasn't been trained on.
	# it performs at around 70% accuracy on various test sets, which is quite good, 
	# given that humans agree on <80% of classifications. 
	testers = tweet_treat(filename, 499)

	counter = 0
	accuracy = 0 
	for test in testers:
		guesses = classifier.classify(extract_features(test[0]))
		counter += 1
		if guesses == test[1]:
			accuracy += 1
	print "This classified %f %% of messages accurately" %(accuracy /float(counter) * 100)


def classifier_training(tweets):

	# generate training set
	training_set = nltk.classify.apply_features(extract_features, tweets)

	# train the classifier 
	classifier = nltk.NaiveBayesClassifier.train(training_set)

	#tester(filename, classifier)

	#export to a pickle file for later.
	f = open('tweet_classifier.pickle', 'wb')
	pickle.dump(classifier, f)
	f.close()



filename = 'training.1600000.processed.noemoticon.csv'
	
tweets = tweet_treat(filename, 500)

word_features = get_word_features(get_words_in_tweets(tweets))


