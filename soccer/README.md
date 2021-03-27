# Overview
The goal of this data wrangling was to be able to prepare a clean dataset in order to build a model that would predict the likelihood of a youth player from a given US region to play professionally for an Major League Soccer (MLS) team. Throughout this part of the data wrangling step I was able to pull together both nationoal youth soccer data: the history of the US Youth National Champions as recorded through the body of the United State Soccer Federation (also known as US Soccer), and data from Major League Soccer which represents the highest professional men's soccer league governed by US Soccer in the United States and Canada.


In order to obtain the MLS player data, as captured in mls_players_cleaned_filled.csv, I went to the MLS website (https://www.mlssoccer.com/players) and iterated through all current players in a handful of webpages to create a list of MLS players and their respective attributes: player name, MLS club, jersey number, hometown city, hometown state/province and home country. Using predefined functions in config.py, I was able to generate a raw list of the MLS players. After this was created, I massaged the data with the get_player_data.py script for further cleaning. 


For the US Youth National championship data, using the script in us_youth_national_champtions.py I scraped a webpage of all former youth national champions using the BeautifulSoup module and pulled the page's raw contents into a txt file before cleaning the data and rewriting to us_youth_national_champs_cleaned.csv. The file here has columns: age group, championship year, club name, club region and club state.



Some clear limitations of this dataset:
- only comparing to professional on the men's side, not able to account for female youth players going pro
- US youth players could later play professionally outside of the United States which would not be accounted for in terms of likelihood to go pro

I have folders of raw and cleaned data, as well as the scripts used to populate files in these repos.

## Next steps
I currently am working on a jupyter notebook for a report of my current status of project.
