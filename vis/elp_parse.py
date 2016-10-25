#!/usr/bin/env python

## script to get interesting things out of a big elp dataset
from __future__ import division

from eelbrain import *
import numpy as np
import math
from lexvars import *
import os.path
import random
from random import shuffle
import collections
from segment_surprisal_tree import *


path = '/Users/lauragwilliams/Documents/experiments/vulnerable_winter/elp/'
file_name = 'elp_dataset.csv'
save_loc = path
celex_path= '/Users/lauragwilliams/Documents/experiments/vulnerable_winter/celex/'

vowels = ['a','e','i','o','u']

def open_file(file,format='csv',header=True,ignore_missing=True):
    """Uses eelbrain to load up a dataset from a file"""
    
    if format == 'csv':
        delim = ','
    elif format == 'tsv':
        delim = '\t'
    
    ds = load.txt.tsv(file, names=True, delimiter=delim, ignore_missing=ignore_missing)
    return ds
    

def elp_info(item,elp):
    """
    Gets basic info for given word
    
    
    """
    
    for i in range(0,len(elp['Word'])):
        word = elp['Word'][i]
        if item in word[0:len(item)] and len(item) == len(word):
            return item, word, elp['Length'][i], elp['Log_Freq_HAL'][i], elp['I_Mean_RT'][i]

def clean_data(ds,log_freq_min=2,freq_HAL_min=0,min_suff_length=0,word_class=None,word_contains=None,mean_RT=None):
    """Takes dataset and returns clean dataset as cleaned by defined variables"""
    
    idx_logfreq = ds['Log_Freq_HAL'] > log_freq_min
    ds1 = ds.sub(idx_logfreq)
    
    idx_freq_HAL = ds1['Freq_HAL'] > freq_HAL_min
    ds1 = ds1.sub(idx_freq_HAL)
    
    if mean_RT != None:
 
        idx_RT = ds1['I_Mean_RT'] > mean_RT
        ds1 = ds1.sub(idx_RT)
        
    if word_contains != None:

        idx_string_contain = [];

        for word in ds1['Word']:
            if word_contains in word:
                idx_string_contain.append(True)
            else:
                idx_string_contain.append(False)
                        
        ds1 = ds1.sub(idx_string_contain)
    
    return ds1
    
def fetch_unique_and_free_stems(ds,suffix_collection='SolomyakMarantz',save_result=False):
    """Gets the words that have a suffix but are monomorphemic, as defined by the ELP.
    
    If suffix_collection=None, then finds all the potential suffixes
    in the dataset.
    
    JJ  :   adjective
    NN  :   noun
    RB  :   adverb
    VB  :   verb"""
    
    result_ds = Dataset()
    
    if suffix_collection != 'SolomyakMarantz':
        suffix_collection = []
        for item in ds['RegSuffix']:
            if item not in suffix_collection:
                suffix_collection.append(item)
    else:
        #suffix_collection = ['able','al','ant','ary','ate','er','ic','ion','ity']
        suffix_collection = ['ry','age','et','ey','ard','ous'] # make sure that one suffix isn't contained in another (e.g., ry and ary)
                
    
    unique_stem_collection = [];
    free_stem_collection = [];
    idx = [];
    unique_suffix = [];
    free_suffix = [];
    
    for i in range(0,len(ds['Word'])):
        for item in suffix_collection:
            
            word = ds['Word'][i]
            x = len(word) - len(item)
            y = len(word)
            
            if item in word[x:y] and ds['NMorph'][i] == 1:
                unique_stem_collection.append(word)
                unique_suffix.append(word[x:y])
                                    
            elif item in word[x:y] and ds['NMorph'][i] == 2:
                free_stem_collection.append(word)
                free_suffix.append(word[x:y])
                             
    print len(unique_stem_collection), " unique stems found."
    
    print len(free_stem_collection), " free stems found."
    
    if save_result == True:
        save.txt(unique_stem_collection,dest=save_loc + 'unique_stems2.csv')
        save.txt(free_stem_collection,dest=save_loc + 'free_stems2.csv')
    
    result_ds.unique_stem_collection = unique_stem_collection
    result_ds.free_stem_collection = free_stem_collection
     
    
    words = [];
    lengths = [];
    log_freqs = [];
    hals = [];
    poss = [];
    stems = [];
    morphsps = [];
    nmorphs = [];
    RTs = [];
    suffixes = []
    
    for i in range(0,len(ds['Word'])):
        if ds['Word'][i] in result_ds.unique_stem_collection:
            words.append(ds['Word'][i])
            lengths.append(ds['Length'][i])
            log_freqs.append(ds['Log_Freq_HAL'][i])
            hals.append(ds['Freq_HAL'][i])
            morphsps.append(ds['MorphSp'][i])
            poss.append(ds['POS'][i])
            nmorphs.append(ds['NMorph'][i])
            stems.append('unique')
            rt = str(ds['I_Mean_RT'][i])
            RTs.append(rt)         
            
            for suffix in suffix_collection: 
                word = ds['Word'][i]
                x = len(word) - len(suffix)
                y = len(word)
             
                if suffix in word[x:y]:
                    suffixes.append(suffix)
                    
    
    for i in range(0,len(ds['Word'])):
        if ds['Word'][i] in result_ds.free_stem_collection:
            words.append(ds['Word'][i])
            lengths.append(ds['Length'][i])
            log_freqs.append(ds['Log_Freq_HAL'][i])
            hals.append(ds['Freq_HAL'][i])
            morphsps.append(ds['MorphSp'][i])
            poss.append(ds['POS'][i])
            nmorphs.append(ds['NMorph'][i])
            stems.append('free')
            rt = str(ds['I_Mean_RT'][i])
            RTs.append(rt)            

            for suffix in suffix_collection: 
                word = ds['Word'][i]
                x = len(word) - len(suffix)
                y = len(word)
             
                if suffix in word[x:y]:
                    suffixes.append(suffix)
    

    ds2 = Dataset() 
    ds2['Word_Type'] = Factor(stems)
    ds2['Word'] = Factor(words)
    ds2['Length'] = Var(lengths)             # you have to make sure to load these up right as vars or factors or it won't work.
    ds2['Log_Freq_HAL'] = Var(log_freqs)
    ds2['Freq_HAL'] = Var(log_freqs)
    ds2['MorphSp'] = Factor(morphsps)
    ds2['NMorph'] = Var(nmorphs)
    ds2['POS'] = Factor(poss)
    ds2['mean_RT'] = Factor(RTs)  
    
    ds2['Suffix'] = Factor(suffixes)
     
    
    print ds2[0:10]
    return ds2

    
