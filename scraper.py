import requests
from bs4 import BeautifulSoup
import re



headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

main_url = 'https://www.timeform.com/horse-racing/results/2020-06-13/'
page = requests.get(main_url, headers=headers)


soup = BeautifulSoup(page.content, 'html.parser')
# list of races for the day, we need to find the hrefs to the race details
results_titles = soup.find_all('a', class_='results-title')


for t in results_titles:

	# load the details for the race
	url = 'https://timeform.com' + t['href']
	details_page = requests.get(url, headers=headers)
	soup = BeautifulSoup(details_page.content, 'html.parser')
	
	#parse the URL for race details
	race = t['href'].split('/')
	print('\n', race[-5], race[-4], race[-3])

	# locate sequential listing of horses, in the order of finishing
	horses = soup.select('.rp-jockeytrainer-show > .rp-horse')
	for h in horses:
		# strip the horse's number from the name
		name = re.split('\s', h.text, 1)[1]
		print(' -> ', name)

