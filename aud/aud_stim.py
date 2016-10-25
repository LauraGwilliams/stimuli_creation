#!/usr/bin/env python


from __future__ import division

from segment_surprisal_tree import *

s = SegmentSurprisalTree()
s.read_elp()


def phoneme_probability(word):
    """
    Conditional probability of phonemes within a word.

    word            :               the item to search


    """
    wp = s.probabilities(word)

    return wp

def phoneme_freq(word):
    """
    Frequency of phoneme sequences along a word (taken from SUBTLEX)

    word            :               the item to search


    """

    wp = s.frequencies(word)

    return wp

def aud_word_freq(word):
    """
    Frequency of a word taken from SUBTLEX

    word            :               the item to search


    """

    wp = s.frequencies(word)

    return wp[-1][1]

def pron(word):
    """splits word in to phonemes"""

    try:
        pron = s.pronunciations[word]
    except:
        pron = 'na' # if the word isn't found (or whatever error to make the func not work) return na

    return pron


def POD(word1,word2,n_amb_phonemes=1):
    """
    Returns the phoneme number that two words with ambiguous beginnings become distinct.

    word1               :               first word of pair - should be the longest
    word2               :               second word of pair - should be the shortest
    n_amb_phonemes      :               how many phonemes in onset are ambiguous

    """

    x = pron(word1)
    y = pron(word2)

    POD = n_amb_phonemes

    for i in range(1,len(x)): # loop through length of first word, not including the first phoneme

        if len(x) == POD:
            print "no divergence point"

        elif x[i] == y[i]:
            POD += 1

        else:
            return POD+1


def ambig_POD_surprisal(target, competitor, phoneme_percent, POD_only = False):
    """

    Example:
    --------

    target = 'parakeet'
    competitor = 'barricade'
    phoneme_percent = {'p': 0.99, 'b': 0.01}


    Parameters:
    -----------

    target              :               the word you want to calculate the surp values for
    competitor          :               the item that is identical until a given POD
    phoneme_percent     :               dict, phoneme and the percent of that phoneme (e.g., {'p': 0.75, 'b': 0.25}) can only be two phonemes
    POD_only            :               bool, just return the surprisal value at the POD


    """

    searches = []
    qs = []

    count = 0

    # load up the frequency of each phoneme in the words

    freq_word1 = phoneme_freq(target)
    freq_word2 = phoneme_freq(competitor)

    pron_t = pron(target)
    pron_c = pron(competitor)
    pron_amb = pron_t[0:] # make an ambiguous set of phonemes
    pron_amb[0] = 'X'

    for i in range(0,len(pron_t)):

        # calculate the q value which will be used to weight the conditional probabilty of the sounds in the word

        # if we are at a letter than exceeds the lengh of the competitor
        if i >= len(pron_c):
            freq1 = freq_word1[i][1]
            freq2 = 0

        # if phonemes are the same, or it's the first phoneme we're looking at
        elif pron_t[i] == pron_c[i] or i == 0:
            freq1 = freq_word1[i][1] # freq of i phoneme in target
            freq2 = freq_word2[i][1] # freq of i phoneme within the competitor

        # if the phonemes diverge, this is either at or past the POD, so freq of competitor phoneme is 0
        else:
            freq1 = freq_word1[i][1]
            freq2 = 0

        total_freq = freq1 + freq2

        prob1 = freq1 / total_freq # relative frequency given the pair
        prob2 = freq2 / total_freq

        acoustic1 = phoneme_percent.values()[0] # weight relative to morph substrate
        acoustic2 = phoneme_percent.values()[1]

        numer1 = prob1 * acoustic1 # combine freq and acoustic into a single weighting
        numer2 = prob2 * acoustic2

        if numer1 + numer2 == 0:
            q1 = 0
            q2 = 0

        else:
            q1 = numer1 / (numer1 + numer2) # get q weight
            q2 = numer2 / (numer2 + numer1)

        ##
        ## apply q to the condition probabilities:
        ##

        if count == 0: # if this is the first phoneme, cond prob doesn't apply

            qs.append('na')

        else:

            if freq_minus_one1 > 0 and freq_minus_one2 > 0:

                cond1 = freq1/freq_minus_one1 # conditional probability of given phoneme
                cond2 = freq2/freq_minus_one2

            else:

                cond1 = freq1/freq_minus_one1
                cond2 = 0 # because can't divide something by 0

            weighted_cond1 = q_minus_one1 * cond1 # conditional probability weighted by q.
            weighted_cond2 = q_minus_one2 * cond2

            final_surp = -np.log2(weighted_cond1 + weighted_cond2) # calculate with complete probability formula, and transform that into a suprisal score

            qs.append(final_surp)

        freq_minus_one1 = freq1 # collect the frequency for use in the cond probability calc of the next phoneme
        freq_minus_one2 = freq2

        q_minus_one1 = q1 # collect the q weighting for use in the cond probability calc of the next phoneme
        q_minus_one2 = q2

        count += 1

    if POD_only == False: # if interested in surp along all phonemes

        return zip(pron_amb,qs)

    elif POD_only == True: # if only interested in surp at the POD

        pod = POD(target,competitor)

        return pron_amb[pod-1],qs[pod-1]


