# Author: Tal Linzen <linzen@nyu.edu>
# License: BSD (3-clause)import csv

import csv

import numpy as np

import paths
from prefix_tree import PrefixTree
from cmu_ipa import ELP2CMU

class SegmentSurprisalTree(object):

    frequency_field = 'SUBTLWF'

    def __init__(self):
        self.elp2cmu = ELP2CMU()

    def read_elp(self):
        self.tree = PrefixTree()
        self.pronunciations = {}

        words = list(csv.DictReader(open(paths.elp)))
        for i, x in enumerate(words):
            pron = self.elp2cmu.translate(x['Pron'])
            if x[self.frequency_field] not in ['0', 'NULL']:
                self.tree.insert(tuple(pron + ['#']), 
                        float(x[self.frequency_field]), x['Word'])

            self.pronunciations[x['Word']] = pron

        self.tree.calculate_probs()

    def surprisals(self, word, with_end=True):
        pron = self.pronunciations[word]
        pron = tuple(pron + ['#'] if with_end else [])
        return self.tree.prefix_surprisals(pron)

    def entropies(self, word, with_end=True):
        pron = self.pronunciations[word]
        pron = tuple(pron + ['#'] if with_end else [])
        return self.tree.prefix_entropies(pron)

    def probabilities(self, word, with_end=True):
        pron = self.pronunciations[word]
        pron = tuple(pron + ['#'] if with_end else [])
        return self.tree.prefix_probabilities(pron)
        
    def frequencies(self, word, with_end=True):
        pron = self.pronunciations[word]
        pron = tuple(pron + ['#'] if with_end else [])
        return self.tree.prefix_frequencies(pron)
        
    def node_frequencies(self, word, with_end=True):
        pron = self.pronunciations[word]
        pron = tuple(pron + ['#'] if with_end else [])
        return self.tree.prefix_frequencies(pron)