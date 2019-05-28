import pandas as pd
from datetime import date, timedelta
import twint_to_db
import sys # for command line argument parsing
import numpy as np # for creation of a an array of ones

"""
-----------------------
Scrape a pre-defined list of cities for a keyword using twint since yesterday. 
If run using the keyword 'test', i.e:
python3.7 scrape_cities.py --test
then the scraping limit will be set to the minimum value (20) for testing. 
Otherwise no limit will be set on the number of scrapes. 
-----------------------
"""

# a function to construct filenames for dataframe storage
def construct_filename(row):
	filename = './'+row['location_name']+'_'+row['searchterm']+'_'+str(row['since'])+'_'+str(row['until'])+'.pkl'
	return(filename)

def main(test=False):
	yesterday = date.today() - timedelta(days=1)
	yesterday = yesterday.strftime('%Y-%m-%d')
	# print(yesterday)

	dataframe_of_cities = pd.DataFrame({
	'location_name':['dublin','london','newyork'],
	'searchterm':['nuclear','nuclear','nuclear'],
	'geo' : ['53.349538,-6.260678,10km','51.516479,-0.096949,10km','40.751177,-73.994641,10km'],
	'since':[yesterday,yesterday,yesterday],
	'until':[False,False,False],
	'limit':[0,0,0]
	},index=[0,1,2])

	if test:
		n=len(dataframe_of_cities)
		dataframe_of_cities.loc[:,'limit'] = 20*np.ones(n).astype(int)

	
	# create new dataframe column based on other columns using a lambda function:
	# https://stackoverflow.com/questions/26886653/pandas-create-new-column-based-on-values-from-other-columns
	dataframe_of_cities['filepath'] = dataframe_of_cities.apply(lambda row: construct_filename(row), axis=1)

	print(dataframe_of_cities)

	# iterate through rows of the dataframe to call the scraper
	for row in dataframe_of_cities.itertuples(index=True, name='Pandas'):
		twint_to_db.main(
			searchterm = getattr(row,"searchterm"),
			geo = getattr(row,"geo"),
			since = getattr(row,"since"),
			until = getattr(row,"until"),
			limit = getattr(row,"limit"),
			filepath = getattr(row,"filepath")
			)


if __name__ == '__main__':
	if len(sys.argv)==2 and str(sys.argv[1])=='--help':
		print("To scrape a limit of 20 tweets per line run: ")
		print("python3 scrape_cities.py --test")

	elif len(sys.argv)==2 and str(sys.argv[1]) == '--test':
		print("Scraping 20 tweets per city as a test.")
		main(test=True)

	else:
		main()