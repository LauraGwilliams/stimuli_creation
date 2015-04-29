from __future__ import division


__author__ = 'lauragwilliams'


#!/usr/bin/env python

# author: laura gwilliams
# email: laura.gwilliams@nyu.edu

## script to get interesting things out of a big elp dataset

from eelbrain import *
import numpy as np
import math
from lexvars import *
import os.path
import random
from random import shuffle
import collections



path = '/Users/lauragwilliams/Documents/experiments/vulnerable_winter/elp/'
file_name = 'elp_dataset.csv'
save_loc = path
celex_path= '/Users/lauragwilliams/Documents/experiments/vulnerable_winter/celex/'

vowels = ['a','e','i','o','u']

class VisStim(object):
    """

    The set of functions for making visual stimuli using celex and elp

    """

    def __init__(self, celex_path):
        self.clx = load_celex(celex_path)


    def load_celex(self, celex_path=celex_path):
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

    def get_morph_freqs(self, search_token,ds=self.clx,whole_or_part=None,loc=None,verbose=False,save_stems=False):
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

                    if search_token in item:
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



    def elp_info(self,item,elp):
        """
        Gets basic info for given word

        """

        for i in range(0,len(elp['Word'])):
            word = elp['Word'][i]
            if item in word[0:len(item)] and len(item) == len(word):
                return item, word, elp['Length'][i], elp['Log_Freq_HAL'][i], elp['I_Mean_RT'][i]

    def clean_data(self, ds,log_freq_min=2,freq_HAL_min=0,min_suff_length=0,word_class=None,word_contains=None,mean_RT=None):
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

    def fetch_unique_and_free_stems(self, ds,suffix_collection='SolomyakMarantz',save_result=False):
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


    def separate_cong_from_incong(self, ds,save_file=False):
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

        assert isinstance(ds_save, object)
        return ds_save

