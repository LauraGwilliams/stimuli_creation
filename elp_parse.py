## script to get interesting things out of a big elp dataset
from __future__ import division

from eelbrain import *
import numpy as np

path = '/Users/lauragwilliams/Documents/experiments/vulnerable_winter/elp/'
file_name = 'elp_dataset.csv'
save_loc = path

def open_file(file,format,header,ignore_missing=True):
    """Uses eelbrain to load up a dataset from a file"""
    
    if format == 'csv':
        delim = ','
    elif format == 'tsv':
        delim = '\t'
    
    ds = load.txt.tsv(file, names=True, delimiter=delim, ignore_missing=ignore_missing)
    return ds
    

def clean_data(ds,log_freq_min,freq_HAL_min=0,min_suff_length=0,word_class=None,word_contains=None,mean_RT=None):
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
    """Gets the words that have a suffix but are monomorphemic.
    
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
        suffix_collection = ['able','al','ant','ary','ate','er','ic','ion','ity']
                
    
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
                             
    print len(unique_stem_collection)
    print " unique stems found."
    
    print len(free_stem_collection)
    print " free stems found."
    
    if save_result == True:
        save.txt(unique_stem_collection,dest=save_loc + 'unique_stems.csv')
        save.txt(free_stem_collection,dest=save_loc + 'free_stems.csv')
    
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
    ds2['Suffix'] = Factor(suffixes)
    ds2['mean_RT'] = Factor(RTs)   
    
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
    

def get_ds_from_celex(celex_path):
    """
    Uses eelbrain to load up celex morph file. First need to change the delimiter of the eml file from
        a backslash to a comma, and save this as eml_copy.cd.
    
    """
    ds = load.txt.tsv(celex_path + '/eml/eml_copy.cd', names=False, delimiter= ",", ignore_missing=True)
    ds.rename('v0','index')
    ds.rename('v1','word')
    ds.rename('v2','surf_freq')
    ds.rename('v11','morph_struc')
    
    ds_thin = Dataset()
    ds_thin['index'] = Var(ds['index'])
    ds_thin['word'] = Factor(ds['word'])
    ds_thin['surf_freq'] = Factor(ds['surf_freq'])
    ds_thin['morph_struc'] = Factor(ds['morph_struc'])
    
    return ds_thin

def get_morph_freqs(ds_thin,search_token,whole_or_part=None,verbose=False):
    """  
    Search token of prefix or suffix should be denoted with a plus (+) at the beginning or end of the morpheme:
    
    e.g.: search_token = '+ion'; search_token = 're+'
    
    morph_type refers to whole word or just the frequency of a string which is part of a word. If you are looking
    for the frequency of a prefix or suffix, this can be left blank.
    
    morph_type = 'whole' | 'part'
    
    """
            
    token_count = 0
    surf_count = 0
    
    for i in range(0,len(ds_thin['morph_struc'])):
        item = ds_thin['morph_struc'][i]
        surf_freq = int(ds_thin['surf_freq'][i])

        if search_token[-1] == '+':
            
            x = len(search_token)
            
            item_search = item[0:x]
            if search_token in item_search:
                token_count += 1
                surf_count += surf_freq           
                if verbose == True:
                    print "matches found:",search_token, item
        
        
        if search_token[0] == '+':
            
            x = len(search_token)
            y = len(item)
            item_search = item[y-x:y]
            if search_token in item_search:
                token_count += 1
                surf_count += surf_freq 
                if verbose == True:
                    print "matches found:",search_token, item
                
        if whole_or_part == 'whole':
            
            item = ds_thin['word'][i]
            
            if len(search_token) == len(item):
                if search_token in item:
                    token_count += 1
                    surf_count += surf_freq
                    if verbose == True:
                        print "matches found:",search_token, item
                        
        if whole_or_part == 'part':
            
            item = ds_thin['word'][i]
            
            if search_token in item:
                token_count += 1
                surf_count += surf_freq
                if verbose == True:
                    print "matches found:",search_token, item

    print "count for", search_token, 'is:', surf_count
    print "your search token was found in ", token_count, "words"
    return surf_count
 
def tp(word,suffix,clx_thin,back_characters=0,verbose=False):
    """Get TP of suffixes and stems of words.
    
    word            :   (str), the full word you want to test
    suffix          :   (str), the affix you wanna test, with +'s placed at the boundary
    clx_thin        :   (ds), the dataset for the celex once stripped of uninteresting variables
    back_char       :   (int), by how many char (if any) need to go back to get to a bound stem
    verbose         :   (bool)
    
    """
    
    x = len(word)
    y = (len(suffix)-1)+back_characters
    stem = word[0:x-y]
    
    suff_freq = get_morph_freqs(clx_thin,suffix)
    word_freq = get_morph_freqs(clx_thin,word,whole_or_part='whole',verbose=verbose)
    stem_freq = get_morph_freqs(clx_thin,stem,whole_or_part='part',verbose=verbose)
    
    TP_suff = float(word_freq/suff_freq)
    print "transition (conditional) probability of the suffix is: ", TP_suff
    
    TP_stem = float(word_freq/stem_freq)
    print "transition (conditional) probability of the stem is: ", TP_stem