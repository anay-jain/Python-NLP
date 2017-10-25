from collections import Counter
import re as regex

ALPHABETS = "abcdefghijklmnopqrstuvwxyz"
FILE = "data.txt"

'''
mail to
sachinsingh31@outlook.com
'''

# function to extract all the words from the big file
def get_words_from_file(file):
	# getting the contents of the file
	file_content = open(file).read()

	# extract all the words from the file and create a
	# counter of it for easy tally
	words = Counter(regex.findall(r'\w+', file_content))

	return words

# function for to return all the possible edits that are 
# one distance away from the word
def edit_distance_1(word):

	# CREATING SPLITS
	# splitting a word into two strings using different midpoints
	# and creating a list of tuples
	splits = [ (word[:i], word[i:]) for i in range(len(word) + 1) ]

	# get all the edits where atleast 1 alphabet is deleted
	# from the word
	deletes = [ left[:-1] + right for left, right in splits if left ]

	# get all the possible edits wherein adjacent alphabets
	# are swapped
	swaps = [ left[:-2] + left[-1] + left[-2] + right for left, right in splits if len(left) >= 2 ]

	# get all possible single alphabet replaces
	replaces = [ left[:-1] + char + right for left, right in splits for char in ALPHABETS if left]

	# get all possible ways in which all the alphabets can be 
	# inserted in the word
	inserts = [ left + char + right for left, right in splits for char in ALPHABETS ]

	return deletes + swaps + replaces + inserts

# function to return all the possible edits that are
# two distance away from the word
def edit_distance_2(word):
	# get all the possible words 1 distance away and find
	# the words 1 distance away from all of those words
	return [ edit_2 for edit_1 in edit_distance_1(word) for edit_2 in edit_distance_1(edit_1) ]

# function to filter the suggestions that are in known words
def get_correct_words(known_words, words):
	return list( set( [ w for w in words if w in known_words ] ) )

# function that suggests the possible corrections or
# returns the same word of correct in the form of list
def suggest_list(known_words, word):
	# check if even edit is required or not
	no_edit = get_correct_words(known_words, [word])
	if no_edit: return no_edit
	else:
		# if only 1 edit is sufficient
		edit_1 = get_correct_words(known_words, edit_distance_1(word))
		if edit_1: return edit_1
		else:
			# if 2 edits are required
			edit_2 = get_correct_words(known_words, edit_distance_2(word))
			if edit_2: return edit_2
			# bad algo..... cannot edit this word
			else: return [word]
# function that returns the most probable word correction
def suggest(known_words, word):
	return max( suggest_list(known_words, word), key = lambda word : known_words[word]/sum(known_words.values()) )


