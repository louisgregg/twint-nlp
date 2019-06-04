import pickle
import pandas as pd

# city_filenames = {
# 'dublin' : 'dublin_nuclear_2019-05-30_False.pkl',
# 'london' : 'london_nuclear_2019-05-30_False.pkl',
# 'newyork': 'newyork_nuclear_2019-05-30_False.pkl'}

city_filenames = {
'dublin' : 'dublin_nuclear.pkl',
'london' : 'london_nuclear.pkl',
'newyork': 'newyork_nuclear.pkl'}

city_colors = {
'dublin':'blue',
'london':'red',
'newyork':'green'}

search_term = 'nuclear'

data = {}
for key, value in city_filenames.items():
	with open(value, "rb") as file:
		data[key] = pickle.load(file)


# Data cleaning: first round. 
import re 
import string

def clean_text_1(text):
    text = text.replace('-',' ')
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\d', '', text)
    return(text)

round1 = lambda x: clean_text_1(x)    

for city in data.keys():
	data[city]['clean_tweet'] = data[city]['tweet'].apply(round1)


# Emoji removal copy-pasta'd from this big discussion on Stack Overflow
# https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
import emoji
def give_emoji_free_text(text):
    try:
        allchars = [str for str in text.decode('utf-8')]
    except AttributeError:
        allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    try:
        clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    except AttributeError:
        clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
    return clean_text

def clean_text_2(text):
    text = give_emoji_free_text(text)    
    #text = re.sub('\ {2,}',' ',text)
    return(text)

#why declare the lambda / anonymous function here? Unecessary intermediate step?     
round2 = lambda x: clean_text_2(x) 

for city in data.keys():
	data[city]['clean_tweet'] = data[city]['clean_tweet'].apply(round2)

########
######## Here begins the sentiment analysis stuff
########

# Convert Unix time to human readable date time. 
# Taken from https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date
from datetime import datetime
def unix_to_human(timestamp):
    try:
        timestamp = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        timestamp = datetime.utcfromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
    return(timestamp)

from textblob import TextBlob

pol = lambda x: TextBlob(x).sentiment.polarity
sub = lambda x: TextBlob(x).sentiment.subjectivity


for city in data.keys():
	data[city]['polarity'] = data[city].clean_tweet.apply(pol)
	data[city]['subjectivity'] = data[city].clean_tweet.apply(sub)


#######
####### Data Plotting
####### 
import matplotlib.pyplot as plt

# plt.rcParams['figure.figsize'] = [10, 8]


for city in data.keys():
	x = data[city].polarity
	y = data[city].subjectivity
	plt.scatter(x, y, color='blue')
	# plt.xlim([-1,1])
	# plt.ylim([0,1])
	plt.axis([-1,1,-0.1,1.1])

	plt.title('Sentiment Analysis: \''+search_term+'\' in '+city, fontsize=20)
	plt.xlabel('<-- Negative -------- Positive -->', fontsize=15)
	plt.ylabel('<-- Facts -------- Opinions -->', fontsize=15)
	plt.savefig(city+'.png', bbox_inches='tight')
	plt.clf()

for city in data.keys():
	x = data[city].polarity
	y = data[city].subjectivity
	plt.scatter(x, y, color=city_colors[city])
	# plt.legend((city),
 #           loc='upper center', shadow=True)
	# plt.xlim([-1,1])
	# plt.ylim([0,1])
	plt.axis([-1,1,-0.1,1.1])

plt.legend([city for city in data.keys()],loc='center right', shadow=True)	
plt.title('Sentiment Analysis: \''+search_term+'\'', fontsize=20)
plt.xlabel('<-- Negative -------- Positive -->', fontsize=15)
plt.ylabel('<-- Facts -------- Opinions -->', fontsize=15)
plt.savefig('combined-cities.png', bbox_inches='tight')