def separate_cong_from_incong(ds,save_file=False):
    """Takes the suffix info and compares to the resulting word class. If there's a mismatch, counts it as a 'winter' word"""
    
    mydict = {
        
        'ion'   :   'NN',
        'ity'   :   'NN',
        'er'    :   'NN',
        'ic'    :   'JJ',
        'able'  :   'JJ',
        'al'    :   ['NN','JJ'],
        'ant'   :   ['NN','JJ'],
        'ary'   :   ['NN','JJ'],
        'ate'   :   ['NN','VB','JJ']
    }
    
    word_types = [];
    words = [];
    expected_pos = [];
    actual_pos = [];
    suffixes = [];
    
    for i in range(0,len(ds['Word'])):
        for dictEnt in mydict.get(ds['Suffix'][i]):
            if str(dictEnt) not in ds['POS'][i]:
                if ds['Word'][i] not in words:
                
                    word_types.append(ds['Word_Type'][i])
                    words.append(ds['Word'][i])
                    expected_ = '-'.join(mydict.get(ds['Suffix'][i]))
                    expected_pos.append(expected_)
                    actual_pos.append(ds['POS'][i])
                    suffixes.append(ds['Suffix'][i])
                
                #print ds['Word_Type'][i], "     word:", ds['Word'][i], "      | actual POS:", ds['POS'][i], "     | Dict POS: ", dictEnt
    
    ds_save = Dataset()
    ds_save['Word_type'] = Factor(word_types)
    ds_save['Suffix'] = Factor(suffixes)
    ds_save['Word'] = Factor(words)
    ds_save['Exp_POS'] = Factor(expected_pos)        
    ds_save['Act_POS'] = Factor(actual_pos)
      
    if save_file == True:
        ds_save.save_txt(save_loc + 'incong_cong.csv', delim=',', header=True)
        
    return ds_save
    

def load_celex(celex_path=celex_path):
    """
    Uses eelbrain to load up celex morph file. First need to change the delimiter of the eml file from
        a backslash to a comma, and save this as eml_copy.cd.
    
    Will return a dataset with both wordform and lemma info as: self.wf1, self.wf2 and self.lem
    
    """
    ds = Dataset()

    ds1 = load.tsv(celex_path + '/emw/emw_copy.cd', names=False, delimiter= ">", ignore_missing=True)
    ds2 = load.tsv(celex_path + '/emw/emw_copy2.cd', names=False, delimiter= ">", ignore_missing=True)

    ds1.rename('v0','index')
    ds1.rename('v1','word')
    ds1.rename('v2','surf_freq')
    ds1.rename('v3','lem_idx')    

    ds_thin1 = Dataset()
    ds_thin1['index'] = Var(ds1['index'])
    ds_thin1['word'] = Factor(ds1['word'])
    ds_thin1['surf_freq'] = Factor(ds1['surf_freq'])
    ds_thin1['lem_idx'] = Factor(ds1['lem_idx'])
    
    ds2.rename('v0','index')
    ds2.rename('v1','word')
    ds2.rename('v2','surf_freq')
    ds2.rename('v3', 'lem_idx')

    ds_thin2 = Dataset()
    ds_thin2['index'] = Var(ds2['index'])
    ds_thin2['word'] = Factor(ds2['word'])
    ds_thin2['surf_freq'] = Factor(ds2['surf_freq'])       
    ds_thin2['lem_idx'] = Factor(ds2['lem_idx'])
     
    ds.wf1 = ds_thin1 
    ds.wf2 = ds_thin2
    
    ds3 = load.tsv(celex_path + '/eml/eml_copy.cd', names=False, delimiter= ",", ignore_missing=True)

    ds3.rename('v0','index')
    ds3.rename('v1','word')
    ds3.rename('v2','surf_freq')
    ds3.rename('v11', 'morph_str')
    
    ds_thin3 = Dataset()
    ds_thin3['index'] = Var(ds3['index'])
    ds_thin3['word'] = Factor(ds3['word'])
    ds_thin3['surf_freq'] = Factor(ds3['surf_freq'])
    ds_thin3['morph_str'] = Factor(ds3['morph_str'])

    ds.lem = ds_thin3 
   
    return ds


def surf_and_lem_freq(surface_form,celex,pseudo_base):
    """
    
    Returns surface frequency, lemma frequency of base and transition probability.
    
    Can only be used for properly morphologically derived items.
    
    Parameters:
    ----------
    
    surface_form        :       (str), the string you want to search for
    celex               :       the celex data object 
    pseudo_base         :       can add a user-defined lemma if you're looking at pseudo-suffixed items like "brother"
    
    """
    
    clx=celex
    
    clx.wfs = combine((clx.wf1,clx.wf2)) # this still screws things up because it becomes too long... need to split them.
    
    # get the word form info for the surface word
    idx = surface_form == clx.wfs['word']
    word_wf = clx.wfs.sub(idx)
    
    # if item not in the corpus, raise error
    if word_wf.n_cases == 0:
        print ("Search item %s not found" %surface_form)
        #return 0, 0, 0
    
    
    # find the lemmas that the word forms correspond to
    unique_indexes = set(word_wf['lem_idx'])
    lem_indexes = map(int, unique_indexes)
    
    
    # otherwise, get the surface frequency of all instances summed    
    checked = []
    freqs = []
    for i in xrange(len(word_wf['surf_freq'])):
        freq = word_wf['surf_freq'][i]
        idx = word_wf['lem_idx'][i]
        
        if idx not in checked and int(idx) in lem_indexes:
            freqs.append(freq)
            checked.append(idx)
        
    word_form_freq = sum(map(int, freqs))
  
   
    lem_surfs = []
    
    # get the frequency of each lemma and sum, if we're dealing with a real morphologically composed item
    if pseudo_base == None:
        for index in lem_indexes:
            idx3 = clx.lem['index'] == index
            lemma = clx.lem.sub(idx3)

            lem_surfs.append(map(int, lemma['surf_freq'])[0])
        
            if '+' in lemma['morph_str'][0]:
                morphs = lemma['morph_str'][0].split('+')
            
                idx_add = clx.lem['word'] == morphs[0]
                lemma_add = clx.lem.sub(idx_add)
            
                lem_surfs.append(map(int, lemma_add['surf_freq'])[0])
                   
        print lemma
                    
        lemma_freq = sum(lem_surfs)
        lemma_searched = lemma['word'][0]

        if lemma_freq != 0:
            tp = word_form_freq / lemma_freq

        else:
            tp = 0

    
    
    # get the frequency of each lemma and sum, if we're dealing with a real morphologically composed item   
    if pseudo_base != None:
        
        lem_words = []
        booln = []
                
        for i in xrange(len(clx.lem['word'])):
            clx_word = clx.lem['word'][i]
            clx_morph = clx.lem['morph_str'][i]
            
            if pseudo_base in clx_word[0:len(pseudo_base)] or '+' + pseudo_base in clx_morph:
                booln.append(True)
            else:
                booln.append(False)
                
        # idx4 = [pseudo_base in clx_word[0:len(pseudo_base)] for clx_word in clx.lem['word']] or ['+' + pseudo_base in clx_word for clx_word in lemma_pseudo['morph_str']]
        idx4 = np.array(booln, dtype=bool) 
        lemma_pseudo = clx.lem.sub(idx4)
                            
        for i in xrange(len(lemma_pseudo['surf_freq'])):
            lem_surf = int(lemma_pseudo['surf_freq'][i])
            lem_morph = lemma_pseudo['morph_str'][i]
            lem_word = lemma_pseudo['word'][i]
            
            
            if pseudo_base in lem_morph:
                ant_leftovers = lem_morph.split(pseudo_base,1)[0]
                post_leftovers = lem_morph.split(pseudo_base,1)[1]
            else:
                ant_leftovers = ''
                post_leftovers = ''
                
            
            if ant_leftovers == '':
                ant_leftovers = 'X'
            
            if post_leftovers == '':
                post_leftovers = 'X'
                    
            if '-' not in lem_word and ' ' not in lem_word:
                if len(lem_word) > 0:
                    if len(lem_morph) <= len(pseudo_base) or ant_leftovers[-1] == '+' or ant_leftovers == 'X':
                                                
                        if post_leftovers[0] == '+' or post_leftovers == 'X':
                    
                            print lem_word, lem_morph
                
                            lem_surfs.append(lem_surf)
                            lem_words.append(lem_word)
        
        #print "the following items found for the family:", lem_words
        
        lemma_freq = sum(lem_surfs)
        lemma_searched = pseudo_base
    
        # for the pseudo-suffixed items, this is how to calculate transition probability per lewis et al., 2011
        if lemma_freq != 0:
            tp = word_form_freq / (word_form_freq + lemma_freq)
        
        else:
            tp = 0    
    
    print "searched for:",surface_form, lemma_searched
    return word_form_freq, lemma_freq
    
