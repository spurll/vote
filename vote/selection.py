from numpy import linspace
from numpy.random import choice


# Each algorithm must take a list of lists (the ballots) and an integer (the
# number of winners to select), then return a list of winners. If the algorithm
# is unable to return a sufficient number of winners, fewer may be returned.
# All selection methods should avoid returning duplicates.


def weighted_sample(ballots, winners, premium_limit=None):
    """
    Selects the apporpriate number of winners at random, but with the selection
    weighted (linearly) toward those choices that were more popular.
    """
    rankings = _to_rankings(ballots)

    if not rankings:
        return []

    # Translate rankings into weights.
    num_options = len(rankings)
    weight_vector = linspace(1, 1/num_options, num_options)
    weights = {
        option: sum([
            weight_vector[rank - 1] for rank in ranks
        ])
        for option, ranks in rankings.items()
    }

    # Make the selection from the weighted votes. We select only one at a time
    # because that allows us to limit the number of premium options selected,
    # and it prevents errors if we ask for more results than the number of
    # options. This code needs refactoring. :(
    selection = []
    premium = 0
    while len(selection) < winners and len(weights) > 0:
        if premium_limit is not None and premium == premium_limit:
            # Remove premium options.
            weights = {
                option: weight for option, weight in weights.items()
                if not option.premium
            }

        if len(weights) > 0:
            # Convert weights into probabilities.
            total = sum(weights.values())
            probabilities = {
                option: weight / total for option, weight in weights.items()
            }

            # Make a selection.
            options, probability = zip(*probabilities.items())
            new = choice(options, p=probability)

            # Make a note of the selection.
            selection.append(new)
            premium += new.premium

            # Don't select the same option twice.
            del weights[new]

    return selection


def instant_runoff(ballots, winners, premium_limit=None):
    pass


def single_transferrable(ballots, winners, premium_limit=None):
    pass


def condorcet(ballots, winners, premium_limit=None):
    # http://en.wikipedia.org/wiki/Condorcet_method#Finding_the_winner
    pass


def approval(ballots, winners, premium_limit=None):
    # http://nielsenhayden.com/makinglight/archives/016206.html
    pass


def _to_rankings(ballots):
    """
    Translates a list of ballots (lists of votes) into a dict with options as
    keys and ranked positions on the ballot as values.
    """
    rankings = {}

    for ballot in ballots:
        for index, option in enumerate(ballot):
            rank = index + 1
            rankings[option] = rankings.get(option, []) + [rank]

    return rankings
