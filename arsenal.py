import time
import telebot
from time import sleep
import requests
from bs4 import BeautifulSoup
import datetime as dt
from datetime import timedelta

URL_SPORTS_RU = 'https://www.sports.ru/arsenal/'
FILENAME_LAST_MATCH = 'last_match.txt'

def check_new_posts_vk():
	logging.info('[VK] Started scanning for new posts')
	with open(FILENAME_VK, 'rt') as file:
		last_id = int(file.read())
		if last_id is None:
			logging.error('Could not read from storage. Skipped Iteration.')
			return
		logging.info('Last ID (VK) = {!s}'.format(last_id))
	try:
		feed = get_data()
		if feed is not None:
			entries = feed['response'][1:]
			try:
				tmp = entries[0]['is_pinned']
				send_new_posts(entries[1:], last_id)
			except KeyError:
				send_new_posts(entries, last_id)
			with open(FILENAME_VK, 'wt') as file:
				try:
					tmp = entries[0]['is_pinned']
					file.write(str(entries[1]['id']))
					logging.info('New last_id (VK) is {!s}'.format((entries[1]['id'])))
				except KeyError:
					file.write(str(entries[0]['id']))
					logging.info('New last_id (VK) is {!s}'.format((entries[0]['id'])))
	except Exception as ex:
		logging.error('Exception of type {!s} in check_new_post(): {!s}'.format(type(ex).__name__, str(ex)))
		pass
	logging.info('[VK] Finished scanning')
	return

def match_info():
	source = requests.get(URL_SPORTS_RU).text
	soup = BeautifulSoup(source, 'lxml')
	with open(FILENAME_LAST_MATCH, 'rt') as file:
		file_time_string = file.read()
		#last_match_time = dt.datetime.strptime(file_time_string, '%Y-%m-%dT%H:%M:%S')

	match_name = soup.find('meta', itemprop='name').get('content')
	
	home_away = match_name.split(' - ')
	if home_away == 'Арсенал':
		match_location = "Играем дома"
	else:
		match_location = "Играем в гостях"

	match_time_mscw = soup.find('meta', itemprop='startDate').get('content')
	match_time_mscw = match_time_mscw.replace('+03:00', '')
	match_time = dt.datetime.strptime(match_time_mscw, '%Y-%m-%dT%H:%M:%S')+ timedelta(hours=3)
	#match_time = format(match_time, '%d %B %Y %H:%M')

	print(match_name)
	print(match_time)
	print(match_location)
	print(file_time_string)

if __name__ == '__main__':
	match_info()