def affix_freq(search_token,clx,verbose=True):
    """
    
    Finds the frequency that an affix is used. In search token, need to include the '+' sign at the point where it will be attached
    to get a morphological count. Leave this out if you just want the orthographic count.
    
    example: affix_freq('+able',celex)
    
    """
    
    # find matches to search token
    idx = np.array([search_token in morph.split('+') for morph in clx.lem['morph_str']],dtype='bool')
    lemmas = clx.lem.sub(idx)
    
    # remove items that are not one orthographic unit
    idx = np.array([" " and "-" not in word for word in lemmas['word']],dtype='bool')
    lemmas = lemmas.sub(idx)
    
    if verbose == True:
        print lemmas
    
    affix_freq = sum(map(int,lemmas['surf_freq']))
    
    return affix_freq

def get_morph_freqs(search_token,ds=None,celex_path=None,whole_or_part=None,loc=None,verbose=False,save_stems=False):
    """  

    returns freq, stem list (if save_stems is true)
    
    if ds is none, it requires putting the path to celex and will load the ds for you. your ds can be a list of ds's.
        
    morph_type refers to whole word or just the frequency of a string which is part of a word. If you are looking
    for the frequency of a prefix or suffix, this can be left blank.
    
    morph_type = 'whole' | 'part'
    
    loc = if you have said 'part', whether that part occurs at the beinning or end of the word. Can be None, "begn" or "end".
    
    save_stems = if you are searching for an affix, you can save the stems that connect to that affix. returns additional object.
    
    """
    
    if whole_or_part == None:
        raise ValueError("whole_or_part not defined! Must define whether you want to search for your item including when it occurs within other words or just when it's a whole word.")

    if ds == None and celex_path == None:
        raise ValueError("Need to define either an already made copy of celex, or the path to celex so that the function can make it for you.")

    if ds == None:
        ds = get_ds_from_celex(celex_path)
         
    token_count = 0
    surf_count = 0
    stem_box = [];
   
    ds_thin = combine((ds.wf1,ds.wf2))
    
    for i in range(0,len(ds_thin['word'])):
        item = ds_thin['word'][i]
        surf_freq = int(ds_thin['surf_freq'][i])
        
        if whole_or_part == 'whole':
        
            item = ds_thin['word'][i]
        
            if len(search_token) == len(item):
                if search_token in item:
                    token_count += 1
                    surf_count += surf_freq
                    if verbose == True:
                        print "matches found:",search_token, item
                    
        if whole_or_part == 'part':
        
            if loc == None:
                                
                if search_token in item and ' ' not in item and '-' not in item: # make sure we don't count words with spaces or hyphens like "charity school" or "cabinet-maker"
                    token_count += 1
                    surf_count += surf_freq
                    if verbose == True:
                        print "matches found:",search_token, item


            if loc == 'begn':
            
                x = len(search_token)
                y = len(item)
            
                item = ds_thin['word'][i][0:x]
        
                if search_token in item:
                    token_count += 1
                    surf_count += surf_freq
                    if verbose == True:
                        print "matches found:",search_token, ds_thin['word'][i]

                        if save_stems == True:
                                    
                            stem = item[x:y]
                            stem_box.append(stem)


            if loc == 'end':
            
                x = len(search_token)
                y = len(item)
                item = ds_thin['word'][i]
                item_end = item[y-x:y]
        
                if search_token in item_end:
                    token_count += 1
                    surf_count += surf_freq
                    if verbose == True:
                        print "matches found:",search_token, ds_thin['word'][i]

                        if save_stems == True:
                                    
                            stem = item
                            stem_box.append(stem)
        
    
    print "\ncount for", search_token, 'is:', surf_count
    print "\nyour search token was found in ", token_count, "words"
    
    if save_stems == True:
        return surf_count, stem_box
    else:
        return surf_count
 
def tp(word,stem,base,clx,suffix=None,back_characters=0,verbose=False,return_freqs=False):
    """Get TP of suffixes and stems of words.
    
    word            :   (str), the full word you want to test
    clx_thin        :   (ds), the dataset for the celex once stripped of uninteresting variables
    back_char       :   (int), by how many char (if any) need to go back to get to a bound stem
    verbose         :   (bool)
    
    """
    
    word_freq = []
    stem_freq = []
    base_freq = []
    
    word_freq = get_morph_freqs(search_token=word,ds=clx,whole_or_part='part',verbose=verbose)
    stem_freq = get_morph_freqs(search_token=stem,ds=clx,whole_or_part='part',verbose=verbose)
    base_freq = get_morph_freqs(search_token=base,ds=clx,whole_or_part='part',verbose=verbose)
    
    if stem_freq > 0:
    
        TP_prefix = float(word_freq/stem_freq)
        print "\n-\ntransition (conditional) probability of", stem,"given prefix is: ", TP_prefix
    
    else:
        TP_prefix = 0
    
    if base_freq > 0:
        
        TP_suffix = float(base_freq/stem_freq)
        print "\n-\ntransition (conditional) probability of", stem,"given suffix is: ", TP_suffix
    
    else:
        TP_suffix = 0
    
    if return_freqs == False:
        return TP_prefix
    
    if return_freqs == True:
        return TP_prefix, TP_suffix, stem_freq, word_freq, base_freq