def ambig_POD_entropy(target, competitor, target_acoustic_weighting, competitor_acoustic_weighting):
    """

    Example:
    --------

    target = 'parakeet'
    competitor = 'barricade'
    target_acoustic_weighting = 0.9
    competitor_acoustic_weighting = 0.1


    Parameters:
    -----------

    target                       :       target word to calculate entropy
    competitor                   :       the word that is identical until a given POD
    target_acoustic_weighting    :       float, acoustic evidence in favour of target word
    competitor_acoustic_weighting:       float, acoustic evidence in favour of competitor


    """

    # pronunciation of words
    vector_t = tuple(pron(target) + ['#'] if True else [])
    vector_c = tuple(pron(competitor) + ['#'] if True else [])

    # extract prefix frequency for target word
    cont_dict_target = {} # empty dict to populate w/ frequencies
    phoneme_count = 0
    for phoneme_iter_t, prefix_t in s.tree.get_prefixes(vector_t):

        # get frequency of all phoneme continuations
        cont_freqs = [x[1] for x in s.tree.get_continuations(prefix_t)]

        # weight by acoustics
        cont_freqs = (np.array(cont_freqs)*target_acoustic_weighting).tolist()

        # add to dictionary
        cont_dict_target.update({ '%s_%s' % (phoneme_count,phoneme_iter_t): cont_freqs })

        # update count
        phoneme_count = phoneme_count + 1

    # same for competitor
    cont_dict_comp = {} # empty dict to populate w/ frequencies
    phoneme_count = 0
    for phoneme_iter_c, prefix_c in s.tree.get_prefixes(vector_c):

        # get frequency of all phoneme continuations
        cont_freqs = [x[1] for x in s.tree.get_continuations(prefix_c)]

        # weight by acoustics
        cont_freqs = (np.array(cont_freqs)*competitor_acoustic_weighting).tolist()

        # add to dictionary
        cont_dict_comp.update({ '%s_%s' % (phoneme_count,phoneme_iter_c): cont_freqs })

        # update count
        phoneme_count = phoneme_count + 1

    # merge freq dictionaries
    combined_freq_dict = {}
    for phoneme_number in range(0,len(vector_t)):

        # if the phoneme number is longer than the competitor, we'll use just the target entropy
        if phoneme_number >= len(vector_c):
            phoneme_c = 'exceeded_word_end'

        else:
            phoneme_c = vector_c[phoneme_number]
            phoneme_t = vector_t[phoneme_number]

        # if the phonemes are the same, or its the onset phoneme
        if phoneme_c == phoneme_t or phoneme_number == 0:
            target_freq = cont_dict_target['%s_%s' % (phoneme_number,phoneme_t)]
            competitor_freq = cont_dict_comp['%s_%s' % (phoneme_number,phoneme_c)]
            new_freq_value = target_freq + competitor_freq # merge into the same list

        # if phoneme sequences have diverged, just take target entropy
        elif phoneme_c != phoneme_t:
            new_freq_value = target_freq

        else:
            raise ValueError("Phoneme Sequence Mismatch")

        # add new values to dictionary
        combined_freq_dict.update({"%s_%s" % (phoneme_number,str(phoneme_t)): new_freq_value})

    # calculate entropy over the frequencies and return
    resultant_entropy_dict = {}
    phoneme_count = 0
    for phoneme in combined_freq_dict.keys():
        entropy_val = s.tree._entropy(combined_freq_dict[phoneme])
        resultant_entropy_dict.update( {"%s" % (phoneme): entropy_val} )
        phoneme_count = phoneme_count + 1

    return resultant_entropy_dict
