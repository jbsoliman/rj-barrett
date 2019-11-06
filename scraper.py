from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


# NBA season we will be analyzing
year = 2020

##Default Rookie URL
url = "https://www.basketball-reference.com/leagues/NBA_{}_rookies.html".format(year)
##rookie PPG URL
rookie_ppg_url =  "https://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&match=single&type=per_game&per_minute_base=36&per_poss_base=100&season_start=1&season_end=1&draft_year=2019&lg_id=NBA&age_min=0&age_max=99&is_active=Y&is_playoffs=N&height_min=0&height_max=99&birth_country_is=Y&as_comp=gt&as_val=0&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&order_by=pts_per_g"
# this is the HTML from the given URL
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")
#soup = soup.encode("utf-8")


# use find_all() to get the column headers that we need
soup.find_all('tr',limit=2)[2:]
# use get_text()to extract the text we need into a list
headers = [th.get_text() for th in soup.find_all('tr', limit=2)[1].find_all('th')]
# exclude the second column as we will not need the ranking order from Basketball Reference for the analysis
headers = headers[1:]

# finds table rows (ignoring first two)
rows = soup.find_all('tr')[2:]
player_stats = [[td.get_text() for td in rows[i].find_all('td')]
            for i in range(len(rows))]


stats = pd.DataFrame(player_stats, columns = headers)

#Sorts table values by Age
stats = stats.sort_values(by=['Age'])
stats = stats.head(30)
print (stats)



# places the DataFrame into a html format without writing it
html = stats.to_html(index=False)


#HTML Skeleton
html_skeleton = """<HTML>
<body>
    <h1>RJ Barrett - Rookie of the Year?</h1>
    {}
</body>
</HTML>""".format(html)

# writes the html format to index.html with proper encoding
with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_skeleton)
