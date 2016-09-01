import dateutil
import train_classifier
import nltk
import re
import time
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import seaborn as sns; sns.set()
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def open_file(filename):

	f = open(filename, 'r')	
	y = f.read()	
	content = y.splitlines()
	return content


def ismessage(string):
	# ditctionary of regex patterns, to find message parts corresponding to these keys.
	patterns = {
		"date"    :'([0-9]{2}/){2}[0-9]{4}',
		"time"    :'[0-9]{2}:[0-9]{2}', 
		"name"    :' - .*?:', 
		"message" :'[a-z]: .*$'
	}
	
	message_dict = {}
	for pattern_key in patterns:
	
		result = re.search(patterns[pattern_key], string)
		
		if result:
			message_dict[pattern_key] = result.group()		

	return message_dict

def process(content):
	
	j = 1	
	
	df = pd.DataFrame(index = range(1, len(content)+1), columns=[ 'Name', 'Message', 'date_string'])
	
	for i in content:

		results = ismessage(i)
		# if the message contains a name, time, date, and content string
		# we add it to the data frame
		if len(results) == 4:
	
			df.iloc[j]['Name']    = results['name'][3:-1]
			df.iloc[j]['Message'] = results['message'][3:]
			df.iloc[j]['date_string'] = results['date'] + ' ' + results['time']		
			j += 1
	
	df = df[pd.notnull(df['Message'])] # remove null messages (if any)

	# retrieve date, day, hour, from date string 
	df['Date'] = pd.to_datetime(df['date_string'], format='%d/%m/%Y %H:%M')
	df['Day']  = df['date_string'].map(lambda x: dateutil.parser.parse(x).strftime("%a"))
	df['Hour'] = df['date_string'].map(lambda x:dateutil.parser.parse(x).strftime("%H"))
	df.index = df['Date']

	return df


def make_plots(df):
	
	fig = plt.figure()	
	plt.title = "Whatsappening"
	ax1 = plt.subplot2grid((4,6), (0,0), rowspan=2, colspan=2)
	ax2 = plt.subplot2grid((4,6), (0,2), rowspan=2, colspan=2)
	ax3 = plt.subplot2grid((4,6), (0,4), rowspan=2, colspan=2)
	ax4 = plt.subplot2grid((4,6), (2,0), rowspan=2, colspan=6)
	
	plt.tight_layout()	

	df.groupby('Hour').count().plot(ax=ax1, legend=None, xlim=[0,23])
	df.groupby('Day').count().plot(y="Message", ax=ax2, kind='bar', legend=None)
	df.Name.value_counts().plot(ax=ax3,kind = 'bar')
	df.groupby(df.index.date).count().plot(y="Message", ax=ax4, legend=None)

	plt.show()

def clean_to_classify(message):
	# remove links, images (not included), punctuation for classification
	patterns = ['http.*?(\s|$)', '\<Media omitted\>', '\p.*?(\s|$)', '[^\w\s\d!]+']

	for pattern in patterns:
		cleaned_text = re.sub(pattern, ' ', message)
		
	# lower case everything, remove any short words, split into an array.		        
	cleaned_text = [e.lower() for e in re.findall("[\w']+|!", cleaned_text) if(len(e) >= 3 or e == '!')]
		
	return cleaned_text

def classify_messages(df):

	cleaned_text = []
	for message in df.Message:
		# get text in classification format
		cleaned_text.append(clean_to_classify(message))

	# read classifier from pickle
	f = open('tweet_classifier.pickle', 'rb')
	classifier = pickle.load(f)
	f.close()

	sentiment = []
	for text in cleaned_text:
		# get the sentiment of each message (using the feature extrator we trained with)
		# and add it to a list
		sentiment.append(classifier.classify(train_classifier.extract_features(text)))
	
	df['sentiment'] = sentiment # put sentiments into the data frame	
	return df


def vader_sentiment(df):

        sith = SentimentIntensityAnalyzer()
        
        sentiment = []
        for sentence in df.Message:
                sent = sith.polarity_scores(sentence)
                sent_total = sent['pos'] - sent['neg']

                sentiment.append(sent_total)
  
        df['sentiment'] = sentiment
        return df


def plot_sentiment(df):
	# plot the sentiments
	fig = plt.figure()
	ax = plt.gca()
	ax.set_yticks([-1,0,1])
	ax.set_yticklabels(['Negative','Neutral','Positive'])
	
	df.groupby(df.index.date).mean().plot(y='sentiment', ylim=[-1.5,1.5], legend=None, ax=ax)	
	
	plt.show()



if __name__ == '__main__':

	filename = 'whatsapp_mess.txt'

	content = open_file(filename)

	processed_df = process(content)
	
	make_plots(processed_df)
        
#        d2 = processed_df.copy()

        data_panel = vader_sentiment(processed_df)

#	data_panel2 = classify_messages(d2)

#       right = 100*sum(data_panel.sentiment*data_panel2.sentiment >= 0) / float(len(data_panel))
#        print 'The Naive Bayes and Vader agree on %.2f%% of classifications' %right

