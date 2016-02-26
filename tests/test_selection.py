import unittest
from collections import Counter

from vote import selection


# To run:
# python3 -m unittest tests.test_selection


class TestObject(object):
    def __init__(self, identifier, premium=False):
        self.identifier = identifier
        self.premium = premium


# Premium limits are never tested. Oh well.


class TestWeightedSample(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestWeightedSample, self).__init__(*args, **kwargs)
        self.selection = selection.weighted_sample
        self.data = [
            [0],
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 3],
            [1, 2, 3, 4],
            [2, 3, 4, 5],
            [3, 4, 5, 6],
            [4, 5, 6, 7, 8],
            [0, 1, 2, 3, 4, 5, 6, 7, 8],
            [0, 1, 2, 3, 4, 5, 6, 8, 7],
        ]
        self.expected = list(range(9))

    def test_basic(self):
        # Select 10000 winners. The test is designed such that the lower values
        # should consistently be selected more often.
        winners = [self.selection(self.data)[0] for i in range(10000)]
        counter = Counter(winners)
        most_common = [key for key, value in counter.most_common()]

        self.assertEqual(most_common, self.expected)


class TestInstantRunoff(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInstantRunoff, self).__init__(*args, **kwargs)
        self.selection = selection.instant_runoff
        self.data = [
            [0, 3, 2],
            [0, 1, 3, 2, 4],
            [2],
            [1, 0],
            [0],
            [0, 1, 2, 4, 3, 5, 6, 7, 8],
            [5, 0],
            [6, 0],
            [7, 2],
            [8],
        ]
        self.expected = list(range(9))

    def test_basic(self):
        self.assertEqual(self.selection(self.data), [self.expected[0]])
        self.assertEqual(self.selection(self.data, winners=9), self.expected)


class TestBordaCount(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestBordaCount, self).__init__(*args, **kwargs)
        self.selection = selection.borda_count
        self.data = [
            [0],
            [0, 3, 1],
            [0, 2, 3, 1, 6],
            [0, 2, 1, 6, 3, 4, 5],
            [1],
            [2, 0],
            [4, 0],
            [5, 0],
            [7, 8, 1],
        ]
        self.expected = list(range(9))

    def test_basic(self):
        self.assertEqual(self.selection(self.data), [self.expected[0]])
        self.assertEqual(self.selection(self.data, winners=9), self.expected)


if __name__ == '__main__':
    unittest.main()
