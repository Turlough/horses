from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

class Strategy(ABC):
    @abstractmethod
    def apply(self, dataframe):
        pass

    @abstractmethod
    def print(self):
        pass


class AlwaysFavouriteStrategy(Strategy):

    betting_history = []
    favourites = []
    winners = []
    amount_spent = 0
    amount_returned = 0
    profit = 0
    mean_take = 0

    def apply(self, races):

        # filter to favourites
        self.favourites = races[races.favourite == 1]
        # bet one unit on each favourite
        self.amount_spent = len(self.favourites)
        # filter again to favourites that won
        self.winners = self.favourites[self.favourites.pos == 1]
        # add the money returned
        self.amount_returned = self.winners.odds.sum()
        # profit
        self.profit = self.amount_returned - self.amount_spent
        # % gain or loss on total spent so far
        self.mean_take = 100 * (self.amount_returned / self.amount_spent - 1)

        self.betting_history.append(self.mean_take)

        return self.betting_history

    def print(self):
        print(f'''
        Num Bets        {len(self.betting_history)}
        Spent           {self.amount_spent}
        Gained          {self.amount_returned:.2f}
        Profit          {self.profit:.2f}
        Profit %        {self.mean_take:.1f}%
        ''')

    def plot(self):
        plt.plot(self.betting_history)
        plt.axhline(y=0)
        plt.show()
        print('Num items in history:', len(self.betting_history))
