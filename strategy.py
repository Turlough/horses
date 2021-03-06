from abc import ABC, abstractmethod
import matplotlib.pyplot as plt


class Strategy(ABC):
    @abstractmethod
    def apply(self, dataframe):
        ...

    @abstractmethod
    def print(self):
        ...


class AlwaysFavouriteStrategy(Strategy):
    """
    This strategy always bets on the favourite in the race
    """
    percentage_takes = [] # running cumulative total of percentage gain, negative if loss
    favourites = []
    winners = []
    winnings = []
    spends = []
    amount_spent = 0
    amount_returned = 0
    cumulative_return = 0
    profit = 0
    percentage_take = 0

    def apply(self, races):
        """
        races: a dataframe with columns 'favourite' and 'odds'
        """
        self.spends.append(len(self.spends) + 1)
        # filter to favourites
        self.favourites = races[races.favourite == 1]
        # bet one unit on each favourite
        self.amount_spent = len(self.spends)
        # filter again to favourites that won
        self.winners = self.favourites[self.favourites.pos == 1]
        # add the money returned
        self.amount_returned = self.winners.odds.sum()
        self.cumulative_return += self.amount_returned
        self.winnings.append(self.cumulative_return)
        # profit
        self.profit = self.amount_returned - self.amount_spent
        # % gain or loss on total spent so far
        self.percentage_take = 100 * (self.amount_returned / self.amount_spent - 1)

        self.percentage_takes.append(self.percentage_take)

        return self.percentage_takes

    def print(self):
        print(f'''
        Num Bets        {len(self.percentage_takes)}
        Spent           {self.amount_spent}
        Gained          {self.amount_returned:.2f}
        Profit          {self.profit:.2f}
        Profit %        {self.percentage_take:.1f}%
        ''')

    def plot_percentage_gain(self):
        plt.plot(self.percentage_takes)
        plt.axhline(y=0)
        plt.show()

    def plot_spend_vs_take(self):

        plt.plot(self.winnings)
        plt.plot(self.spends)
        plt.show()
