import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
from tabulate import tabulate
from minimiser import Minimiser
from strategy import AlwaysFavouriteStrategy
from datetime import timedelta, date

strategy = AlwaysFavouriteStrategy()

cols = ['venue', 'horse', 'pos', 'ran', 'odds', 'favourite']

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/50.0.2661.102 Safari/537.36'
}

site_root = 'https://www.timeform.com/horse-racing/results/'
start_date = date(2020, 8, 1)
end_date = date(2020, 8, 8)

# summary_urls = [
#     'https://www.timeform.com/horse-racing/results/2020-06-06/',
#     'https://www.timeform.com/horse-racing/results/2020-06-07/',
#     'https://www.timeform.com/horse-racing/results/2020-06-08/',
#     'https://www.timeform.com/horse-racing/results/2020-06-09/',
#     'https://www.timeform.com/horse-racing/results/2020-06-10/',
#     'https://www.timeform.com/horse-racing/results/2020-06-11/',
#     'https://www.timeform.com/horse-racing/results/2020-06-12/',
#     'https://www.timeform.com/horse-racing/results/2020-06-13/'
# ]


def create_date_list(start, end):
    """returns the list of dates between start and end"""
    d = start
    result = []
    while d <= end:
        result.append(d.strftime('%Y-%m-%d'))
        d = d + timedelta(days=1)
    return result


def create_urls(start_date, end_date):
    dates = create_date_list(start_date, end_date)
    return list(map(lambda u: site_root + u, dates))


def get_day_summary(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # list of races for the day, we need to find the hrefs to the race details
    summaries = soup.find_all('a', class_='results-title')
    urls = map(lambda x: 'https://timeform.com' + x['href'], summaries)

    return urls


def get_races(url):
    print('get_races', url)
    # parse the URL for race details
    split_url = url.split('/')
    race = '_'.join(split_url[-5:-2])
    memo = os.path.join('./csv', race + '.csv')
    print('\n', race)

    # use local filesystem memo if available
    if os.path.exists(memo):
        print('From memo')
        return pd.read_csv(memo)

    # Otherwise, fetch url and memoize the frame
    details_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(details_page.content, 'html.parser')

    # appending rows to dataframes is best done by appending a list of dictionaries
    rows = []

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
        d['venue'] = '_'.join(split_url[-5:-2])
        # Cleanup the horse's name
        d['horse'] = re.split(r'\s', h.text, 1)[1]

        rows.append(d)

    r = m.smallest()
    rows[r]['favourite'] = 1

    df = pd.DataFrame(rows, columns=cols)
    # create the memo
    df.to_csv(memo)
    return df


def scrape_summary(summary_url):
    urls = get_day_summary(summary_url)
    print(*urls)
    summary_df = pd.DataFrame(columns=cols)

    for url in urls:
        df = get_races(url)
        summary_df = summary_df.append(df, ignore_index=True)

    return summary_df


def main():
    master_df = pd.DataFrame(columns=cols)
    summary_urls = create_urls(start_date, end_date)

    for summary_url in summary_urls:
        print()
        print(summary_url)

        detail_urls = get_day_summary(summary_url)

        for url in list(detail_urls):

            try:

                print('Scraping page', url)
                df = get_races(url)
                print(tabulate(df, headers=cols, tablefmt='fancy_grid', showindex=False))

                strategy.apply(df)
                strategy.print()
                master_df = master_df.append(df)

            except Exception as e:
                print('Failed to read data from', url, str(e))

    print()

    # print(tabulate(master_df, headers=cols, tablefmt='psql', showindex=True))
    print('FAVOURITES')
    predicate = master_df.favourite == 1
    df = master_df[predicate]
    print(tabulate(df, headers=cols, tablefmt='fancy_grid', showindex=False))

    strategy.plot_spend_vs_take()


if __name__ == "__main__":
    main()
