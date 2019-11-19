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
def make_html(html,table_title):
    html_skeleton = """<!DOCTYPE html>
    <HTML lang="en">
    <head>
    <link rel="icon" href="https://user-images.githubusercontent.com/16616543/38898937-6a56f3b0-4264-11e8-997d-139dccf4314d.png">
    <link rel="stylesheet" type="text/css" href="style.css">
    <title>RJ Barrett Rookie Stat Tracker</title>
    </head>
    <body>

        <h1><a href="https://jbsoliman.github.io/rj-barrett">RJ Barrett - Rookie of the Year? Here are the facts.</a></h1>
        <h3>Among all Rookies, RJ Barrett is:
        <ul>
        <li><a href="https://jbsoliman.github.io/rj-barrett/ppg">#{} in Points Per Game</a></li>
        <li><a href="https://jbsoliman.github.io/rj-barrett/rpg">#{} in Rebounds Per Game</a></li>
        <li><a href="https://jbsoliman.github.io/rj-barrett/apg">#{} in Assists Per Game</a></li>
        </ul>
        </h3>

        <h3>Here are the leaders in {}:</h3>
        {}
    </body>
    </HTML>""".format(rj_ppg_rank,rj_rpg_rank,rj_apg_rank,table_title,html)

    return html_skeleton

#Row/Column Highlighting from https://css-tricks.com/simple-css-row-column-highlighting/
def make_css(row):
    css_skeleton = """html, body, h1, h2, h3, h4, h5, h6 {{
    font-family: "Trebuchet MS", Helvetica, sans-serif;
    }}
    body {{
        background-color: #BEC0C2;
    }}
    table {{
        overflow: hidden;


    }}
    table tbody tr:nth-of-type({}){{background-color: #F58426;}}
    tr:hover {{ background-color: #ffa;}}
    th {{
        background-color: #006BB6;
        text-align: left;
        }}
    td, th {{
        position: relative;
    }}
    td:hover::after,
    th:hover::after {{
        content: "";
        position: absolute;
        background-color: #ffa !important;
        left: 0;
        top: -5000px;
        height: 10000px;
        width: 100%;
        z-index: -1;
    }}

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
stats["mp_rank"]=stats["MP"].rank(ascending=False,method='first')
stats["ppg_rank"]=stats["PPG"].rank(ascending=False,method='first')
#stats["blk_rank"]=stats["BLK"].rank(ascending=False,method='first')
stats["rpg_rank"]=stats["RPG"].rank(ascending=False,method='first')
stats["apg_rank"]=stats["APG"].rank(ascending=False,method='first')

#removes the "empty" tables
stats = stats.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)

#retreive values for RJ Barrett
rj_mp_rank = stats.at[1,'mp_rank']
rj_ppg_rank = stats.at[1,'ppg_rank']
#rj_blk_rank = stats.at[1,'blk_rank']
rj_rpg_rank = stats.at[1,'rpg_rank']
rj_apg_rank = stats.at[1,'apg_rank']

#Converting ranks to INTS for HTML
rj_mp_rank = int(rj_mp_rank)
rj_ppg_rank = int(rj_ppg_rank)
#rj_blk_rank = int(rj_blk_rank)
rj_rpg_rank = int(rj_rpg_rank)
rj_apg_rank = int(rj_apg_rank)


#Dropping unneeeded columns from table
stats = stats.drop('mp_rank', axis=1)
stats = stats.drop('ppg_rank', axis=1)
#stats = stats.drop('blk_rank', axis=1)
stats = stats.drop('rpg_rank', axis=1)
stats = stats.drop('apg_rank', axis=1)
stats = stats.drop('Debut', axis=1)
stats = stats.drop('Yrs', axis=1)


#Sorts table values by MP Descending
stats = stats.sort_values(by=['MP'],ascending=False)
ppg_stats = stats.sort_values(by=['PPG'],ascending=False)
#blk_stats = stats.sort_values(by=['BLK'],ascending=False)
apg_stats = stats.sort_values(by=['APG'],ascending=False)
rpg_stats = stats.sort_values(by=['RPG'],ascending=False)

stats = stats.head(20)
ppg_stats = ppg_stats.head(20)
apg_stats = apg_stats.head(20)
rpg_stats = rpg_stats.head(20)



# places the DataFrame into a html format without writing it
home_html = stats.to_html(index=False)
ppg_html = ppg_stats.to_html(index=False)
#blk_html = blk_stats.to_html(index=False)
apg_html = apg_stats.to_html(index=False)
rpg_html = rpg_stats.to_html(index=False)






# writes the html format to index.html with proper encoding
with open("index.html", "w", encoding="utf-8") as file:
    file.write(make_html(home_html,'total minutes'))

with open("ppg/index.html", "w", encoding="utf-8") as file:
    file.write(make_html(ppg_html,'Points Per Game'))

#with open("blk/index.html", "w", encoding="utf-8") as file:
#    file.write(make_html(blk_html))

with open("apg/index.html", "w", encoding="utf-8") as file:
    file.write(make_html(apg_html,'Assists Per Game'))

with open("rpg/index.html", "w", encoding="utf-8") as file:
    file.write(make_html(rpg_html,'Rebounds Per Game'))


with open("style.css", "wt") as file:
    file.write(make_css(rj_mp_rank))

with open("ppg/style.css", "wt") as file:
    file.write(make_css(rj_ppg_rank))

#with open("blk/style.css", "wt") as file:
#    file.write(make_css(rj_blk_rank))

with open("apg/style.css", "wt") as file:
    file.write(make_css(rj_apg_rank))

with open("rpg/style.css", "wt") as file:
    file.write(make_css(rj_rpg_rank))
