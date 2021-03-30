## NBA Rookie Stat Tracker

This project parses through the 2020-2021 NBA Rookie Statistics from Basketball-Reference.com and ranks a targeted player among league leaders in the following stats:
* Points Per Game
* Rebounds Per Game
* Assists Per Game

Created for educational purposes only.

### Technologies used:
* Python
    * BeautifulSoup
        * Parses through bballref page
    * pandas (Dataframe)
        * Stores needed data into table
        * Data is sorted to provide rankings for various stats
* HTML
    * Displays ranked stats as well as a table sorted by current stat based on page
* CSS
    * Highlights RJ Barrett's row as well as highlights specific row/column on mouse hover


#### Update 0.01:
* Added daily updating of pages through Windows Task Scheduler
