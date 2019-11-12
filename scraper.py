from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True

def isint(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b


#HTML Skeleton
def make_html(html):
    html_skeleton = """<!DOCTYPE html>
    <HTML>
    <head>
    <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>

        <h1>RJ Barrett - Rookie of the Year?</h1>
        <h3>RJ Barrett is:
        <ul>
        <li><a href="https://jbsoliman.github.io/rj-barrett/ppg/">#{} in Points Per Game</a></li>
        <li><a href="https://jbsoliman.github.io/rj-barrett/blk/">#{} in Total Blocks</a></li>
        <li><a href="https://jbsoliman.github.io/rj-barrett/rpg/">#{} in Rebounds Per Game</a></li>
        <li><a href="https://jbsoliman.github.io/rj-barrett/apg/">#{} in Assists Per Game</a></li>
        </ul>
        </h3>
        {}
    </body>
    </HTML>""".format(rj_ppg_rank, rj_blk_rank,rj_rpg_rank,rj_apg_rank,html)

    return html_skeleton


def make_css(row):
    css_skeleton = """table tr:nth-of-type({}){{background-color: coral;}}

    """.format(str(row))

    return css_skeleton

#def find_row(df):
#    for i in range(len(df.index)):
#        if df.at[i,'Player'] == 'RJ Barrett':
#            return i




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



# converting table to floats for sorting // setting rank for ppg
for i in range(len(player_stats)):
    for j in range(len(player_stats[i])):
        if isfloat(player_stats[i][j]):
            player_stats[i][j] = float(player_stats[i][j])

# Renaming the per game columns for later ranking
headers[23] = 'MPG'
headers[24] = 'PPG'
headers[25] = 'RPG'
headers[26] = 'APG'


stats = pd.DataFrame(player_stats, columns = headers)
stats["ppg_rank"]=stats["PPG"].rank(ascending=False)
stats["blk_rank"]=stats["BLK"].rank(ascending=False,method='first')
stats["rpg_rank"]=stats["RPG"].rank(ascending=False)
stats["apg_rank"]=stats["APG"].rank(ascending=False)

#removes the "empty" tables
stats = stats.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

#retreive values for RJ Barrett

rj_ppg_rank = stats.at[1,'ppg_rank']
rj_blk_rank = stats.at[1,'blk_rank']
rj_rpg_rank = stats.at[1,'rpg_rank']
rj_apg_rank = stats.at[1,'apg_rank']

#Converting ranks to INTS for HTML
rj_ppg_rank = int(rj_ppg_rank)
rj_blk_rank = int(rj_blk_rank)
rj_rpg_rank = int(rj_rpg_rank)
rj_apg_rank = int(rj_apg_rank)


#Dropping ranking columns from table
stats = stats.drop('ppg_rank', axis=1)
stats = stats.drop('blk_rank', axis=1)
stats = stats.drop('rpg_rank', axis=1)
stats = stats.drop('apg_rank', axis=1)



#Sorts table values by MP Descending
stats = stats.sort_values(by=['MP'],ascending=False)
ppg_stats = stats.sort_values(by=['PPG'],ascending=False)
blk_stats = stats.sort_values(by=['BLK'],ascending=False)
apg_stats = stats.sort_values(by=['APG'],ascending=False)
rpg_stats = stats.sort_values(by=['RPG'],ascending=False)

stats = stats.head(30)
print (stats)
print (headers)


# places the DataFrame into a html format without writing it
home_html = stats.to_html(index=False)
ppg_html = ppg_stats.to_html(index=False)
blk_html = blk_stats.to_html(index=False)
apg_html = apg_stats.to_html(index=False)
rpg_html = rpg_stats.to_html(index=False)






# writes the html format to index.html with proper encoding
with open("index.html", "w", encoding="utf-8") as file:
    file.write(make_html(home_html))

with open("ppg/index.html", "w", encoding="utf-8") as file:
    file.write(make_html(ppg_html))

with open("blk/index.html", "w", encoding="utf-8") as file:
    file.write(make_html(blk_html))

with open("apg/index.html", "w", encoding="utf-8") as file:
    file.write(make_html(apg_html))

with open("rpg/index.html", "w", encoding="utf-8") as file:
    file.write(make_html(rpg_html))


with open("ppg/style.css", "wt") as file:
    file.write(make_css(rj_ppg_rank))

with open("blk/style.css", "wt") as file:
    file.write(make_css(rj_blk_rank))

with open("apg/style.css", "wt") as file:
    file.write(make_css(rj_apg_rank))

with open("rpg/style.css", "wt") as file:
    file.write(make_css(rj_rpg_rank))
