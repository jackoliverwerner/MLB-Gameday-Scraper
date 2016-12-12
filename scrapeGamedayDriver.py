from scrapeGameday import *

# Make URLs
url_dir = '/Users/jackwerner/Documents/My Stuff/Baseball/Scraping Files/Game IDs'
writeURLs(2014, url_dir)

# Save XML files
xml_dir = '/Users/jackwerner/Documents/My Stuff/Baseball/Scraping Files/Game IDs/2014xml'
scrapeURLs(url_dir, xml_dir, verbose = True)

# Make into CSV
directoryToCSV(xml_dir, "pitch_data_2014.csv")