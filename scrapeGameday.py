'''
Collection of functions for scraping MLB Gameday data

getTeamURLs: Output a list of URLs for one team in one season.
	- ARG 'year': Desired season
	- ARG 'team': Desired team (abbreviated)
	- OUTPUT: list of URLs

writeURLs: Write all URLs for a given season to a file.
	- ARG 'year': Desired season
	- ARG 'location': desired location of output file
	- OUTPUT: saves file of game URLs for a whole season

scrapeURLs: Take a file of URLs, save them as xml documents
	- ARG 'URLFileName': file containing URLs
	- ARG 'saveDir': desired location of output files
	- ARG 'verbose': should progress be printed?
	- OUTPUT: saves xml files for each game in the URL file

makeList: Helper function, turns a tag's given values into a list
	- ARG 'tag': Desired tag
	- ARG 'names': List of elements of interest
	- OUTPUT: list of tag values

xmlToCSV: Format an xml file and save in a CSV
	- ARG 'xmlfile': XML file of interest
	- ARG 'csvfile': Output file
	- OUTPUT: saves CSV with XML data 

directoryToCSV: Format a directory of CSV files into one CSV 
	- ARG 'directory': Folder containing the XML files
	- ARG 'outFileName': Name of output CSV file 
	- OUTPUT: saves CSV with XML data

'''
import urllib
from bs4 import BeautifulSoup
import re
import os
import sets


def getTeamURLs(year, team):

	if year >= 2012:
		teamsDict = {'TOR':'tor', 'NYY':'nya', 'BAL':'bal', 'TBR':'tba', 'BOS':'bos',
						'KCR':'kca', 'MIN':'min', 'CLE':'cle', 'CHW':'cha', 'DET':'det', 
						'TEX':'tex', 'HOU':'hou', 'LAA':'ana', 'SEA':'sea', 'OAK':'oak', 
						'NYM':'nyn', 'WSN':'was', 'MIA':'mia', 'ATL':'atl', 'PHI':'phi', 
						'STL':'sln', 'PIT':'pit', 'CHC':'chn', 'MIL':'mil', 'CIN':'cin',
						'LAD':'lan', 'SFG':'sfn', 'ARI':'ari','SDP':'sdn', 'COL':'col'}
	elif 2008 <= year <= 2011:
		teamsDict = {'TOR':'tor', 'NYY':'nya', 'BAL':'bal', 'TBR':'tba', 'BOS':'bos',
						'KCR':'kca', 'MIN':'min', 'CLE':'cle', 'CHW':'cha', 'DET':'det', 
						'TEX':'tex', 'HOU':'hou', 'LAA':'ana', 'SEA':'sea', 'OAK':'oak', 
						'NYM':'nyn', 'WSN':'was', 'FLA':'flo', 'ATL':'atl', 'PHI':'phi', 
						'STL':'sln', 'PIT':'pit', 'CHC':'chn', 'MIL':'mil', 'CIN':'cin',
						'LAD':'lan', 'SFG':'sfn', 'ARI':'ari','SDP':'sdn', 'COL':'col'}
	else:
		teamsDict = {'TOR':'tor', 'NYY':'nya', 'BAL':'bal', 'TBD':'tba', 'BOS':'bos',
						'KCR':'kca', 'MIN':'min', 'CLE':'cle', 'CHW':'cha', 'DET':'det', 
						'TEX':'tex', 'HOU':'hou', 'LAA':'ana', 'SEA':'sea', 'OAK':'oak', 
						'NYM':'nyn', 'WSN':'was', 'FLA':'flo', 'ATL':'atl', 'PHI':'phi', 
						'STL':'sln', 'PIT':'pit', 'CHC':'chn', 'MIL':'mil', 'CIN':'cin',
						'LAD':'lan', 'SFG':'sfn', 'ARI':'ari','SDP':'sdn', 'COL':'col'}

	schedURL = 'http://www.baseball-reference.com/teams/' + team + \
	'/' + str(year) + '-schedule-scores.shtml'

	urls = []


	monthMatch = {'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 
		'Aug': '08', 'Sep': '09','Oct': '10', 'Nov': '11'}

	schedPre = urllib.urlopen(schedURL).read()
	sched = BeautifulSoup(schedPre, "lxml")

	gamesTab = sched.findAll('table', id = 'team_schedule')[0].findAll('tbody')[0].findAll('tr', {'class':''})

	for i in gamesTab:
		if len(i.findAll('td')) < 6:
			continue

		#Deal with team names
		if len(i.findAll('td')[5].contents) > 0:
			homeTeam = teamsDict[str(i.findAll('td')[4].contents[0])]
			awayTeam = teamsDict[str(i.findAll('td')[6].findAll('a')[0].contents[0])]
		else:
			awayTeam = teamsDict[str(i.findAll('td')[4].contents[0])]
			homeTeam = teamsDict[str(i.findAll('td')[6].findAll('a')[0].contents[0])]

		#Deal with doubleheaders
		fullDate = str(i.findAll('td')[2].contents)
		if re.search('\(2\)', fullDate) == None:
			dhead = '1'
		else:
			dhead = '2'

		#Deal with the date
		try:
			date = i.findAll('td')[2].findAll('a')[0].contents[0]
		except:
			break

		monthChar = re.search('\s...\s' , date).group().strip()
		monthNum = monthMatch[monthChar]

		dateDay = re.search('\s[0-9]{1,2}', date).group().strip()

		if len(dateDay) < 2:
			dateDay = '0' + dateDay


		newURL = 'http://gd2.mlb.com/components/game/mlb/year_' + str(year) + '/month_' + \
			monthNum + '/day_' + dateDay + '/gid_' + str(year) + '_' + monthNum + '_' + \
			dateDay + '_' + homeTeam + 'mlb_' + awayTeam + 'mlb_' + dhead

		urls.append(newURL)

	return(urls)


