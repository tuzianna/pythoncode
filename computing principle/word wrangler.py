"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_list = []
    
    for item in list1:
        if new_list.count(item) == 0:
            new_list.append(item)
        
    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    interset_list = []
    for item in list1:
        if item in list2:
            interset_list.append(item)
    return interset_list

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    result = []
    len1 = len(list1)
    len2 = len(list2)
    dummy_i = 0
    dummy_j = 0
    
    if len1 == 0:
        result.extend(list2)
    elif len2 == 0:
        result.extend(list1)
    else:
        while dummy_i < len1 and dummy_j < len2:
            if list1[dummy_i] < list2[dummy_j]:
                result.append(list1[dummy_i])
                dummy_i += 1
            else:
                result.append(list2[dummy_j])
                dummy_j += 1

        if dummy_i <= len1 -1:
            result.extend(list1[dummy_i:])
        if dummy_j <= len2 -1:
            result.extend(list2[dummy_j:])
                         
    return result
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) == 1 or len(list1) == 0:
        return list(list1)
    else:
        sorted_list = merge_sort(list1[1:])
        return merge([list1[0]], sorted_list)
                 

# Function to generate all strings for the word wrangler game
def insert_into_string(string, pos, dummy):
    '''
    insert a character into a string in the specified position
    '''
    if len(string) == 0:
        return dummy
    else:
        return string[0:pos] + dummy + string[pos:]


def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    result = []
    if len(word) == 1:
        result = ['', word]
    elif len(word) == 0:
        result = ['']
    else:
        word_list = gen_all_strings(word[1:])
        for item in word_list:
            for dummy in range(len(item) + 1):
                result.append(insert_into_string(item, dummy, word[0]))
            
        result.extend(word_list)
    return result

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
   
    """
    words = []
    file_url = codeskulptor.file2url(filename)
    word_file = urllib2.urlopen(file_url)
    for line in word_file.readlines():
        word = line[:-1]
        words.append(word)
    return words

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    
