from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def apply(self, dataframe):
        pass


class AlwaysFavouriteStrategy(Strategy):
    history = []
    favourites = []
    winners = []
    amount_spent = 0
    amount_returned = 0
    profit = 0
    mean_take = 0

    def apply(self, race):
        # filter to favourites
        self.favourites = race[race.favourite == 1]
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

        self.history.append(self.mean_take)

        return self.history

    def print(self):
        print(f'''
        Spent           {self.amount_spent}
        Gained          {self.amount_returned:.2f}
        Profit          {self.profit:.2f}
        Profit %        {self.mean_take:.1f}%
        ''')

