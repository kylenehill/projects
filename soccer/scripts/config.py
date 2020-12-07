import requests
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup


#####
##### lists used in script: clubs, url_list, filename_list
#####


# clubs contains names of all MLS club teams
clubs =	['Atlanta United FC', 
			'Chicago Fire FC', 
			'Colorado Rapids', 
			'Columbus Crew SC', 	
			'D.C. United', 
			'FC Cincinnati', 
			'FC Dallas', 
			'Houston Dynamo FC', 
			'Inter Miami CF', 
			'LA Galaxy', 
			'Los Angeles Football Club', 
			'Minnesota United FC', 
			'Montreal Impact', 
			'Nashville SC', 
			'New England Revolution', 
			'New York City FC', 
			'New York Red Bulls', 
			'Orlando City SC', 
			'Philadelphia Union', 
			'Portland Timbers', 
			'Real Salt Lake', 
			'San Jose Earthquakes', 
			'Seattle Sounders FC', 
			'Sporting Kansas City', 
			'Toronto FC', 
			'Vancouver Whitecaps FC']


# url_list contains full list of urls with MLS player data
url_list = ['https://www.mlssoccer.com/players?sort=name&order=ASC',
			'https://www.mlssoccer.com/players?page=1&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=2&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=3&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=4&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=5&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=6&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=7&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=8&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=9&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=10&sort=name&order=ASC',
			'https://www.mlssoccer.com/players?page=11&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=12&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=13&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=14&sort=name&order=ASC',
			'https://www.mlssoccer.com/players?page=15&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=16&sort=name&order=ASC',
			'https://www.mlssoccer.com/players?page=17&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=18&sort=name&order=ASC',
			'https://www.mlssoccer.com/players?page=19&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=20&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=21&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=22&sort=name&order=ASC',
			'https://www.mlssoccer.com/players?page=23&sort=name&order=ASC', 
			'https://www.mlssoccer.com/players?page=24&sort=name&order=ASC',
			'https://www.mlssoccer.com/players?page=25&sort=name&order=ASC']


# filename_list is list of txt files containing player data from urls
filename_list = ['player_list.txt',
				'players_list1.txt', 
				'players_list2.txt',
				'players_list3.txt', 
				'players_list4.txt', 
				'players_list5.txt', 
				'players_list6.txt',
				'players_list7.txt', 
				'players_list8.txt',
				'players_list9.txt', 
				'players_list10.txt',
				'players_list11.txt', 
				'players_list12.txt',
				'players_list13.txt', 
				'players_list14.txt',
				'players_list15.txt', 
				'players_list16.txt', 
				'players_list17.txt', 
				'players_list18.txt',
				'players_list19.txt', 
				'players_list20.txt',
				'players_list21.txt', 
				'players_list22.txt',
				'players_list23.txt', 
				'players_list24.txt',
				'players_list25.txt']


# can_provs (fornerly geo_can) is a dict of Canadian provinces and their corresponding abbreviations
can_provs = {"British Columbia":'BC', 
			"Ontario":'ON', 
			"Alberta":'AB', 
			"Quebec":'QC', 
			'Manitoba': 'MB',
			'New Brunswick': 'NB',
			'Newfoundland and Labrador': 'NL',
			'Northwest Territories':'NT',
			'Nova Scotia': 'NS',
			'Nunavut': 'NU',
			'Prince Edward Island':'PE',
			'Saskatchewan':'SK',
			'Yukon':'YT'}



# us_states (formerly states) is a dict of all states in the US and the corresponding state abbreviations
us_states = {
	"Alabama": 'AL',
	"Alaska": 'AK',
	"Arizona": 'AZ',
	"Arkansas": 'AR',
	"California": 'CA',
	"Colorado": 'CO',
	"Connecticut": 'CT',
	"Delaware": 'DE',
	"Florida": 'FL',
	"Georgia": 'GA',
	"Hawaii": 'HI',
	"Idaho": 'ID',
	"Illinois": 'IL',
	"Indiana": 'IN',
	"Iowa": 'IA',
	"Kansas":'KS',
	"Kentucky": 'KY',
	"Louisiana": 'LA',
	"Maine": 'ME',
	"Maryland": 'MD',
	"Massachusetts": 'MA',
	"Michigan": 'MI',
	"Minnesota": 'MN',
	"Mississippi": 'MS',
	"Missouri": 'MO',
	"Montana": 'MT',
	"Nebraska": 'NE',
	"Nevada": 'NV',
	"New Hampshire": 'NH',
	"New Jersey": 'NJ',
	"New Mexico": 'NM',
	"New York" : 'NY',
	"North Carolina": 'NC',
	"North Dakota": 'ND',
	"Ohio": 'OH',
	"Oklahoma": 'OK',
	"Oregon": 'OR',
	"Pennsylvania": 'PA',
	"Rhode Island": 'RI',
	"South Carolina": 'SC',
	"South Dakota": 'SD',
	"Tennessee": 'TN',
	"Texas": 'TX',
	"Utah": 'UT',
	"Vermont": 'VT',
	"Virginia": 'VA',
	"Washington": 'WA',
	"West Virginia" : 'WV',
	"Wisconsin": 'WI',
	"Wyoming": 'WY'
}


# formerly clean_abr_states
states_cleaned = {'Kan.': 'Kansas',
					'Md.': 'Maryland', 
					'Pa.': 'Pennsylvania',
					'Tenn.': 'Tennessee', 
					'Wis.':'Wisconsin', 
					'Mass.':'Massachusetts', 
					'N.Y.':'New York', 
					'Colo.':'Colorado', 
					'Mo.':'Montana', 
					'Ariz.':'Arizona', 
					'N.J.':'New Jersey', 
					'Ill.': 'Illinois', 
					'Fla.':'Florida', 
					'Calif.':'California', 
					'Ind.':'Indiana', 
					'La.':'Louisiana'}




#####
##### functions used in script
#####

# func to get html text from url and create player_list.txt file with subset
# of raw html text, specifically player info, to further clean and analyze
def create_player_txt_file(url, filename):

	html_text = requests.get(url).text
	soup = BeautifulSoup(html_text, 'html.parser')

	# subsets on player list
	player_list = soup.find('div', {'class':'item-list'}).text

	filename = '../raw_data/' + filename
	file = open(filename,"w") 
	file.write(player_list) 
	file.close()



# func to append and clean raw player_list.txt files to a single list of players
def create_players_list(filename):

	filename = '../raw_data/' + filename
	data = open(filename, 'r').read()
	lines = data.splitlines()

	players = []
	player_info = [] 

	# appends each line of file (which corresponds to a single player) to list of players
	for info in lines:
		if info == 'View More':
			players.append(player_info)
			player_info = []
		else:
			player_info.append(info)


	## first pass of cleanup of list of players -specificaly on Club and Age columns,
	## to align properties of players
	for player in players:
		for club in clubs:
			if club in player[0]:
				#print('team found:', club)
				team = club
				player[0] = player[0].replace(club,'')
				player.insert(1, team)

		# removes and aligns column of 'Age:' where applicable
		for meta in player:
			if meta == 'Age:':
				continue
			else:
				if 'Age:' in meta:
					meta_indx = meta.index('Age:')
					player_indx = player.index(meta)
					age = 'Age:'
					player.insert((player_indx + 1), age) 
					player[player_indx] = player[player_indx].replace('Age:', '')

	return players