def most_wordclass_continuation(clx_thin,item,word_class,celex_path=celex_path):
    """
    From a stem, find a continuation that is used least ambiguously as a given word class
    
    clx_thin    :         the reduced celex database
    item        :         the word you want to evaluate
    word_class  :         the word-class you want the continuation to be
    
    """
    
    conts = []
    vals = []
    
    c = Celex(celex_path)
    c.load_lemmas()
    lv = LexVars(c)
    
    c.map_lemmas_to_wordforms()
    cont_list = c.lemma_to_wordforms(c.lemma_lookup(item)[1])
    for i in range(0,len(cont_list)):
        cont = cont_list[i].Word
        print cont
        conts.append(cont)
    
    for cont in conts:
        val = lv.cond_prob_of_word_class(cont,word_class)
        vals.append(val)
    
    conts_and_vals = dict(zip(conts,vals))
    return conts_and_vals
    
def check_continuations(clx,item,return_cont=False,vbs=False,celex_path=celex_path):
    
    '''
    Checks if the word you are inputting had any valid continuations. If yes, it returns the continuations.
    
    clx         :       clx database created by get_ds_from_celex
    celex_path  :       path to where your celex folder is
    item        :       (str), the item you wanna search for
    vbs         :       boolean, say if you want to print out all the continuations or not
    
    '''
    
    conts = []
    
    if item not in clx.lem['word']:
        conts.append("Word_not_found")
        print '0'
        #print "%s not found" % item   
    else:   
        
    
        c = Celex(celex_path)
        c.load_lemmas()
        lv = LexVars(c)
        c.map_lemmas_to_wordforms()
    
        cont_list = c.lemma_to_wordforms(c.lemma_lookup(item)[0])
        for i in range(0,len(cont_list)):
            cont = cont_list[i].Word
            conts.append(cont)
    
        booln = []
        for cont in conts:
            if len(cont) > len(item):
                booln.append(True)
            else:
                booln.append(False)
            
        valid_conts = [val for is_cont, val in zip(booln, conts) if is_cont]
        if vbs == True:
            print valid_conts
        if len(valid_conts) > 0:
            if return_cont == True:
                return item, conts
            if return_cont == False:
                return item
            
def cond_prob_wordclass_wordform(clx,celex_path,word_form,word_class):
    '''
    clx              :       clx database created by get_ds_from_celex
    celex_path       :       path to where your celex folder is
    word_form        :       (str), the item you wanna search for
    word_class       :       (str), the word class you want to assess the item in terms of
    
    '''

    c = Celex(celex_path)
    c.load_lemmas()
    lv = LexVars(c)

    counter = 0

    for i in range(0,len(clx.wf1['word'])):
        if word_form in clx.wf1['word'][i][0:len(word_form)] and len(clx.wf1['word'][i]) == len(word_form):
            idx = clx.wf1['lem_idx'][i]
            counter += 1
            print clx.wf1['word'][i]
    for i in range(0,len(clx.wf2['word'])):
        if word_form in clx.wf2['word'][i][0:len(word_form)] and len(clx.wf2['word'][i]) == len(word_form):
            idx = clx.wf2['lem_idx'][i]
            counter += 1
            print clx.wf1['word'][i]
    
    if counter < 1:
        ValueError("your word (%s) is not found in the corpus" % word_form)
    
    if counter > 1:
        print "Warning, there are a number of different possible mappings from wordform to lemma"
    
    idx = int(idx) - 1   

    cor_lem = clx.lem['word'][idx]
    print clx.lem['word'][idx]
    
    val = lv.cond_prob_of_word_class(cor_lem,word_class)     
    print cor_lem, val
    return val
    
    
def word_struc(clx,item):
    """
    Finds your word and returns a list of the constituent morphemes.
    
    
    clx         :       the dataset that contains celex
    item        :       the word you want to find the structure of
    
    """
    
    for i in range(0,len(clx.lem['word'])):
        word = clx.lem['word'][i]
        if item in word[0:len(item)] and len(item) == len(word):

            morph = clx.lem['morph_str'][i]
            
            if len(morph) > 1:            
                morph_spl = morph.split("+")
                
            else:
                morph_spl = item.split("+")
                
            return morph_spl
        
def list_in_list(list1,list2,index=False,dataset_to_index=None):
    """
    
    Finds which items of one list are in which items of the other list.
    
    List1             :       can be a list or the column of a dataset
    List2             :       can be a list or the column of a dataset
    Index             :       Set to true if you want to index your ds by removing entries that occur in the other list.
    dataset_to_index  :       If Index is true, need to say what your dataset is that you want to index.
    
    """
    
    items = []
    booln = []
    
    for i in range(0,len(list1)):
        item = list1[i]
        if not any([word in item for word in list2]):
            booln.append(True)
          
        else:
            booln.append(False)
            items.append(item)
    
        if index == False:
            return items
        
        if index == True:
            idx = np.array(booln, dtype=bool)        
            ds_sub = dataset_to_index.sub(idx)
            return ds_sub
            
