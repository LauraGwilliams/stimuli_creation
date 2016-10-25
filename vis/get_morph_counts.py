from __future__ import division

from eelbrain import *
import numpy as np

def load_celex(celex_path=celex_path):
    """
    Uses eelbrain to load up celex morphologically parsed file.
    
    Will return a dataset with both wordform and lemma info as: self.wf1, self.wf2 and self.lem
	
	usage: clx = load_celex(celex_path)
    
    """
    ds = Dataset()

    ds_wf = load.tsv(celex_path + '/emw/emw.cd', names=False, delimiter= "\\", ignore_missing=True)

    ds_wf.rename('v0','index')
    ds_wf.rename('v1','word')
    ds_wf.rename('v2','surf_freq')
    ds_wf.rename('v3','lem_idx')    

    ds_thin1 = Dataset()
    ds_thin1['index'] = Var(ds_wf['index'])
    ds_thin1['word'] = Factor(ds_wf['word'])
    ds_thin1['surf_freq'] = Factor(ds_wf['surf_freq'])
    ds_thin1['lem_idx'] = Factor(ds_wf['lem_idx'])
     
    ds.wf1 = ds_thin1 
    
    ds_lem = load.tsv(celex_path + '/eml/eml.cd', names=False, delimiter= ",", ignore_missing=True)

    ds_lem.rename('v0','index')
    ds_lem.rename('v1','word')
    ds_lem.rename('v2','surf_freq')
    ds_lem.rename('v11', 'morph_str')
    
    ds_thin2 = Dataset()
    ds_thin2['index'] = Var(ds_lem['index'])
    ds_thin2['word'] = Factor(ds_lem['word'])
    ds_thin2['surf_freq'] = Factor(ds_lem['surf_freq'])
    ds_thin2['morph_str'] = Factor(ds_lem['morph_str'])

    ds.lem = ds_thin2 
   
    return ds


def affix_freq(search_token,clx,verbose=True):
    """
    
    Finds the frequency that an affix is used. In search token, need to include the '+' sign at the point where it will be attached
    to get a morphological count. Leave this out if you just want the orthographic count.
    
    usage: affix_freq('+able',clx)
    
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