from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


# NBA season we will be analyzing
year = 2020
# URL page we will scraping (see image above)
url = "https://www.basketball-reference.com/leagues/NBA_{}_rookies.html".format(year)
# this is the HTML from the given URL
html = urlopen(url)
soup = BeautifulSoup(html)


# use findALL() to get the column headers that we need
soup.findAll('tr',limit=2)[2:]
# use getText()to extract the text we need into a list
headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
# exclude the second column as we will not need the ranking order from Basketball Reference for the analysis
headers = headers[1:]
headers

# avoid the first two header rows
rows = soup.findAll('tr')[3:]
player_stats = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]

stats = pd.DataFrame(player_stats, columns = headers)
stats.head(10)

print (stats)


