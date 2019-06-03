""" Code to extract tweets from twitter and update local database """

# connect to main database (MySQL or import from CSV or whatever)
# for the moment it's easiest to make this a pickled pandas dataframe
from pathlib import Path # to check if file exists https://therenegadecoder.com/code/how-to-check-if-a-file-exists-in-python/
import pickle
import pandas as pd
from pprint import pprint
import twint
def open_local_dataframe(file_path):
	local_dataframe = pd.read_pickle(file_path)
	return(local_dataframe)

# scrape data into a dataframe
def scrape_into_dataframe(search_term, geo, since=False, until=False, limit=0, lang = 'en', hide_output = True):
	c = twint.Config()
	if limit != 0:
		c.Limit = limit
	else:
		pass
	c.Lang = lang	
	c.Hide_output = hide_output
	c.Pandas = True
	c.Store_pandas = True
	c.Hide_output = hide_output
	c.Search = search_term
	c.Location = True
	c.Geo = geo
	if since:
		c.Since = since
	if until:
		c.Until = until
	# Start search
	twint.run.Search(c)

	# store scrape results as dataframe
	results_dataframe = twint.storage.panda.Tweets_df

	# return a dataframe of tweets
	return(results_dataframe)

def update_main_dataframe(main_dataframe, new_dataframe):
	if main_dataframe.empty:
		main_dataframe = new_dataframe
	else:
		# rather than iterating, I've merged / deleted duplicates database-style (vertically)
		# https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
		updated_dataframe = pd.concat([main_dataframe, new_dataframe])
		# remove duplicates (based on ID column) https://stackoverflow.com/questions/22648591/add-new-rows-to-a-dataframe-that-does-not-yet-exist-in-it
		updated_dataframe.drop_duplicates(subset=['id'], inplace=True, keep='first') 
		# reset index of updated dataframe https://stackoverflow.com/questions/35528119/pandas-recalculate-index-after-a-concatenation
		updated_dataframe.reset_index(inplace=True,drop=True)
		return(updated_dataframe)			

def read_dataframe_file(file_path):
	try:
		dataframe = pd.read_pickle(file_path)
	except FileNotFoundError:
		dataframe = pd.DataFrame() # create an empty dataframe to fill
	return(dataframe)

def write_dataframe_file(dataframe, file_path):
	pickle.dump(dataframe, open(file_path, "wb") ) 
	# 'w'	open for writing, truncating the file first (to truncate means to empty)
	# 'b'	binary mode

def check_if_file_exists(path):
	config = Path(path)
	if config.is_file():
	    return(True)
	else:
	    return(False)

def test():	

	#scrape for the word fruit near the Dublin GPO for 20 tweets in march 2019
	scraped_dataframe = scrape_into_dataframe("fruit","53.349538,-6.260678,10km",since="2019-03-15",until="2019-04-15", limit=20, hide_output = True)
	print('-----------------------------------------')
	print('The scraped dataframe: ')
	print(scraped_dataframe.dtypes)
	print(scraped_dataframe.tweet)
	print('-----------------------------------------')

	# open local dataframe of data scraped using the same search query
	# if it doesn't exist create it
	local_dataframe_path = './local_test_dataframe.pkl'
	if check_if_file_exists(local_dataframe_path):
		local_dataframe = read_dataframe_file(local_dataframe_path)	
		# update local dataframe with new tweets
		local_dataframe = update_main_dataframe(local_dataframe, scraped_dataframe)
	else: 
		local_dataframe = scraped_dataframe

	print('-----------------------------------------')
	print('The updated local dataframe: ')
	print(local_dataframe.dtypes)
	print(local_dataframe.tweet)
	print('-----------------------------------------')

	# write newly updated dataframe to the file. 
	write_dataframe_file(local_dataframe, local_dataframe_path)

def main(searchterm, geo, since, until, limit, filepath):
	# scrape new data
	scraped_dataframe = scrape_into_dataframe(searchterm, geo, since=since, until=until, limit=limit)

	# open local dataframe 
	if check_if_file_exists(filepath):
		local_dataframe = read_dataframe_file(filepath)	
		# update local dataframe with new tweets
		local_dataframe = update_main_dataframe(local_dataframe, scraped_dataframe)
	else: 
		local_dataframe = scraped_dataframe	
	# write newly updated dataframe to the file. 
	write_dataframe_file(local_dataframe, filepath)	

if __name__ == "__main__":
	# if run as a script then test functionality
	test()



