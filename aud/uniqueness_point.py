# Laura Gwilliams
# leg5@nyu.edu
#
# purpose: get uniqueness point of a word
# date: 25th October 2016
# dependencies: segment_surprisal_tree, elp

from segment_surprisal_tree import SegmentSurprisalTree

# init elp segmenter
s = SegmentSurprisalTree()
s.read_elp()


def get_word_continuations(word):

    # get pronunciation of the word
    try:
        word_pron = s.pronunciations[word]
    except:
        raise NotImplementedError("Word '%s' not found in corpus." % word)

    # convert into expected tuple format
    word_tuple = tuple(word_pron + ['#'] if True else [])

    # extract prefix frequency for target word
    continuation_dict = {} # empty dict to populate w/ frequencies
    phoneme_count = 0
    for phoneme_iter, prefix in s.tree.get_prefixes(word_tuple):

        # get frequency of all phoneme continuations
        cont_freqs = [x[1] for x in s.tree.get_continuations(prefix)]

        # add to dictionary
        continuation_dict.update({ '%s_%s' % (phoneme_count, phoneme_iter): cont_freqs })

        # update phoneme count
        phoneme_count = phoneme_count + 1

    return continuation_dict


def get_uniqueness_point(word):

    # get word continuation dict
    continuation_dict = get_word_continuations(word)

    # sort key entries
    phoneme_list = continuation_dict.keys()
    phoneme_list.sort()

    # loop through each phoneme entry
    for n, phoneme in enumerate(phoneme_list):
        conts = continuation_dict[phoneme]

        # when there is only one continuation, we have found the UP.
        if len(conts) == 1:
            return n, phoneme

    # if no UP found, return error.
    raise ValueError("No uniqueness point found.")
