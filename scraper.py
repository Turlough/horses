import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tabulate import tabulate
from minimiser import Minimiser
import matplotlib.pyplot as plt

cols = ['venue', 'horse', 'pos', 'ran', 'odds', 'favourite']

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

summary_urls = [
    'https://www.timeform.com/horse-racing/results/2020-06-10/',
    'https://www.timeform.com/horse-racing/results/2020-06-11/',
    'https://www.timeform.com/horse-racing/results/2020-06-12/',
    'https://www.timeform.com/horse-racing/results/2020-06-13/'
]


def get_day_summary(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # list of races for the day, we need to find the hrefs to the race details
    summaries = soup.find_all('a', class_='results-title')
    urls = map(lambda x: 'https://timeform.com' + x['href'], summaries)

    return urls


def get_races(url):
    print('get_races', url)
    details_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(details_page.content, 'html.parser')

    # appending rows to dataframes is best done by appending a list of dictionaries
    rows = []

    # parse the URL for race details
    split_url = url.split('/')
    print('\n', split_url[-5], split_url[-4], split_url[-3])

    # locate sequential listing of horses, in the order of finishing
    horses = soup.select('.rp-jockeytrainer-show > .rp-horse')
    odds_dec = list(soup.select('.rp-result-bsp-show > .price-decimal'))

    position = 0
    m = Minimiser()
    for h in horses:
        d = {}

        current_odds = float(odds_dec[position].text)
        m.submit(current_odds, position)

        d['favourite'] = 0
        d['odds'] = current_odds
        position += 1
        d['pos'] = position
        d['ran'] = len(horses)
        d['venue'] = '|'.join(split_url[-5:-2])
        # Cleanup the horse's name
        d['horse'] = re.split('\s', h.text, 1)[1]

        rows.append(d)

    r = m.smallest()
    rows[r]['favourite'] = 1

    # DataFrame
    return pd.DataFrame(rows, columns=cols)


def scrape_summary(summary_url):
    urls = get_day_summary(summary_url)
    print(*urls)
    summary_df = pd.DataFrame(columns=cols)

    for url in urls:
        df = get_races(url)
        summary_df = summary_df.append(df, ignore_index=True)

    return summary_df


def analyse(df, history):
    # filter to favourites
    favourites = df[df.favourite == 1]
    # bet one unit on each favourite
    amount_spent = len(favourites)
    # filter again to favourites that won
    winners = favourites[favourites.pos == 1]
    # add the money returned
    amount_returned = winners.odds.sum()
    # profit
    profit = amount_returned - amount_spent
    # % gain or loss on total spent so far
    mean_take = 100 * (amount_returned / amount_spent - 1)

    history.append(mean_take)

    print(f'''
    Spent           {amount_spent}
    Gained          {amount_returned:.2f}
    Profit          {profit:.2f}
    Profit %        {mean_take:.1f}%
    ''')

    return history


def main():
    master_df = pd.DataFrame(columns=cols)

    history = []
    for summary_url in summary_urls:
        print()
        print(summary_url)

        detail_urls = get_day_summary(summary_url)

        for url in list(detail_urls):

            try:

                print('Scraping page', url)
                df = get_races(url)
                print(tabulate(df, headers=cols, tablefmt='psql', showindex=False))

                master_df = master_df.append(df, ignore_index=True)
                history = analyse(master_df, history)

            except Exception as e:
                print('Failed to read data from', url)

    print()

    # print(tabulate(master_df, headers=cols, tablefmt='psql', showindex=True))
    print('FAVOURITES')
    predicate = master_df.favourite == 1
    df = master_df[predicate]
    print(tabulate(df, headers=cols, tablefmt='psql', showindex=True))

    plt.plot(history)
    plt.axhline(y=0)
    plt.show()
    print('Num items in history:', len(history))


if __name__ == "__main__":
    main()