def best_match(ds,base_cond,cond1,cond2,var_dict):
    """
    Takes sets of possible stimuli items from different conditions, and finds matches for a word in the other conditions
    based on the set of dimensions provided by the user.
    
    It makes the most sense to make the base_cond the set that you have the least items for - this may mean that you end up getting a larger final set of items, and
    there will be more matched on the first than the second round of matching.
    
    ds              :       the table that contains all of the words you want to match
    base_cond       :       the condition that you want to find matching words for
    cond1           :       first cond to compare
    cond2           :       second
    cond3           :       third
    
    var_dict {
    
        'length_word'       :   (1,1),
        'log_freq_stem'     :   (1,2)
    
    }
    
    """
    
    idx = ds['cond'] == base_cond
    ds_base_cond = ds.sub(idx)
    
    idx = ds['cond'] == cond1
    ds_cond1 = ds.sub(idx)
    
    idx = ds['cond'] == cond2
    ds_cond2 = ds.sub(idx)   
    
    idx = ds['cond'] == cond3
    ds_cond3 = ds.sub(idx)
    
    idx = ds['cond'] == cond4
    ds_cond4 = ds.sub(idx)
    
    pairs_w1 = []
    pairs_w1_m = []
    
    pairs_w2 = []
    pairs_w2_m = []
    
    pairs_w3 = []
    pairs_w3_m = []

    pairs_w4 = []
    pairs_w4_m = []
    
    full_set = []
    
    for i in range(0,len(ds_base_cond['Word'])):
        targ_surf_log = ds_base_cond['Log_Freq_HAL'][i]
        targ_surf_raw = ds_base_cond['surf_freq'][i]
        #targ_stem = ds_base_cond['free_stem_freq'][i]
        targ_RT = ds_base_cond['mean_RT'][i]
        targ_length = ds_base_cond['Length'][i]
        targ_suff = ds_base_cond['Suffix'][i]
        word = ds_base_cond['Word'][i]
        
        
        dses = (ds_cond1,ds_cond2,ds_cond3,ds_cond4)
        
        for ds_ in dses:
            booln = []
                
            for i in range(0,len(ds_['Word'])):
                surf_log1 = ds_['Log_Freq_HAL'][i]
                surf_raw1 = ds_['surf_freq'][i]
                #stem1 = ds_['free_stem_freq'][i]
                RT1 = ds_['mean_RT'][i]
                length1 = ds_['Length'][i]
                suff1 = ds_['Suffix'][i]
                word1 = ds_['Word'][i]
                
                            
                if targ_suff == suff1 and abs(targ_surf_log - surf_log1) < lower_log_freq and abs(targ_surf_raw - surf_raw1) < lower_raw_freq and abs(targ_RT - RT1) < mean_RT and abs(targ_length - length1) < lower_length:
                    # and abs(targ_stem - stem1 < 200)  and 
                    
                    if ds_ == ds_cond1:
                        if word1 not in pairs_w1_m and word not in pairs_w1:
                            pairs_w1.append(word)
                            pairs_w1_m.append(word1)
            
                    if ds_ == ds_cond2:
                        if word1 not in pairs_w2_m and word not in pairs_w2:
                                pairs_w2.append(word)                        
                                pairs_w2_m.append(word1)  
                                  
                        if ds_ == ds_cond3:
                            if word1 not in pairs_w3_m and word not in pairs_w3:
                                pairs_w3.append(word)                        
                                pairs_w3_m.append(word1)
                                
                        if ds_ == ds_cond4:
                            if word1 not in pairs_w4_m and word not in pairs_w4:
                                pairs_w4.append(word)                        
                                pairs_w4_m.append(word1)
                    
                    booln.append(True)
                
                else:
                    booln.append(False)
                    
            ds_['booln'] = booln
            
            for i in range(0,len(ds_['Word'])):
                surf_log1 = ds_['Log_Freq_HAL'][i]
                surf_raw1 = ds_['surf_freq'][i]
                #stem1 = ds_['free_stem_freq'][i]
                RT1 = ds_['mean_RT'][i]
                length1 = ds_['Length'][i]
                suff1 = ds_['Suffix'][i]
                word1 = ds_['Word'][i]
                boo = ds_['booln'][i]
                
                if boo is False and abs(targ_surf_log - surf_log1) < upper_log_freq and abs(targ_surf_raw - surf_raw1) < upper_raw_freq and abs(targ_RT - RT1) < mean_RT and abs(targ_length - length1) < lower_length:
        
                    if ds_ == ds_cond1:
                        if word1 not in pairs_w1_m and word not in pairs_w1:
                            pairs_w1.append(word)
                            pairs_w1_m.append(word1)

                    if ds_ == ds_cond2:
                        if word1 not in pairs_w2_m and word not in pairs_w2:
                            pairs_w2.append(word)                        
                            pairs_w2_m.append(word1)  
                      
                    if ds_ == ds_cond3:
                        if word1 not in pairs_w3_m and word not in pairs_w3:
                            pairs_w3.append(word)                        
                            pairs_w3_m.append(word1)
                            
                    if ds_ == ds_cond4:
                        if word1 not in pairs_w4_m and word not in pairs_w4:
                            pairs_w4.append(word)                        
                            pairs_w4_m.append(word1)                            
                        
        if word in pairs_w1 and pairs_w2 and pairs_w3 and pairs_w4:
            full_set.append(word)
 
    cond1_match = dict(zip(pairs_w1,pairs_w1_m))
    cond2_match = dict(zip(pairs_w2,pairs_w2_m))
    cond3_match = dict(zip(pairs_w3,pairs_w3_m))
    cond4_match = dict(zip(pairs_w4,pairs_w4_m))

    print len(cond1_match), '/', len(ds_base_cond['Word'])
    print len(cond2_match), '/', len(ds_base_cond['Word'])
    print len(cond3_match), '/', len(ds_base_cond['Word'])
    print len(cond4_match), '/', len(ds_base_cond['Word'])
    
    cond1_match_nomatch = []
    cond2_match_nomatch = []
    cond3_match_nomatch = []
    cond4_match_nomatch = []
            
    for item in full_set:
        cond1_match_nomatch.append(cond1_match.get(item))
        cond2_match_nomatch.append(cond2_match.get(item))
        cond3_match_nomatch.append(cond3_match.get(item))
        cond4_match_nomatch.append(cond4_match.get(item))
    
    ds_match = Dataset()
    ds_match[base_cond] = Factor(full_set)
    ds_match[cond1] = Factor(cond1_match_nomatch)     
    ds_match[cond2] = Factor(cond2_match_nomatch)  
    ds_match[cond3] = Factor(cond3_match_nomatch)  
    ds_match[cond4] = Factor(cond4_match_nomatch) 
    
    return ds_match
            

