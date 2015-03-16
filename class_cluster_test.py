# import dependencies
import os
import numpy as np
import mne
import eelbrain as e

class ClusterTest:
    """This is a wrapper for computing spatio-temporal cluster tests in Eelbrain."""
    
    def __init__(self,stc_path,subjects_dir):
        self.stc_path = stc_path
        self.subjects_dir = subjects_dir
        self.description = "Test not described yet."
                
    def load_data(self,factor1,factor2,participant_list):
        """Load up stc files. Factor1 and Factor2 should be lists of conditions."""
        
        subjects_dir = self.subjects_dir
        stc_path = self.stc_path
        
        subjects = []
        cond1s = []
        cond2s = []
        stcs = []
        
        for subject in participant_list:
            for cond1 in factor1:
                for cond2 in factor2:
                
                    stc_fname = stc_path % (cond2, cond1, cond2, cond1, subject)
                    stc = mne.read_source_estimate(stc_fname, subject=subject)
                    print stc_fname
                                        
                    subjects.append(subject)
                    cond1s.append(cond1)
                    cond2s.append(cond2)
                    stcs.append(stc)
                    
        ds = e.Dataset()
        ds['subject'] = e.Factor(subjects, random=True)
        ds['cond1'] = e.Factor(cond1s)
        ds['cond2'] = e.Factor(cond2s)
        ds['src'] = e.load.fiff.stc_ndvar(stcs, 'fsaverage', 'ico-4', subjects_dir)
        src = ds['src']
        
        self.ds = ds
        self.src = src

        print "summary of dataset:"
        print ds[0:10]
        return ds
        
    def run_threshold_cluster_test(self,test_type,parc,test_cond,tmin,tmax,brain_plot=False,pmin=0.1,samples=1000,mintime=0.02,minsource=10):
        """Cluster tests."""
        subjects_dir = self.subjects_dir
        src = self.src
        ds = self.ds
        
        # load up the source space that we're going to test over
        annot = mne.read_labels_from_annot(subject='fsaverage',parc='aparc',hemi='lh',surf_name='inflated',regexp=parc,subjects_dir=subjects_dir)
        idx = [src.source.index_for_label(l) for l in annot]
        idx = np.any([i.x for i in idx], 0)
        parc_src = src.sub(source=idx)
        
        # run the anova test
        if test_type == 'anova':
                
            res = e.testnd.anova(parc_src, ds[test_cond], ds=ds,
    	        samples=samples,  # number of permutations
    	        pmin=pmin,  # threshold for clusters (uncorrected p-value)
    	        tstart=tmin,  # start of the time window of interest
    	        tstop=tmax,  # stop of the time window of interest
    	        mintime=mintime,  # minimum duration for clusters
    	        minsource=minsource,  # minimum number of sources for clusters
    	        match='subject')  # needs to be specified in a by-subject design
        
            res.clusters.sort("p")
            table = res.clusters.as_table()
            print table
        
            if brain_plot == True:
                x = 0
                # retrieve cluster
                c_0 = res.clusters[x, 'cluster']
                cstart = res.clusters[x, 'tstart'] * 1000
                cstop = res.clusters[x, 'tstop'] * 1000
                hemi = res.clusters[x, 'hemi'].encode('utf-8')

                # average over time and plot the cluster extent
                c_extent = c_0.sum('time')
                plt_extent = e.plot.brain.cluster(c_extent, views = ['ve','lat'], surf = 'inflated')
                return plt_extent
        
        elif test_type == 'ttest':
        
            res = e.testnd.ttest_rel(parc_src,
                ds[test_cond], ds=ds, tstart=tmin, tstop=tmax, samples=samples,
                pmin=pmin, mintime=mintime, minsource = minsource, match='subject')
                
            res.clusters.sort("p")
            table = res.clusters.as_table()
            print table
        
            if brain_plot == True:
                x = 0
                # retrieve cluster
                c_0 = res.clusters[x, 'cluster']
                cstart = res.clusters[x, 'tstart'] * 1000
                cstop = res.clusters[x, 'tstop'] * 1000
                hemi = res.clusters[x, 'hemi'].encode('utf-8')

                # average over time and plot the cluster extent
                c_extent = c_0.sum('time')
                plt_extent = e.plot.brain.cluster(c_extent, views = ['ve','lat'], surf = 'inflated')
                return plt_extent
            