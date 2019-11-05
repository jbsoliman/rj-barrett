from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


# NBA season we will be analyzing
year = 2020
# URL page we will scraping (see image above)
advanced_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_advanced.html".format(year)
url_rookies_default = "https://www.basketball-reference.com/leagues/NBA_{}_rookies.html".format(year)
url =  "https://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&match=single&type=per_game&per_minute_base=36&per_poss_base=100&season_start=1&season_end=1&draft_year=2019&lg_id=NBA&age_min=0&age_max=99&is_active=Y&is_playoffs=N&height_min=0&height_max=99&birth_country_is=Y&as_comp=gt&as_val=0&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&order_by=pts_per_g"
# this is the HTML from the given URL
html = urlopen(url)
soup = BeautifulSoup(html,from_encoding="utf-8")


# use findALL() to get the column headers that we need
soup.findAll('tr',limit=2)[2:]
# use getText()to extract the text we need into a list
headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
# exclude the second column as we will not need the ranking order from Basketball Reference for the analysis
headers = headers[1:]
headers

# avoid the first two header rows
rows = soup.findAll('tr')[2:]
player_stats = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]

stats = pd.DataFrame(player_stats, columns = headers)

print (stats)


###############################       LOADING TO HTML        #####################################

stats.to_html('index.html')