def best_match_beta(ds,word_column,conds,var_dict):
    """
    Takes sets of possible stimuli items from different conditions, and finds matches for a word in the other conditions
    based on the set of dimensions provided by the user.
    
    It makes the most sense to make the base_cond the set that you have the least items for - this may mean that you end up getting a larger final set of items, and
    there will be more matched on the first than the second round of matching.
    
    ds              :       the table that contains all of the words you want to match
    conds           :       list of conditions to match
    var_dict        :       a dictionary that contains your first and second threshold for each variable
    
        example:
    
            var_dict = {
    
                'length_word'       :   (1,2),
                'log_freq_stem'     :   (0.5,1.5) # 1 is first, 2 is second
    
            }
    
    """
        
    cond_datas = []
    
    for cond in conds:
    
        idx = ds['cond'] == cond        # loops over each condition given by user and adds them to a datalist
        cond_data = ds.sub(idx)
        cond_data.name = cond
        cond_datas.append(cond_data)

    pairs_w1 = []                       # set up bins that will be used later - got to be a better way to do this.
    pairs_w1_m = []
    
    pairs_w2 = []
    pairs_w2_m = []
    
    full_set = []
 
    blank_ds = Dataset() 
        
    cond0 = cond_datas[0]               # the first condition will be the base condition
    
    finder = cond0.keys()[0]            # take the first column and iterate over its range
    
    for i in range(0,len(cond0[finder])):
        for key in var_dict.keys():
            blank_ds[key] = Factor([str(cond0[key][i])])
            blank_ds[word_column] = Factor([str(cond0[word_column][i])])
                    
        for ds_ in cond_datas[1:]:

            blank_ds2 = Dataset()
                
            for n in range(0,len(ds_[finder])):
                for key2 in var_dict.keys():
                    blank_ds2[key2] = Factor([str(ds_[key2][n])])
                    blank_ds2[word_column] = Factor([str(ds_[word_column][n])])
                
                first = var_dict.keys()[0]
                second = var_dict.keys()[1]
                 
                # looks at the user's dict, and takes the first range as the range of interest. again, there has to be a better way so that we don't have to put another arugment for each additional variable we're matching over
                                            
                if abs(float(blank_ds[first][0]) - float(blank_ds2[first][0])) < var_dict.get(first)[0] and abs(float(blank_ds[second][0]) - float(blank_ds2[second][0])) < var_dict.get(second)[0]:
                    
                    
                    if ds_.name == cond_datas[1].name:
                    
                        if blank_ds[word_column][0] not in pairs_w1 and blank_ds2[word_column][0] not in pairs_w1_m:
                            pairs_w1.append(blank_ds[word_column][0])
                            pairs_w1_m.append(blank_ds2[word_column][0])

                    if ds_.name == cond_datas[2].name:
                    
                        if blank_ds[word_column][0] not in pairs_w2 and blank_ds2[word_column][0] not in pairs_w2_m:
                            pairs_w2.append(blank_ds[word_column][0])
                            pairs_w2_m.append(blank_ds2[word_column][0])                    
                                                         
                        
        if blank_ds[word_column][0] in pairs_w1 and pairs_w2:
            full_set.append(blank_ds[word_column][0])
 
 
    # here, too. it's all dependant on how many conditions and how many variables you have. need to change this so it can figure it out regardless of the input.
 
    cond1_match = dict(zip(pairs_w1,pairs_w1_m))
    cond2_match = dict(zip(pairs_w2,pairs_w2_m))

    print len(cond1_match), '/', len(cond0[finder])
    print len(cond2_match), '/', len(cond0[finder])
   
    cond1_match_nomatch = []
    cond2_match_nomatch = []

            
    for item in full_set:
        cond1_match_nomatch.append(cond1_match.get(item))
        cond2_match_nomatch.append(cond2_match.get(item))
    
    ds_match = Dataset()
    
    ds_match[conds[0]] = Factor(full_set)
    ds_match[conds[1]] = Factor(cond1_match_nomatch)     
    ds_match[conds[2]] = Factor(cond2_match_nomatch)  
    
    for col in ds_match:
        
        # get rid of all the "none" entries in all collumns
        idx = np.array(['None' not in item for item in ds_match[col]],dtype=bool)
        ds_match2 = ds_match.sub(idx)
        
    return ds_match
            

def matched_stim_dataset_beta(ds_match,ds_full,word_column):
    """
    
    ds_match            :           the Dataset where you have the items matched
    ds_full             :           the full dataset used in the best_match_beta function
    
    """
    
    total = []
    emp = Dataset()
    
    for col in ds_match:
        
        # get rid of all the "none" entries in all collumns
        idx = np.array(['None' not in item for item in ds_match[col]],dtype=bool)
        ds_match = ds_match.sub(idx)
    
    for col in ds_match:
        
        for item in ds_match[col]:
            total.append(item)
        
    emp['total'] = Factor(total)
    
    idx = np.array([word in emp['total'] for word in ds_full[word_column]],dtype=bool)
    ds_final = ds_full.sub(idx)
    
    return ds_final
    
    

def check_sig_lexVar(ds,test_vars,cond_column):
    """
    
    Check that your conditions are not significantly different across certain dimensions.
    
    ds              :           your dataset collection of stimuli items, with a column called "conds" for your different conditions
    test_vars       :           the variables you want to check the significance of (need a column for each of these)
    cond_column     :           string, the name of the column that has the different conditions in your ds
    
    """
    
    reses = []
    
    for var in test_vars:
        reses.append(test.pairwise(Y=ds[var], X=ds[cond_column],ds=ds))
        print var, test.pairwise(Y=ds[var], X=ds[cond_column],ds=ds)
        
    return reses,var
    
            

def match_conditions(ds,cond_colum,item_column,length_column,vars):
    """matches items into conditions so that they don't vary on given lexical dimensions.
    
    Does not match item-by-item. Will automatically match by length, so no need to include this in vars.
    
    base    :   base condition (the conditions with the least items)
    conds   :   list of the conditions you want to match
    
    """
    
    count = 0
    
    cond_freq = table.frequencies(cond_colum,ds=ds)
    cond_freq.sort('n')
    conds = cond_freq['cell']
    
    cond_list = [0]*len(conds)
    
    names = []
    
    for i in range(0,len(conds)):
        cond = conds[i]
        
        idx = ds[cond_colum] == cond
        cond_list[i] = ds.sub(idx)
        cond_list[i]['idx'] = Var(range(0,len(cond_list[i][item_column])))
        cond_list[i].name = cond
        names.append(cond_list[i].name)
            
    n_items = cond_list[0].n_cases
    
    cond_sub = Dataset()
    
    lengths = []
    
    # length_table = table.frequencies(length_column,cond_colum,ds=ds)
    # for n in length_table[0].keys():
    #     if n != 'cond':
    #         lengths.append(n)
    
    # should add here something about matching for length, but can't figure out how to do it
    
    count = 0
    
    matched = False    
    while matched == False:
        count += 1
        #print count
    
        for cond in cond_list:
    
            rand_array = random.sample(population=range(0,cond.n_cases), k=n_items) # gets random indices that are the length of the smallest condition
        
            boo = np.array([n in rand_array for n in cond['idx']],dtype=bool)
            cond_sub[cond.name] = cond.sub(boo)
    
        el1 = cond_sub[names[0]]
        el2 = cond_sub[names[1]]
        el3 = cond_sub[names[2]]
        el4 = cond_sub[names[3]]
        el5 = cond_sub[names[4]]
    
        total = combine((el1,el2,el3,el4,el5))
            
        sigs,var = check_sig_lexVar(total,vars,cond_colum)
        
        sig_total = sigs[0]       
        tsv = sig_total.get_str()
        x = len(tsv)                # the results themselves have an asterix in the correction so need to cut this out!!
        y = x-40
        tsv = tsv[0:y]
        
        if '*' in tsv:
            print tsv,vars
            matched = False
        elif '*' not in tsv:
            matched = True
        
    
    return total,sigs

