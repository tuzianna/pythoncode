"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set



def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: sorted tuple representing a full Yahtzee hand

    Returns an integer score 
    """
    max_score = 0
    temp = set(hand)
    for num in temp:
        count = hand.count(num)
        outcome = num*count
        if max_score < outcome:
            max_score = outcome
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: a sorted tuple representing dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """

    dice_value = [num + 1 for num in range(num_die_sides)]
    free_hand_set = gen_all_sequences(dice_value, num_free_dice)
    num_of_all_outcomes = len(free_hand_set)
    
    outcomes = []
    for free_hand in free_hand_set:
        hand = list(held_dice) + list(free_hand)
        outcome = score(tuple(hand))
        outcomes.append(outcome)
        
    temp = set(outcomes)
    expected = 0
    for outcome in temp:
        expected += float(outcome * outcomes.count(outcome)) / num_of_all_outcomes
    
    return expected


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: sorted tuple representing a full Yahtzee hand

    Returns a set of sorted tuples, where each tuple is dice to hold
    """
    answer_set = set([()])
    
    for value in hand:
        temp = set()
        for ans in answer_set:
            temp_list = list(ans)
            temp_list.append(value)
            temp.add(tuple(temp_list))
        answer_set = answer_set.union(temple)
        print answer_set
    return answer_set


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: sorted tuple representing a full Yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    all_holds = gen_all_holds(hand)
    
    max_exp = 0
    best = ()
    for hold in all_holds:
        num_free_dice = len(hand) - len(hold)
        exp_value = expected_value(hold, num_die_sides, num_free_dice)
        if max_exp < exp_value:
            max_exp = exp_value
            best = (max_exp, hold)
    return best


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