def writeURLs(year, location):

	if year >= 2012:
		teamsDict = {'TOR':'tor', 'NYY':'nya', 'BAL':'bal', 'TBR':'tba', 'BOS':'bos',
						'KCR':'kca', 'MIN':'min', 'CLE':'cle', 'CHW':'cha', 'DET':'det', 
						'TEX':'tex', 'HOU':'hou', 'LAA':'ana', 'SEA':'sea', 'OAK':'oak', 
						'NYM':'nyn', 'WSN':'was', 'MIA':'mia', 'ATL':'atl', 'PHI':'phi', 
						'STL':'sln', 'PIT':'pit', 'CHC':'chn', 'MIL':'mil', 'CIN':'cin',
						'LAD':'lan', 'SFG':'sfn', 'ARI':'ari','SDP':'sdn', 'COL':'col'}
	elif 2008 <= year <= 2011:
		teamsDict = {'TOR':'tor', 'NYY':'nya', 'BAL':'bal', 'TBR':'tba', 'BOS':'bos',
						'KCR':'kca', 'MIN':'min', 'CLE':'cle', 'CHW':'cha', 'DET':'det', 
						'TEX':'tex', 'HOU':'hou', 'LAA':'ana', 'SEA':'sea', 'OAK':'oak', 
						'NYM':'nyn', 'WSN':'was', 'FLA':'flo', 'ATL':'atl', 'PHI':'phi', 
						'STL':'sln', 'PIT':'pit', 'CHC':'chn', 'MIL':'mil', 'CIN':'cin',
						'LAD':'lan', 'SFG':'sfn', 'ARI':'ari','SDP':'sdn', 'COL':'col'}
	else:
		teamsDict = {'TOR':'tor', 'NYY':'nya', 'BAL':'bal', 'TBD':'tba', 'BOS':'bos',
						'KCR':'kca', 'MIN':'min', 'CLE':'cle', 'CHW':'cha', 'DET':'det', 
						'TEX':'tex', 'HOU':'hou', 'LAA':'ana', 'SEA':'sea', 'OAK':'oak', 
						'NYM':'nyn', 'WSN':'was', 'FLA':'flo', 'ATL':'atl', 'PHI':'phi', 
						'STL':'sln', 'PIT':'pit', 'CHC':'chn', 'MIL':'mil', 'CIN':'cin',
						'LAD':'lan', 'SFG':'sfn', 'ARI':'ari','SDP':'sdn', 'COL':'col'}

	fileFull = location + '/urls' + \
	    str(year) + '.txt'

	allURLs = []

	c = 1

	for i in teamsDict:
		allURLs = allURLs + getTeamURLs(year, i)

		print 'Completed ' + str(c) + '/30'
		c += 1

	allURLs = list(set(allURLs))

	outFile = open(fileFull, 'w')

	for i in allURLs:
		outFile.write(i)
		outFile.write('\n')


