import requests
import csv
import data
from urllib.request import urlopen
from bs4 import BeautifulSoup

####
#### PART 1 - set variables
####

us_states = data.us_states
us_states_long = list(us_states.keys())
us_states_abr = list(us_states.values())




####
#### PART 2 - create txt file with data from webpage
####

url = 'http://championships.usyouthsoccer.org/PastNationalChamps/PastUSYouthSoccerNationalChampionshipWinners19352007/#19_Girls'
filename = 'us_youth_national_champions.txt'

html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'lxml')

blob = soup.find('div', {'class': 'block'}).text

file = open(filename,"w") 
file.write(blob) 
file.close()





####
#### PART 3
#### open txt file with data, clean and format row to [category, year, team, region, state]
####
filename = 'us_youth_national_champions_raw.txt'
data = open(filename, 'r').read()
lines = data.splitlines()

all_winners = []

for line in lines:
	try:
		line = line.strip()

		if (line[0] == 'G' or line[0] == 'B'):
			categories = line.split('-')
			category = categories[0]

		else:
			year = int(line[0:4])
			team, region = line.split(',')
			team = team.replace(str(year), '').strip()
			region = region.strip()
			winner = [category, year, team, region]
			all_winners.append(winner)
	except:
		continue


####
#### add column with state name to row, depeding on region
for champ in all_winners:

	region = champ[3].split('-')
	for part in region:

		# this denotes a particular region in state such as the 'N' in CA-N 
		if len(part) == 1:
			continue

		# this denotes the state such as 'CA' in CA-N 
		if len(part) == 2:
			part2 = part

			if part2 in us_states_abr:
				state_name = us_states_long[us_states_abr.index(part2)]
				champ.append(state_name)
 


####
#### PART 4
#### write out list of winners to csv file
####

filename = 'us_youth_national_champs_cleaned.csv'

with open(filename, 'w') as csvfile:  
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(all_winners) 

print("cleaned file written to dir..")  

