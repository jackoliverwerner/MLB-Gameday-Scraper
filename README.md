# MLB-Gameday-Scraper
#### Functions for scraping MLB Gameday pitch data

## Overview
This repository contains two Python scripts. The first, scrapeGameday.py, provides functions needed to scrape data from the MLB Gameday site. The second, scrapeGamedayDriver.py, gives an example of using these functions in sequence to scrape the data.

A quick overview of the workflow: first the script uses the writeURLs function to create a text file with all of the Gameday IDs for each game in a season. This function uses data from [Baseball Reference](www.baseball-reference.com). Then the script uses the file scrapeURLs to scrape the pitch data associated with each Gameday ID and save them locally as individual XML files. Finally the script uses the directoryToCSV function to parse these files into a CSV containing all of the data for that season.
