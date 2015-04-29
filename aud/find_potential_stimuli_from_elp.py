import eelbrain
from eelbrain import *

path = "/Users/lauragwilliams/Dropbox/Experiments/Ideas/Phoneme_Restore/stimuli_produdction/collocations_from_elp/w2c.txt"

# load file and make column names
ds_big = load.txt.tsv(path, False, delimiter='\t', ignore_missing=True)
ds_big.rename('v0','freq')
ds_big.rename('v1','w1')
ds_big.rename('v2','w2')
ds_big.rename('v3','pos1')
ds_big.rename('v4','pos2')

# make the dataset smaller by removing words we won't be interested in:

# - if first or second position is an article
ds_index = ds_big['pos1']!="at1" or ds['pos2']!="at1" or ds['pos1']!="at" or ds['pos2']!="at"
ds = ds_big.sub(ds_index)
ds.shape 		# check out the new size of the ds


stimuli_words = "/Users/lauragwilliams/Dropbox/Experiments/Ideas/Phoneme_Restore/stimuli_produdction/lists_of_minimal_pairs/minimal_pairs_total.txt"

ds_stimuli = load.txt.tsv(stimuli_words, False, delimiter='\t', ignore_missing=True)

word_props = [];

for word in ds_stimuli['v0']:
	for x in range(1,len(ds['w1'])):
		if word in ds['w1'][x][0:len(word)]:
			word_props.append(ds[x])	
			print ds[x]
	