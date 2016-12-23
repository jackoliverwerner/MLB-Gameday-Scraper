from scrapeGameday import *

# Make URLs
url_dir = '/Users/jackwerner/Documents/My Stuff/Baseball/Scraping Files/Game IDs'
writeURLs(2016, url_dir)

# Save XML files
xml_dir = '/Users/jackwerner/Documents/My Stuff/Baseball/Scraping Files/Game IDs/2016xml'
url_file = url_dir + '/urls2016.txt'
scrapeURLs(url_file, xml_dir, verbose = True)

# Make into CSV
directoryToCSV(xml_dir, "pitch_data_2016.csv")
