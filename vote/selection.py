from numpy import linspace
from numpy.random import choice


# Each algorithm must take a list of lists (the ballots) and an integer (the
# number of winners to select), then return a list of winners. If the algorithm
# is unable to return a sufficient number of winners, fewer may be returned.
# All selection methods should avoid returning duplicates.


def weighted_sample(ballots, winners):
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

    # Convert weights into probabilities.
    total_weight = sum(weights.values())
    weighted_options = [
        (option, weight / total_weight) for option, weight in weights.items()
    ]
    options, prob = zip(*weighted_options)

    # Make the selection from the weighted votes.
    try:
        selection = list(choice(options, size=winners, replace=False, p=prob))
    except ValueError:
        # We asked for a sample larger than the number of choices.
        selection = list(
            choice(options, size=len(options), replace=False, p=prob)
        )

    return selection


def instant_runoff(ballots, winners):
    pass


def single_transferrable(ballots, winners):
    pass


def condorcet(ballots, winners):
    # http://en.wikipedia.org/wiki/Condorcet_method#Finding_the_winner
    pass


def approval(ballots, winners):
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
