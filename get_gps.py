import requests 

# http://www.gps-coordinates.net/api/eiffeltower
def get_gps_from_name(name):
	response_tuple = requests.get('http://www.gps-coordinates.net/api/'+name)
	return(response_tuple.text)

# run from command line for testing
def main(list_of_placenames):
	for name in list_of_placenames:
		name = name.replace(' ','')
		print(get_gps_from_name(name))

if __name__ == '__main__':
	places = ['dublin','london','new york','toronto']
	main(places)		
"""
these placename-gps links are crowd sourced so unreliable. 
For example the query above produces:
{"responseCode" : "400", "identifier" : "dublin", "message" : "No result"}                                    
{"responseCode" : "200", "identifier" : "london", "latitude" : "51.5073509", "longitude" : "-0.12775829999998"}
{"responseCode" : "200", "identifier" : "newyork", "latitude" : "40.7127753", "longitude" : "-74.0059728"}    
{"responseCode" : "400", "identifier" : "toronto", "message" : "No result"}  
"""