import unittest

from vote import selection


# To run:
# python3 -m unittest tests.test_selection


class TestObject(object):
    def __init__(self, identifier, premium=False):
        self.identifier = identifier
        self.premium = premium


primitive_data = [
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



# Add super basic tests with just one winner (called with default number of
# winners).


class TestWeightedSample(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestWeightedSample, self).__init__(*args, **kwargs)
        self.selection = selection.weighted_sample

    def test_basic(self):
        pass

    def test_premium_limit(self):
        # Basic testing with premium limits.

        # Test with primitives (no premium limit attributes).
        pass


class TestInstantRunoff(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestInstantRunoff, self).__init__(*args, **kwargs)
        self.selection = selection.instant_runoff

    def test_basic(self):
        expected = list(range(9))
        self.assertEqual(self.selection(primitive_data, winners=9), expected)


if __name__ == '__main__':
    unittest.main()
