# 8a.nu Scraper
Scrape the world's largest rock climbing logbook!

### Pitch
Who's the biggest downgrader? Is it better to be short, tall, or average height? How many years does it take the average climber to send her first 5.12? After countless crag debates over these and similar topics, I set out to find the answers. Now you can prove <b><i>statistically</i></b> why that dude who tagged your multi-year project "Soft" is wrong. (Sorry, he might actually be right.)

## Overview
I used Python3 to build a web-scraper to collect all of the user and ascent information from the world's largest rock climbing logbook, https://www.8a.nu/. I actually ended up scraping their beta site, https://beta.8a.nu/, as it provided well-formed JSON objects. The scraper dumps all of the data into an SQLite database.

## Contents
1. `8ascraper.py` - This Python3 module does the heavy lifting. Run it from the shell. I ran it in 5,000 user increments concurrently in separate Terminal sessions. Ideally, on the next scraping pass to update the database, I will implement better parallelism :). It will prompt you for three inputs:
    1. The starting user ID number (inclusive)
    2. The final user ID number (inclusive)
    3. y/n to start scraping
2. `databasesetup.py` - This Python3 module initializes the SQLite database and, using SQLAlchemy, provides the Base and table interaction for `8ascraper.py`.
3. `formatter.json` - This is an example of the JSON object that is included in each user's log on the 8a.nu beta site. It's very large! If you use Atom, I recommend the package `Pretty JSON` to make it much easier to parse.

### Requirements
1. Python3 and standard libraries
2. The following Python3 libraries:
    1. SQLAlchemy (`pip3 install sqlalchemy`)
    2. BeautifulSoup (`pip3 install bs4`)
    3. Requests (`pip3 install requests`)

### Accessing the Data
If you're not interested in running the scripts yourself, I am hosting the dataset on Kaggle at https://www.kaggle.com/dcohen21/8anu-climbing-logbook. This data was collected on 9/13/2017. Analyze away!

##### Notes
1. As of 9/13/2017, there were 67025 users (some deactivated, some anonymous). I'm sure there are more now.
2. `ascent.date` (date the ascent occurred) and `ascent.recdate` (date the ascent was entered into the log) are stored as Unix timestamps.
3. `ascent.climb_type` maps as follows: 0: route, 1: boulder.
4. `ascent.notes` is where "Soft", "Second Go", and "First Ascent" are stored.

### Future Directions
There are so many questions that can be asked of this dataset, which is why I am open-sourcing it. Please share your findings!

I would like to build a route-recommendation engine based on this data. If you're interested in collaborating or have any ideas you want to share, message me.

### Acknowledgments
Thanks to Andrew Cassidy (https://github.com/andrewcassidy) for the idea and mentorship. Thanks to Jens Larssen and 8a.nu for creating the logbook and maintaining a thriving community.
