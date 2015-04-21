"""
    Merge function for 2048 game.
    """

# get the none zero list to paire
def get_none_zero_list(line):
    """
        get all the none zero numbers
        """
    new_line = []
    for dummy_i in range(0,len(line)):
        if line[dummy_i] != 0:
            new_line.append(line[dummy_i])
    return new_line

#get the zero list without operation
def get_zero_list(line):
    """
        get a list with all zero
        """
    zero_list = []
    for dummy_i in range(0, len(line)):
        if line[dummy_i] == 0:
            zero_list.append(0)
    return zero_list


# get the slided list
def slide(line):
    """
        slide the list first
        """
    none_zero_list = get_none_zero_list(line)
    zero_list = get_zero_list(line)
    return none_zero_list + zero_list


# to find if there is a pair
def find_pair(line):
    """
        this is to save time
        """
    if len(line) >1:
        for dummy_i in range(0,len(line) - 1):
            if line[dummy_i] !=0 and line[dummy_i] == line[dummy_i+1]:
                return True
    return False


# to get the INDEX of first paired element in list
def get_index(line):
    """
        get the index of first paired
        """
    for dummy_i in range(0,len(line) - 1):
        if line[dummy_i] !=0 and line[dummy_i] == line[dummy_i+1]:
            return dummy_i


# get the list after the first paired tiles
def get_list_before_paired(line):
    """
        get the list after the first paired tiles
        """
    if find_pair(line):
        index = get_index(line)
        return line[ :index + 2]
    return []


def get_list_after_paired(line):
    """
        get the list after the first paired tiles
        """
    if find_pair(line):
        index = get_index(line)
        return line[index + 2: ]
    return []


# if there is a pair, merge the pair
# if no, return the original pair
def pair_list(line):
    """
        merge the pair
        """
    paired_line = []
    
    for dummy_i in range(0, len(line)-1):
        if line[dummy_i] !=0 and line[dummy_i] == line[dummy_i+1]:
            paired_line.append(2 * line[dummy_i])
            paired_line.append(0)
            break
        else:
            paired_line.append(line[dummy_i])
    return paired_line


# merge tiles
def merge(line):
    """
        Function that merges a single row or column in 2048.
        """
    # replace with your code
    none_zero_list = get_none_zero_list(line)
    zero_list = get_zero_list(line)
    if find_pair(none_zero_list):
        before_pair = get_list_before_paired(none_zero_list)
        after_pair = get_list_after_paired(none_zero_list)
        pair1 = pair_list(before_pair)
        while(find_pair(after_pair)):
            before_pair = get_list_before_paired(after_pair)
            after_pair = get_list_after_paired(after_pair)
            pair1 = pair1 + pair_list(before_pair)
        pair1 = pair1 + after_pair + zero_list
        return slide(pair1)
    else:
        return none_zero_list + zero_list


print merge([4,4,8])
print merge([0,0,0,0])
print merge([2, 3, 4, 4])
print merge([2, 2, 4, 4])
print merge([2, 2, 0, 0])
print merge([2, 2, 2, 2])
print merge([8, 16, 16, 8])
print merge([2,0,2,4])
print merge([0, 0, 2, 2])




