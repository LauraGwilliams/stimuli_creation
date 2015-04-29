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
        
        if len(pron_t) != len(pron_c):
            raise NotImplementedError('Words have different number of phonemes (%i different)' % (len(pron_t) - len(pron_c))) 
        
        if pron_t[i] == pron_c[i] or i == 0: # if phonemes are the same, or it's the first phoneme we're looking at
            freq1 = freq_word1[i][1] # freq of i phoneme in target
            freq2 = freq_word2[i][1] # freq of i phoneme within the competitor
        
        else:
            freq1 = freq_word1[i][1]
            freq2 = 0  # if the phonemes diverge, this is either at or past the POD, so freq of competitor phoneme is 0
                
        total_freq = freq1 + freq2 
                
        prob1 = freq1 / total_freq # relative frequency given the pair
        prob2 = freq2 / total_freq
        
        acoustic1 = phoneme_percent.values()[0] # weight relative to morph substrate
        acoustic2 = phoneme_percent.values()[1]
        
        numer1 = prob1 * acoustic1 # combine freq and acoustic into a single weighting
        numer2 = prob2 * acoustic2
        
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
        
        