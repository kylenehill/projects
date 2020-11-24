import requests
import csv
import data
from urllib.request import urlopen
from bs4 import BeautifulSoup



#####
##### import text files of club and player data and set variables
#####

clubs = data.clubs
url_list = data.url_list
filename_list = data.filename_list

# can_provs is a dict with the 2 following variables lists of k/v values
can_provs = data.can_provs
can_provs_long = list(can_provs.keys())
can_provs_abr = list(can_provs.values())


# us_states is a dict with the 2 following variables lists of k/v values
us_states = data.us_states
us_states_long = list(us_states.keys())
us_states_abr = list(us_states.values())

states_cleaned = data.states_cleaned




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

	file = open(filename,"w") 
	file.write(player_list) 
	file.close()



# func to append and clean raw player_list.txt files to a single list of players
def create_players_list(filename):
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






#####
##### call function to create txt files of raw player data,
##### then function to return initial list of all players ('everyone')
#####
	
for url, filename in zip(url_list, filename_list):
	create_player_txt_file(url, filename)
print("please check the html txt files in dir..")


everyone = [] 

for filename in filename_list:
	#print("going through list:", filename)
	indiv_page_players_list = create_players_list(filename)
	everyone = everyone + indiv_page_players_list




#####
##### clean up list of players
##### part 1 - general
#####

drop_col_indx = [4, 5, 6, 7, 8]

# adjust and drop columns to align player fields
for player in everyone:

	if player[4] == 'Age:':
		player.insert(4, '')
		player.insert(5, '')

for player in everyone:
	try:
		for col in drop_col_indx:
			del player[col]
	except:
		#print('error with dropping columns in line: ', player)
		pass
	if len(player) > 8:
		del player[8:]



#convert number values to type int (jersey number, age, weight)
int_col_indx = [2, 5, 7]
for player in everyone:
	for col in int_col_indx:
		try:
			player[col] = int(player[col])
		except:
			#print('error with converting columns to int type in line: ', player, col)
			pass



# remove incorrect player attributes found in the weight column for select players
# convert missed numbers to int in weight col
for player in everyone:

	# if a values exists in the weight col and is type str
	if len(player) > 7:
		if type(player[7]) is str:

			# if the value is a weight number convert to int
			if len(player[7]) == 3:
				try:
					player[7] = int(player[7])
				except:
					print('failed to weight col value convert to int', player[7])
			else:
				player[7] = ''
			


#####
##### clean up list of players
##### part 2 - split and format hometown information into city, state, country .. (geo1, geo2, geo3)
#####

for person in everyone:

	# split hometown data into list of items
	location = person[4].split(',')
	location = [x.strip() for x in location]
	geo1 = location[0]


	# if location has only one item , set geo1 to geo3 and set geo1 and geo2 to blank. also 
	# add flag noting that these few need to be manually checked for geo
	if (len(location) == 1 and location != ['']) or (location == ['']):

		# if location is blank, set geo1, geo2, and geo3 to blank
		if location == ['']:
			person.insert(5, '')
			person.insert(5, '')

		# if location has 1 value, set value to geo3 and set geo1 and geo2 to blank, also add flag
		if (len(location) == 1 and location != ['']):
			person.insert(4, '')
			person.insert(4, '')
			person.append('** flag to manually check these geos')




	# formatting of location metadata to output geo data in long string format and not abbrv. (ex. "California", not 'CA')
	# if the location consists of two items (ie city, state // city, country etc) set geo2
	if len(location) == 2:

		geo2 = location[1].strip()

		# if the second geo item has length of 2, check if it's a US or CAN state
		if len(geo2) == 2:

			if geo2 in us_states_abr:
				geox = us_states_long[us_states_abr.index(geo2)]
				geo3 = 'United States of America'
				person[4] = geo1
				person.insert(5, geox)
				person.insert(6, geo3)

			elif geo2 in can_provs_abr:
				geox = can_provs_long[can_provs_abr.index(geo2)]
				geo3 = 'Canada'
				person[4] = geo1
				person.insert(5, geox)
				person.insert(6, geo3)

			else:
				print('didnt find state abr for geo2 of length 2', geo2)

		else:

			# manually confirmed all values with a period 
			# were truncated state names -- corrected these here and
			# where location has geo1 and geo2, 
			# check if geo2 is US/CAN state
			if '.' in geo2:

				if geo2 in states_cleaned:
					geox = states_cleaned[geo2]
					geo3 = 'United States of America'
					person[4] = geo1
					person.insert(5, geox)
					person.insert(6, geo3)

			elif geo2 in us_states_long:
				geo3 = 'United States of America'
				person[4] = geo1
				person.insert(5, geo2)
				person.insert(6, geo3)


			elif geo2 in can_provs_long:
				geo3 = 'Canada'
				person[4] = geo1
				person.insert(5, geo2)
				person.insert(6, geo3)


			else:

				# if location has length of 2 but is not a US/CAN,
				# assume geo1 is city and geo3 is country -- 
				# set geo3 to be geo2 and set geo2 to blank
				geo3 = geo2
				geo2 = ''
				person[4] = geo1
				person.insert(5, geo2)
				person.insert(6, geo3)





#####
##### write out final player list to csv
#####

filename = "mls_players_cleaned.csv"
     
with open(filename, 'w') as csvfile:  
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(everyone) 
      

print("cleaned file written to dir..")  

