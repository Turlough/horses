import requests
from bs4 import BeautifulSoup
import pprint

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

main_url = 'https://www.timeform.com/horse-racing/results/2020-06-13/'
page = requests.get(main_url, headers=headers)


soup = BeautifulSoup(page.content, 'html.parser')
results_titles = soup.find_all('a', class_='results-title')

# for t in results_titles:
# 	print(t['href'])

for t in results_titles[0:2]:
	url = 'https://timeform.com' + t['href']
	details_page = requests.get(url, headers=headers)
	soup = BeautifulSoup(details_page.content, 'html.parser')
	# horses = soup.find(class_= 'rp-jockeytrainer-show').find(class_= 'rp-horse').find_all('a')
	print('\n', t['href'])
	


	horses = soup.select('.rp-jockeytrainer-show > .rp-horse')
	for h in horses:

		print(' -> ', h.text)

