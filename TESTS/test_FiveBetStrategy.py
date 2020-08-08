import unittest
from dataclasses import dataclass

import pandas as pd
from FiveBetStrategy import FiveBetStrategy


@dataclass
class Horse:
    name: str
    is_favourite = False
    is_winner = False
    odds = float(0)


strategy = FiveBetStrategy()
horses = [
    Horse('Donkey', is_favourite=True),
    Horse('Stubborn'),
    Horse('Face')
]
df = pd.DataFrame(horses)


class TestFiveBetStrategy(unittest.TestCase):

    def test_get_favourites(self):
        self.assertEqual(1, strategy.get_races(horses))


if __name__ == '__main__':
    unittest.main()