def nonwords_from_nonwordlist(non_word_list,clx,suff_list,word_len_max=20):
    """
    From a set of words will turn them into non-words.
    
    
    non_word_list           :           the items that you want to turn into non-words
    clx                     :           the clx database
    suff_list               :           the suffixes you want to append to your items to make them non-words
    
    """
    
    testbin = non_word_list
    suff_count = suff_list
    
    stems = []
    suffixes = []

    for word in testbin:
        for suffix in suff_list:
            if suffix in word:            
            
                x = len(word)
                y = len(suffix)
                stem = word[0:x-y]
                stems.append(stem)
                suffixes.append(word[x-y:x])
         
    non_words = []
    rand_suff = []
            
    for i in range(0,len(stems)):
    
        stem = stems[i]
        suffix = suffixes[i]
        
        if len(stem) >= word_len_max-3:
            stem = stem[0:len(stem)-3] 
        
        n = random.randint(0,len(suff_count)-1)
        rand_suff = suff_count.keys()[n]
        word = stem + rand_suff   
    
        while rand_suff[0] in vowels and stem[-1] in vowels or word in clx.lem['word'] or word in testbin or len(word) >= word_len_max:
                    
            n = random.randint(0,len(suff_count)-1)
            rand_suff = suff_count.keys()[n]
            word = stem + rand_suff
            print word
                    
        if word not in non_words and word not in testbin:
            non_words.append(word)
    
    return non_words
    

def nonwords_from_wordlist(ds,rest,clx):
    """
    Uses the sets of words that could have been used but weren't, and makes a load of matched non-word items.
    
    ds              :           the Dataset() where your final critical items are (so that these aren't included)
    rest            :           the Dataset() where all the items were (can include the ones you ended up picking)
    clx             :           celex database, as made with get_ds_from_celex()
    
    """
    
    path = '/Users/lauragwilliams/Documents/experiments/vulnerable_winter/elp/non_words'
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    items = []
    
    for word in rest['Word']:
        if word not in ds['word']:
            items.append(word)
    
    if not os.path.exists(path + '/mono_bin.pickled'):    
    
        mono_bin = []
        bimorph_bin = []
    
        for item in items:
            struc = word_struc(clx,item)
            print struc
        
            if len(struc) == 1:
                mono_bin.append(item)
            elif len(struc) > 1:
                bimorph_bin.append(item)
            
        save.pickle(mono_bin, dest=path + '/mono_bin')
        save.pickle(bimorph_bin, dest=path + '/bimorph_bin')
    
    else:
        mono_bin = load.unpickle(path + '/mono_bin.pickled')
        bimorph_bin = load.unpickle(path + '/bimorph_bin.pickled')
        
    suff_count = {
        
        'able'  :   23,
        'age'   :   35,
        'al'    :   32,
        'ant'   :   11,
        'ard'   :   10,
        'ary'   :   3,
        'ate'   :   16,
        'er'    :   74,
        'et'    :   16,
        'ey'    :   6,
        'ial'   :   9,
        'ic'    :   10,
        'ion'   :   6,
        'let'   :   3,
        'ous'   :   10,
        'ric'   :   1
            
    }
    
    
    bins = (mono_bin,bimorph_bin)
    
    
    for testbin in bins:
            
        non_words = nonwords_from_nonwordlist(testbin,clx,suff_count)
    
        if testbin == mono_bin:
            NW_mono = non_words
            save.pickle(non_words, dest = path + '/mono_nonwords.pickled')
        
        elif testbin == bimorph_bin:
            NW_bi = non_words
            save.pickle(non_words, dest = path + '/bimorph_nonwords.pickled')
    
    return NW_mono + NW_bi
        
       
def match_freqs_to_non_words(word_list,dict_var):
    """docstring for match_freqs_to_non_words
    
    word_list           :           the possible non-words you wanna clean up
    dict                :           a key-frequency pairing of values
    
    """
    
    lengths = [len(word) for word in word_list]
    
    ds = Dataset()
    
    non_words = []
    suffixes = []
    lens = []
    
    for suffix in dict_var:
        count = 0
        seven = 0
        val = dict_var.get(suffix)
    
        while count < val:
                
            for word in word_list:
                x = len(word)
                y = len(suffix)

                if x == 7:
                    seven += 1
                
                if suffix in word[x-y:x] and count < val and x < 10 and x > 6:
                    count += 1
                    non_words.append(word)
                    suffixes.append(suffix)
                    lens.append(x)
                

                
    ds['non_words'] = Factor(non_words)
    ds['suffix'] = Factor(suffixes)
    ds['length'] = Var(lens)
    
    return ds
        
def shuffle_pres_list(ds,save=False,file_path=None):
    """
    Makes randomised presentation lists
    
    ds              :               set of words you want to put into random lists
    save            :               save the random ds's that are created
    path            :               if save=True, include the path to save the files
    
    """
    
    ref = ds.keys()[0]

    array = range(0,len(ds[ref]))
    shuffle(array) # randomise the order of the numbers in the array
            
    ds['order'] = Var(array)
    ds.sort('order')
        
    
    if save==True:
        ds.save_txt(file_path + 'rand_stim_set_' + str(n) + '.csv')
        
    return ds 
    
def presentation_restrictions(ds,common_column,diff_column,factor_restriction,first_cond,second_cond,rep_min):
    """
    
    ds                 :            the set that has your items and their information
    common_column      ;            the column of the dataset where there is overlap (e.g., complain, complain)
    diff_column        :            the column of the dataset where the items are different (e.g., complain, complaining)
    factor_restriction :            the column name that contains the first and second cond restrictions (e.g., "stem_complexity")
    first_cond         :            which condition you want to be presented first
    second_cond        :            which condition you want to be presented second
    
    """
    
    repeated = []
    uniq = []
    for x in ds[common_column]: # collect the repeteated items
        if x in uniq:
            repeated.append(x)
        if x not in uniq:
            uniq.append(x)
    
    rep_ds_idx = np.array([rep in repeated for rep in ds[common_column]],dtype=bool)
    re_ds = ds.sub(rep_ds_idx)
    #order_old = re_ds['order']
        
    bases=[]
    orders=[]
    count = 1
    for i in range(0,len(re_ds[common_column])):
        base=re_ds[common_column][i]
        item=re_ds[diff_column][i]
        stem_type=re_ds[factor_restriction][i]
        order=re_ds['order'][i]
        
                
        # if it is a complex stem and the first occurance, keep the same order; if a monostem and the first occurance, add 100 to the order.
        
        if base not in bases and stem_type == first_cond:
            orders.append(order)
            bases.append(base)
        
        elif base in bases and stem_type == first_cond:
            orders.append(count + 50)
            bases.append(base)
            count += 2
        
        elif base not in bases and stem_type == second_cond:
            orders.append(order + 100)
            bases.append(base)  
        
        # make sure that base don't occur within x items of each other.            
        elif base in bases[-(rep_min+1):] and stem_type == second_cond:
            orders.append(order + rep_min)
            bases.append(base)

        elif base in bases[-len(bases):-(rep_min+1)] and stem_type == second_cond:
            orders.append(order)
            bases.append(base) 
   
    re_ds['order'] = orders
    
    
    bi_idx = re_ds[factor_restriction] == first_cond
    bi_order = re_ds['order'][bi_idx]

    mo_idx = re_ds[factor_restriction] == second_cond
    mo_order = re_ds['order'][mo_idx]  
    
    bi_count = 0
    mo_count = 0
    
    for i in range(0,len(ds[diff_column])):
        word = ds[diff_column][i]
        complexity = ds[factor_restriction][i]
        
        if word in re_ds[diff_column] and complexity == first_cond:
            ds['order'][i] = bi_order[bi_count]
            bi_count += 1

        if word in re_ds[diff_column] and complexity == second_cond:
            ds['order'][i] = mo_order[mo_count]
            mo_count += 1
    
    ds.sort('order')
    
    return ds
    
