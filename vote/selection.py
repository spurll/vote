from numpy import linspace
from numpy.random import choice


# Each algorithm must take a list of lists (the ballots) and an integer (the
# number of winners to select), then return a list of winners. If the algorithm
# is unable to return a sufficient number of winners, fewer may be returned.
# All selection methods should avoid returning duplicates.


def weighted_sample(ballots, winners=1, premium_limit=None):
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
                if not getattr(option, 'premium', False)
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
            premium += getattr(new, 'premium', False)

            # Don't select the same option twice.
            del weights[new]

    return selection


def instant_runoff(ballots, winners=1, premium_limit=None):
    """
    http://en.wikipedia.org/wiki/Instant-runoff_voting

    Example:
    >>> ballots
    [[1, 2, 3], [4, 5, 2], [2, 4], [2]]
    >>> vote.selection.instant_runoff(ballots, 7)
    [2, 4, 5, 1, 3]
    
    It might seem like 1 should have been picked before 5, because 5 is second
    place and 1 is first. It didn't happen this way because by the time it came
    to choose between the two of them, 4 had been removed, bumping 5 up to
    first place on the second ballot. So... Shrug.
    """
    selection = []
    premium = 0

    while len(selection) < winners and sum(len(b) for b in ballots) > 0:
        if premium_limit is not None and premium == premium_limit:
            # Remove premium options.
            ballots = _remove_from_ballots(
                ballots, lambda x: getattr(x, 'premium', False)
            )

        # Don't destroy the full set of ballots during this iteration.
        current = ballots

        # While we don't have a majority and there are still votes, remove the
        # least popular item.
        while _first_picks(current) and _majority(current) is None:
            current = _remove_from_ballots(
                current, lambda x: x == _least_popular(current)
            )

        majority = _majority(current)

        # If we have a majority, add it to the selection and make it
        # unselectable for future iterations by removing it from the ballots.
        if majority is not None:
            selection.append(majority)
            premium += getattr(majority, 'premium', False)
            ballots = _remove_from_ballots(ballots, lambda x: x == majority)

        # If we don't have a majority, we can't find any more winners.
        else:
            break

    return selection


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


def _first_picks(ballots):
    return [ballot[0] for ballot in ballots if ballot]


def _least_popular(ballots):
    # Examines all ballots and returns the item that appears as a first choice
    # the fewest times.
    all_options = {option for ballot in ballots for option in ballot}
    return min(all_options, key=_first_picks(ballots).count)


def _majority(ballots):
    first_picks = _first_picks(ballots)
    mode = max(set(first_picks), key=first_picks.count)

    # Doesn't matter whether this is integer division or not.
    return mode if first_picks.count(mode) > len(first_picks) / 2 else None


def _remove_from_ballots(ballots, key):
    """
    Removes the options matching the key from ballots, returning the result.
    """
    return [
        [option for option in ballot if not key(option)]
        for ballot in ballots
    ]
