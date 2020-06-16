import requests
from bs4 import BeautifulSoup
import re
import pandas as pd 
from tabulate import tabulate


cols = ['venue', 'horse', 'pos', 'total', 'odds-d', 'odds-f']


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

main_url = 'https://www.timeform.com/horse-racing/results/2020-06-13/'


def get_day_summary(url):

	page = requests.get(url, headers=headers)

	soup = BeautifulSoup(page.content, 'html.parser')
	# list of races for the day, we need to find the hrefs to the race details
	summaries = soup.find_all('a', class_='results-title')
	urls = map(lambda x: 'https://timeform.com' + x['href'], summaries)
	return urls


def get_races(url):

	details_page = requests.get(url, headers=headers)
	soup = BeautifulSoup(details_page.content, 'html.parser')

	# appending rows to dataframes is best done by appending a list of dictionaries
	rows = []

	
	# parse the URL for race details
	race = url.split('/')
	print('\n', race[-5], race[-4], race[-3])

	# locate sequential listing of horses, in the order of finishing
	horses = soup.select('.rp-jockeytrainer-show > .rp-horse')
	odds_dec  = list(soup.select('.rp-result-bsp-show > .price-decimal'))
	odds_frac = list(soup.select('.rp-result-bsp-show > .price-fractional'))


	position = 0
	for h in horses:

		d = {}
		d['odds-d'] = float(odds_dec[position].text)
		d['odds-f'] = odds_frac[position].text
		position += 1
		d['pos'] = position
		d['total'] = len(horses)
		d['venue'] = '|'.join(race[-5:-2])
		# Cleanup the horse's name
		d['horse'] = re.split('\s', h.text, 1)[1]
		rows.append(d)
	
	# DataFrame
	return pd.DataFrame(rows, columns = cols)


def main():

	master_df = pd.DataFrame(columns = cols)
	urls = get_day_summary(main_url)
	for url in urls:
		df = get_races(url)
		master_df = master_df.append(df, ignore_index = True)

		print(tabulate(df, headers = cols, tablefmt='psql', showindex = False))

	print()
	print('\n ALL RESULTS\n')	

	print(tabulate(master_df, headers = cols, tablefmt='psql', showindex = True))


if __name__ == "__main__":

	main()