def pseudo_rand_lists(ds,n_lists,common_column,diff_column,factor_restriction,first_cond,second_cond,rep_min,save=False,file_path=None,pres=False):
    """
    
    Makes pseudo-random lists, making sure that items that appear in both a first and second condition appear first in the first condition and then in the second condition.
    
    ds          :               the dataset you want to make lists from
    n_lists     :               number of lists for output
    common_column      ;        the column of the dataset where there is overlap (e.g., complain, complain)
    diff_column        :        the column of the dataset where the items are different (e.g., complain, complaining)
    factor_restriction :        the column name that contains the first and second cond restrictions (e.g., "stem_complexity")
    first_cond         :        which condition you want to be presented first
    second_cond        :        which condition you want to be presented second
    save               :        save lists to disk
    file_path          :        place to save the lists (if save = True) 
    pres               :        (bool), will save a word/trigger list for export into presentation   
    
    """
 
    rand_lists = []
  
    for n in range(0,n_lists):
    
        list = shuffle_pres_list(ds=ds,save=False,file_path=None)
    
        print list[diff_column][0:10]
        rand = presentation_restrictions(ds=list,common_column=common_column,diff_column=diff_column,factor_restriction=factor_restriction,first_cond=first_cond,second_cond=second_cond,rep_min=rep_min)
        rand_lists.append(rand)
    
        if save==True:
            rand.save_txt(file_path + 'pseudo_rand_list' + str(n))
            
        if pres == True:
            presentation_code(rand=rand,cor_but=factor_restriction,diff_column=diff_column,file_path=file_path,n=n)
            
    return rand_lists

def text_obj_setup_presentation(row):
    """
    
    row         :           the column in your dataset to get the presentation output for
    
    """
    
    lines = []
    
    for item in row:
        lines.append( "text { caption = '" + item + "'; font_size = 50; font_color = 0,0,0; background_color=150,150,150; }" + item + ";")
    
    ds = Dataset()
    ds['lines'] = Factor(lines)
    
    return ds
    
def presentation_code(rand,cor_but,diff_column,file_path,n=None):
    """
    
    rand            :           random presentation list
    cor_but         :           the column that has the thing that determines correct button
    file_path       :           where to save the lists
    n               :           list number to append to file
    
    """
    
    
    buttons = []
    
    for status in rand[cor_but]:
        if status == 'bad':
            buttons.append(1)
        elif status == 'good':
            buttons.append(2)
    
    ds_temp = Dataset()
    word = rand[diff_column]
    Port_Code = rand['trigger']
    s = ";"
    ds_temp['word'] = Factor(word)
    ds_temp['Port_Code'] = Var(Port_Code)
    ds_temp['correct_button'] = Var(buttons)
    ds_temp['order'] = rand['order']
    ds_temp['s'] = Factor(s*len(ds_temp['word']))

    ds_temp.save_txt(file_path + 'presentation_files' + str(n))
    
def phoneme_probability(word):
    """
    Will get the conditional probability of phonemes within a word.
    
    word            :               the item to search

    
    """
    
    s = SegmentSurprisalTree()
    s.read_elp()
    
    wp = s.probabilities(word)
    
    return wp

def phoneme_freq(word):
    """
    Will get the conditional probability of phonemes within a word.
    
    word            :               the item to search

    
    """
    
    s = SegmentSurprisalTree()
    s.read_elp()
    
    wp = s.frequencies(word) # need to check this - think it gets the log freq not the raw freq...
    
    return wp
    
def ambig_POD_surprisal(target, competitor, phoneme_percent):
    """
    
    target              :               the word you want to calculate the surp values for
    competitor          :               the item that is identical until a given POD
    phoneme_percent     :               dict, phoneme and the percent of that phoneme (e.g., {'p': 0.75, 'b': 0.25}) can only be two phonemes
    clx                 :               loaded from load_celex()
    
    
    """
    
    s = SegmentSurprisalTree()
    s.read_elp()
    
    searches = []
    qs = []
    
    count = 0
    
    # load up the frequency of each phoneme in the words
    
    freq_word1 = phoneme_freq(target)
    print freq_word1 
    
    freq_word2 = phoneme_freq(competitor)
    print freq_word2
    
    pron_t = s.pronunciations[target]
    pron_c = s.pronunciations[competitor]
        
    for i in range(0,len(pron_t)):
        
        # calculate the q value which will be used to weight the conditional probabilty of the sounds in the word
        
        if len(pron_t) != len(pron_c):
            raise NotImplementedError('Words have different number of phonemes (%i different)' % (len(pron_t) - len(pron_c))) 
        
        if pron_t[i] == pron_c[i]:
            freq1 = freq_word1[i][1] # value of i phoneme
            freq2 = freq_word2[i][1] # freq of phoneme within the competitor
        
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
        
        # apply q to the condition probabilities
        
        if count == 0:
           
            qs.append('na')
        
        else:
            
            
            if freq_minus_one2 > 0:
            
                cond1 = freq1/freq_minus_one1 # conditional probability of given phoneme
                cond2 = freq2/freq_minus_one2
                
            else:
                
                cond1 = freq1/freq_minus_one1
                cond2 = 0 # because can't divide something by 0
            
            weighted_cond1 = q1 * cond1 # conditional probability weighted by q
            weighted_cond2 = q2 * cond2

            final_surp = -np.log2(weighted_cond1 + weighted_cond2) # and transform that into a suprisal score
            
            qs.append(final_surp)
             

        freq_minus_one1 = freq1
        freq_minus_one2 = freq2
                
        count += 1
    
    pron_t[0] = "X"
        
    return zip(pron_t,qs)
        
        
  
    
    
    
    
    