def scrapeURLs(URLFileName, saveDir, verbose):
	urls = open(URLFileName, 'r')


	j = 1
	#included for connection purposes
	#if there's a documented last URL, run the URL file until it gets there without adding data
	keyURL = open('keyURL.txt', 'r')
	lastURL = keyURL.readline()
	if lastURL != '':
		for i in urls:
			j += 1
			if i == lastURL:
				break
	keyURL.close()


	for i in urls:
		# Get URL, add suffix to it
		pageURL = i.rstrip() + '/inning/inning_all.xml'

		# Get game ID, used in XML file name
		gid = i.split('/')[9].rstrip()

		# Make location and name for new XML file
		saveFile = saveDir + '/' + gid + '.xml'

		# Get the actual XML text of the page
		txt = urllib.urlopen(pageURL).read()

		# Open, write, save
		f = open(saveFile, 'w')
		f.write(txt)
		f.close()

		# Print progress
		if verbose:
			print str(j) + ": " + gid
			j += 1

		# Save last URL in case connection cuts out
		k = open('keyURL.txt', 'w')
		k.write(i)
		k.close()

	# Close URL file
	urls.close()


def makeList(tag, names):
	outList = []
	for i in names:
		outList.append(str(tag.get(i, 'NULL')).strip().replace(',', ''))
	return(outList)


def xmlToCSV(xmlfile, csvfile):

	# Define the elements to collect at each level
	cols_inning = ['num', 'away_team', 'home_team']

	cols_ab = ['num', 'b', 's', 'o', 'start_tfs', 'batter', 'stand', 
	'b_height', 'pitcher', 'p_throws', 'event', 'home_team_runs', 
	'away_team_runs']

	cols_pitch = ['des', 'id', 'type', 'x', 'y', 'start_speed', 'end_speed',
	'sz_top', 'sz_bot', 'pfx_x', 'pfx_z', 'px', 'pz', 'x0', 'y0', 'z0', 
	'vx0', 'vy0', 'vz0', 'ax', 'ay', 'az', 'break_y', 'break_angle', 
	'break_length', 'pitch_type', 'type_confidence', 'sv_id', 'spin_dir',
	'spin_rate']

	# Open file, get right set of tags
	with open(xmlfile, 'r') as g:
		txt = g.read()
	tab = BeautifulSoup(txt, 'lxml')

	# Data will go here
	dataLines = []

	# Also extract the game ID from the filepath
	gid = re.search("gid.*\.", xmlfile).group().strip(".")

	# Loop through innings
	innings = tab.find_all('inning')

	for inn in innings:
		# Initialize data applying to the whole inning
		inningData = [gid] + makeList(inn, cols_inning)

		# Go through the top of the inning, collect data on AB and pitch
		for j in inn.top.find_all('atbat'):
			abData = ['top'] + makeList(j, cols_ab)
			for k in j.find_all('pitch'):
				pitchData = makeList(k, cols_pitch)
				fullLine = inningData + abData + pitchData
				dataLines.append(str(fullLine).strip('[]').replace("'", "").replace(", ", ",").replace("NULL","") + '\n')

		# Go through the bottom of the inning (if present), collect data on AB and pitch
		try:
			for j in inn.bottom.find_all('atbat'):
				abData = ['bot'] + makeList(j, cols_ab)
				for k in j.find_all('pitch'):
					pitchData = makeList(k, cols_pitch)
					fullLine = inningData + abData + pitchData
					dataLines.append(str(fullLine).strip('[]').replace("'", "").replace(", ", ",").replace("NULL","") + '\n')
		except:
			pass


	# Write the data to a file
	csvfile.writelines(dataLines)
	return dataLines


def directoryToCSV(directory, outFileName):
	outFile = open(outFileName, 'a')
	
	outFile.write('gid, inning, away_team, home_team, half_inning, ab_num, b, s, o, ' +
		'start_tfs, batter, b_hand, b_height, pitcher, p_throws, event, ' +
		'home_team_runs, away_team_runs, ' +
		'pitch_result, id, type, x, y, start_speed, end_speed,  sz_top, ' +
		'sz_bot, pfx_x, pfx_z, px, pz, x0, y0, z0, vx0, vy0, vz0, ax, ay, ' +
		'az, break_y, break_angle, break_length, pitch_type, type_confidence, ' +
		'sv_id, spin_dir, spin_rate\n')



	numFiles = len(os.listdir(directory))
	j = 1

	for i in os.listdir(directory):
		if not i.startswith('.'):
			fullPath = directory + '/' + i
			xmlToCSV(fullPath, outFile)

			print str(j) + '/' + str(numFiles)
			j += 1

	outFile.close()
